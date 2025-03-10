class SpreadsheetService {
  final GoogleSignInAccount account;
  final SheetsApi sheetsApi;

  Future<void> initializeSpreadsheets() async {
    final folderId = await _createOrGetAppFolder();
    
    for (int i = 1; i <= 30; i++) {
      await _createDaySpreadsheet(i, folderId);
    }
  }

  Future<void> migrateData() async {
    // 30일차부터 역순으로 데이터 이동
    for (int i = 30; i > 1; i--) {
      final sourceData = await _readSpreadsheetData(i - 1);
      await _writeSpreadsheetData(i, sourceData);
    }
  }
} 