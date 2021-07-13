import subprocess
import shlex
import os
from pathlib import Path
from telegram.message import Video, Audio, Message
from telegram.files.file import File
from typing import Optional

from logging import getLogger

logger = getLogger(__name__)

    
def from_file_to_bytes(input_file: str, action :str="-f nut -vn -c:a libopus -ac 1", ss=None, to=None):
    command = f"ffmpeg -i {input_file} {action} -"

    if ss != None and to != None:
        command += f" -ss {ss} -to {to}"

    ffmpeg_cmd = subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.PIPE,
        shell=False
    )
    b = b''
    while True:
        output = ffmpeg_cmd.stdout.read()
        if len(output) > 0:
            b += output
        else:
            error_msg = ffmpeg_cmd.poll()
            if error_msg is not None:
                break
    return b

class Media(object):

    def __init__(self, media_type: Optional[str], message:Message):
        super.__init__()
        self._download_media(message, 'tmp_media/')

    def _download_media(self, message: Message, tmp_save_path: str):
        Path(tmp_save_path).mkdir(parents=True, exist_ok=True)
        self.media_file : File = message.get_file()
        if self.media_file.file_size > (100 * 1024 * 1024):
            logger.warning(f"File size too huge! {self.media_file.file_size / (1024 * 1024)} MBs")
        self.media_path = self.media_file.download(custom_path=tmp_save_path)
        
    def get_bytes(self, message:Message, start=None, end=None):
        return from_file_to_bytes(self.media_path, ss=start, to=end)

    def _download_video(self, message:Video):
        pass

    def _download_audio(self, message:Audio):
        pass