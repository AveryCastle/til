import os

# 데이터베이스 연결 설정
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_DATABASE'),
    'user': os.getenv('DB_USER'), # 'within_dev' # 'yeogi' #os.environ['DB_USER']
    'password': os.getenv('DB_PASSWORD'), #'With!n@()' # 'DQlapaTm&79()' #os.environ['DB_PASSWORD']
    'port': 3306
}
