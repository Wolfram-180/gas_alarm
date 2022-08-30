# pip install aiogram
# pip install sqlite3
import token
import logging
import sqlite3

from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = token.bot_token

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi there, I will notify you by high air pollution level in Vidnoe. Use /join command to subscribe for notifications or /exit to unsubscribe from them\n")
    await message.reply("Привет, я буду сообщать о загрязнении воздуха в Видном. Введите команду /join чтобы получать уведомления или /exit чтобы отписаться\n")
    

@dp.message_handler()
async def echo(message: types.Message):
    await message.reply('Введите команду /join чтобы получать уведомления о загрязнении воздуха в Видном или /exit чтобы отписаться\n')
    await message.reply('Use /join command to subscribe for Vidnoe air pollution notifications or /exit to unsubscribe from them')
    

@dp.message_handler(commands=['join'])
async def send_welcome(message: types.Message):
    await message.reply("Добавляем в БД уведомлений о загрязнении воздуха в Видном\n")

    conn = sqlite3.connect("user_info.db")
	
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS user(
        id INTEGER
        )""")
    conn.commit()
    userid = message.chat.id
    cursor.execute(f"SELECT id FROM user WHERE id = {userid}")
    data = cursor.fetchone()
    if data is None:
        cursor.execute(f"INSERT INTO user (id) VALUES ({userid})")
        conn.commit()

    await message.reply("Вы добавлены в БД уведомлений о загрязнении воздуха в Видном\n")
    await message.reply('Введите команду /exit чтобы отписаться\n')      
    

@dp.message_handler(commands=['exit'])
async def send_leave(message: types.Message):
    await message.reply("Убираем из БД уведомлений о загрязнении воздуха в Видном\n")

    conn = sqlite3.connect("user_info.db")
	
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS user(
        id INTEGER
        )""")
    conn.commit()
    userid = message.chat.id
    cursor.execute(f"DELETE FROM user WHERE id = {userid}")
    conn.commit()

    await message.reply("Вы удалены из БД уведомлений о загрязнении воздуха в Видном\n")
    await message.reply('Введите команду /join чтобы подписаться\n')  



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)    