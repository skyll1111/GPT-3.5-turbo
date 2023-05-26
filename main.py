

import json

import openai
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from model import resp, reset

file = open('config.json', 'r')
config = json.load(file)

openai.api_key = config['api_key']
bot = Bot(config['token'])
dp = Dispatcher(bot)


@dp.message_handler(commands="reset_dialog")
async def clear_history(message: types.Message):
    reset()
    await message.answer('Диалог успешно очищен')


@dp.message_handler(commands=['start', "help"])
async def inform(message: types.Message):
    await message.answer(
        "Привет! Я твой личный ChatGPT-бот. Задавай вопросы, получай полезную информацию "
        "и наслаждайся удивительным опытом общения. Чем я могу помочь сегодня?")


@dp.message_handler(content_types=types.ContentType.TEXT)
async def send(message: types.Message):
    if message.text[0] != '/':
        username = message.from_user.id
        await message.answer('ответ обрабатывается')
        response = resp(message.text, username)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)
        await message.answer(response["choices"][0]["message"]["content"], parse_mode='HTML')


executor.start_polling(dp)
