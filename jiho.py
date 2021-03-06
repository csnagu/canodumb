# coding=utf-8
from os.path import join
from os import getcwd, environ
from pit import Pit
from time import sleep
from watson_developer_cloud import TextToSpeechV1
import datetime
import subprocess

def get_time(tts_id, tts_pass):
    text_to_speech = TextToSpeechV1(
        username=tts_id,
        password=tts_pass,
        x_watson_learning_opt_out=True)  # Optional flag

    now = datetime.datetime.now()
    time = str(now.hour) + '時' + str(now.minute) + '分になりました。'

    with open(join(getcwd(), '/home/pi/cron_scripts/canodumb/now.wav'), 'wb') as audio_file:
        audio_file.write(text_to_speech.synthesize(time, accept='audio/wav', voice="ja-JP_EmiVoice"))


if __name__ == '__main__':
    if not environ.get('EDITOR'):
        environ['EDITOR'] = 'vi'
    user_info = Pit.get('watson_tts', {'require': {
        'tts_id': '',
        'tts_pass': ''}})
    get_time(user_info['tts_id'], user_info['tts_pass'])

    command = 'aplay /home/pi/cron_scripts/canodumb/jihou.wav;aplay /home/pi/cron_scripts/canodumb/now.wav'
    subprocess.call(command, shell=True)
