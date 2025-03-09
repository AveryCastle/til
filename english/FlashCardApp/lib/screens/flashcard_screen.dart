class FlashcardScreen extends StatefulWidget {
  @override
  _FlashcardScreenState createState() => _FlashcardScreenState();
}

class _FlashcardScreenState extends State<FlashcardScreen> {
  bool isFlipped = false;
  bool showConfetti = false;
  late Timer _flipTimer;
  late Timer _nextCardTimer;
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        children: [
          if (showConfetti)
            ConfettiWidget(
              confettiController: _confettiController,
              blastDirection: pi/2,
              maxBlastForce: 5,
              minBlastForce: 2,
              emissionFrequency: 0.05,
            ),
          AnimatedBuilder(
            animation: _cardAnimation,
            builder: (context, child) {
              return Transform(
                transform: Matrix4.identity()
                  ..setEntry(3, 2, 0.001)
                  ..rotateY(pi * _cardAnimation.value),
                alignment: Alignment.center,
                child: Card(
                  child: _buildCardContent(),
                ),
              );
            },
          ),
        ],
      ),
    );
  }

  Widget _buildCardContent() {
    if (_cardAnimation.value < 0.5) {
      return Text(currentCard.preferredLanguageText);
    } else {
      return Transform(
        alignment: Alignment.center,
        transform: Matrix4.identity()..rotateY(pi),
        child: Text(currentCard.secondaryLanguageText),
      );
    }
  }
} 