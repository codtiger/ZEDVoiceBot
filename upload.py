import re
from media import Media
import logging
from telegram.ext import ConversationHandler
from telegram import KeyboardButton, ReplyKeyboardMarkup , ReplyKeyboardRemove, Message

logger=logging.Logger(name=__name__)

state_dict = dict(UPLOAD_INFO=0, FILE_UPLOAD=1, CLIP_INTERVAL=2, DB_PROECSS=3)

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
        
    def upload_info(self, update, context):
        if self.upload_state == 0:
            update.message.reply_text("Enter the owner of the voice(who recorded the goddman voice)",quote=True,
            reply_markup=self.__reply_markup(),one_time_keyboard=True)
            self.upload_state = 1
            return state_dict['UPLOAD_INFO']

        elif self.upload_state == 1:
            self.voice_owner = update.message.text
            self.owner_id = self.members_by_id[self.voice_owner]
            logger.info("voice_owner name is %s",self.voice_owner)
            update.message.reply_text("Enter the voice name you like to call",quote=True,reply_markup=ReplyKeyboardRemove())
            self.upload_state = 2
            return state_dict['UPLOAD_INFO']

        elif self.upload_state == 2:
            self.voice_name = update.message.text
            logger.info("voice name is %s",self.voice_name)
            update.message.reply_text("Enter the tags to ease the pain of searching",quote=True)
            self.upload_state = 3
            return state_dict['UPLOAD_INFO']
            
        elif self.upload_state == 3:
            self.tags = update.message.text
            update.message.reply_text("Now send me the voice",quote=True)
            logger.info("tags used for this voice are %s",self.tags)
            return state_dict['FILE_UPLOAD']
            
    def parse_media_type(self, update, context):
        if update.message.voice:
            self.media_type = 'Voice'
            self.upload_media(update, context)

        elif update.message.video :
            self.media_type = 'Video'
            self.media = Media(self.media_type, update.message)
            update.message.reply_text("Enter the interval you want to clip \
             \n (format <start> - <end> like: 10-20 or 1:20 - 2:00 \n \
             If you do not want to clip write gibberish or -1 ")
            return state_dict['CLIP_INTERVAL']

        elif update.message.audio:
            self.media_type = 'Audio'
            self.media = Media(self.media_type, update.message)
            update.message.reply_text("Enter the interval you want to clip \
             \n (format <start> - <end> like: 10-20 or 1:20 - 2:00 \n \
             If you do not want to clip write gibberish or -1 ")

            return state_dict['CLIP_INTERVAL']
        else:
            logger.warn('Unsupported Media type at this stage')
            update.message.reply_text("Unsupported Media Type! Try again.")
            return state_dict['FILE_UPLOAD']

    def upload_media(self, update, context, start=None, end=None):
        if self.media_type == 'Voice': 
            voice_message = update.message

        elif self.media_type == 'Audio':
            byte_array = self.media.get_bytes(update.message, start=start, end=end)
            voice_message : Message = context.bot.send_voice(chat_id=update.message.chat_id, voice=byte_array)
        # May change the functions depending on audio or video. For now same 
        elif self.media_type == 'Video':
            byte_array = self.media.get_bytes(update.message, start=start, end=end)
            voice_message : Message = context.bot.send_voice(chat_id=update.message.chat_id, voice=byte_array)

        file_id = voice_message.voice.file_id

        self.sess.add(self.Voice(owner_id=self.owner_id, file_id=file_id, tags=self.tags,voice_name=self.voice_name))
        self.sess.commit()
        # voice = update.message.voice.get_file()
        # voice.download(self.voice_name+'.ogg')
        update.message.reply_text("Thanks for your contribution to the ZEDVoice Directory, comrade.")
        self.upload_state = 0
        return ConversationHandler.END

    def get_clip_interval(self, update, context):
        interval = update.message.text
        interval = re.sub(r'[\s+]', '', interval)
        re_text =  r'\d+:*\d*-\d+:*\d*'
        match = re.match(re_text, interval)

        if match and match.start() == 0 and match.end() == len(interval):
            hyphen = interval.find('-')
            start = interval[:hyphen]
            end = interval[hyphen + 1:]
        
        else:
            logger.info("Wrong Interval Format")
            start, end = None, None
        
        self.upload_media

    def cancel(self,update,context):
        user = update.message.from_user
        logger.info("user %s cancelled the upload operation",user.first_name)
        update.message.reply_text("Upload operation cancelled by user:(")
        self.upload_state=0
        return ConversationHandler.END

    def get_members(self):
        return dict(self.sess.query(self.User.username,self.User.id).all())
