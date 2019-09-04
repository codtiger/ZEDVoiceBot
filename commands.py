from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,ConversationHandler, InlineQueryHandler)
from telegram import (InlineQueryResultCachedVoice, ReplyKeyboardMarkup, ReplyKeyboardRemove,KeyboardButton)
from sqlalchemy import create_engine , or_
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import logging
import os

logging.basicConfig(level=logging.INFO)

logger=logging.Logger(name=__name__,level=logging.INFO)

def start(update,context):
   context.bot.send_message(chat_id=update.message.chat_id,text='Hello and welcome to the first ever ZEDVoiceBot,\
where you can send you favorite voices from our fellow friends\n, \
Long Live ZED!');

UPLOAD_INFO, FILE_UPLOAD = 0, 1

class Upload:

    def __init__(self,session_db,tables):
        self.sess = session_db
        self.upload_state = 0
        self.User,self.Voice = tables
        self.members_by_id = self.get_members()

    def __build_menu(self,buttons, n_rows, n_cols, header_buttons=None, footer_buttons=None):

        menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
        if header_buttons:
            menu.insert(0, [header_buttons])
        if footer_buttons:
            menu.append([footer_buttons])
        return menu
    
    def __reply_markup(self):
        button_list = []
        for i in self.members_by_id.keys():
            button_list.append(KeyboardButton(i))
        button_list = self.__build_menu(button_list,3,2)
        return ReplyKeyboardMarkup(button_list)
        
    def upload_info(self,update,context):
        if self.upload_state == 0:
            update.message.reply_text("Enter the owner of the voice(who recorded the goddman voice)",quote=True,
            reply_markup=self.__reply_markup(),one_time_keyboard=True)
            self.upload_state = 1
            return UPLOAD_INFO
        elif self.upload_state == 1:
            self.voice_owner = update.message.text
            self.owner_id = self.members_by_id[self.voice_owner]
            logger.info("voice_owner name is %s",self.voice_owner)
            update.message.reply_text("Enter the voice name you like to call",quote=True,reply_markup=ReplyKeyboardRemove())
            self.upload_state = 2
            return UPLOAD_INFO
        elif self.upload_state == 2:
            self.voice_name = update.message.text
            logger.info("voice name is %s",self.voice_name)
            update.message.reply_text("Enter the tags to ease the pain of searching",quote=True)
            self.upload_state = 3
            return UPLOAD_INFO
            
        elif self.upload_state == 3:
            self.tags = update.message.text
            update.message.reply_text("Now send me the voice",quote=True)
            logger.info("tags used for this voice are %s",self.tags)
            return FILE_UPLOAD
        
    def upload_audio(self,update,context):
        self.file_id = update.message.voice.file_id 
        self.sess.add(self.Voice(owner_id=self.owner_id, file_id=self.file_id, tags=self.tags,voice_name=self.voice_name))
        self.sess.commit()
        voice = update.message.voice.get_file()
        # voice.download(self.voice_name+'.ogg')
        update.message.reply_text("Thanks for your contribution to the ZEDVoice Directory,comrade")
        self.upload_state = 0
        return ConversationHandler.END

    def cancel(self,update,context):
        user = update.message.from_user
        logger.info("user %s cancelled the upload operation",user.first_name)
        update.message.reply_text("Upload operation cancelled by user:(")
        self.upload_state=0
        return ConversationHandler.END

    def get_members(self):
        return dict(self.sess.query(self.User.username,self.User.id).all())


class Search:
    def __init__(self,session_db,tables):
        self.sess = session_db
        self.User,self.Voice = tables
        # self.members_by_id = self.get_members()

    def search(self,update,context):
        query = update.inline_query.query
        # search_string = update.message.text
        results = []
        if (query != '' or query != None):
            result = self.sess.query(self.Voice).filter(or_(self.Voice.tags.like(query+u'%'),
            self.Voice.voice_name.like(query+u'%'))).all()
             
            for res in result:
                results.append(InlineQueryResultCachedVoice(id=res.voice_id, voice_file_id=res.file_id, title=res.voice_name))
            # results = [
            #     InlineQueryResultCachedVoice(id='0',voice_file_id='AwADBAADVgMAAmWq-FJkfcXcHoZodwI',title='کس لیسی میلاد')
            # ]
            update.inline_query.answer(results)

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

    start_handler = CommandHandler('start',start)
    upload_handler = ConversationHandler(entry_points=[CommandHandler('upload',upload.upload_info)],
    states={
        UPLOAD_INFO : [MessageHandler(Filters.text,upload.upload_info)],
        FILE_UPLOAD : [MessageHandler(Filters.voice,upload.upload_audio)]
    },
    fallbacks=[CommandHandler('cancel',upload.cancel)]

    )
    search_handler = InlineQueryHandler(select.search)
    dsp.add_handler(start_handler)
    dsp.add_handler(upload_handler)
    dsp.add_handler(search_handler)
    updater.start_polling()
    updater.idle()

if __name__=='__main__':
    main()
