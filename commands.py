import logging
import os
import re

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, InlineQueryHandler)
from telegram import (InlineQueryResultCachedVoice, ReplyKeyboardMarkup, ReplyKeyboardRemove,KeyboardButton)

from sqlalchemy import create_engine 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

from src.media import Media
from src.upload import Upload, state_dict
from src.search import Search

logging.basicConfig(level=logging.INFO)

logger=logging.Logger(name=__name__,level=logging.INFO)

def start(update,context):
   context.bot.send_message(chat_id=update.message.chat_id,text='Hello and welcome to the first ever ZEDVoiceBot,\
where you can send you favorite voices from our fellow friends\n, \
Long Live ZED!');


def main():
    DATABASE_URL = os.environ['DATABASE_URL']
    TOKEN = os.environ['TOKEN']
    db = create_engine(DATABASE_URL)
    conn = db.connect()
    Base = automap_base()
    Base.prepare(db, reflect=True)
    User = Base.classes.users
    Voice = Base.classes.voices
    session = Session(db)

    upload = Upload(session_db=session,tables=[User, Voice])
    select = Search(session_db=session,tables=[User, Voice])
    # with open('token.txt','r') as token_file:
    #    token = token_file.readline().strip('\n')
    token = TOKEN
    updater = Updater(token=token, use_context=True)
    
    
    dsp = updater.dispatcher

    start_handler = CommandHandler('help',start)
    upload_handler = ConversationHandler(entry_points=[CommandHandler('upload',upload.upload_info)],
    states={
        state_dict['UPLOAD_INFO'] : [MessageHandler(Filters.text, upload.upload_info)],
        state_dict['FILE_UPLOAD']: [MessageHandler(Filters.video | Filters.audio | Filters.voice, upload.parse_media_type)],
        state_dict['CLIP_INTERVAL'] : [MessageHandler(Filters.text, upload.get_clip_interval)]
    },
    fallbacks=[CommandHandler('cancel',upload.cancel)],
    allow_reentry=True
    )
    search_handler = InlineQueryHandler(select.search)
    dsp.add_handler(start_handler)
    dsp.add_handler(upload_handler)
    dsp.add_handler(search_handler)
    updater.start_polling()
    updater.idle()

if __name__=='__main__':
    main()
