from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from bitly_api import bitly_api
import logging
ref = "" #Put your ref in ""
shortner = bitly_api.Connection(access_token="") #Put your token in ""
gamivo_web = ["gamivo.com", "GAMIVO.COM", "Gamivo.com"]
updater = Updater(token="1860763458:AAFi-rJvNt573lNTU7jZjwv-gUL_oD3Qi7o", use_context=True)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Un bot per aggiungere ref a link gamivo in modo automatico")
def about(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bot realizzato da @diegoistech")
def version(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="La verisone attuale è la 1.0")
def github(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="https://github.com/DiegoDev-It/GamivoRef/")
def text(update, context):
    user = update.message.from_user
    text_message = update.message.text
    for x in gamivo_web:
        if x in text_message:
            if "?glv" in text_message:
                ref_text = text_message.split("?glv")
                long_url = "https://" + ref_text[0] + ref
                short_url = shortner.shorten(long_url)
                context.bot.send_message(chat_id=update.effective_chat.id, text="@" + user["username"] + " ecco il tuo link:\n" + short_url["url"])
                context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
            else:
                long_url = "https://" + text_message + ref
                short_url = shortner.shorten(long_url)
                context.bot.send_message(chat_id=update.effective_chat.id, text="@" + user["username"] + " ecco il tuo link:\n" + short_url["url"])
                context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
                
    
dispatcher = updater.dispatcher
start_handler = CommandHandler("start", start)
info_handler = CommandHandler("about", about)
version_handler = CommandHandler("version", version)
github_handler = CommandHandler("github", github)
text_handler = MessageHandler(Filters.text, text)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(info_handler)
dispatcher.add_handler(version_handler)
dispatcher.add_handler(github_handler)
dispatcher.add_handler(text_handler)
updater.start_polling()
