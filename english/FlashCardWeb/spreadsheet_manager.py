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

    def update_row(self, sheet_name, row_id, english, korean, description):
        try:
            range_name = f"{sheet_name}!A{row_id+1}:C{row_id+1}"
            values = [[english, korean, description]]
            body = {
                'values': values
            }
            self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                body=body
            ).execute()
        except Exception as e:
            raise Exception(f"데이터 수정 중 오류 발생: {str(e)}")

    def delete_row(self, sheet_name, row_id):
        try:
            # 해당 행을 빈 값으로 업데이트하여 "삭제" 처리
            range_name = f"{sheet_name}!A{row_id+1}:C{row_id+1}"
            body = {
                'values': [['']*3]  # 3개의 열을 빈 값으로 설정
            }
            self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                body=body
            ).execute()
        except Exception as e:
            raise Exception(f"데이터 삭제 중 오류 발생: {str(e)}")

    def move_data_to_next_day(self):
        try:
            # 30일차 데이터 삭제
            day_30_data = self.get_sheet_data('30일')
            if day_30_data:
                self.clear_sheet_data('30일')

            # 역순으로 데이터 이동 (29일 -> 30일, 28일 -> 29일, ...)
            days = ['30일', '15일', '7일', '5일', '3일', '2일', '1일']
            hidden_days = ['29일', '28일', '27일', '26일', '25일', '24일', '23일', '22일', '21일', '20일', 
                           '19일', '18일', '17일', '16일', '14일', '13일', '12일', '11일', '10일', '9일', 
                           '8일', '6일', '4일']  # 숨겨진 시트들
            
            # 숨겨진 시트 생성 (없는 경우)
            existing_sheets = self.get_all_sheets()
            for hidden_day in hidden_days:
                if hidden_day not in existing_sheets:
                    self.create_sheet(hidden_day)
                    self.format_headers(hidden_day)
                    self.hide_sheet(hidden_day)

            # 데이터 이동
            for i in range(len(days) - 1):
                current_day = days[i]
                prev_day = days[i + 1]
                
                # 7일차 -> 8일차(숨김), 15일차 -> 16일차(숨김) 등의 특수 케이스 처리
                if current_day in ['7일', '15일']:
                    hidden_next_day = f"{int(current_day.replace('일', '')) + 1}일"
                    if hidden_next_day not in existing_sheets:
                        self.create_sheet(hidden_next_day)
                        self.format_headers(hidden_next_day)
                        self.hide_sheet(hidden_next_day)
                    self.copy_data_between_sheets(current_day, hidden_next_day)
                
                # 일반적인 데이터 이동
                prev_data = self.get_sheet_data(prev_day)
                if prev_data:
                    self.clear_sheet_data(current_day)
                    self.write_data_to_sheet(current_day, prev_data)
                    self.clear_sheet_data(prev_day)

        except Exception as e:
            raise Exception(f"데이터 이동 중 오류 발생: {str(e)}")

    def clear_sheet_data(self, sheet_name):
        try:
            range_name = f"{sheet_name}!A2:C"  # 헤더 제외
            body = {
                'values': []
            }
            self.service.spreadsheets().values().clear(
                spreadsheetId=self.spreadsheet_id,
                range=range_name
            ).execute()
        except Exception as e:
            raise Exception(f"데이터 삭제 중 오류 발생: {str(e)}")

    def write_data_to_sheet(self, sheet_name, data):
        try:
            range_name = f"{sheet_name}!A2:C"  # 헤더 제외
            body = {
                'values': data
            }
            self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                body=body
            ).execute()
        except Exception as e:
            raise Exception(f"데이터 쓰기 중 오류 발생: {str(e)}")

    def hide_sheet(self, sheet_name):
        try:
            sheet_id = self.get_sheet_id(sheet_name)
            if sheet_id:
                body = {
                    'requests': [{
                        'updateSheetProperties': {
                            'properties': {
                                'sheetId': sheet_id,
                                'hidden': True
                            },
                            'fields': 'hidden'
                        }
                    }]
                }
                self.service.spreadsheets().batchUpdate(
                    spreadsheetId=self.spreadsheet_id,
                    body=body
                ).execute()
        except Exception as e:
            raise Exception(f"시트 숨기기 중 오류 발생: {str(e)}")

    def copy_data_between_sheets(self, source_sheet, target_sheet):
        try:
            data = self.get_sheet_data(source_sheet)
            if data:
                self.clear_sheet_data(target_sheet)
                self.write_data_to_sheet(target_sheet, data)
        except Exception as e:
            raise Exception(f"데이터 복사 중 오류 발생: {str(e)}") 