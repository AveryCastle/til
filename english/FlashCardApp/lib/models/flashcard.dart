class Flashcard {
  final String english;
  final String korean;
  final int dayNumber;
  DateTime? lastReviewed;

  Flashcard({
    required this.english,
    required this.korean,
    required this.dayNumber,
    this.lastReviewed,
  });

  factory Flashcard.fromJson(Map<String, dynamic> json) {
    return Flashcard(
      english: json['english'],
      korean: json['korean'],
      dayNumber: json['dayNumber'],
      lastReviewed: json['lastReviewed'] != null 
          ? DateTime.parse(json['lastReviewed'])
          : null,
    );
  }
} 