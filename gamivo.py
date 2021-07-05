from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from bitly_api import bitly_api
import logging
import os
ref = "?glv=tejit6ep" #Put your ref in ""
shortner = bitly_api.Connection(access_token="a41ddd1af9770b446f5f36b8b09230744bed3114")
updater = Updater(token="1860763458:AAFi-rJvNt573lNTU7jZjwv-gUL_oD3Qi7o", use_context=True)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Un bot per aggiungere ref a link gamivo in modo automatico")
def about(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bot realizzato da @diegoistech")
def version(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="La verisone attuale è la 1.1a")
def github(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="https://github.com/DiegoDev-It/GamivoRef/")
def status(update, context):
    response = os.system("ping -c 1 " + "192.168.1.21")
    if response == 0:
        interno_text = "Stato interno server: " + "✅" + "\n"
    elif response != 0:
        interno_text = "Stato interno server: " + "❌" + "\n"
    response_b = os.system("ping -c 1 " + "bit.ly")
    if response_b == 0:
        bitly_text="Stato server bit.ly: " + "✅" + "\n"
    elif response_b != 0:
        bitly_text = "Stato server bit.ly: " + "❌" + "\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=interno_text + bitly_text)
def text(update, context):
    user = update.message.from_user
    text_message = update.message.text
    lowered_text_message = text_message.lower()
    if "gamivo.com" in lowered_text_message:
        print(lowered_text_message)
        if "?glv" in lowered_text_message:
            ref_text = lowered_text_message.split("?glv")
            if "https://" in lowered_text_message:
                long_url = ref_text[0] + ref
            else:
                long_url = "https://" + ref_text[0] + ref   
                short_url = shortner.shorten(long_url)
            context.bot.send_message(chat_id=update.effective_chat.id, text="@" + user["username"] + " ecco il tuo link:\n" + short_url["url"])
            context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
        else:
            if "https://" in lowered_text_message:
                long_url = lowered_text_message + ref
                short_url = shortner.shorten(long_url)
            else:
                long_url = "https://" + lowered_text_message + ref
                short_url = shortner.shorten(long_url)
            context.bot.send_message(chat_id=update.effective_chat.id, text="@" + user["username"] + " ecco il tuo link:\n" + short_url["url"])
            context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
                
    
dispatcher = updater.dispatcher
start_handler = CommandHandler("start", start)
info_handler = CommandHandler("about", about)
version_handler = CommandHandler("version", version)
github_handler = CommandHandler("github", github)
status_handler = CommandHandler("status", status)
text_handler = MessageHandler(Filters.text, text)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(info_handler)
dispatcher.add_handler(version_handler)
dispatcher.add_handler(github_handler)
dispatcher.add_handler(status_handler)
dispatcher.add_handler(text_handler)
updater.start_polling()

