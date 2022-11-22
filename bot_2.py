import telebot
from collections import Counter

bot = telebot.TeleBot('5594968248:AAEb4rHYoPUZDowrczr3sGvxtixPBWTi1Kk')


def all_words(txt):
    words = []
    marks = '''!()-[]{};?@#$%:'"\,./^&amp;*_'''
    for elem in marks:
        txt = txt.replace(elem, '')
    for word in txt.split():
        words.append(word.lower())
    return words


def unique_words(txt):
    words = all_words(txt)
    unique = set(words)
    return len(unique)


def common_word(txt):
    words = all_words(txt)
    conj_and_prep = ['и', 'да', 'ни', 'как', 'тоже', 'также', 'а', 'но', 'зато', 'или', 'либо', 'то', 'не',
                     'в', 'к', 'до', 'по', 'через', 'после', 'из', 'за', 'над', 'под', 'перед', 'у', 'возле',
                     'мимо', 'около', 'от', 'для', 'обо', 'но', 'без', 'c', 'на']

    for word in words:
        if word in conj_and_prep:
            words.remove(word)
    counter_dict = Counter(words)
    max_count = counter_dict.most_common(1)[0][0]
    return max_count


def sentences(txt):
    dot = 0
    end_of_sent = ['.', '!', '?']
    for elem in txt:
        if elem in end_of_sent:
            dot += 1
    return dot


@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, 'Отправь мне какой-нибудь текст или напиши /help')


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == '/help':
        bot.send_message(message.from_user.id,
                         'Привет! \nОтправь мне какой-нибудь текст, я проанализирую его и отправлю тебе статистику')

    else:
        user_msg = message.text
        unq_w = unique_words(user_msg)
        cmn_w = common_word(user_msg)
        sntnc = sentences(user_msg)
        bot.send_message(message.from_user.id, f'Результат анализа: \n'
                                               f'Итого количество уникальных слов - {unq_w} \n'
                                               f'Итого самое популярное слово - {cmn_w} \n'
                                               f'Итого количество предложений - {sntnc}')


bot.polling(none_stop=True, interval=0)
