import 'package:flutter/material.dart';
import 'package:flashcard_app/models/flashcard_model.dart';
import 'package:flashcard_app/services/sheets_service.dart';

enum SyncStatus { initial, syncing, success, error }

class FlashcardProvider extends ChangeNotifier {
  List<Flashcard> _flashcards = [];
  int _currentIndex = 0;
  bool _isShowingFront = true;
  SyncStatus _syncStatus = SyncStatus.initial;
  String? _errorMessage;
  bool _isAuthenticated = false;

  // 기본 플래시카드 세트 제거 (빈 리스트로 시작)
  
  FlashcardProvider() {
    _initialize();
  }

  List<Flashcard> get flashcards => _flashcards;
  int get currentIndex => _currentIndex;
  bool get isShowingFront => _isShowingFront;
  Flashcard? get currentCard => _flashcards.isNotEmpty ? _flashcards[_currentIndex] : null;
  SyncStatus get syncStatus => _syncStatus;
  String? get errorMessage => _errorMessage;
  bool get isAuthenticated => _isAuthenticated;

  Future<void> _initialize() async {
    // 앱 시작 시 기본 플래시카드 로드하지 않음
    // 로그인 후에만 데이터를 로드하도록 변경
  }

  Future<void> _loadFlashcards() async {
    // 빈 상태로 시작 (기본 카드 없음)
    _flashcards = [];
    notifyListeners();

    // 로그인된 경우에만 Google Sheets에서 데이터 로드
    if (_isAuthenticated) {
      await _loadFromSheets();
    }
  }

  Future<bool> authenticate() async {
    _syncStatus = SyncStatus.syncing;
    _errorMessage = null;
    notifyListeners();

    try {
      final success = await SheetsService.signIn();
      _isAuthenticated = success;
      _syncStatus = success ? SyncStatus.success : SyncStatus.error;
      if (!success) {
        _errorMessage = '구글 로그인에 실패했습니다.';
      } else {
        await _loadFromSheets();
      }
      notifyListeners();
      return success;
    } catch (e) {
      _syncStatus = SyncStatus.error;
      _errorMessage = '인증 오류: $e';
      notifyListeners();
      return false;
    }
  }

  Future<void> _loadFromSheets() async {
    if (!_isAuthenticated) return;

    _syncStatus = SyncStatus.syncing;
    notifyListeners();

    try {
      final cards = await SheetsService.getFlashcards();
      _flashcards = cards;
      _currentIndex = 0; // 항상 첫 번째 카드부터 시작
      _syncStatus = SyncStatus.success;
    } catch (e) {
      _syncStatus = SyncStatus.error;
      _errorMessage = '데이터 로드 오류: $e';
    }
    
    notifyListeners();
  }

  Future<void> syncToSheets() async {
    if (!_isAuthenticated) {
      final success = await authenticate();
      if (!success) return;
    }

    _syncStatus = SyncStatus.syncing;
    notifyListeners();

    try {
      final success = await SheetsService.saveAllFlashcards(_flashcards);
      _syncStatus = success ? SyncStatus.success : SyncStatus.error;
      if (!success) {
        _errorMessage = '동기화에 실패했습니다.';
      }
    } catch (e) {
      _syncStatus = SyncStatus.error;
      _errorMessage = '동기화 오류: $e';
    }
    
    notifyListeners();
  }

  // 양방향 동기화 - 로컬 데이터와 스프레드시트 데이터를 병합
  Future<void> syncBidirectional() async {
    if (!_isAuthenticated) {
      final success = await authenticate();
      if (!success) return;
    }

    _syncStatus = SyncStatus.syncing;
    notifyListeners();

    try {
      // 1. 스프레드시트에서 최신 데이터 가져오기
      final sheetCards = await SheetsService.getFlashcards();
      
      // 2. 로컬 데이터와 스프레드시트 데이터 병합
      final mergedCards = _mergeFlashcards(_flashcards, sheetCards);
      
      // 3. 병합된 데이터로 로컬 상태 업데이트
      _flashcards = mergedCards;
      if (_currentIndex >= _flashcards.length) {
        _currentIndex = _flashcards.isEmpty ? 0 : _flashcards.length - 1;
      }
      
      // 4. 병합된 데이터를 스프레드시트에 저장
      final success = await SheetsService.saveAllFlashcards(mergedCards);
      
      // 5. 결과 상태 업데이트
      _syncStatus = success ? SyncStatus.success : SyncStatus.error;
      if (!success) {
        _errorMessage = '양방향 동기화에 실패했습니다.';
      }
    } catch (e) {
      _syncStatus = SyncStatus.error;
      _errorMessage = '양방향 동기화 오류: $e';
    }
    
    notifyListeners();
  }
  
  // 두 플래시카드 목록 병합 (ID 기준으로 중복 제거)
  List<Flashcard> _mergeFlashcards(List<Flashcard> localCards, List<Flashcard> sheetCards) {
    // 모든 카드를 담을 맵 (ID를 키로 사용)
    final Map<String, Flashcard> mergedMap = {};
    
    // 로컬 카드 추가
    for (final card in localCards) {
      mergedMap[card.id] = card;
    }
    
    // 스프레드시트 카드 추가 (동일한 ID가 있으면 덮어씀)
    for (final card in sheetCards) {
      // 이미 로컬에 있는 카드면 isLearned 상태 유지
      if (mergedMap.containsKey(card.id)) {
        final existingCard = mergedMap[card.id]!;
        mergedMap[card.id] = card.copyWith(isLearned: existingCard.isLearned);
      } else {
        mergedMap[card.id] = card;
      }
    }
    
    // ID 기준으로 정렬하여 리스트 반환
    final result = mergedMap.values.toList();
    result.sort((a, b) => int.parse(a.id).compareTo(int.parse(b.id)));
    
    return result;
  }

  void flipCard() {
    _isShowingFront = !_isShowingFront;
    notifyListeners();
  }

  void nextCard() {
    if (_flashcards.isEmpty) return;
    
    if (_currentIndex < _flashcards.length - 1) {
      _currentIndex++;
      _isShowingFront = true;
      notifyListeners();
    }
  }

  void previousCard() {
    if (_flashcards.isEmpty) return;
    
    if (_currentIndex > 0) {
      _currentIndex--;
      _isShowingFront = true;
      notifyListeners();
    }
  }

  Future<void> resetLearningStatus() async {
    if (!_isAuthenticated || _flashcards.isEmpty) return;
    
    // isLearned 필드는 더 이상 사용하지 않지만 인터페이스 유지를 위해 함수 유지
    // 실제로는 아무 작업도 수행하지 않음
    
    notifyListeners();
  }

  Future<void> addCard(String english, String korean) async {
    if (!_isAuthenticated) return;
    
    // 새 ID 생성 (마지막 ID + 1 또는 첫 카드면 1)
    final lastId = _flashcards.isEmpty ? 0 : int.parse(_flashcards.last.id);
    final newId = (lastId + 1).toString();
    
    final newCard = Flashcard(
      id: newId,
      english: english,
      korean: korean,
    );
    
    _flashcards.add(newCard);
    notifyListeners();
    
    // Google Sheets에 새 카드 추가
    await SheetsService.addFlashcard(newCard);
  }

  int get learnedCount {
    // isLearned 필드를 더 이상 사용하지 않으므로 항상 0 반환
    return 0;
  }

  Future<void> signOut() async {
    await SheetsService.signOut();
    _isAuthenticated = false;
    _flashcards = []; // 로그아웃 시 카드 비우기
    _currentIndex = 0;
    notifyListeners();
  }
} 