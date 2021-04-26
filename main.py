# Импортируем необходимые классы.
import sqlite3

from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup
import random
import _sqlite3



incorrect = {}
answers = []
answers_true = []
reply_keyboard = [['/help', '/start_test']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
# Определяем функцию-обработчик сообщений.
# У неё два параметра, сам бот и класс updater, принявший сообщение


def start(update, context):
    update.message.reply_text(
        "Привет! Я помогу тебе подготовиться к тестовой части ЕГЭ по математике. Командой /start_test ты "
        "можешь начать тестирование из 10 вопросов, после чего я покажу тебе результат.", reply_markup=markup)

global answer_quan
answer_quan = 1


def start_test(update, context):
    # Импорт библиотек
    # Подключение к БД
    global answer_quan
    con = sqlite3.connect('database.db')

    # Создание курсора
    cur = con.cursor()
    if answer_quan != 11:
        keyboard = ['1', '2', '3', '4']
        user_answer = update.message.text
        if user_answer != '/start_test' and user_answer != 'start_test':
            answers.append(user_answer)
            result = cur.execute("""SELECT * From exam""", ).fetchall()
            true_answ = result[answer_quan - 1][2]
            answers_true.append(true_answ)
            if user_answer != true_answ:
                incorrect[answer_quan - 1] = [result[answer_quan - 1][1], result[answer_quan - 1][2], user_answer, result[answer_quan - 1][-1], result[answer_quan - 1][2 + int(user_answer)], result[answer_quan - 1][2 + int(result[answer_quan - 1][2])]]
        markup1 = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        # Выполнение запроса и получение всех результатов
        result = cur.execute("""SELECT * From exam""", ).fetchall()
        update.message.reply_text(f'{answer_quan}. {result[answer_quan][1]}')
        update.message.reply_text(f'Варианты ответов:')
        update.message.reply_text(f'1) {result[answer_quan][3]}')
        update.message.reply_text(f'2) {result[answer_quan][4]}')
        update.message.reply_text(f'3) {result[answer_quan][5]}')
        update.message.reply_text(f'4) {result[answer_quan][6]}', reply_markup=markup1)
        answer_quan += 1
        print(f'in{incorrect}')
        return answer_quan + 1
    else:
        reply_keyboard = [['/help', '/start_test']]
        markup2 = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        update.message.reply_text(f'Тест завершен! Твой результат {10 - len(incorrect)}/10.', reply_markup=markup2)
        if len(incorrect) != 0:
            for i in incorrect:
                update.message.reply_text(f'Ошибка! № {i}.')
                update.message.reply_text(f'{incorrect[i][0]}. Ваш ответ - {incorrect[i][-2]}. Правильный ответ - {incorrect[i][-1]}')
            mistake_plots = []
            for i in incorrect:
                if incorrect[i][-3] not in mistake_plots:
                    mistake_plots.append(incorrect[i][-3])
            mistakes = ', '.join(mistake_plots)
            update.message.reply_text(f'Вам стоит повторить: {mistakes}')
        else:
            update.message.reply_text(f'Молодчина! У тебя нету ошибок!')

def help(update, context):
    update.message.reply_text(f'Нажав на кнопку /start_test, ты начнешь тестирование из 10 вопросов. После его прохождения ты увидишь свой результат и сделаешь выводы)')


def stop_test(update, context):
    update.message.reply_text(
        f'Ты остановил тестирование, но сможешь перепройти его в любой момент.')

test_handler = ConversationHandler(
    # Точка входа в диалог.
    # В данном случае — команда /start. Она задаёт первый вопрос.
    entry_points=[CommandHandler('start_test', start_test)],

    # Состояние внутри диалога.
    # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
    states={
        # Функция читает ответ на первый вопрос и задаёт второй.
        1: [MessageHandler(Filters.text, start_test)],
        2: [MessageHandler(Filters.text, start_test)],
        3: [MessageHandler(Filters.text, start_test)],
        4: [MessageHandler(Filters.text, start_test)],
        5: [MessageHandler(Filters.text, start_test)],
        6: [MessageHandler(Filters.text, start_test)],
        7: [MessageHandler(Filters.text, start_test)],
        8: [MessageHandler(Filters.text, start_test)],
        9: [MessageHandler(Filters.text, start_test)],
        10: [MessageHandler(Filters.text, start_test)],
        11: [MessageHandler(Filters.text, start_test)],
        12: [MessageHandler(Filters.text, start_test)]
    },

    # Точка прерывания диалога. В данном случае — команда /stop.
    fallbacks=[CommandHandler('stop_test', stop_test)]
)

def main():

    # Создаём объект updater.
    # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен
    updater = Updater('1732179850:AAEKnX7h8iNivSH3SMUDD8PgOyHG32K1siQ', use_context=True)

    # Получаем из него диспетчер сообщений.
    dp = updater.dispatcher

    # Создаём обработчик сообщений типа Filters.text
    # из описанной выше функции echo()
    # После регистрации обработчика в диспетчере
    # эта функция будет вызываться при получении сообщения
    # с типом "текст", т. е. текстовых сообщений.

    # Регистрируем обработчик в диспетчере.
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(test_handler)
    # Запускаем цикл приема и обработки сообщений.
    updater.start_polling()

    # Ждём завершения приложения.
    # (например, получения сигнала SIG_TERM при нажатии клавиш Ctrl+C)
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()