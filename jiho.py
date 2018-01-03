# coding=utf-8
from __future__ import print_function
from os.path import join
from os import getcwd, environ
from watson_developer_cloud import TextToSpeechV1
import datetime
from time import sleep
import pyaudio
import wave
from pit import Pit

def get_time(tts_id, tts_pass):
    text_to_speech = TextToSpeechV1(
        username=tts_id,
        password=tts_pass,
        x_watson_learning_opt_out=True)  # Optional flag

    now = datetime.datetime.now()
    time = str(now.hour) + '時' + str(now.minute) + '分ごろをお知らせします。'

    with open(join(getcwd(), 'now.wav'), 'wb') as audio_file:
        audio_file.write(text_to_speech.synthesize(time, accept='audio/wav', voice="ja-JP_EmiVoice"))

def play_audio():
    buffer_size = 1024
    wf = wave.open('now.wav', 'rb')
    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    remain = wf.getnframes()
    while remain > 0:
        buf = wf.readframes(min(buffer_size, remain))
        stream.write(buf)
        remain -= buffer_size

    stream.close()
    p.terminate()
    wf.close()


if __name__ == '__main__':
    if not environ.get('EDITOR'):
        environ['EDITOR'] = 'vi'
    user_info = Pit.get('watson_tts', {'require': {
        'tts_id': '',
        'tts_pass': ''}})
    get_time(user_info['tts_id'], user_info['tts_pass'])
    sleep(2)
    play_audio()
