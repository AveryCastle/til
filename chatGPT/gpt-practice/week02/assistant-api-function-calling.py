import os
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
 
# function 정의 및 assistant 생성
assistant = client.beta.assistants.create(
  instructions="날씨 봇입니다. 제공된 함수를 사용하여 질문에 답하세요.",
  model="gpt-4o",
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
    @override
    def on_event(self, event):
      # Retrieve events that are denoted with 'requires_action'
      # since these will have our tool_calls
      if event.event == 'thread.run.requires_action':
        run_id = event.data.id  # Retrieve the run ID from the event data
        self.handle_requires_action(event.data, run_id)
 
    def handle_requires_action(self, data, run_id):
      tool_outputs = []
        
      for tool in data.required_action.submit_tool_outputs.tool_calls:
        if tool.function.name == "get_current_temperature":
          tool_outputs.append({"tool_call_id": tool.id, "output": "27"})
        elif tool.function.name == "get_rain_probability":
          tool_outputs.append({"tool_call_id": tool.id, "output": "0.03"})
        
      # Submit all tool_outputs at the same time
      self.submit_tool_outputs(tool_outputs, run_id)
 
    def submit_tool_outputs(self, tool_outputs, run_id):
      # Use the submit_tool_outputs_stream helper
      with client.beta.threads.runs.submit_tool_outputs_stream(
        thread_id=self.current_run.thread_id,
        run_id=self.current_run.id,
        tool_outputs=tool_outputs,
        event_handler=EventHandler(),
      ) as stream:
        for text in stream.text_deltas:
          print(text, end="", flush=True)
        print()
 
 
with client.beta.threads.runs.stream(
  thread_id=thread.id,
  assistant_id=assistant.id,
  event_handler=EventHandler()
) as stream:
  stream.until_done()
