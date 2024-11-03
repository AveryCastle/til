import os
import sys
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class Bcolors:
    Black = '\033[30m'
    Red = '\033[31m'
    Green = '\033[32m'
    Yellow = '\033[33m'
    Blue = '\033[34m'
    Magenta = '\033[35m'
    Cyan = '\033[36m'
    White = '\033[37m'
    Endc = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Install the Slack app and get xoxb- token in advance
SLACK_BOT_TOKEN=os.environ["CHEERY_MATE_SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["CHEERY_MATE_SLACK_APP_TOKEN"]
print(f"SLACK_BOT_TOKEN={SLACK_BOT_TOKEN}")
print(f"SLACK_APP_TOKEN={SLACK_APP_TOKEN}")


def conversations_open(bot_token, user_id):
    # https://api.slack.com/methods/conversations.open
    client = WebClient(token=bot_token)
    try:
        result = client.conversations_open(users=user_id)
        if result['ok']:
            return result['channel']['id']
        else:
            return None
    except SlackApiError as e:
        print(f'{Bcolors.Yellow}- Api Error:: {e} {Bcolors.Endc}')
        return None
        

def chat_post_message(bot_token, channel_id, message):
    # https://api.slack.com/methods/chat.postMessage
    client = WebClient(token=bot_token)
    try:
        result = client.chat_postMessage(channel=channel_id, text=message, as_user=True)
        print(result)
    except SlackApiError as e:
        print(f'{Bcolors.Yellow}- Api Error:: {e} {Bcolors.Endc}')


def main():
    bot_token = SLACK_BOT_TOKEN
    user_id = 'U041PVBG8JD'
  
    chat_id = conversations_open(bot_token, user_id)
    if chat_id:
        message = f'<@{user_id}> hello my freiend.'
        chat_post_message(bot_token, chat_id, message)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f'{Bcolors.Yellow}- ::Exception:: Func:[{__name__.__name__}] '
              f'Line:[{sys.exc_info()[-1].tb_lineno}] [{type(e).__name__}] {e}{Bcolors.Endc}')