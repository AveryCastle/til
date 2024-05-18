import os
import openai
from openai import OpenAI

class FrenAssistant:
    def __init__(self, assistant_id):
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)
        self.assistant_id = 'asst_YaAriwexxjH8XhKZE3nXwoBk'
        # 생성한 assistant 가져오기
        self.thread = self.client.beta.assistants.retrieve(assistant_id=self.assistant_id)

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
            assistant_id=self.assistant_id
        )
        return run
      
    def get_response(thread_id):
      messages = self.client.beta.threads.messages.list(
        thread_id=thread_id
      )
      if messages.data:
        return messages.data[0].content[0].text.value
      else:
        return None