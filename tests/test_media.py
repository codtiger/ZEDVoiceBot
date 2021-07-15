import pytest
import os
import subprocess
import wave
import contextlib
from datetime import datetime

from src.media import from_file_to_bytes

@pytest.fixture(autouse=True)
def cleanup_directory():
    yield
    files = ["test.wav", "test.ogg"]
    for f in files:
        if os.path.exists(f):
            os.remove(f)

@pytest.fixture
def create_sine_audio(duration=10):
    return subprocess.run(['ffmpeg',  '-f',  'lavfi', '-i', f'sine=frequency=10:duration={duration}', 'test.wav']).returncode

def test_ffmpeg_installed():
    """ 
    Tests if ffmpeg is installed.
    """
    assert subprocess.call(['ffmpeg', '-h']) == 0
    
def test_ffmpeg_can_create_sine_audio(create_sine_audio):
    """
    Tests if ffmpeg can create sine audio.
    """
    assert create_sine_audio == 0
    assert os.path.exists("test.wav")
    with contextlib.closing(wave.open('test.wav','r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate * f.getnchannels())
    assert duration == 10.0

def test_conversion_to_ogg(create_sine_audio):
    """
    Tests if ffmpeg can create sine audio.
    """
    byte_array = from_file_to_bytes('test.wav', ss=7, to=10)
    assert isinstance(byte_array, bytes)
    with open('test.ogg', 'wb') as f:
        f.write(byte_array)
    out = subprocess.check_output("ffmpeg -i test.ogg 2>&1 | grep Duration | awk \'{print $2}\' | tr -d ,", shell=True)
    assert datetime.strptime(out.decode('ascii').strip(), "%H:%M:%S.%f").time().second == 3
    