from openai import OpenAI
client = OpenAI()

# 질문 설정
question = """
    대한민국 역대 대통령을 과거부터 현재 순서로 이름과 임기 기간을 '{키:값}' 쌍으로 출력해주세요.
    이때, 예시와 같은 포맷으로 출력해주세요.
    예시) 문재인: 2017년 5월 10일 ~ 2022년 5월 9일
  """

response = client.chat.completions.create(
  model="gpt-4-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": question},
  ]
)

# API 응답에서 답변 추출
answer = response.choices[0].message.content

# 결과 출력
print(answer)
