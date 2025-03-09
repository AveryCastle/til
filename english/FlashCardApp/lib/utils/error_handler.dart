class ErrorHandler {
  static void handleError(BuildContext context, dynamic error) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(_getErrorMessage(error)),
        action: SnackBarAction(
          label: '재시도',
          onPressed: () {
            // 재시도 로직
          },
        ),
      ),
    );
  }

  static String _getErrorMessage(dynamic error) {
    if (error is NetworkException) {
      return '네트워크 연결을 확인해주세요.';
    } else if (error is GoogleAPIException) {
      return 'Google 서비스 연결에 실패했습니다.';
    }
    return '오류가 발생했습니다. 다시 시도해주세요.';
  }
} 