import datetime
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def set_date(update, context):
    pass


def schedule(update, context):
    context.user_data['day'] = datetime.date.today()
    keyboard = [
        [
            InlineKeyboardButton("<--", callback_data='last'),
            InlineKeyboardButton("X", callback_data='close'),
            InlineKeyboardButton("-->", callback_data='next')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        f"Расписание на {context.user_data['day']}:",
        reply_markup=reply_markup)


def button(update, context):
    query = update.callback_query
    variant = query.data

    # `CallbackQueries` требует ответа, даже если
    # уведомление для пользователя не требуется, в противном
    #  случае у некоторых клиентов могут возникнуть проблемы.
    # смотри https://core.telegram.org/bots/api#callbackquery.

    query.answer()

    # редактируем сообщение, тем самым кнопки
    # в чате заменятся на этот ответ.

    if variant == 'last':
        context.user_data['day'] = context.user_data['day'] - datetime.timedelta(days=1)
        schedule(update, context)
    elif variant == 'next':
        context.user_data['day'] = context.user_data['day'] + datetime.timedelta(days=1)
        schedule(update, context)
    else:
        query.edit_message_text(text=f"Выбранный вариант: {variant}")


def help_command(update, context):
    update.message.reply_text("Используйте `/schedule` для тестирования.")


if __name__ == '__main__':
    # Передайте токен вашего бота.
    updater = Updater("5149454743:AAGiUTkSNAnEgeQq-xyjJosFGlEd5h9A37w")

    updater.dispatcher.add_handler(CommandHandler('schedule', schedule))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('help', help_command))

    # Запуск бота
    updater.start_polling()
    updater.idle()
