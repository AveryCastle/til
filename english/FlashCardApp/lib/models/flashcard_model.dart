class Flashcard {
  final String id;
  final String english;
  final String korean;
  bool isLearned;

  Flashcard({
    required this.id,
    required this.english,
    required this.korean,
    this.isLearned = false,
  });

  Flashcard copyWith({
    String? id,
    String? english,
    String? korean,
    bool? isLearned,
  }) {
    return Flashcard(
      id: id ?? this.id,
      english: english ?? this.english,
      korean: korean ?? this.korean,
      isLearned: isLearned ?? this.isLearned,
    );
  }

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'english': english,
      'korean': korean,
    };
  }

  factory Flashcard.fromMap(Map<String, dynamic> map) {
    return Flashcard(
      id: map['id'],
      english: map['english'],
      korean: map['korean'],
    );
  }
} 