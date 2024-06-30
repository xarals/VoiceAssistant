from threading import Thread
from modules import command
from modules import neural
from modules import config
from modules import tts
from modules import stt
from modules.log import log
from modules import music
from modules import emotion

def va_respond(voice):
    if voice != "":
        print(f"User: {voice}")
        emotion.last_message = voice
    if voice.startswith(config.VA_ALIAS):
        cmd_n = command.filter_cmd(voice)
        cmd = command.recognize_cmd(cmd_n)
        if cmd not in config.VA_CMD_LIST.keys():
            execute_cmd(cmd_n)
        else:
            execute_cmd(cmd)

def execute_cmd(cmd):
    if cmd == 'ctime':
        command.ctime()
    elif cmd == 'news':
        command.news()
    elif cmd == 'weather':
        command.weather()
    elif cmd == "start_music":
        command.start_music()
    elif cmd == "stop_music":
        command.stop_music()
    elif cmd == "pause_songs":
        command.pause_songs()
    elif cmd == "continue_songs":
        command.continue_songs()
    elif cmd == "next_song":
        command.next_song()
    elif cmd == "previous_song":
        command.previous_song()
    elif cmd == "reduce_songs":
        command.reduce_songs()
    elif cmd == "increase_songs":
        command.increase_songs()
    elif cmd == "more_reduce_songs":
        command.more_reduce_songs()
    elif cmd == "more_increase_songs":
        command.more_increase_songs()
    elif cmd == "open_menu":
        command.open_menu()
    elif cmd == "play_chess":
        command.play_chess(0)
    elif cmd == "emotions":
        th = Thread(target=command.emotions)
        th.start()
    else:
        answer = neural.speak(cmd)
        try:
            log(cmd, answer)
        except:
            print("Logging error!")
        tts.va_speak(answer)

if __name__ == "__main__":
    print(f"Ассистент {config.VA_NAME} начала свою работу ...")
    command.open_menu()
    stt.va_listen(va_respond)
