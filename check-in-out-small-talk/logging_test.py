import logging
from logging.handlers import TimedRotatingFileHandler
import os

# 로그 파일 경로 설정
log_directory = "blackhole/log"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)  # 디렉토리가 없으면 생성합니다.

log_file_path = os.path.join(log_directory, "app.log")

# 로깅 설정
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# 날짜별 로그 파일 핸들러 설정 (매일 자정에 로그 파일을 새로 생성)
handler = TimedRotatingFileHandler(
    log_file_path,
    when="midnight",
    interval=1,
    backupCount=7  # 최근 7일치 로그 파일을 보관
)
handler.suffix = "%Y-%m-%d"  # 로그 파일에 날짜 포맷 추가
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# 테스트 로그 출력
logger.debug("This is a debug message.")
logger.info("This is an info message.")
logger.warning("This is a warning message.")
logger.error("This is an error message.")
logger.critical("This is a critical message.")
