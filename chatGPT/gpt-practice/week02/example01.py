import os
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
PROJECT_ID = 'proj_CDixB8aUF6mvyvzLMzMfsvPx'

client = OpenAI(api_key=api_key, project=PROJECT_ID)

# 사용자로부터 여러 줄의 입력을 받습니다.
print("질문을 입력하세요. 입력을 마치려면 Enter 키를 두 번 누르세요.")

lines = []
while True:
    line = input()
    if line == "":
        break
    lines.append(line)    
question = "\n".join(lines)

print("잠시만 기다려주세요.")

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": question},
  ]
)

# API 응답에서 답변 추출
answer = response.choices[0].message.content

# 결과 출력
print(answer)
