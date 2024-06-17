from database_manager import DatabaseManager
from user_manager import UserManager
from FriendAssistants import FrenAssistant
from conversation_manager import ConversationManager
from smart_greeting_assistant import SmartGreetingAssistant

def main():
    db_manager = DatabaseManager()
    user_manager = UserManager(db_manager)
    conversation_manager = ConversationManager(db_manager)

    user_id, thread_id = __get_user_and_thread_id__(user_manager)
    if (user_id is None):
        print("User not found.")
        return
    
    # FrenAssistant 객체 생성
    assistant = FrenAssistant(thread_id)
    
    # thread_id가 None인 경우, assistant를 통해 thread_id 획득 및 업데이트
    if thread_id is None:
        thread_id = assistant.get_thread_id()      
        user_manager.update_thread_id(user_id, thread_id)

    # 사용자와의 대화 히스토리 출력
    conversation_history, history_thread_id = conversation_manager.get_conversations(user_id)
    print("대화 히스토리: ", conversation_history, history_thread_id)
    
    smartGreetingAssistant = SmartGreetingAssistant(thread_id=history_thread_id)
    print("smartGreetingAssistant.thread_id", smartGreetingAssistant.get_thread_id())
    greeting = smartGreetingAssistant.generate_smart_greeting(conversation_history)
    print(greeting)

    new_conversation = [{'role':'assistant', 'message':greeting}]
    
    while True:
        # 사용자로부터 질문 입력 받기
        user_question = input("하고 싶은 말 해(종료하려면 'exit' 입력): ")
        new_conversation.append({'role':'user', 'message':user_question})
        
        # 사용자가 'exit'를 입력하면 종료
        if user_question.lower() == 'exit':
            print("smartGreetingAssistant.get_thread_id() => ", smartGreetingAssistant.get_thread_id())
            # conversation_manager.upsert_conversation(new_conversation, smartGreetingAssistant.get_thread_id())
            break

        # 질문 제출
        response = assistant.ask_question(user_question)
        new_conversation.append({'role':'assistant', 'message':response})
        
        # 응답 출력
        print(response)

def __get_user_and_thread_id__(user_manager):
        user_id = None
        thread_id = None
        attempts = 0
        while user_id is None and attempts < 3:
            user_id, thread_id = user_manager.user_input()
            attempts += 1
        return user_id, thread_id        

if __name__ == '__main__':
    main()