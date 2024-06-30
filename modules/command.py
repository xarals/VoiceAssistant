import datetime
import random
import webbrowser
import requests
from threading import Thread
from num2words import num2words
from modules import tts
from modules import config
from modules.music import Music
from modules import menu
from modules.play_chess import play
from modules.emotion import camera_emotions

music = Music(directory="music")

def ctime():
    now = datetime.datetime.now()
    time_h = num2words(now.hour, lang='ru')
    time_m = now.minute
    h = " часов "
    m = " минут "
    if now.hour == 1 or now.hour == 21:
        h = " час "
    elif now.hour == 2 or now.hour == 3 or now.hour == 4 or now.hour == 22 or now.hour == 23:
        h = " часа "
    if now.minute == 1 or now.minute == 21 or now.minute == 31 or now.minute == 41 or now.minute == 51:
        m = " минута "
    elif now.minute == 2 or now.minute == 22 or now.minute == 32 or now.minute == 42 or now.minute == 52 or now.minute == 3 or now.minute == 23 or now.minute == 33 or now.minute == 43 or now.minute == 53 or now.minute == 4 or now.minute == 24 or now.minute == 34 or now.minute == 44 or now.minute == 54:
        m = " минуты "
    if now.minute == 1:
        time_m = "одна"
    elif now.minute == 21:
        time_m = "двадцать одна"
    elif now.minute == 31:
        time_m = "тридцать одна"
    elif now.minute == 41:
        time_m = "сорок одна"
    elif now.minute == 51:
        time_m = "пятьдесят одна"
    elif now.minute == 2:
        time_m = "две"
    elif now.minute == 22:
        time_m = "двадцать две"
    elif now.minute == 32:
        time_m = "тридцать две"
    elif now.minute == 42:
        time_m = "сорок две"
    elif now.minute == 52:
        time_m = "пятьдесят две"
    else:
        time_m = num2words(now.minute, lang='ru')
    text = f"Сейчас {time_h} {h} {time_m} {m}"
    tts.va_speak(text)

def news():
    ans = ['Запускаю новости.', 'Включаю новости.', 'Выполняю ваш запрос.']
    tts.va_speak(random.choice(ans))
    webbrowser.open("https://www.ukr.net/")

def weather():
    try:
        appid = "ffbd8e5bc0af7229040f3dc0809d8ee6"
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                 params={'id': config.VA_CITY[1], 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        w = data['weather'][0]['description']
        text = f"Сейчас погода в городе {config.VA_CITY[0]} - {w}."
        tts.va_speak(text)
    except Exception as e:
        text = f"Не удалось узнать погоду в вашем городе."
        tts.va_speak(text)
        print("Exception (weather):", e)

def start_music():
    if music.play and music.pause:
        music.stop_songs()
    elif music.play:
        tts.va_speak("Музыка уже включена.")
        return
    ans = ['Запускаю музыку.', 'Включаю музыку.', 'Выполняю ваш запрос.']
    tts.va_speak(random.choice(ans))
    music.start_songs()

def stop_music():
    if not music.play:
        tts.va_speak("Музыка не включена.")
        return
    music.stop_songs()
    tts.va_speak("Музыка выключена.")

def pause_songs():
    if not music.play:
        tts.va_speak("Музыка не включена.")
        return
    elif music.pause:
        tts.va_speak("Музыка уже приостановлена.")
        return
    music.pause_songs()
    tts.va_speak("Музыка приостановлена.")

def continue_songs():
    if not music.play:
        tts.va_speak("Музыка не включена.")
        return
    elif not music.pause:
        return
    music.continue_songs()

def next_song():
    music.next_song()

def previous_song():
    music.previous_song()

def reduce_songs():
    music.reduce_songs()

def increase_songs():
    music.increase_songs()

def more_reduce_songs():
    music.more_reduce_songs()

def more_increase_songs():
    music.more_increase_songs()

def change_volume(volume):
    music.change_volume(volume)

def open_menu():
    th = Thread(target=menu.open_menu)
    th.start()

def play_chess(color):
    th = Thread(target=play, args=[color])
    th.start()

def emotions():
    emot = camera_emotions()
    if emot == -1:
        tts.va_speak("Не удалось считать эмоции.")
        return
    tts.va_speak(f"Ваши эмоции - {emot}.")

def voice():
    config.VA_VOICE = not config.VA_VOICE

def filter_cmd(raw_voice):
    cmd = raw_voice

    for x in config.VA_ALIAS:
        cmd = cmd.replace(x, "").strip()

    return cmd

def recognize_cmd(cmd):
    rc = ""
    for c, v in config.VA_CMD_LIST.items():
        for x in v:
            if cmd == x:
                rc = c
                return rc
    return rc