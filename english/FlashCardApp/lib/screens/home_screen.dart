import 'package:flutter/material.dart';
import 'package:flashcard_app/screens/flashcard_screen.dart';
import 'package:flashcard_app/screens/add_card_screen.dart';
import 'package:flashcard_app/providers/flashcard_provider.dart';
import 'package:provider/provider.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final flashcardProvider = Provider.of<FlashcardProvider>(context);
    
    return Scaffold(
      appBar: AppBar(
        title: const Text('영어-한글 플래시카드'),
        elevation: 2,
        actions: [
          IconButton(
            icon: const Icon(Icons.sync),
            tooltip: '구글 스프레드시트와 동기화',
            onPressed: () async {
              if (!flashcardProvider.isAuthenticated) {
                final result = await _showLoginDialog(context);
                if (result != true) return;
              }
              await flashcardProvider.syncToSheets();
              
              // 동기화 결과 표시
              if (!context.mounted) return;
              if (flashcardProvider.syncStatus == SyncStatus.success) {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('동기화 완료!')),
                );
              } else if (flashcardProvider.syncStatus == SyncStatus.error) {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text('동기화 오류: ${flashcardProvider.errorMessage}')),
                );
              }
            },
          ),
          if (flashcardProvider.isAuthenticated)
            IconButton(
              icon: const Icon(Icons.logout),
              tooltip: '로그아웃',
              onPressed: () async {
                await flashcardProvider.signOut();
                if (!context.mounted) return;
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('로그아웃 되었습니다')),
                );
              },
            ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // 구글 로그인 상태 표시
            _buildGoogleLoginStatus(context, flashcardProvider),
            const SizedBox(height: 16),
            
            // 상단 정보 카드
            Card(
              elevation: 3,
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  children: [
                    const Text(
                      '학습 현황',
                      style: TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 16),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                      children: [
                        _buildStatCard(
                          context,
                          '총 단어 수',
                          '${flashcardProvider.flashcards.length}',
                          Icons.library_books,
                        ),
                        _buildStatCard(
                          context,
                          '학습 완료',
                          '${flashcardProvider.learnedCount}',
                          Icons.check_circle,
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 32),
            
            // 메인 버튼들
            ElevatedButton.icon(
              icon: const Icon(Icons.school),
              label: const Text('플래시카드 학습하기'),
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.all(16),
                textStyle: const TextStyle(fontSize: 18),
              ),
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => const FlashcardScreen(),
                  ),
                );
              },
            ),
            const SizedBox(height: 16),
            ElevatedButton.icon(
              icon: const Icon(Icons.add),
              label: const Text('새 단어 추가하기'),
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.all(16),
                textStyle: const TextStyle(fontSize: 18),
              ),
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => const AddCardScreen(),
                  ),
                );
              },
            ),
            const SizedBox(height: 16),
            OutlinedButton.icon(
              icon: const Icon(Icons.refresh),
              label: const Text('학습 상태 초기화'),
              style: OutlinedButton.styleFrom(
                padding: const EdgeInsets.all(16),
                textStyle: const TextStyle(fontSize: 18),
              ),
              onPressed: () {
                showDialog(
                  context: context,
                  builder: (context) => AlertDialog(
                    title: const Text('학습 상태 초기화'),
                    content: const Text('모든 단어의 학습 상태를 초기화하시겠습니까?'),
                    actions: [
                      TextButton(
                        child: const Text('취소'),
                        onPressed: () {
                          Navigator.of(context).pop();
                        },
                      ),
                      TextButton(
                        child: const Text('초기화'),
                        onPressed: () async {
                          Navigator.of(context).pop();
                          await flashcardProvider.resetLearningStatus();
                          if (!context.mounted) return;
                          ScaffoldMessenger.of(context).showSnackBar(
                            const SnackBar(
                              content: Text('학습 상태가 초기화되었습니다.'),
                            ),
                          );
                        },
                      ),
                    ],
                  ),
                );
              },
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildGoogleLoginStatus(BuildContext context, FlashcardProvider provider) {
    final isAuthenticated = provider.isAuthenticated;
    final syncStatus = provider.syncStatus;
    
    return Card(
      color: isAuthenticated ? Colors.green.shade50 : Colors.orange.shade50,
      child: Padding(
        padding: const EdgeInsets.all(12.0),
        child: Row(
          children: [
            Icon(
              isAuthenticated ? Icons.cloud_done : Icons.cloud_off,
              color: isAuthenticated ? Colors.green : Colors.orange,
              size: 28,
            ),
            const SizedBox(width: 12),
            Expanded(
              child: Text(
                isAuthenticated 
                    ? '구글 스프레드시트에 연결됨' 
                    : '구글 스프레드시트에 연결되지 않음',
                style: const TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.w500,
                ),
              ),
            ),
            if (syncStatus == SyncStatus.syncing)
              const SizedBox(
                width: 20,
                height: 20,
                child: CircularProgressIndicator(
                  strokeWidth: 2,
                ),
              )
            else if (!isAuthenticated)
              TextButton(
                child: const Text('로그인'),
                onPressed: () => _showLoginDialog(context),
              ),
          ],
        ),
      ),
    );
  }

  Future<bool?> _showLoginDialog(BuildContext context) {
    return showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('구글 로그인'),
        content: const Text(
          '구글 스프레드시트에 플래시카드를 저장하려면 구글 계정에 로그인해야 합니다.\n\n'
          '로그인하시겠습니까?'
        ),
        actions: [
          TextButton(
            child: const Text('취소'),
            onPressed: () {
              Navigator.of(context).pop(false);
            },
          ),
          TextButton(
            child: const Text('로그인'),
            onPressed: () async {
              final provider = Provider.of<FlashcardProvider>(context, listen: false);
              await provider.authenticate();
              if (!context.mounted) return;
              Navigator.of(context).pop(true);
              
              // 로그인 결과 메시지
              if (!context.mounted) return;
              if (provider.isAuthenticated) {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('구글 계정에 로그인되었습니다')),
                );
              } else {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text('로그인 실패: ${provider.errorMessage}')),
                );
              }
            },
          ),
        ],
      ),
    );
  }

  Widget _buildStatCard(
    BuildContext context,
    String title,
    String value,
    IconData icon,
  ) {
    return Container(
      width: 140,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.blue.withOpacity(0.1),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Column(
        children: [
          Icon(icon, size: 32, color: Theme.of(context).primaryColor),
          const SizedBox(height: 8),
          Text(
            title,
            style: const TextStyle(
              fontSize: 14,
              fontWeight: FontWeight.w500,
            ),
          ),
          const SizedBox(height: 4),
          Text(
            value,
            style: const TextStyle(
              fontSize: 24,
              fontWeight: FontWeight.bold,
            ),
          ),
        ],
      ),
    );
  }
} 