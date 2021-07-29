from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from bitly_api import bitly_api
from unshortenit import UnshortenIt
import logging
import os
import re
unshortener = UnshortenIt()
short_url_list = [""]
short_bitly_list = [""]
bitly_list = [""]
long_url_list = [""]
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
    context.bot.send_message(chat_id=update.effective_chat.id, text="La verisone attuale è la 1.5")
def github(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="https://github.com/DiegoDev-It/GamivoRef/")
def devgroup(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=" @angolodidiegogruppo")
def devchannel(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=" @angolodidiego")
def ref_link(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=" @angolodidiego")
def send(update, context):
    user_says = " ".join(context.args)
    user_sayed = update.message.from_user
    if user_sayed['username'] == "diegoistech":
        context.bot.send_message(chat_id=update.effective_chat.id, text=user_says)
def status(update, context):
    response = os.system("ping -c 1 " + "https://zonadidiego.tk") #Put your ip in ""
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
        x = re.findall(r"(?:https?://)?(?:www.)?gamivo.com\S*", lowered_text_message)
        if len(x) > 70:
            context.bot.send_message(chat_id=update.effective_chat.id, text="@" + user["username"] + " il tuo messaggio contiene troppi url.")
            context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
        else:
            for y in x:
                long_url_list.append(y)
                if "https://" in y:
                    y = y.split("?")[0] + ref
                    short_url = shortner.shorten(y)
                elif "http://" in y:
                    y = y.replace("http://", "https://")
                    y = y.split("?")[0] + ref
                    short_url = shortner.shorten(y)
                else:
                    y = "https://" + y
                    y = y.split("?")[0] + ref
                    short_url = shortner.shorten(y)
                short_url_list.append(short_url["url"])         
                for i,j in zip(short_url_list,long_url_list):
                    lowered_text_message = lowered_text_message.replace(j,i)
            context.bot.send_message(chat_id=update.effective_chat.id, text="@" + user["username"] + " aveva scritto: " + lowered_text_message)
            context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
    elif "bit.ly" in lowered_text_message:
        x = re.findall(r"(?:https?://)?(?:www.)?bit.ly\S*", lowered_text_message)
        for y in x:
            short_url = unshortener.unshorten(y)
            if "gamivo.com" in short_url:
                bitly_list.append(y)
                if "https://" in short_url:
                    short_url = short_url.split("?")[0] + ref
                    short_url = shortner.shorten(short_url)
                elif "http://" in short_url:
                    short_url = short_url.replace("http://", "https://")
                    short_url = short_url.split("?")[0] + ref
                    short_url = shortner.shorten(short_url)
                else:
                    short_url = "https://" + short_url
                    short_url = short_url.split("?")[0] + ref
                    short_url = shortner.shorten(short_url)
                for i,j in zip(short_bitly_list, bitly_list):
                    lowered_text_message = lowered_text_message.replace(j,i)
                long_url_list.clear()
                short_url_list.clear()
        context.bot.send_message(chat_id=update.effective_chat.id, text="@" + user["username"] + " aveva scritto: " + lowered_text_message)
        context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
                
dispatcher = updater.dispatcher
start_handler = CommandHandler("start", start)
info_handler = CommandHandler("about", about)
version_handler = CommandHandler("version", version)
github_handler = CommandHandler("github", github)
devgroup_handler = CommandHandler("devgroup", devgroup)
devchannel_handler = CommandHandler("devchannel", devchannel)
ref_link_handler = CommandHandler("ref", ref)
send_handler = CommandHandler("talk", send)
status_handler = CommandHandler("status", status)
text_handler = MessageHandler(Filters.text, text)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(info_handler)
dispatcher.add_handler(version_handler)
dispatcher.add_handler(github_handler)
dispatcher.add_handler(devgroup_handler)
dispatcher.add_handler(devchannel_handler)
dispatcher.add_handler(ref_link_handler)
dispatcher.add_handler(send_handler)
dispatcher.add_handler(status_handler)
dispatcher.add_handler(text_handler)
updater.start_polling()
