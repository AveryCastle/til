from db.database_manager import DatabaseManager
from user_manager import UserManager
from conversation_manager import ConversationManager
from email_conversation import EmailConversation
from telegram_converstation import TelegramConversation

def main():
    choice = input("Choose conversation method (1: Email, 2: Telegram): ")

    db_manager = DatabaseManager()
    user_manager = UserManager(db_manager)
    conversation_manager = ConversationManager(db_manager)
        
    if choice == "1":
        email_conversation = EmailConversation(user_manager, conversation_manager)
        email_conversation.start()
    elif choice == "2":
        telegram_conversation = TelegramConversation()
        telegram_conversation.start()
    else:
        print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()