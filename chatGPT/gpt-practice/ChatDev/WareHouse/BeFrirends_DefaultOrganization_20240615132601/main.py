import schedule
import time
from sns import send_greeting
def schedule_greetings():
    schedule.every().day.at("09:00").do(send_greeting, "Good morning!")
    schedule.every().day.at("13:00").do(send_greeting, "Good afternoon!")
    schedule.every().day.at("18:00").do(send_greeting, "Good evening!")
    while True:
        schedule.run_pending()
        time.sleep(1)
if __name__ == "__main__":
    schedule_greetings()