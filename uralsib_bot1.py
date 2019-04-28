import telebot
import sqlite3
from telebot import types

token = '720487101:AAGzHf5Iq7GeNFixTWzc1gae5E4OA-Yu3Yc'
database_name = 'uralsib.db'  #Файл с базой данных
bot = telebot.TeleBot(token)
conn = sqlite3.connect('/Users/apple/PycharmProjects/Usib/uralsib.db')
cursor = conn.cursor()
cursor.execute("SELECT count(*) FROM banks")
count = cursor.fetchall()
j = 0

x=[]#массив с координатами lon
y=[]#массив с координатами lat
for i in range (1, count [0][0]+1):
    cursor = conn.cursor()
    cursor.execute("SELECT coordinates_lon FROM banks WHERE id = '{}'".format(i))
    a = cursor.fetchall()
    cursor.execute("SELECT coordinates_lat FROM banks WHERE id = '{}'".format(i))
    b = cursor.fetchall()
    x.append(a[0][0])
    y.append(b[0][0])

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*[types.KeyboardButton(name) for name in ['Физическое лицо', 'Юридическое лицо', 'Телефон для справки']])
    msg = bot.send_message(message.chat.id, "Добрый день! Вас приветствует компания Уралсиб.", reply_markup=markup)
    bot.register_next_step_handler(msg, name)

def name(m):
    if m.text == 'Физическое лицо':
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup1.row('Платежи')
        markup1.row('Валютные депозиты')
        markup1.row('Кредиты частным лицам')
        markup1.row('Банковские карты')
        markup1.row('Дебетовые карты')
        markup1.row('Телефон для справки', 'Назад')
        msg = bot.send_message(m.chat.id, "Выберете необходимую операцию:", reply_markup=markup1)
        bot.register_next_step_handler(msg, name1)
    elif m.text == 'Юридическое лицо':
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup1.row('Платежи')
        markup1.row('Валютные депозиты')
        markup1.row('Банковские карты')
        markup1.row('Дебетовые карты')
        markup1.row('Телефон для справки', 'Назад')
        msg = bot.send_message(m.chat.id, "Выберете необходимую операцию:", reply_markup=markup1)
        bot.register_next_step_handler(msg, name1)
    elif m.text == 'Телефон для справки':
        bot.send_message(m.chat.id, '8-495-723-77-77')

def name1(m):
    if m.text == 'Платежи':
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup1.row('Интернет', 'Коммунальные услуги')
        markup1.row('ТВ', 'IP телефония', 'Телефон')
        markup1.row('Сотовая связь', 'Штрафы')
        markup1.row('Образование', 'Благотворительность')
        markup1.row('Система безопасности')
        markup1.row('Телефон для справки', 'Назад')
        msg = bot.send_message(m.chat.id, "Платежи:", reply_markup=markup1)
        bot.register_next_step_handler(msg, name2)
    elif m.text == 'Валютные депозиты':
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup1.row('RUB', 'USD', 'EUR')
        markup1.row('Телефон для справки', 'Назад')
        msg = bot.send_message(m.chat.id, "Выберете валюту депозита:", reply_markup=markup1)
        bot.register_next_step_handler(msg, name2)
    elif m.text == 'Кредиты частным лицам':
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup1.row('Автокредит')
        markup1.row('Ипотечный кредит')
        markup1.row('Потребительский кредит')
        markup1.row('Целевой кредит')
        markup1.row('Телефон для справки', 'Назад')
        msg = bot.send_message(m.chat.id, "Выберете тип кредита:", reply_markup=markup1)
        bot.register_next_step_handler(msg, name2)
    elif m.text == 'Банковские карты':
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup1.row('VISA')
        markup1.row('MasterCard')
        markup1.row('AmericanExpress')
        markup1.row('Телефон для справки', 'Назад')
        msg = bot.send_message(m.chat.id, "Выберете тип банковской карты:", reply_markup=markup1)
        bot.register_next_step_handler(msg, name2)
    elif m.text == 'Дебетовые карты':
        msg = bot.send_message(m.chat.id, "Отправте Вашу геопозицию")
        bot.register_next_step_handler(msg, name3)
    elif m.text == 'Телефон для справки':
        bot.send_message(m.chat.id, '8-495-723-77-77')
    elif m.text == 'Назад':
        start(m)

def name2(m):
    if m.text == 'Телефон для справки':
        bot.send_message(m.chat.id, '8-495-723-77-77')
    elif m.text == 'Назад':
        start(m)
    else:
        global j
        conn = sqlite3.connect('/Users/apple/PycharmProjects/Usib/uralsib.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO clients (service, username) VALUES ('{}', '{}');".format(m.text, m.chat.username))
        cursor.execute("SELECT id FROM clients WHERE rowid=last_insert_rowid()")
        a = cursor.fetchall()
        j = a[0][0]
        #print(j[0][0])
        conn.commit()
        msg = bot.send_message(m.chat.id, "Отправте Вашу геопозицию")
        bot.register_next_step_handler(msg, name3)

def name3(m):
    if m.location != None:
        s = repeat_all_messages(m)
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup1.row(s[0])
        markup1.row(s[1])
        markup1.row(s[2])
        markup1.row('Телефон для справки', 'Назад')
        msg = bot.send_message(m.chat.id, "Рядом с Вами находятся следующие отделения, выберете подходящее:", reply_markup=markup1)
        bot.register_next_step_handler(msg, name4)
    elif m.text == 'Телефон для справки':
        bot.send_message(m.chat.id, '8-495-723-77-77')
    elif m.text == 'Назад':
        start(m)

def name4(m):
    if m.text == 'Телефон для справки':
        bot.send_message(m.chat.id, '8-495-723-77-77')
    elif m.text == 'Назад':
        start(m)
    else:
        global j
        msg = bot.send_message(m.chat.id, "Вы записаны в отделение " + m.text +". Ваш номер " + str(j))
        conn = sqlite3.connect('/Users/apple/PycharmProjects/Usib/uralsib.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE clients SET adress = '{}' WHERE id = {}".format(m.text, j))
        conn.commit()

#@bot.message_handler(content_types=['location'])
def repeat_all_messages(message):
    x0 = message.location.longitude
    y0 = message.location.latitude
    #print(x0, y0)
    # min1 - минимальное min2 - среднее  min3 - большое
    min1 = 1000000000000
    min2 = 1000000000000
    min3 = 1000000000000
    #id соответсвующих отделений
    id1 = 0
    id2 = 0
    id3 = 0
    for i in range (0, count [0][0]):
        t = (y0-x[i])**2+(x0-y[i])**2#похоже, что координаты в файле перепутаны
        if (t < min1):
            min3 = min2
            min2 = min1
            min1 = t
            id3 = id2
            id2 = id1
            id1 = i+1
        elif (t < min2):
            min3 = min2
            min2 = t
            id3 = id2
            id2 = i+1
        elif (t < min3):
            min3 = t
            id3 = i+1
    conn = sqlite3.connect('/Users/apple/PycharmProjects/Usib/uralsib.db')
    cursor = conn.cursor()
    cursor.execute("SELECT adress FROM banks WHERE id = '{}'".format(id1))
    a = cursor.fetchall()
    cursor.execute("SELECT adress FROM banks WHERE id = '{}'".format(id2))
    b = cursor.fetchall()
    cursor.execute("SELECT adress FROM banks WHERE id = '{}'".format(id3))
    c = cursor.fetchall()
    return(a[0][0], b[0][0], c[0][0])


bot.polling(none_stop=True)