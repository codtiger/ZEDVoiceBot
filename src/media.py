import subprocess
import shlex
import os
from pathlib import Path
from telegram.message import Video, Audio, Message
from telegram.files.file import File
from telegram.error import BadRequest
from typing import Optional

import logging

logger = logging.getLogger(__name__)

def from_file_to_ogg(input_file: str, action : str= "-vn -c:a libopus", ss=None, to=None):
    command = f"ffmpeg -i \'{input_file}\' {action}"

    if ss != None and to != None:
        command += f" -ss {ss} -to {to}"

    out_path = Path(input_file).stem + ".ogg"
    command += f" \'{out_path}\'"
    cmd_out = subprocess.run(command, shell=True).returncode
    return cmd_out, out_path

def from_file_to_bytes(input_file: str, action :str="-f nut -vn -c:a libopus -ac 1", ss=None, to=None):
    command = f"ffmpeg -i \'{input_file}\' {action}"

    if ss != None and to != None:
        command += f" -ss {ss} -to {to}"

    command += "  -"
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
        super().__init__()
        self.media_type = media_type
        self.ogg_voice = None
        self._download_media(message, 'tmp_media/')
        

    def _download_media(self, message: Message, tmp_save_path: str):
        Path(tmp_save_path).mkdir(parents=True, exist_ok=True)

        if self.media_type == 'Video':
            logger.info(f"Downloading Video {message.video.file_id}")
            self.media_file : File = message.video.get_file()
            self.media_name = message.video.file_name

        elif self.media_type == 'Audio':
            logger.info(f"Downloading Audio {message.audio.file_id}")
            self.media_file : File = message.audio.get_file()
            self.media_name = message.audio.file_name

        self.media_path = self.media_file.download(custom_path=Path(tmp_save_path) / Path(self.media_name))
        logger.info(self.media_path)

    def get_voice(self, message:Message, start=None, end=None):
        ret_code, self.ogg_voice = from_file_to_ogg(self.media_path, ss=start, to=end)
        os.remove(self.media_path)
        return ret_code, self.ogg_voice

    def _download_video(self, message:Video):
        pass

    def _download_audio(self, message:Audio):
        pass

    def __del__(self):
        if self.ogg_voice is not None:
            os.remove(self.ogg_voice)