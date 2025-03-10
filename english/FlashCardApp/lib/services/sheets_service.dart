import 'package:google_sign_in/google_sign_in.dart';
import 'package:googleapis/sheets/v4.dart';
import 'package:googleapis/drive/v3.dart' as drive;
import 'package:http/http.dart' as http;
import 'package:googleapis_auth/auth_io.dart';
import 'package:flashcard_app/config/app_config.dart';
import 'package:flashcard_app/models/flashcard_model.dart';

class SheetsService {
  static final _googleSignIn = GoogleSignIn(
    scopes: [
      'email',
      'https://www.googleapis.com/auth/spreadsheets',
      'https://www.googleapis.com/auth/drive.readonly', // 드라이브 파일 목록 읽기 권한 추가
    ],
    clientId: AppConfig.clientId,
  );
  
  // 스프레드시트 이름과 시트 이름 상수
  static const String _spreadsheetName = 'FlashcardApp_Data';
  static const String _activeSheetName = '1일전';
  static const List<String> _headers = ['id', 'english', 'korean'];
  
  // API 및 스프레드시트 ID 저장 변수
  static SheetsApi? _sheetsApi;
  static drive.DriveApi? _driveApi;
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
      _driveApi = drive.DriveApi(authClient);
      return true;
    } catch (e) {
      print('Authentication error: $e');
      return false;
    }
  }
  
  // 스프레드시트 초기화 - 존재하면 사용, 없으면 새로 생성
  static Future<bool> initSpreadsheet() async {
    if (_sheetsApi == null || _driveApi == null) {
      final isSignedIn = await signIn();
      if (!isSignedIn) return false;
    }
    
    try {
      // 드라이브 API를 사용하여 FlashcardApp_Data 이름의 스프레드시트 검색
      final fileList = await _driveApi!.files.list(
        q: "name = '$_spreadsheetName' and mimeType = 'application/vnd.google-apps.spreadsheet' and trashed = false",
      );
      
      final files = fileList.files ?? [];
      
      if (files.isNotEmpty) {
        // 기존 스프레드시트 사용
        _spreadsheetId = files.first.id;
        print('기존 스프레드시트 사용: $_spreadsheetId');
        
        // 필요한 시트가 모두 있는지 확인하고 필요한 경우 추가
        await _ensureRequiredSheets();
      } else {
        // 스프레드시트가 없는 경우 새로 생성
        print('새 스프레드시트 생성: $_spreadsheetName');
        await _createNewSpreadsheet(_spreadsheetName);
      }
      
      return true;
    } catch (e) {
      print('Spreadsheet initialization error: $e');
      return false;
    }
  }
  
  // 새 스프레드시트 생성
  static Future<void> _createNewSpreadsheet(String title) async {
    // 기본 시트 1개로 스프레드시트 생성
    final spreadsheet = Spreadsheet(
      properties: SpreadsheetProperties(
        title: title,
      ),
    );
    
    final createdSheet = await _sheetsApi!.spreadsheets.create(spreadsheet);
    _spreadsheetId = createdSheet.spreadsheetId;
    
    // 첫 번째 시트 이름을 '1일전'으로 변경
    if (_spreadsheetId != null && createdSheet.sheets != null && createdSheet.sheets!.isNotEmpty) {
      final firstSheetId = createdSheet.sheets![0].properties!.sheetId;
      
      await _sheetsApi!.spreadsheets.batchUpdate(
        BatchUpdateSpreadsheetRequest(
          requests: [
            Request(
              updateSheetProperties: UpdateSheetPropertiesRequest(
                properties: SheetProperties(
                  sheetId: firstSheetId,
                  title: '1일전',
                ),
                fields: 'title',
              ),
            ),
          ],
        ),
        _spreadsheetId!,
      );
    }
    
    // 나머지 29개 시트 생성 (2일전 ~ 30일전)
    await _createRemainingSheets();
    
    // 모든 시트에 헤더 추가
    await _addHeadersToAllSheets();
  }
  
  // 모든 필요한 시트가 있는지 확인하고 없으면 추가
  static Future<void> _ensureRequiredSheets() async {
    final spreadsheet = await _sheetsApi!.spreadsheets.get(_spreadsheetId!);
    final existingSheets = spreadsheet.sheets!.map((s) => s.properties!.title).toList();
    
    // 필요한 모든 시트 이름 생성 (1일전 ~ 30일전)
    final requiredSheets = List.generate(30, (i) => '${i+1}일전');
    
    // 누락된 시트 찾기
    final missingSheets = requiredSheets.where((name) => !existingSheets.contains(name)).toList();
    
    // 누락된 시트 추가
    if (missingSheets.isNotEmpty) {
      final requests = missingSheets.map((sheetName) => 
        Request(
          addSheet: AddSheetRequest(
            properties: SheetProperties(
              title: sheetName,
            ),
          ),
        )
      ).toList();
      
      await _sheetsApi!.spreadsheets.batchUpdate(
        BatchUpdateSpreadsheetRequest(requests: requests),
        _spreadsheetId!,
      );
      
      // 새로 추가된 시트에 헤더 추가
      for (final sheetName in missingSheets) {
        await _sheetsApi!.spreadsheets.values.update(
          ValueRange(values: [_headers]),
          _spreadsheetId!,
          '$sheetName!A1:C1',
          valueInputOption: 'USER_ENTERED',
        );
      }
    }
    
    // 기존 시트에 헤더가 있는지 확인하고 없으면 추가
    for (final sheetName in requiredSheets) {
      if (existingSheets.contains(sheetName)) {
        final headerResponse = await _sheetsApi!.spreadsheets.values.get(
          _spreadsheetId!,
          '$sheetName!A1:C1',
        );
        
        if (headerResponse.values == null || headerResponse.values!.isEmpty) {
          await _sheetsApi!.spreadsheets.values.update(
            ValueRange(values: [_headers]),
            _spreadsheetId!,
            '$sheetName!A1:C1',
            valueInputOption: 'USER_ENTERED',
          );
        }
      }
    }
  }
  
  // 나머지 29개 시트 생성 (2일전 ~ 30일전)
  static Future<void> _createRemainingSheets() async {
    final requests = List.generate(29, (i) => 
      Request(
        addSheet: AddSheetRequest(
          properties: SheetProperties(
            title: '${i+2}일전',
          ),
        ),
      )
    );
    
    if (requests.isNotEmpty) {
      await _sheetsApi!.spreadsheets.batchUpdate(
        BatchUpdateSpreadsheetRequest(requests: requests),
        _spreadsheetId!,
      );
    }
  }
  
  // 모든 시트에 헤더 추가
  static Future<void> _addHeadersToAllSheets() async {
    final sheetNames = List.generate(30, (i) => '${i+1}일전');
    
    for (final sheetName in sheetNames) {
      await _sheetsApi!.spreadsheets.values.update(
        ValueRange(values: [_headers]),
        _spreadsheetId!,
        '$sheetName!A1:C1',
        valueInputOption: 'USER_ENTERED',
      );
    }
  }
  
  // 모든 카드 가져오기 (1일전 시트에서만)
  static Future<List<Flashcard>> getFlashcards() async {
    if (_spreadsheetId == null) {
      final isInitialized = await initSpreadsheet();
      if (!isInitialized) return [];
    }
    
    try {
      final response = await _sheetsApi!.spreadsheets.values.get(
        _spreadsheetId!,
        '$_activeSheetName!A2:C',
      );
      
      final values = response.values;
      if (values == null || values.isEmpty) return [];
      
      return values.map((row) {
        return Flashcard(
          id: row[0].toString(),
          english: row[1].toString(),
          korean: row[2].toString(),
          isLearned: false, // isLearned 필드는 사용하지 않음
        );
      }).toList();
    } catch (e) {
      print('Error getting flashcards: $e');
      return [];
    }
  }
  
  // 모든 카드 저장하기 (1일전 시트에만)
  static Future<bool> saveAllFlashcards(List<Flashcard> flashcards) async {
    if (_spreadsheetId == null) {
      final isInitialized = await initSpreadsheet();
      if (!isInitialized) return false;
    }
    
    try {
      // 데이터를 2D 배열로 변환 (id, english, korean만 포함)
      final values = flashcards.map((card) => [
        card.id,
        card.english,
        card.korean,
      ]).toList();
      
      // 기존 데이터 지우기
      await _sheetsApi!.spreadsheets.values.clear(
        ClearValuesRequest(),
        _spreadsheetId!,
        '$_activeSheetName!A2:C',
      );
      
      // 새 데이터 추가
      if (values.isNotEmpty) {
        await _sheetsApi!.spreadsheets.values.update(
          ValueRange(values: values),
          _spreadsheetId!,
          '$_activeSheetName!A2:C${values.length + 1}',
          valueInputOption: 'USER_ENTERED',
        );
      }
      
      return true;
    } catch (e) {
      print('Error saving flashcards: $e');
      return false;
    }
  }
  
  // 카드 추가하기 (항상 1일전 시트에 추가)
  static Future<bool> addFlashcard(Flashcard card) async {
    if (_spreadsheetId == null) {
      final isInitialized = await initSpreadsheet();
      if (!isInitialized) return false;
    }
    
    try {
      // 가장 마지막 행 찾기
      final response = await _sheetsApi!.spreadsheets.values.get(
        _spreadsheetId!,
        '$_activeSheetName!A:A',
      );
      
      final rowCount = response.values?.length ?? 1;
      final nextRow = rowCount + 1;
      
      // 새 카드 추가
      await _sheetsApi!.spreadsheets.values.update(
        ValueRange(values: [[
          card.id,
          card.english,
          card.korean,
        ]]),
        _spreadsheetId!,
        '$_activeSheetName!A$nextRow:C$nextRow',
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
    _driveApi = null;
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