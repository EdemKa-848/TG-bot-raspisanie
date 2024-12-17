import telebot
from telebot import types
from config import *


MI_ADMIN_ID = (ADMIN_ID)
bot = telebot.TeleBot(TOKEN)

schedule = {
    "Понедельник": [{"subject": "Математика", "time": "9:00"}, {"subject": "Русский язык", "time": "10:00"}],
    "Вторник": [{"subject": "История", "time": "9:00"}, {"subject": "Физика", "time": "10:00"}],
    "Среда": [{"subject": "Математика", "time": "9:00"}, {"subject": "Русский язык", "time": "10:00"}],
    "Четверг": [{"subject": "История", "time": "9:00"}, {"subject": "Физика", "time": "10:00"}],
    "Пятница": [{"subject": "Математика", "time": "9:00"}, {"subject": "Русский язык", "time": "10:00"}],
    "Суббота": [{"subject": "История", "time": "9:00"}, {"subject": "Физика", "time": "10:00"}],
}



def create_schedule_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    schedule_button = types.KeyboardButton("Получить расписание")
    schedule_button1 = types.KeyboardButton("Добавить расписание")
    schedule_button2 = types.KeyboardButton("Главное меню")
    markup.add(schedule_button,schedule_button1,schedule_button2)
    return markup
markup = create_schedule_keyboard()

@bot.message_handler(commands=['start'])
def start(message):
    markup = create_schedule_keyboard()
    bot.send_message(message.chat.id, "Мы - онлайн-школа, стремящаяся обеспечить наших учеников удобными и эффективными инструментами для обучения. Нажми на кнопку, чтобы получить расписание:", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "Получить расписание")
def get_schedule(message):
    try:
        schedule_text = "Расписание уроков:\n\n"
        if not schedule:
            schedule_text += "Расписание еще не задано.\n"
            bot.send_message(message.chat.id, schedule_text, reply_markup=markup)
            return

        for day, lessons in schedule.items():
            schedule_text += f"{day}:\n"
            for lesson in lessons:
                try:
                    schedule_text += f"- {lesson['subject']}: {lesson['time']}\n"
                except KeyError as e:
                    schedule_text += f"Ошибка в данных для урока: {e}\n" #
            schedule_text += "\n"
        markup = create_schedule_keyboard()
        bot.send_message(message.chat.id, schedule_text, reply_markup=markup)
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {e}", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "Добавить расписание")
def set_schedule_command(message):
    if message.chat.id == MI_ADMIN_ID:
        bot.reply_to(message, "У вас нет прав для изменения расписания.", reply_markup=markup)
        return
    bot.send_message(message.chat.id, "Введите расписание в формате:\n'Понедельник: предмет1 время1, предмет2 время2; Вторник: предмет1 время1; ...'\n")
    bot.register_next_step_handler(message, set_schedule_input)

@bot.message_handler(func=lambda message: True, pass_args=True)
def set_schedule_input(message):
    try:
        data = message.text.split(';')
        global schedule
        schedule = {}
        for line in data:
            parts = line.split(':', 1)
            if len(parts) == 2:
                day = parts[0].strip()
                lessons_str = parts[1].strip()           
                lessons = [item.strip().split() for item in lessons_str.split(',')]
                schedule[day] = [{'subject': l[0], 'time': l[1]} for l in lessons if len(l) == 2]
            bot.send_message(message.chat.id, "Расписание обновлено.", reply_markup=markup)
    except (IndexError, ValueError) as e:
        bot.reply_to(message, f"Ошибка в формате данных: {e}. Пожалуйста, используйте правильный формат.", reply_markup=markup)
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка при обновлении расписания: {e}", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Главное меню")
@bot.message_handler(commands=['start'])
def start(message):
    markup = create_schedule_keyboard()
    bot.send_message(message.chat.id, "Привет! Нажми на кнопку, чтобы получить расписание:", reply_markup=markup)


if __name__ == '__main__':
    bot.polling(none_stop=True)