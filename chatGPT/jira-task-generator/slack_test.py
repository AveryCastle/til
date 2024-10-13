from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os
import openai
import requests

# Slack 및 Jira API 클라이언트 설정
slack_client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])
jira_base_url = "https://your-domain.atlassian.net"
jira_email = os.environ['JIRA_EMAIL']
jira_api_token = os.environ['JIRA_API_TOKEN']
jira_project_key = "PROJ"

# LLM (OpenAI GPT) 설정
openai.api_key = os.environ['OPENAI_API_KEY']

def handle_slack_command(event):
    # Slack에서 전달된 메시지
    message_text = event['text']

    # LLM으로 메시지 분석하여 Jira 이슈의 필드 생성
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Create a Jira task based on this message: {message_text}",
        max_tokens=100
    )
    task_data = response['choices'][0]['text'].strip()

    # 태스크 제목과 설명을 분리 (예시로 콜론을 기준으로 분리)
    title, description = task_data.split(":") if ":" in task_data else (task_data, task_data)

    # Jira API로 태스크 생성
    create_jira_issue(title, description)

    # Slack에 생성 결과 피드백
    slack_client.chat_postMessage(
        channel=event['channel'],
        text=f"Jira 이슈가 생성되었습니다: {title}"
    )

def create_jira_issue(title, description):
    url = f"{jira_base_url}/rest/api/3/issue"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {jira_email}:{jira_api_token}"
    }
    issue_data = {
        "fields": {
            "project": {
                "key": jira_project_key
            },
            "summary": title,
            "description": description,
            "issuetype": {
                "name": "Task"
            }
        }
    }

    response = requests.post(url, json=issue_data, headers=headers)
    if response.status_code == 201:
        print("Jira 이슈가 성공적으로 생성되었습니다.")
    else:
        print(f"Jira 이슈 생성 실패: {response.status_code}")

# 슬랙 이벤트 핸들러 (명령어 실행 시)
@slack_event_adapter.on("message")
def message(event_data):
    event = event_data['event']
    if event['text'].startswith("/jira create"):
        handle_slack_command(event)
