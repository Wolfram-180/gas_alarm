# pip install aiogram
from safe_bot_token import bot_token
import logging
import sqlite3

from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = bot_token

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_start(message: types.Message):
    await message.answer("Hi there, that bot will notify you by air pollution in Vidnoe. Use /join command to subscribe for notifications or /exit to unsubscribe from them\n")
    await message.answer("Привет, этот бот будет сообщать о загрязнении воздуха в Видном. Введите команду /join чтобы получать уведомления или /exit чтобы отписаться\n")


@dp.message_handler(commands=['join'])
async def send_join(message: types.Message):
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

    await message.answer("You subscribed for notifications to be informed on air pollution in Vidnoe\n")
    await message.answer("Вы подписаны на уведомления о загрязнении воздуха в Видном\n")
    await message.answer('Send /exit command to unsubscribe\n')
    await message.answer('Введите команду /exit если захотите отписаться\n')


@dp.message_handler(commands=['exit'])
async def send_exit(message: types.Message):
    conn = sqlite3.connect("user_info.db")

    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS user(
        id INTEGER
        )""")
    conn.commit()
    userid = message.chat.id
    cursor.execute(f"DELETE FROM user WHERE id = {userid}")
    conn.commit()

    await message.answer("You unsubscribed for notifications on air pollution in Vidnoe\n")
    await message.answer("Вы отписаны от уведомлений о загрязнении воздуха в Видном\n")
    await message.answer('Send /join command to subscribe\n')
    await message.answer('Введите команду /join чтобы подписаться\n')    


@dp.message_handler(commands=['showdb'])
async def send_showdb(message: types.Message):
    conn = sqlite3.connect("user_info.db")

    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS user(
        id INTEGER
        )""")
    conn.commit()

    cursor.execute(f"SELECT id FROM user")
    data = cursor.fetchall()

    for i in data:
        await message.answer(i)


@dp.message_handler()
async def echo(message: types.Message):
    send_start(message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
