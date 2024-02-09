import re
from time import sleep

import telebot
from openai import OpenAI

BOT_TOKEN = '6891743735:AAFV3_ezfHZ4tLPQWcwxyJH_LU8drb3cb_4'
assistant = 'asst_0DNaLTH6eCjJa5G4Z2UBj9yd'
bot = telebot.TeleBot(BOT_TOKEN)
client = OpenAI(api_key="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")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,
                 'Приветствую вас! Я бот компании AirAstana. Готов помочь вам с любыми вопросами о наших рейсах, бронировании билетов, услугах и многое другое. Просто спросите, и я постараюсь ответить максимально информативно и оперативно!')


@bot.message_handler(func=lambda msg: True)
def echo_all(user_message):
    bot.send_message(user_message.chat.id, 'Одну минуту, уточняю информацию')

    thread = client.beta.threads.create()
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_message.text
    )
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant
    )
    loops = 0
    while loops < 180:
        loops += 1
        sleep(1)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        if run.status == 'completed':
            break
    else:
        bot.reply_to(user_message,
                     'Извините, кажется, у меня нет достаточной информации, чтобы ответить на ваш вопрос. Пожалуйста, свяжитесь с нашим службой поддержки для получения более подробной помощи.')
        return
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )
    bot.reply_to(user_message, re.sub(r'【(.*)】',' ',messages.data[0].content[0].text.value))
    bot.send_message(user_message.chat.id, 'Чем еще могу вам помочь?')


if __name__ == '__main__':
    bot.infinity_polling()
