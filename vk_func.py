import requests
import telebot
import os
from dotenv import load_dotenv


load_dotenv()
tg_token = os.getenv('TG_TOKEN')
bot = telebot.TeleBot(tg_token)


def get_friends_list(user_id, token):
    data = {
        'access_token': token,
        'v': 5.92,
        'user_id': user_id,
        'order': 'hints',
        'fields': 'nickname, bdate, online'
    }
    friends_list = requests.get('https://api.vk.com/method/friends.get', params=data)
    return friends_list.json()


def get_friends(user_id, token, message):
    data = {
        'access_token': token,
        'v': 5.92,
        'user_id': user_id,
        'fields': 'online'
    }
    friends_list = requests.get('https://api.vk.com/method/friends.get', params=data)
    return friends_list.json()['response']['items']


def get_changed_status(current_friends, old_friends):
    for friend in current_friends:
        if current_friends['online'] != old_friends['online']:
            if current_friends['online'] == 1:
                bot.send_message(current_friends['user_id'],
                                 f"{current_friends['first_name']} {current_friends['last_name']} - появился в сети")
            else:
                bot.send_message(current_friends['user_id'],
                                 f"{current_friends['first_name']} {current_friends['last_name']} - вышел из сети")