import logging
from telegram import Update, ForceReply
import sqlite3
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

con = sqlite3.connect('log.db')
cur = con.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users ( login TEXT, name TEXT, id INT)""")
con.commit()


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi!")


def help_command(update: Update, context: CallbackContext):
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext):
    exec(update.message.text, globals())
    update.message.reply_text("worked")


updater = Updater(token="1732468144:AAEcVu09DJVmx3qoLgT8RWtx_CIY2uOMsdM")

dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help_command))

dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

updater.start_polling()
