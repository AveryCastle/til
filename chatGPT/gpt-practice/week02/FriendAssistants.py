import os
import openai
from openai import OpenAI
import json

class FrenAssistant:
    def __init__(self, thread_id=None):
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)
        self.tools = self.__get_tools__()
                
        # 생성한 assistant 가져오기
        self.assistant_id = 'asst_YaAriwexxjH8XhKZE3nXwoBk'
        self.assistant = self.client.beta.assistants.update(
            assistant_id=self.assistant_id,
            # tools=self.tools,
            model="gpt-4-turbo",
            response_format={ "type" : "json_object" }
        )
        
        # thread 생성하기
        if thread_id:
            self.thread = self.client.beta.threads.retrieve(thread_id=thread_id)
        else:
            self.thread = self.client.beta.threads.create()

    def get_thread_id(self):
        return self.thread.id
        
    def ask_question(self, question):
        # message 를 쓰레드에 추가하기
        message = self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=question
        )

        # run 생성 및 실행 
        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
            tools=self.tools,
            instructions="tools 에 기재한 내용과 같이 json format 으로 응답해줘.",
        )
        return self.__get_json_response__(run)
      
    def __get_response__(self, run):
        if run.status == 'completed': 
            messages = self.client.beta.threads.messages.list(
                thread_id=self.thread.id
            )
            return messages.data[0].content[0].text.value
        else:
            return run.status
        
    def __get_json_response__(self, run):
        # Define the list to store tool outputs
        tool_outputs = []
        
        if run.status == 'requires_action':
            # Loop through each tool in the required action section
            for tool in run.required_action.submit_tool_outputs.tool_calls:
                if tool.function.name == "get_json_response":
                    tool_outputs.append({
                        "tool_call_id": tool.id,
                        "output": "57"
                    })
            # Submit all tool outputs at once after collecting them in a list
        if tool_outputs:
            try:
                run = self.client.beta.threads.runs.submit_tool_outputs_and_poll(
                    thread_id=self.thread.id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )
                print("Tool outputs submitted successfully.")
            except Exception as e:
                print("Failed to submit tool outputs:", e)
            else:
                print("No tool outputs to submit.")

            if run.status == 'completed':
                messages = self.client.beta.threads.messages.list(
                    thread_id=self.thread.id
                )
                print(messages)
            else:
                print(run.status)

        elif run.status == 'completed': 
            messages = self.client.beta.threads.messages.list(
                thread_id=self.thread.id
            )
            return messages
        else:
            return run.status
    
    def __get_tools__(self):
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_json_response",
                    "description": "JSON 포맷으로 답변을 받는 함수",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "OriginalRequest": {
                                "type": "string",
                                "description": "User 의 질문",
                            },
                            "Answer": {
                                "type": "string", 
                                "description": "Assistant 의 답변" 
                            },
                        },
                        "required": ["OriginalRequest", "Answer"],
                    },
                },
            }
        ]
        return tools
    