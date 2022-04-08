from telegram.ext import Updater, MessageHandler, Filters, ConversationHandler
from telegram.ext import CallbackContext, CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton
from skripty import singin

TOKEN = "5117275801:AAGHwoaUCbusJavBHxd9r4mEBC3yKdlh6rs"
indices = {}


def login(update, context):
    update.message.reply_text(
        "Начинаем процедуру входа \n"
        "Для выхода из диалога авторизации введите команду /stop\n"
        "Вы готовы, дети?",
        # reply_markup=ReplyKeyboardMarkup(markup, one_time_keyboard=True)
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
        indices['district'] = singin.districts[context.user_data['district']][0]
        # global locality
        # locality = singin.districts[context.user_data['district']]
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
        indices['locality'] = singin.districts[context.user_data['district']][1][context.user_data['locality']][0]
        # type = locality
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
        indices['type_oo'] = singin.districts[context.user_data['district']][1][context.user_data['locality']][1][
            context.user_data['type_oo']][0]
        # type = locality
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
        indices['oo'] = singin.districts[context.user_data['district']][1][context.user_data['locality']][1][
            context.user_data['type_oo']][1][context.user_data['oo']]

        update.message.reply_text(
            "Введите логин пароль через пробел\n"
            "Например: 'ИвановИ 12345678'", reply_markup=ReplyKeyboardRemove()
        )
        return 6
    except KeyError:
        update.message.reply_text('Нет такой образовательной организации')


def end(update, context):
    try:
        indices['login'], indices['password'] = update.message.text.split()
        update.message.reply_text(
            "Класс! молодец"
        )
        print(indices)
        return ConversationHandler.END
    except ValueError:
        return 5


def stop(update, context):
    update.message.reply_text("Жаль. А было бы интересно пообщаться. Всего доброго!")
    return ConversationHandler.END  # Константа, означающая конец диалога.


def help(update, context):
    update.message.reply_text(
        "Для того чтобы приступить к авторизации введите /login")




def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('login', login)],  # Точка входа в диалог.
        # В данном случае команда /login. Она задает первый вопрос.

        states={
            # Добавили user_data для сохранения ответа.
            1: [MessageHandler(Filters.text & ~Filters.command, district, pass_user_data=True)],

            # ...и для его использования.
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

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
