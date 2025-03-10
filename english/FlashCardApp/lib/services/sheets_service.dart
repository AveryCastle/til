import 'package:google_sign_in/google_sign_in.dart';
import 'package:googleapis/sheets/v4.dart';
import 'package:http/http.dart' as http;
import 'package:googleapis_auth/auth_io.dart';
import 'package:flashcard_app/config/app_config.dart';
import 'package:flashcard_app/models/flashcard_model.dart';

class SheetsService {
  static final _googleSignIn = GoogleSignIn(
    scopes: [
      'email',
      'https://www.googleapis.com/auth/spreadsheets',
    ],
    clientId: AppConfig.clientId,
  );
  
  static const String _spreadsheetName = 'FlashcardApp_Data';
  static const List<String> _headers = ['id', 'english', 'korean', 'isLearned'];
  
  static SheetsApi? _sheetsApi;
  static String? _spreadsheetId;
  
  // 로그인 및 인증
  static Future<bool> signIn() async {
    try {
      final account = await _googleSignIn.signIn();
      if (account == null) return false;
      
      // 인증 정보 가져오기
      final auth = await account.authentication;
      final accessToken = auth.accessToken;
      if (accessToken == null) return false;
      
      // HTTP 클라이언트에 토큰 설정
      final client = http.Client();
      final authClient = AuthClient(client, accessToken);
      
      _sheetsApi = SheetsApi(authClient);
      return true;
    } catch (e) {
      print('Authentication error: $e');
      return false;
    }
  }
  
  // 스프레드시트 초기화
  static Future<bool> initSpreadsheet() async {
    if (_sheetsApi == null) {
      final isSignedIn = await signIn();
      if (!isSignedIn) return false;
    }
    
    try {
      // 새 스프레드시트 생성
      final spreadsheet = Spreadsheet(properties: SpreadsheetProperties(
        title: _spreadsheetName,
      ));
      
      final createdSheet = await _sheetsApi!.spreadsheets.create(spreadsheet);
      _spreadsheetId = createdSheet.spreadsheetId;
      
      // 헤더 추가
      await _sheetsApi!.spreadsheets.values.update(
        ValueRange(values: [_headers]),
        _spreadsheetId!,
        'A1:D1',
        valueInputOption: 'USER_ENTERED',
      );
      
      return true;
    } catch (e) {
      print('Spreadsheet initialization error: $e');
      return false;
    }
  }
  
  // 모든 카드 가져오기
  static Future<List<Flashcard>> getFlashcards() async {
    if (_spreadsheetId == null) {
      final isInitialized = await initSpreadsheet();
      if (!isInitialized) return [];
    }
    
    try {
      final response = await _sheetsApi!.spreadsheets.values.get(
        _spreadsheetId!,
        'A2:D',
      );
      
      final values = response.values;
      if (values == null || values.isEmpty) return [];
      
      return values.map((row) {
        return Flashcard(
          id: row[0].toString(),
          english: row[1].toString(),
          korean: row[2].toString(),
          isLearned: row[3].toString() == '1',
        );
      }).toList();
    } catch (e) {
      print('Error getting flashcards: $e');
      return [];
    }
  }
  
  // 모든 카드 저장하기
  static Future<bool> saveAllFlashcards(List<Flashcard> flashcards) async {
    if (_spreadsheetId == null) {
      final isInitialized = await initSpreadsheet();
      if (!isInitialized) return false;
    }
    
    try {
      // 데이터를 2D 배열로 변환
      final values = flashcards.map((card) => [
        card.id,
        card.english,
        card.korean,
        card.isLearned ? '1' : '0',
      ]).toList();
      
      // 기존 데이터 지우기
      await _sheetsApi!.spreadsheets.values.clear(
        ClearValuesRequest(),
        _spreadsheetId!,
        'A2:D',
      );
      
      // 새 데이터 추가
      if (values.isNotEmpty) {
        await _sheetsApi!.spreadsheets.values.update(
          ValueRange(values: values),
          _spreadsheetId!,
          'A2:D${values.length + 1}',
          valueInputOption: 'USER_ENTERED',
        );
      }
      
      return true;
    } catch (e) {
      print('Error saving flashcards: $e');
      return false;
    }
  }
  
  // 카드 추가하기
  static Future<bool> addFlashcard(Flashcard card) async {
    if (_spreadsheetId == null) {
      final isInitialized = await initSpreadsheet();
      if (!isInitialized) return false;
    }
    
    try {
      // 가장 마지막 행 찾기
      final response = await _sheetsApi!.spreadsheets.values.get(
        _spreadsheetId!,
        'A:A',
      );
      
      final rowCount = response.values?.length ?? 1;
      final nextRow = rowCount + 1;
      
      // 새 카드 추가
      await _sheetsApi!.spreadsheets.values.update(
        ValueRange(values: [[
          card.id,
          card.english,
          card.korean,
          card.isLearned ? '1' : '0',
        ]]),
        _spreadsheetId!,
        'A$nextRow:D$nextRow',
        valueInputOption: 'USER_ENTERED',
      );
      
      return true;
    } catch (e) {
      print('Error adding flashcard: $e');
      return false;
    }
  }
  
  // 로그아웃
  static Future<void> signOut() async {
    await _googleSignIn.signOut();
    _sheetsApi = null;
    _spreadsheetId = null;
  }
}

// OAuth 토큰을 사용하는 HTTP 클라이언트 구현
class AuthClient extends http.BaseClient {
  final http.Client _inner;
  final String _accessToken;
  
  AuthClient(this._inner, this._accessToken);
  
  @override
  Future<http.StreamedResponse> send(http.BaseRequest request) {
    request.headers['Authorization'] = 'Bearer $_accessToken';
    return _inner.send(request);
  }
} 