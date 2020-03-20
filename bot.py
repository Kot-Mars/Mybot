import telebot
import pyowm
import random
import os
from telebot import types
global a

token = os.environ.get('TOKEN')
tokenpog =os.environ.get('TOKPOG')
bot = telebot.TeleBot(token)  #ТОКИН БОТА БЕРИТ С config.py
owm = pyowm.OWM(tokenpog, language='ru')#Токин погоды

@bot.message_handler(commands=['start']) #команда /start
def welcome(message): #Функция приветствия
    sti = open('welcome.webp', 'rb')#открывает картинку
    bot.send_sticker(message.chat.id, sti)#бот отправляет картинку

    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)#создание клавиатуры
    item1 = types.KeyboardButton("🎲 Рандомное число")#1 кнопка Рандомное число
    item2 = types.KeyboardButton("Погода")#2- кнопка погода

    markup.add(item1, item2)#добавление кнопок 

    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот, создан, чтобы помогать тебе 😉".format(message.from_user, bot.get_me()),
        parse_mode='html', reply_markup=markup)#Ввод сообщение приветсвия и ввывод клавиатуры пользователю  reply_markup=markup  
        
def get_pogoga(message): #функция погоды
    try: 
        global pogoga  #глобальная переменая
        pogoga = message.text #погода = тому что напишит пользователь
        if pogoga == "Спб": #если пользователь написал Спб то
           pogoga = "Санкт-Петербург"#он превращает его в Санкт-Петербург для работы программы
        observation = owm.weather_at_place(pogoga)#смотрит место и ищит его
        w = observation.get_weather() #сохраняет статус
        temp = w.get_temperature('celsius')['temp']#сохраняет температуру
        humidity=w. get_humidity ()#сохраняет влажность
        windy = w. get_wind () ['speed']#сохраняет скорость ветра
        answer='В городе ' +  pogoga  +  " cейчас " +  w.get_detailed_status()+ "\n"#сохраняет для ответа стутус погоды
        answer += 'Сейчас в районе температура '+ str(temp) +'\n'#сохраняет для ответа температуру
        answer +='Влажность: ' + str(humidity) +"\n"#сохраняет для ответа влажность
        answer +='Скорость ветра: '+str(windy)+"\n"#сохраняет для ответа скорость ветра
        bot.send_message(message.chat.id, answer)#Ввыводит все,что сохранил
    except: #Если виден неверно город 
        global a #Глобальная переменая
        if a == 0: #Если а==0 то
            markup = types.InlineKeyboardMarkup(row_width=2) #Создается клавиатура под текстом
            item1 = types.InlineKeyboardButton("Отменить ввод погоды", callback_data='bad')#в ней Отменить ввод клавиатуры
            markup.add(item1) #Ввывод её
            bot.send_message(message.chat.id,"Что-то тут не так😔 Побробуй ещё раз",reply_markup=markup) #Бот пишет Что-то тут не так😔 Побробуй ещё раз 
            bot.register_next_step_handler(message, get_pogoga) #Ввозвращает на поиск города пока пользователю нужно вести город правильно или нажать на отмену


  
@bot.message_handler(content_types=['text']) #проверка кнопок
def pogoga(message):
  if message.chat.type == 'private':
   if message.text == '🎲 Рандомное число': #Если рандом кнопка
      bot.send_message(message.chat.id, str(random.randint(0,100)))  #Выводит рандомно число от 0 до 99
   elif message.text == 'Погода': #Если погода 
      bot.send_message(message.chat.id,'В каком вы горороде/стране?:')#Бот спращивает В каком вы горороде/стране?
      global a
      a=0
      bot.register_next_step_handler(message, get_pogoga) #отправляет в фунцию погода
   else:
      bot.send_message(message.chat.id, "Я не знаю, что ответить😢") #Если пишут что-то боту то он отвечает

@bot.callback_query_handler(func=lambda call: True) #кнопка под текстом для погоды
def callback_inline(call):
    try:
        if call.message:
           if call.data == 'bad': #проверка кнопки  Отменить ввод погоды
                bot.send_message(call.message.chat.id, 'Как скажешь😉') #Бот отправляет сообщение как скажешь
                global a
                a=1
           bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Ввод отменен",
                reply_markup=None) #меняет сообщение Что-то тут не так😔 Побробуй ещё раз на Ввод отменен,удаляет клавиатуру под текстом
    except Exception as e:
        pass 
bot.polling(none_stop =  True)    