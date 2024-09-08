import telebot
from random import choice
import settings  # Файл с токеном

# Создание экземпляра бота с токеном из файла settings
bot = telebot.TeleBot(token='7488139606:AAHKKi6VC9FUVa8B-AWLHJyHU0r046uCv4U')

# Функция для проверки, есть ли в сообщении ссылка
def contains_link(text):
    return "http://" in text or "https://" in text or "www." in text

# Обработчик команды /coin
@bot.message_handler(commands=['coin'])
def coin_handler(message):
    # Выбор случайной стороны монеты
    coin = choice(["ОРЕЛ", "РЕШКА"])
    # Отправка ответа пользователю
    bot.reply_to(message, coin)

# Обработчик сообщений (банит пользователя за отправку ссылки)
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_message(message):
    if message.chat.type in ['group', 'supergroup']:  # Только в группах или супергруппах
        if contains_link(message.text):  # Если сообщение содержит ссылку
            try:
                # Получаем информацию о пользователе
                user_id = message.from_user.id
                chat_id = message.chat.id

                # Баним пользователя
                bot.kick_chat_member(chat_id, user_id)

                # Отправляем уведомление в чат
                bot.reply_to(message, f"Пользователь {message.from_user.first_name} был забанен за отправку ссылки.")
            except Exception as e:
                bot.reply_to(message, f"Ошибка при попытке забанить пользователя: {e}")
        else:
            # Если сообщение не содержит ссылку, делаем эхо-ответ
            bot.reply_to(message, message.text)

# Запуск бота
if __name__ == "__main__":  # Проверка точки входа
    try:
        print("Бот запущен...")
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Произошла ошибка: {e}")
