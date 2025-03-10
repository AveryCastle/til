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
    final isAuthenticated = flashcardProvider.isAuthenticated;
    
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
            // 구글 로그인 상태 표시 - 더 눈에 띄게 수정
            _buildGoogleLoginStatus(context, flashcardProvider),
            const SizedBox(height: 16),
            
            // 상단 정보 카드 - 로그인했을 때만 표시
            if (isAuthenticated) 
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
                      _buildStatCard(
                        context,
                        '총 단어/문장 수',
                        '${flashcardProvider.flashcards.length}',
                        Icons.library_books,
                      ),
                    ],
                  ),
                ),
              ),
            
            if (!isAuthenticated)
              // 로그인 안 된 경우 안내 메시지
              Card(
                elevation: 3,
                child: Padding(
                  padding: const EdgeInsets.all(24.0),
                  child: Column(
                    children: [
                      const Icon(
                        Icons.info_outline,
                        size: 48,
                        color: Colors.blue,
                      ),
                      const SizedBox(height: 16),
                      const Text(
                        '서비스 이용을 위해 로그인이 필요합니다',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: 8),
                      const Text(
                        '구글 계정으로 로그인하면 플래시카드를 사용할 수 있습니다.',
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: 24),
                      ElevatedButton.icon(
                        icon: const Icon(Icons.login),
                        label: const Text('구글 로그인'),
                        style: ElevatedButton.styleFrom(
                          padding: const EdgeInsets.symmetric(
                            vertical: 12,
                            horizontal: 24,
                          ),
                        ),
                        onPressed: () => _showLoginDialog(context),
                      ),
                    ],
                  ),
                ),
              ),
            
            const SizedBox(height: 32),
            
            // 메인 버튼들 - 로그인 상태에 따라 활성화/비활성화
            ElevatedButton.icon(
              icon: const Icon(Icons.school),
              label: const Text('플래시카드 학습하기'),
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.all(16),
                textStyle: const TextStyle(fontSize: 18),
                // 비활성화 시 색상 설정
                disabledBackgroundColor: Colors.grey.shade300,
                disabledForegroundColor: Colors.grey.shade600,
              ),
              onPressed: isAuthenticated && flashcardProvider.flashcards.isNotEmpty
                  ? () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) => const FlashcardScreen(),
                        ),
                      );
                    }
                  : null, // 로그인 안 되어 있으면 비활성화
            ),
            const SizedBox(height: 16),
            ElevatedButton.icon(
              icon: const Icon(Icons.add),
              label: const Text('새 단어/문장 추가하기'),
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.all(16),
                textStyle: const TextStyle(fontSize: 18),
                disabledBackgroundColor: Colors.grey.shade300,
                disabledForegroundColor: Colors.grey.shade600,
              ),
              onPressed: isAuthenticated
                  ? () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) => const AddCardScreen(),
                        ),
                      );
                    }
                  : null, // 로그인 안 되어 있으면 비활성화
            ),
            const SizedBox(height: 16),
            OutlinedButton.icon(
              icon: const Icon(Icons.sync_alt),  // 아이콘 변경: refresh → sync_alt
              label: const Text('단어/문장 동기화'),  // 라벨 변경: '학습 상태 초기화' → '단어/문장 동기화'
              style: OutlinedButton.styleFrom(
                padding: const EdgeInsets.all(16),
                textStyle: const TextStyle(fontSize: 18),
                disabledForegroundColor: Colors.grey.shade400,
              ),
              onPressed: isAuthenticated
                  ? () {
                      showDialog(
                        context: context,
                        builder: (context) => AlertDialog(
                          title: const Text('단어/문장 동기화'),
                          content: const Text(
                            '앱 데이터와 구글 스프레드시트의 데이터를 양방향으로 동기화합니다.\n\n'
                            '- 앱에만 있는 데이터는 스프레드시트에 추가됩니다.\n'
                            '- 스프레드시트에만 있는 데이터는 앱에 추가됩니다.\n\n'
                            '진행하시겠습니까?'
                          ),
                          actions: [
                            TextButton(
                              child: const Text('취소'),
                              onPressed: () {
                                Navigator.of(context).pop();
                              },
                            ),
                            TextButton(
                              child: const Text('동기화'),
                              onPressed: () async {
                                Navigator.of(context).pop();
                                
                                // 로딩 다이얼로그 표시
                                showDialog(
                                  context: context,
                                  barrierDismissible: false,
                                  builder: (context) => const Center(
                                    child: CircularProgressIndicator(),
                                  ),
                                );
                                
                                // 양방향 동기화 실행
                                await flashcardProvider.syncBidirectional();
                                
                                // 로딩 다이얼로그 닫기
                                if (!context.mounted) return;
                                Navigator.of(context).pop();
                                
                                // 결과 메시지 표시
                                if (!context.mounted) return;
                                ScaffoldMessenger.of(context).showSnackBar(
                                  const SnackBar(
                                    content: Text('단어/문장 동기화가 완료되었습니다.'),
                                  ),
                                );
                              },
                            ),
                          ],
                        ),
                      );
                    }
                  : null, // 로그인 안 되어 있으면 비활성화
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
      elevation: 4, // 더 눈에 띄게 그림자 강화
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
        side: BorderSide(
          color: isAuthenticated ? Colors.green.shade300 : Colors.orange.shade300,
          width: 1.5,
        ),
      ),
      child: Padding(
        padding: const EdgeInsets.symmetric(vertical: 16.0, horizontal: 12.0),
        child: Row(
          children: [
            Icon(
              isAuthenticated ? Icons.cloud_done : Icons.cloud_off,
              color: isAuthenticated ? Colors.green : Colors.orange,
              size: 32, // 아이콘 크기 증가
            ),
            const SizedBox(width: 16),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    isAuthenticated 
                        ? '구글 스프레드시트에 연결됨' 
                        : '구글 스프레드시트에 연결되지 않음',
                    style: const TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                  if (!isAuthenticated)
                    const Text(
                      '서비스 이용을 위해 로그인이 필요합니다',
                      style: TextStyle(
                        fontSize: 12,
                        color: Colors.black54,
                      ),
                    ),
                ],
              ),
            ),
            if (syncStatus == SyncStatus.syncing)
              const SizedBox(
                width: 24,
                height: 24,
                child: CircularProgressIndicator(
                  strokeWidth: 2,
                ),
              )
            else if (!isAuthenticated)
              TextButton.icon(
                icon: const Icon(Icons.login),
                label: const Text('로그인'),
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
          ElevatedButton.icon(
            icon: const Icon(Icons.login),
            label: const Text('로그인'),
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
      width: double.infinity, // 전체 폭 사용
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