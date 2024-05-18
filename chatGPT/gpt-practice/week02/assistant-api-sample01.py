import os
import openai
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
# PROJECT_ID = 'proj_CDixB8aUF6mvyvzLMzMfsvPx'

client = OpenAI(api_key=api_key)

# assistant 생성
assistant = client.beta.assistants.create(
  name="Math Tutor",
  instructions="당신은 수학 과외 선생님입니다. 수학 질문에 대한 답변을 코드를 쓰고 실행해주세요.",
  tools=[{"type": "code_interpreter"}],
  model="gpt-3.5-turbo",
)

# thread 생성
thread = client.beta.threads.create()

# 질문 설정
question = "`3x + 11 = 14` 문제를 풀어야 합니다. 도와줄 수 있나요?"

# message 를 쓰레드에 추가하기
message = client.beta.threads.messages.create(
  thread_id=thread.id,
  role="user",
  content=question
)

# run 생성 및 실행 
run = client.beta.threads.runs.create_and_poll(
  thread_id=thread.id,
  assistant_id=assistant.id,
  instructions="사용자를 에이버리라고 불러주세요. 사용자에게 프리미엄 계정이 있습니다."
)

# 응답 출력
if run.status == 'completed': 
  messages = client.beta.threads.messages.list(
    thread_id=thread.id
  )
  print(messages)
else:
  print(run.status)
