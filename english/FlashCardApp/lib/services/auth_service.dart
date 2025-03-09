class AuthService {
  final GoogleSignIn _googleSignIn = GoogleSignIn(
    scopes: [
      'https://www.googleapis.com/auth/drive.file',
      'https://www.googleapis.com/auth/spreadsheets'
    ],
    clientId: '15020443312-kji0bs11r7ct46gr48mmn796p3o1d5p9.apps.googleusercontent.com', // iOS 클라이언트 ID
  );
  final FlutterSecureStorage _storage = FlutterSecureStorage();
  
  GoogleSignInAccount? _currentUser;
  
  // 현재 로그인된 사용자 가져오기
  GoogleSignInAccount? get currentUser => _currentUser;

  // 초기 인증 상태 확인
  Future<void> initAuth() async {
    _currentUser = await _googleSignIn.signInSilently();
  }

  // 로그인
  Future<GoogleSignInAccount?> signIn() async {
    try {
      final account = await _googleSignIn.signIn();
      if (account != null) {
        _currentUser = account;
        final auth = await account.authentication;
        
        // 토큰 안전하게 저장
        await _storage.write(
          key: 'google_access_token',
          value: auth.accessToken,
        );
        await _storage.write(
          key: 'google_id_token',
          value: auth.idToken,
        );
        
        // 토큰 만료 시간 저장
        final expiryTime = DateTime.now().add(Duration(hours: 1));
        await _storage.write(
          key: 'token_expiry',
          value: expiryTime.toIso8601String(),
        );
      }
      return account;
    } catch (error) {
      print('Sign in error: $error');
      throw AuthException('Google 로그인 중 오류가 발생했습니다');
    }
  }

  // 로그아웃
  Future<void> signOut() async {
    await _googleSignIn.signOut();
    await _storage.deleteAll();
    _currentUser = null;
  }

  // 토큰 새로고침
  Future<String?> refreshToken() async {
    try {
      final account = _currentUser ?? await _googleSignIn.signInSilently();
      if (account != null) {
        final auth = await account.authentication;
        await _storage.write(
          key: 'google_access_token',
          value: auth.accessToken,
        );
        return auth.accessToken;
      }
      return null;
    } catch (error) {
      print('Token refresh error: $error');
      throw AuthException('토큰 갱신 중 오류가 발생했습니다');
    }
  }

  // 토큰 유효성 검사
  Future<bool> isTokenValid() async {
    final expiryTimeStr = await _storage.read(key: 'token_expiry');
    if (expiryTimeStr == null) return false;
    
    final expiryTime = DateTime.parse(expiryTimeStr);
    return DateTime.now().isBefore(expiryTime);
  }
}

class AuthException implements Exception {
  final String message;
  AuthException(this.message);
} 