import os
import openai
from openai import OpenAI

class FrenAssistant:
    def __init__(self, thread_id=None):
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)
        
        # 생성한 assistant 가져오기
        self.assistant_id = 'asst_YaAriwexxjH8XhKZE3nXwoBk'
        self.assistant = self.client.beta.assistants.retrieve(assistant_id=self.assistant_id)
        
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
        )
        return self.__get_response__(run)
      
    def __get_response__(self, run):
        if run.status == 'completed': 
            messages = self.client.beta.threads.messages.list(
                thread_id=self.thread.id
            )
            return messages.data[0].content[0].text.value
        else:
            return run.status
    