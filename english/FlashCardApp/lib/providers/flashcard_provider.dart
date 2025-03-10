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

  // 기본 플래시카드 세트
  final List<Flashcard> _defaultFlashcards = [
    Flashcard(id: '1', english: 'Hello', korean: '안녕하세요'),
    Flashcard(id: '2', english: 'Thank you', korean: '감사합니다'),
    Flashcard(id: '3', english: 'Good morning', korean: '좋은 아침입니다'),
    Flashcard(id: '4', english: 'Goodbye', korean: '안녕히 가세요'),
    Flashcard(id: '5', english: 'Sorry', korean: '죄송합니다'),
    Flashcard(id: '6', english: 'Friend', korean: '친구'),
    Flashcard(id: '7', english: 'Love', korean: '사랑'),
    Flashcard(id: '8', english: 'Food', korean: '음식'),
    Flashcard(id: '9', english: 'Water', korean: '물'),
    Flashcard(id: '10', english: 'Book', korean: '책'),
  ];

  FlashcardProvider() {
    _initialize();
  }

  List<Flashcard> get flashcards => _flashcards;
  int get currentIndex => _currentIndex;
  bool get isShowingFront => _isShowingFront;
  Flashcard get currentCard => _flashcards[_currentIndex];
  SyncStatus get syncStatus => _syncStatus;
  String? get errorMessage => _errorMessage;
  bool get isAuthenticated => _isAuthenticated;

  Future<void> _initialize() async {
    await _loadFlashcards();
  }

  Future<void> _loadFlashcards() async {
    // 먼저 기본 카드로 초기화
    _flashcards = [..._defaultFlashcards];
    notifyListeners();

    // Google Sheets에서 데이터 로드 시도
    try {
      await _loadFromSheets();
    } catch (e) {
      print('Error loading from sheets: $e');
      // 오류 발생 시 기본 카드 유지
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
    _syncStatus = SyncStatus.syncing;
    notifyListeners();

    try {
      final cards = await SheetsService.getFlashcards();
      if (cards.isNotEmpty) {
        _flashcards = cards;
        _syncStatus = SyncStatus.success;
      } else {
        // 스프레드시트에 데이터가 없으면 기본 카드 저장
        await SheetsService.saveAllFlashcards(_defaultFlashcards);
        _syncStatus = SyncStatus.success;
      }
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

  void flipCard() {
    _isShowingFront = !_isShowingFront;
    notifyListeners();
  }

  void nextCard() {
    if (_currentIndex < _flashcards.length - 1) {
      _currentIndex++;
      _isShowingFront = true;
      notifyListeners();
    }
  }

  void previousCard() {
    if (_currentIndex > 0) {
      _currentIndex--;
      _isShowingFront = true;
      notifyListeners();
    }
  }

  Future<void> markAsLearned() async {
    _flashcards[_currentIndex] = _flashcards[_currentIndex].copyWith(isLearned: true);
    notifyListeners();
    
    // 변경사항 자동 동기화
    await syncToSheets();
  }

  Future<void> resetLearningStatus() async {
    _flashcards = _flashcards.map((card) => card.copyWith(isLearned: false)).toList();
    notifyListeners();
    
    // 변경사항 자동 동기화
    await syncToSheets();
  }

  Future<void> addCard(String english, String korean) async {
    // 새 ID 생성 (마지막 ID + 1)
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
    if (_isAuthenticated) {
      await SheetsService.addFlashcard(newCard);
    } else {
      await syncToSheets();
    }
  }

  int get learnedCount {
    return _flashcards.where((card) => card.isLearned).length;
  }

  Future<void> signOut() async {
    await SheetsService.signOut();
    _isAuthenticated = false;
    notifyListeners();
    
    // 기본 카드로 초기화
    _flashcards = [..._defaultFlashcards];
    _currentIndex = 0;
    notifyListeners();
  }
} 