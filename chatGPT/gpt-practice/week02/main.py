from database_manager import DatabaseManager
from user_manager import UserManager
from FriendAssistants import FrenAssistant

def main():
    db_manager = DatabaseManager()
    user_manager = UserManager(db_manager)
    user_id, thread_id = user_manager.user_input()
    
    # FrenAssistant 객체 생성
    assistant = FrenAssistant(thread_id)
    
    # thread_id가 None인 경우, assistant를 통해 thread_id 획득 및 업데이트
    if thread_id is None:
        thread_id = assistant.get_thread_id()        
        user_manager.update_thread_id(user_id, thread_id)

    while True:
        # 사용자로부터 질문 입력 받기
        user_question = input("하고 싶은 말 해(종료하려면 'exit' 입력): ")

        # 사용자가 'exit'를 입력하면 종료
        if user_question.lower() == 'exit':
            break

        # 질문 제출
        response = assistant.ask_question(user_question)

        # 응답 출력
        print(response)

if __name__ == '__main__':
    main()