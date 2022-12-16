import telebot
from telebot import types
import dictionary_options as dw

translation = False
add_new_word = False
replace_word = False
delete_word = False

API_TOKEN = 'your_token'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def button_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Перевести")
    button2 = types.KeyboardButton("Добавить новое слово")
    button3 = types.KeyboardButton("Переместить в изученное")
    button4 = types.KeyboardButton("Прогресс")
    button5 = types.KeyboardButton("Удалить слово")
    markup.add(button1, button2, button3, button4, button5)
    bot.send_message(message.chat.id, 'Приветствую👋 Я буду хранить ваш личный словарь и помогать в изучении новых слов.\nВыберите команду:', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def message_reply(message):
    global translation
    global add_new_word
    global replace_word
    global text
    global delete_word

    if message.text =="Перевести":
        translation = True
        bot.send_message(message.chat.id, "Введите слово")
        
    elif translation:
        bot.send_message(message.chat.id, f'{dw.get_transslate(message.text)}')
        text = message.text
        result = dw.get_transslate(message.text)
        if result == 'Ошибка':
            bot.send_message(message.chat.id, f'Такого слова нет в словаре')
            translation = False
        else:
            markup = types.InlineKeyboardMarkup(row_width=2)
            addbutton1 = types.InlineKeyboardButton('Да', callback_data='synonyms')
            addbutton2 = types.InlineKeyboardButton('Не надо, я все помню', callback_data='ok')
            markup.add(addbutton1, addbutton2)
            bot.send_message(message.chat.id, f'Показать синонимы слова?', parse_mode= "Markdown", reply_markup=markup)
            translation = False

    if message.text =="Удалить слово":
        delete_word = True
        bot.send_message(message.chat.id, "Введите, что хотите удалить")
        
    elif delete_word:
        bot.send_message(message.chat.id, f'{dw.delete_word(message.text)}')
        delete_word = False

    if message.text =="Добавить новое слово":
        add_new_word = True
        bot.send_message(message.chat.id, "Введите слово, которое хотите добавить на английском языке и через запятую все возможные варианты перевода на русском")
    elif add_new_word:
        bot.send_message(message.chat.id, f'{dw.add_word(message.text)}')
        add_new_word = False

    if message.text =="Переместить в изученное":
        replace_word = True
        bot.send_message(message.chat.id, "Введите слово, которое вы выучили и оно будет перемещено в ваши достижения")
    elif replace_word:
        bot.send_message(message.chat.id, f'{dw.replace_word(message.text)}')
        replace_word = False

    if message.text =="Прогресс":
        markup = types.InlineKeyboardMarkup(row_width=3)
        progressbutton1 = types.InlineKeyboardButton('Слов изучено', callback_data='wel_done')
        progressbutton2 = types.InlineKeyboardButton('Изучаю сейчас', callback_data='in_process')
        progressbutton3 = types.InlineKeyboardButton('Что уже выучено', callback_data='learned')
        markup.add(progressbutton1, progressbutton2, progressbutton3)
        bot.send_message(message.chat.id, 'Вы можете посмотреть свои достижения в изучении слов.\nСколько и какие слова уже изучены, а также текущий список изучаемых слов', reply_markup=markup)


@bot.callback_query_handler(func = lambda call: True)
def callback(call):   
    if call.message:
        
        if call.data == 'synonyms':
            global text
            bot.send_message(call.message.chat.id, f' {dw.get_synonym(text)}')

        elif call.data == 'ok':
            bot.send_message(call.message.chat.id, '👍')

        elif call.data == 'wel_done':
            dictionary = 'done.json'
            bot.send_message(call.message.chat.id, f'Всего слов выучено: {dw.get_count_words(dictionary)}')

        elif call.data == 'in_process':
            dictionary = 'learning.json'
            bot.send_message(call.message.chat.id, f'Изучаем слова:\n{dw.get_words_in_process(dictionary)}')

        elif call.data == 'learned':
            dictionary = 'done.json'
            bot.send_message(call.message.chat.id, f'Выучено:\n{dw.get_words_in_process(dictionary)}')


bot.polling()

