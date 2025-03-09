import 'package:flutter/material.dart';
import 'package:flashcard_app/models/flashcard_model.dart';

class FlashcardProvider extends ChangeNotifier {
  List<Flashcard> _flashcards = [];
  int _currentIndex = 0;
  bool _isShowingFront = true;

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
    _loadFlashcards();
  }

  List<Flashcard> get flashcards => _flashcards;
  int get currentIndex => _currentIndex;
  bool get isShowingFront => _isShowingFront;
  Flashcard get currentCard => _flashcards[_currentIndex];

  void _loadFlashcards() {
    // 실제 앱에서는 여기서 데이터베이스에서 로드
    _flashcards = [..._defaultFlashcards];
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

  void markAsLearned() {
    _flashcards[_currentIndex] = _flashcards[_currentIndex].copyWith(isLearned: true);
    notifyListeners();
  }

  void resetLearningStatus() {
    _flashcards = _flashcards.map((card) => card.copyWith(isLearned: false)).toList();
    notifyListeners();
  }

  void addCard(String english, String korean) {
    final newId = (int.parse(_flashcards.last.id) + 1).toString();
    _flashcards.add(
      Flashcard(
        id: newId,
        english: english,
        korean: korean,
      ),
    );
    notifyListeners();
  }

  int get learnedCount {
    return _flashcards.where((card) => card.isLearned).length;
  }
} 