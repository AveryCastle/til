from FriendAssistants import FrenAssistant

# 메인 함수
def main():
    # FrenAssistant 객체 생성
    assistant = FrenAssistant(thread_id='thread_5ZZXs8U7zFJW2qT1i1ymMgVS')

    while True:
        # 사용자로부터 질문 입력 받기
        user_question = input("질문을 입력하세요 (종료하려면 'exit' 입력): ")

        # 사용자가 'exit'를 입력하면 종료
        if user_question.lower() == 'exit':
            break

        # 질문 제출
        response = assistant.ask_question(user_question)

        # 응답 출력
        print(response)

if __name__ == '__main__':
    main()