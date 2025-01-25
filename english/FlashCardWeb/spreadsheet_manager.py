from googleapiclient.errors import HttpError

class SpreadsheetManager:
    def __init__(self, sheets_service, spreadsheet_id):
        self.service = sheets_service
        self.spreadsheet_id = spreadsheet_id
        self.sheet_names = ['1일', '2일', '3일', '5일', '7일', '15일', '30일']
        self.headers = [['영어', '한글', '상세설명']]

    def get_all_sheets(self):
        try:
            spreadsheet = self.service.spreadsheets().get(
                spreadsheetId=self.spreadsheet_id
            ).execute()
            return [sheet['properties']['title'] for sheet in spreadsheet['sheets']]
        except HttpError as error:
            raise Exception(f'시트 정보 조회 중 오류 발생: {error}')

    def create_sheet(self, sheet_name):
        try:
            body = {
                'requests': [{
                    'addSheet': {
                        'properties': {
                            'title': sheet_name
                        }
                    }
                }]
            }
            self.service.spreadsheets().batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body=body
            ).execute()
        except HttpError as error:
            raise Exception(f'시트 생성 중 오류 발생: {error}')

    def format_headers(self, sheet_name):
        try:
            # 헤더 데이터 입력
            range_name = f'{sheet_name}!A1:C1'
            self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                body={'values': self.headers}
            ).execute()

            # 볼드체 적용
            body = {
                'requests': [{
                    'repeatCell': {
                        'range': {
                            'sheetId': self.get_sheet_id(sheet_name),
                            'startRowIndex': 0,
                            'endRowIndex': 1,
                            'startColumnIndex': 0,
                            'endColumnIndex': 3
                        },
                        'cell': {
                            'userEnteredFormat': {
                                'textFormat': {
                                    'bold': True
                                }
                            }
                        },
                        'fields': 'userEnteredFormat.textFormat.bold'
                    }
                }]
            }
            self.service.spreadsheets().batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body=body
            ).execute()
        except HttpError as error:
            raise Exception(f'헤더 포맷팅 중 오류 발생: {error}')

    def get_sheet_id(self, sheet_name):
        try:
            spreadsheet = self.service.spreadsheets().get(
                spreadsheetId=self.spreadsheet_id
            ).execute()
            for sheet in spreadsheet['sheets']:
                if sheet['properties']['title'] == sheet_name:
                    return sheet['properties']['sheetId']
            return None
        except HttpError as error:
            raise Exception(f'시트 ID 조회 중 오류 발생: {error}')

    def initialize_sheets(self):
        existing_sheets = self.get_all_sheets()
        
        for sheet_name in self.sheet_names:
            if sheet_name not in existing_sheets:
                self.create_sheet(sheet_name)
                self.format_headers(sheet_name) 

    def get_sheet_data(self, sheet_name):
        try:
            range_name = f'{sheet_name}!A2:C'  # A2부터 시작하여 헤더 제외
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=range_name
            ).execute()
            return result.get('values', [])
        except HttpError as error:
            raise Exception(f'데이터 조회 중 오류 발생: {error}')

    def append_to_sheet(self, sheet_name, english, korean, description):
        try:
            range_name = f"{sheet_name}!A:C"
            values = [[english, korean, description]]
            body = {
                'values': values
            }
            self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                insertDataOption='INSERT_ROWS',
                body=body
            ).execute()
        except Exception as e:
            raise Exception(f"데이터 추가 중 오류 발생: {str(e)}") 