import os
import logging
from telegram import InlineQueryResultCachedVoice
from sqlalchemy import or_

logging = logging.getLogger(__name__)

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
            result = self.sess.query(self.Voice).filter(or_(self.Voice.tags.ilike(u'%'+ query +u'%'),
            self.Voice.voice_name.like(u'%' + query + u'%'))).limit(15).all()
             
            for res in result:
                results.append(InlineQueryResultCachedVoice(id=res.voice_id, voice_file_id=res.file_id, title=res.voice_name))
            # results = [
            #     InlineQueryResultCachedVoice(id='0',voice_file_id='AwADBAADVgMAAmWq-FJkfcXcHoZodwI',title='کس لیسی میلاد')
            # ]
            update.inline_query.answer(results)