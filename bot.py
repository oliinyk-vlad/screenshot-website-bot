import logging
import time

from aiogram import Bot, types, executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.webhook import SendDocument, SendMessage
from aiogram.utils.executor import start_webhook

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from config import (API_TOKEN, WEBHOOK_URL, WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT)

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--start-maximized')
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(message.chat.id,
                           "Hello, i`m website screenshot bot, send a website link to get a screenshot.\n"
                           "Link example: https://www.google.com.ua/")


@dp.message_handler()
async def screenshot(message: types.Message):
    if message.text.startswith('http://') or message.text.startswith('https://'):
        await bot.send_message(chat_id=message.chat.id, text="Wait a second...")

        url = message.text
        picture_path = "image.png"
        try:
            driver.get(url)
        except:
            return SendMessage(chat_id=message.chat.id, text="Incorrect link")

        window_size = driver.get_window_size()
        width = driver.execute_script('return document.body.parentNode.scrollWidth')
        height = driver.execute_script('return document.body.parentNode.scrollHeight')
        driver.set_window_size(width, height)

        await message.reply(text="taking a website screenshot...")

        driver.find_element_by_tag_name('body').screenshot(picture_path)
        driver.set_window_size(window_size['width'], window_size['height'])

        await message.reply(text="Done")
        return SendDocument(chat_id=message.chat.id, document=types.InputFile(picture_path), caption=url)
    return SendMessage(chat_id=message.chat.id, text="Incorrect link")


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dp):
    logging.warning('Shutting down..')
    await bot.delete_webhook()
    logging.warning('Bye!')


if __name__ == '__main__':
    # long polling
    executor.start_polling(dp, skip_updates=True)
    # webhook
    # start_webhook(
    #     dispatcher=dp,
    #     webhook_path=WEBHOOK_PATH,
    #     on_startup=on_startup,
    #     on_shutdown=on_shutdown,
    #     skip_updates=True,
    #     host=WEBAPP_HOST,
    #     port=WEBAPP_PORT,
    # )