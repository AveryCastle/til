from conversation_assistant import FrenAssistant
from smart_greeting_assistant import SmartGreetingAssistant

class EmailConversation:
    def __init__(self, user_manager, conversation_manager):
        self.user_manager = user_manager
        self.conversation_manager = conversation_manager

    def start(self):
        user_id, thread_id = self.__get_user_and_thread_id__()
        if user_id is None:
            print("User not found.")
            return
        
        assistant = FrenAssistant(thread_id)
        
        if thread_id is None:
            thread_id = assistant.get_thread_id()      
            self.user_manager.update_thread_id(user_id, thread_id)

        conversation_history, history_thread_id = self.conversation_manager.get_conversations(user_id)
        
        smartGreetingAssistant = SmartGreetingAssistant(thread_id=history_thread_id)
        greeting = smartGreetingAssistant.generate_smart_greeting(conversation_history)
        print(greeting)

        new_conversation = [{'role':'assistant', 'message':greeting}]
        
        while True:
            user_question = input("하고 싶은 말 해(종료하려면 'exit' 입력): ")
            new_conversation.append({'role':'user', 'message':user_question})
            
            if user_question.lower() == 'exit':
                new_conversation.pop()
                self.conversation_manager.upsert_conversation(user_id, new_conversation, smartGreetingAssistant.get_thread_id())
                break

            response = assistant.ask_question(user_question)
            new_conversation.append({'role':'assistant', 'message':response})
            print(response)

    def __get_user_and_thread_id__(self):
        user_id = None
        thread_id = None
        attempts = 0
        while user_id is None and attempts < 3:
            user_id, thread_id = self.user_manager.user_input("1")
            attempts += 1
        return user_id, thread_id