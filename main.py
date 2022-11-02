from pprint import pprint
from time import sleep

import vk_func as VK
import get_id as GI
import telebot
import os
import requests
from dotenv import load_dotenv
load_dotenv()
tg_token = os.getenv('TG_TOKEN')
vk_token = os.getenv('VK_TOKEN')
bot = telebot.TeleBot(tg_token)
first_time = True


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f"Привет, чтобы начать отслеживать друзей "
                                      f"напиши команду /trace 'ссылка на страницу'")


@bot.message_handler(commands=['trace'])
def start_tracing(message):
    bot.send_message(message.chat.id, f"Начинаю слежку")
    if len(message.text.split()) != 2:
        bot.send_message(message.chat.id, f"Неправильный ввод данных")
    else:
        url = message.text.split()[1]
        correct_url = False
        try:
            response = requests.get(url)
            if response.status_code != 200:
                bot.send_message(message.chat.id, f"Страница {url} не найдена")
            else:
                correct_url = True
        except:
            bot.send_message(message.chat.id, f"Страница {url} не найдена")
        if correct_url:
            user_id = GI.get_vk_id(url)
            current_friends = VK.get_friends(user_id, vk_token, message)
            list_of_friends = '\n'
            for friend in current_friends:
                if friend['online'] == 1:
                    list_of_friends += f"{friend['first_name']} {friend['last_name']}\n"
            bot.send_message(message.chat.id,
                             f"Пользователи онлайн:"
                             f"{list_of_friends}")
            for i in range(0, 50):
                bot.send_message(message.chat.id, f"Проверка {i+1} из 50")
                current_friends = VK.get_friends(user_id, vk_token, message)
                if i == 0:
                    old_friends = current_friends
                else:
                    for item in range(0, len(current_friends)):
                        if current_friends[item]['online'] != old_friends[item]['online']:
                            if current_friends[item]['online'] == 1:
                                bot.send_message(message.chat.id,
                                                 f"{current_friends[item]['first_name']} {current_friends[item]['last_name']} - появился в сети")
                            else:
                                bot.send_message(message.chat.id,
                                                 f"{current_friends[item]['first_name']} {current_friends[item]['last_name']} - вышел из сети")
                    old_friends = current_friends
                sleep(60)


if __name__ == '__main__':
    bot.polling(non_stop=True)
