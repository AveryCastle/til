import asyncio
import telegram
import os

# step1.
# async def main():
#   TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
#   bot = telegram.Bot(TELEGRAM_TOKEN)
#   async with bot:
#     print(await bot.get_me())
# Result=>
# User(can_connect_to_business=False, can_join_groups=True, can_read_all_group_messages=False, first_name='Befriend', id=6903031291, is_bot=True, supports_inline_queries=False, username='Hi_Firend_Bot')

# step2
# async def main():
#   TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
#   bot = telegram.Bot(TELEGRAM_TOKEN)
#   async with bot:
#       updates = (await bot.get_updates())[0]
#       print(updates)
# Result      
# Update(message=Message(channel_chat_created=False, chat=Chat(first_name='estel', id=46749936, last_name='seong', type=<ChatType.PRIVATE>, username='estelcastle'), date=datetime.datetime(2024, 6, 19, 13, 21, 22, tzinfo=datetime.timezone.utc), delete_chat_photo=False, from_user=User(first_name='estel', id=46749936, is_bot=False, language_code='en', last_name='seong', username='estelcastle'), group_chat_created=False, message_id=4, supergroup_chat_created=False, text='안녕....?'), update_id=107910470)
# chat_id: 46749936
  
# step3      
async def main():
  TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
  bot = telegram.Bot(TELEGRAM_TOKEN)
  async with bot:
      await bot.send_message(text='안녕, estel!', chat_id=46749936)
                
if __name__ == '__main__':
    asyncio.run(main())
