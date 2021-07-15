from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from bitly_api import bitly_api
import logging
import os
ref = "" #Put your ref in ""
shortner = bitly_api.Connection(access_token="") #Put your token in ""
updater = Updater(token="", use_context=True) #Put your token in ""

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Un bot per aggiungere ref a link gamivo in modo automatico")
def about(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bot realizzato da @diegoistech")
def version(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="La verisone attuale è la 1.3")
def github(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="https://github.com/DiegoDev-It/GamivoRef/")
def send(update, context):
    user_says = " ".join(context.args)
    user_sayed = update.message.from_user
    if user_sayed['username'] == "diegoistech":
        context.bot.send_message(chat_id=update.effective_chat.id, text=user_says)
def status(update, context):
    response = os.system("ping -c 1 " + "") #Put your ip in ""
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
        if "https://" in lowered_text_message: #if https
            if "www.gamivo.com" in lowered_text_message: #if www
                new_url = lowered_text_message.split("https://www.gamivo.com/product/")
                if "?" in lowered_text_message:
                    new_url_1 = new_url[1].split("?")
                    long_url = "https://gamivo.com/product/" + new_url_1[0] + ref
                elif "?" not in lowered_text_message:
                    long_url = "https://gamivo.com" + new_url[0] + ref
            elif "gamivo.com" in lowered_text_message: #if not www
                new_url = lowered_text_message.split("https://gamivo.com/product/")
                if "?" in lowered_text_message:
                    new_url_1 = new_url[1].split("?")
                    long_url = "https://www.gamivo.com/product/" + new_url_1[0] + ref
                elif "?" not in lowered_text_message:
                    long_url = "https://gamivo.com" + new_url[0] + ref
            short_url = shortner.shorten(long_url)
            context.bot.send_message(chat_id=update.effective_chat.id, text="@" + user["username"] + " ecco il tuo link:\n" + short_url["url"])
            context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
        else:
            if "www.gamivo.com" in lowered_text_message: #if www
                new_url = lowered_text_message.split("www.gamivo.com/product/")
                if "?" in lowered_text_message:
                    new_url_1 = new_url[1].split("?")
                    long_url = "https://www.gamivo.com/product/" + new_url_1[0] + ref
                elif "?" not in lowered_text_message:
                    long_url = "https://" + "gamivo.com" + new_url[0] + ref
            elif "gamivo.com" in lowered_text_message: #if not www
                new_url = lowered_text_message.split("gamivo.com/product/")
                if "?" in lowered_text_message:
                    new_url_1 = new_url[1].split("?")
                    long_url = "https://www.gamivo.com/product/" + new_url_1[0] + ref
                elif "?" not in lowered_text_message:
                    long_url = "https://" + "gamivo.com" + new_url[0] + ref
            print(long_url)
            short_url = shortner.shorten(long_url) 
            context.bot.send_message(chat_id=update.effective_chat.id, text="@" + user["username"] + " ecco il tuo link:\n" + short_url["url"])
            context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
                
    
dispatcher = updater.dispatcher
start_handler = CommandHandler("start", start)
info_handler = CommandHandler("about", about)
version_handler = CommandHandler("version", version)
github_handler = CommandHandler("github", github)
send_handler = CommandHandler("talk", send)
status_handler = CommandHandler("status", status)
text_handler = MessageHandler(Filters.text, text)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(info_handler)
dispatcher.add_handler(version_handler)
dispatcher.add_handler(github_handler)
dispatcher.add_handler(send_handler)
dispatcher.add_handler(status_handler)
dispatcher.add_handler(text_handler)
updater.start_polling()
