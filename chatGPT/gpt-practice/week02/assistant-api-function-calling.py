import os
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
 
# function 정의 및 assistant 생성
assistant = client.beta.assistants.create(
  instructions="날씨 봇입니다. 제공된 함수를 사용하여 질문에 답하세요.",
  model="gpt-3.5-turbo",
  tools=[
    {
      "type": "function",
      "function": {
        "name": "get_current_temperature",
        "description": "특정 위치의 현재 온도를 가져옵니다.",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "도시와 구와 동, 예: 서울시/송파구/문정동"
            },
            "unit": {
              "type": "string",
              "enum": ["Celsius", "Fahrenheit"],
              "description": "사용할 온도 단위입니다. 사용자의 위치에서 추론합니다."
            }
          },
          "required": ["location", "unit"]
        }
      }
    },
    {
      "type": "function",
      "function": {
        "name": "get_rain_probability",
        "description": "특정 위치의 비 올 확률을 가져옵니다.",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "도시와 구와 동, 예: 서울시/송파구/문정동"
            }
          },
          "required": ["location"]
        }
      }
    }
  ]
)

thread = client.beta.threads.create()
message = client.beta.threads.messages.create(
  thread_id=thread.id,
  role="user",
  content="오늘 강남구 역삼동의 날씨와 비가 올 확률은 어떻게 되나요?",
)

from typing_extensions import override
from openai import AssistantEventHandler
 
class EventHandler(AssistantEventHandler):
    def __init__(self, client):
        self.client = client
        self.current_run = None  # 현재 실행 중인 run 정보 저장

    @override
    def on_event(self, event):
        if event.event == 'thread.run.started':
            self.current_run = event.data  # run 시작 시 정보 저장
        elif event.event == 'thread.run.requires_action':
            run_id = event.data.id
            self.handle_requires_action(event.data, run_id)

    def handle_requires_action(self, data, run_id):
        tool_outputs = []

        for tool in data.required_action.submit_tool_outputs.tool_calls:
            function_name = tool.function.name
            function_args = tool.function.arguments

            # 실제 함수 호출 (예시: OpenAI API를 사용하여 날씨 정보 가져오기)
            if function_name == "get_current_temperature":
                temperature_response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "당신은 날씨 봇입니다."},
                        {"role": "user", "content": f"현재 {function_args['location']}의 온도는 {function_args['unit']} 단위로 알려줘."}
                    ]
                )
                output = temperature_response.choices[0].message.content
            elif function_name == "get_rain_probability":
                rain_response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "당신은 날씨 봇입니다."},
                        {"role": "user", "content": f"현재 {function_args['location']}의 비 올 확률은?"}
                    ]
                )
                output = rain_response.choices[0].message.content

            tool_outputs.append({"tool_call_id": tool.id, "output": output})

        self.submit_tool_outputs(tool_outputs, run_id)

    def submit_tool_outputs(self, tool_outputs, run_id):
        with self.client.beta.threads.runs.submit_tool_outputs_stream(
            thread_id=self.current_run.thread_id,  # 저장된 run 정보 사용
            run_id=self.current_run.id,             # 저장된 run 정보 사용
            tool_outputs=tool_outputs,
            event_handler=EventHandler(self.client),
        ) as stream:
            for text in stream.text_deltas:
                print(text, end="", flush=True)
            print()


with client.beta.threads.runs.stream(
    thread_id=thread.id,
    assistant_id=assistant.id,
    event_handler=EventHandler(client)  # 이벤트 핸들러에 client 전달
) as stream:
    stream.until_done()
