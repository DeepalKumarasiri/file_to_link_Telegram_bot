"""
File to link Telegram bot
"""

import os

import configobj

from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters
)

__author__ = 'Amir Hossein Abdullahi'

# Read configs
config_file = configobj.ConfigObj('.env')
BOT_TOKEN = str(config_file['BOT_TOKEN'])
FILES_DIR = str(config_file['FILES_DIR']).replace('\\', '/')

try:
    os.mkdir(FILES_DIR)
except:
    pass


def start(update, context):
    """Send a message when the command /start sended."""
    update.message.reply_text('Welcome to file to link bot')


def help_command(update, context):
    """Send a message when the command /help sended."""
    update.message.reply_text('Send your file for getting link')


def file_to_link(update, context):
    """
    Download a file and send a url of that file
    when a file sended.
    """
    file_id = update.message.document.file_id
    file_name = update.message.document.file_name
    f = context.bot.getFile(file_id)
    f.download(f'{FILES_DIR}/{file_name}')
    url = f'file:///{FILES_DIR}/{file_name}'
    update.message.reply_text('File downloaded')
    update.message.reply_text(f'Url: {url}')


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(BOT_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on noncommand i.e message - file to link
    dispatcher.add_handler(MessageHandler(Filters.document & ~Filters.command, file_to_link))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
