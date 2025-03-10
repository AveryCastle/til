import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:flashcard_app/providers/flashcard_provider.dart';
import 'dart:math' as math;

class FlashcardScreen extends StatelessWidget {
  const FlashcardScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('플래시카드 학습'),
      ),
      body: const _FlashcardContent(),
      backgroundColor: Colors.grey.shade100,
    );
  }
}

class _FlashcardContent extends StatefulWidget {
  const _FlashcardContent();

  @override
  _FlashcardContentState createState() => _FlashcardContentState();
}

class _FlashcardContentState extends State<_FlashcardContent> with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _frontRotation;
  late Animation<double> _backRotation;
  bool _isFrontVisible = true;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(milliseconds: 500),
      vsync: this,
    );

    _frontRotation = TweenSequence<double>([
      TweenSequenceItem<double>(
        tween: Tween<double>(begin: 0.0, end: math.pi / 2)
            .chain(CurveTween(curve: Curves.easeInOut)),
        weight: 50.0,
      ),
      TweenSequenceItem<double>(
        tween: ConstantTween<double>(math.pi / 2),
        weight: 50.0,
      ),
    ]).animate(_controller);

    _backRotation = TweenSequence<double>([
      TweenSequenceItem<double>(
        tween: ConstantTween<double>(math.pi / 2),
        weight: 50.0,
      ),
      TweenSequenceItem<double>(
        tween: Tween<double>(begin: -math.pi / 2, end: 0.0)
            .chain(CurveTween(curve: Curves.easeInOut)),
        weight: 50.0,
      ),
    ]).animate(_controller);

    _controller.addStatusListener((status) {
      if (status == AnimationStatus.completed ||
          status == AnimationStatus.dismissed) {
        _isFrontVisible = _controller.value == 0.0;
        final provider = Provider.of<FlashcardProvider>(context, listen: false);
        if (provider.isShowingFront != _isFrontVisible) {
          provider.flipCard();
        }
      }
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void _flipCard() {
    if (_controller.isAnimating) return;

    if (_controller.value == 0.0) {
      _controller.forward();
    } else {
      _controller.reverse();
    }
  }

  @override
  Widget build(BuildContext context) {
    final provider = Provider.of<FlashcardProvider>(context);
    final flashcards = provider.flashcards;
    
    // 카드가 없는 경우 처리
    if (flashcards.isEmpty) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(
              Icons.info_outline,
              size: 64,
              color: Colors.blue,
            ),
            const SizedBox(height: 16),
            const Text(
              '등록된 플래시카드가 없습니다',
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 8),
            const Text(
              '새 단어/문장 추가하기 버튼을 통해\n학습할 내용을 추가해보세요.',
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 32),
            ElevatedButton.icon(
              icon: const Icon(Icons.add),
              label: const Text('새 단어/문장 추가하기'),
              onPressed: () {
                Navigator.pop(context); // 이전 화면으로 돌아가기
              },
            ),
          ],
        ),
      );
    }
    
    final currentCard = provider.currentCard!;
    final currentIndex = provider.currentIndex;

    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        children: [
          // 진행 상태 표시
          Padding(
            padding: const EdgeInsets.symmetric(vertical: 12.0),
            child: Text(
              '${currentIndex + 1} / ${flashcards.length}',
              style: const TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.w500,
              ),
            ),
          ),
          LinearProgressIndicator(
            value: (currentIndex + 1) / flashcards.length,
            backgroundColor: Colors.grey.shade300,
          ),
          const SizedBox(height: 24),
          
          // 플래시카드
          Expanded(
            child: GestureDetector(
              onTap: _flipCard,
              child: AnimatedBuilder(
                animation: _controller,
                builder: (context, child) {
                  return Stack(
                    alignment: Alignment.center,
                    children: [
                      // 앞면 (영어)
                      Transform(
                        transform: Matrix4.identity()
                          ..setEntry(3, 2, 0.001)
                          ..rotateY(_frontRotation.value),
                        alignment: Alignment.center,
                        child: _isFrontVisible
                            ? _buildCard(
                                context,
                                currentCard.english,
                                Colors.white,
                                '탭하여 한글 보기',
                              )
                            : const SizedBox.shrink(),
                      ),
                      
                      // 뒷면 (한글)
                      Transform(
                        transform: Matrix4.identity()
                          ..setEntry(3, 2, 0.001)
                          ..rotateY(_backRotation.value),
                        alignment: Alignment.center,
                        child: !_isFrontVisible
                            ? _buildCard(
                                context,
                                currentCard.korean,
                                Colors.blue.shade50,
                                '탭하여 영어 보기',
                              )
                            : const SizedBox.shrink(),
                      ),
                    ],
                  );
                },
              ),
            ),
          ),
          
          // 하단 컨트롤 버튼
          const SizedBox(height: 24),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              IconButton(
                icon: const Icon(Icons.arrow_back),
                iconSize: 32,
                onPressed: currentIndex > 0
                    ? () {
                        provider.previousCard();
                        setState(() {
                          _isFrontVisible = true;
                          _controller.value = 0.0;
                        });
                      }
                    : null,
                color: Colors.blue,
              ),
              // '학습 완료' 버튼 제거 - 가운데 공간 유지
              const SizedBox(width: 100),
              IconButton(
                icon: const Icon(Icons.arrow_forward),
                iconSize: 32,
                onPressed: currentIndex < flashcards.length - 1
                    ? () {
                        provider.nextCard();
                        setState(() {
                          _isFrontVisible = true;
                          _controller.value = 0.0;
                        });
                      }
                    : null,
                color: Colors.blue,
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildCard(
    BuildContext context,
    String text,
    Color color,
    String helpText,
  ) {
    return Card(
      elevation: 8,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
      ),
      color: color,
      child: Container(
        width: double.infinity,
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            // 스크롤 가능한 텍스트 영역 (수직, 수평 정중앙에 배치)
            Expanded(
              child: Center(
                child: SingleChildScrollView(
                  physics: const BouncingScrollPhysics(),
                  child: Container(
                    // 전체 높이를 활용하기 위한 Container
                    padding: const EdgeInsets.symmetric(vertical: 20),
                    child: Center(
                      child: Text(
                        text,
                        style: const TextStyle(
                          fontSize: 32,
                          fontWeight: FontWeight.bold,
                          height: 1.3, // 줄 간격 조정
                        ),
                        textAlign: TextAlign.center,
                      ),
                    ),
                  ),
                ),
              ),
            ),
            // 스크롤 힌트 표시기
            Container(
              height: 4,
              width: 40,
              margin: const EdgeInsets.only(top: 8, bottom: 16),
              decoration: BoxDecoration(
                color: Colors.grey.withOpacity(0.3),
                borderRadius: BorderRadius.circular(2),
              ),
            ),
            // 도움말 텍스트
            Text(
              helpText,
              style: TextStyle(
                fontSize: 14,
                color: Colors.grey.shade600,
              ),
            ),
          ],
        ),
      ),
    );
  }
} 