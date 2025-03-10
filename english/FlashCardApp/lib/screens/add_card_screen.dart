import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:flashcard_app/providers/flashcard_provider.dart';

class AddCardScreen extends StatefulWidget {
  const AddCardScreen({Key? key}) : super(key: key);

  @override
  State<AddCardScreen> createState() => _AddCardScreenState();
}

class _AddCardScreenState extends State<AddCardScreen> {
  final _formKey = GlobalKey<FormState>();
  final _englishController = TextEditingController();
  final _koreanController = TextEditingController();

  @override
  void dispose() {
    _englishController.dispose();
    _koreanController.dispose();
    super.dispose();
  }

  void _submitForm() {
    if (_formKey.currentState!.validate()) {
      final provider = Provider.of<FlashcardProvider>(context, listen: false);
      provider.addCard(
        _englishController.text.trim(),
        _koreanController.text.trim(),
      );

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('새 단어/문장이 추가되었습니다!'),
          duration: Duration(seconds: 2),
        ),
      );

      _englishController.clear();
      _koreanController.clear();
    }
  }

  @override
  Widget build(BuildContext context) {
    // 화면 높이를 구하기 위한 MediaQuery
    final screenHeight = MediaQuery.of(context).size.height;
    
    return Scaffold(
      appBar: AppBar(
        title: const Text('새 단어/문장 추가하기'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // 영어 입력 필드 - 높이를 화면의 약 1/4로 설정
              TextFormField(
                controller: _englishController,
                decoration: InputDecoration(
                  labelText: '영어 단어/문장',
                  hintText: '예: Hello',
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(8),
                  ),
                  prefixIcon: const Icon(Icons.language),
                  alignLabelWithHint: true, // 레이블이 큰 텍스트필드에서도 정렬되도록
                ),
                textCapitalization: TextCapitalization.sentences,
                validator: (value) {
                  if (value == null || value.trim().isEmpty) {
                    return '영어 단어/문장을 입력해주세요';
                  }
                  return null;
                },
                maxLines: null, // 여러 줄 입력 가능
                minLines: 5, // 최소 5줄
                textAlignVertical: TextAlignVertical.top, // 텍스트를 상단에서 시작
              ),
              const SizedBox(height: 16),

              // 한글 입력 필드 - 높이를 화면의 약 1/4로 설정
              TextFormField(
                controller: _koreanController,
                decoration: InputDecoration(
                  labelText: '한글 의미',
                  hintText: '예: 안녕하세요',
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(8),
                  ),
                  prefixIcon: const Icon(Icons.translate),
                  alignLabelWithHint: true, // 레이블이 큰 텍스트필드에서도 정렬되도록
                ),
                validator: (value) {
                  if (value == null || value.trim().isEmpty) {
                    return '한글 의미를 입력해주세요';
                  }
                  return null;
                },
                maxLines: null, // 여러 줄 입력 가능
                minLines: 5, // 최소 5줄
                textAlignVertical: TextAlignVertical.top, // 텍스트를 상단에서 시작
              ),
              const SizedBox(height: 32),

              // 추가 버튼
              ElevatedButton.icon(
                icon: const Icon(Icons.add),
                label: const Text('단어/문장 추가하기'),
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.all(16),
                  textStyle: const TextStyle(fontSize: 18),
                ),
                onPressed: _submitForm,
              ),
              const SizedBox(height: 16),

              // 팁 카드
              Card(
                margin: const EdgeInsets.only(top: 16),
                color: Colors.amber.shade50,
                child: const Padding(
                  padding: EdgeInsets.all(16.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        '💡 팁',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      SizedBox(height: 8),
                      Text(
                        '• 단어뿐만 아니라 자주 쓰는 문장도 추가해보세요.\n'
                        '• 관련 단어들을 함께 학습하면 기억하기 쉽습니다.\n'
                        '• 매일 일정 시간 학습하는 것이 효과적입니다.',
                        style: TextStyle(fontSize: 14),
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
} 