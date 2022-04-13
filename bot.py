from pprint import pprint

from telegram.ext import Updater, MessageHandler, Filters, ConversationHandler
from telegram.ext import CallbackContext, CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, User, Update
from skripty import singin
import datetime
import json
from preparation import preparation

TOKEN = "5117275801:AAGHwoaUCbusJavBHxd9r4mEBC3yKdlh6rs"
indices = {}
indices['url'] = "region.obramur.ru"


def login_message(update: Update, context):
    user_id = str(update.message.from_user.id)
    print(type(user_id))
    context.user_data['user_id'] = user_id
    update.message.reply_text(
        "Начинаем процедуру входа \n"
        "Для выхода из диалога авторизации введите команду /stop\n"
        "Вы готовы, дети?",
        reply_markup=ReplyKeyboardRemove()
    )
    return 1


def district(update, context):
    district_markup = [[i] for i in singin.districts.keys()]
    update.message.reply_text(
        "Выберите городской округ / муниципальный район",
        reply_markup=ReplyKeyboardMarkup(district_markup, one_time_keyboard=True)
    )
    return 2


def locality(update, context):
    try:
        context.user_data['district'] = update.message.text
        locality_markup = [[i] for i in singin.districts[context.user_data['district']][1].keys()]
        update.message.reply_text(
            "Выберите населенный пункт",
            reply_markup=ReplyKeyboardMarkup(locality_markup, one_time_keyboard=True)
        )
        return 3
    except KeyError:
        update.message.reply_text('Нет такого района')


def type_oo(update, context):
    try:
        context.user_data['locality'] = update.message.text
        type_oo_markup = [[i] for i in
                          singin.districts[context.user_data['district']][1][context.user_data['locality']][1].keys()]
        update.message.reply_text(
            "Выберите тип оо",
            reply_markup=ReplyKeyboardMarkup(type_oo_markup, one_time_keyboard=True)
        )
        return 4
    except KeyError:
        update.message.reply_text('Нет такого города')


def oo(update, context):
    try:
        context.user_data['type_oo'] = update.message.text
        oo_markup = [[i] for i in
                     singin.districts[context.user_data['district']][1][context.user_data['locality']][1][
                         context.user_data['type_oo']][1].keys()]
        update.message.reply_text(
            "Выберите образовательную организацию",
            reply_markup=ReplyKeyboardMarkup(oo_markup, one_time_keyboard=True)
        )
        return 5
    except KeyError:
        update.message.reply_text('Нет такого типа')


def password(update, context):
    try:
        context.user_data['oo'] = update.message.text
        indices['school'] = context.user_data['oo']

        update.message.reply_text(
            "Введите логин пароль через пробел\n"
            "Например: 'ИвановИ 12345678'", reply_markup=ReplyKeyboardRemove()
        )
        return 6
    except KeyError:
        update.message.reply_text('Нет такой образовательной организации')


def end(update, context):
    try:
        indices['user_name'], indices['password'] = update.message.text.split()
        update.message.reply_text(
            "Класс! молодец"
        )

        try:
            preparation
        with open(f'users/{context.user_data["user_id"]}.json', 'w', encoding="utf-8") as cfg:
            json.dump(indices, cfg, ensure_ascii=False)

        return ConversationHandler.END
    except ValueError:
        return 5


def schedule(day):
    pass


def schedule_today():
    schedule(datetime.date.today())


def schedule_not_today():
    schedule(datetime.date())


def start(update, context):
    # context['user_id'] = User.id
    print(update.chat)
    update.message.reply_text(
        "Перед началом работы необходима авторизация"
        "Для того чтобы приступить к ней введите /login")


def stop(update, context):
    update.message.reply_text("Жаль. А было бы интересно пообщаться. Всего доброго!")
    return ConversationHandler.END  # Константа, означающая конец диалога.


def help(update, context):
    update.message.reply_text(
        "Для того чтобы приступить к авторизации введите /login")


def login(update, context):
    with open(f'users/config.json', 'w', encoding='utf-8') as cfg:
        json.dump(indices, cfg, ensure_ascii=False)


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('login', login_message)],  # Точка входа в диалог.
        # В данном случае команда /login. Она задает первый вопрос.

        states={
            # Добавили user_data для сохранения ответа.
            1: [MessageHandler(Filters.text & ~Filters.command, district, pass_user_data=True)],
            2: [MessageHandler(Filters.text & ~Filters.command, locality, pass_user_data=True)],
            3: [MessageHandler(Filters.text & ~Filters.command, type_oo, pass_user_data=True)],
            4: [MessageHandler(Filters.text & ~Filters.command, oo, pass_user_data=True)],
            5: [MessageHandler(Filters.text & ~Filters.command, password, pass_user_data=True)],
            6: [MessageHandler(Filters.text & ~Filters.command, end, pass_user_data=True)]
        },
        fallbacks=[CommandHandler('stop', stop)]  # Точка прерывания диалога. В данном случае команда /stop.
    )
    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('schedule_today', schedule_today))
    dp.add_handler(CommandHandler('schedule', schedule_not_today))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
