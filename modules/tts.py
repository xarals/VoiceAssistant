import pyttsx3
from modules import config

def va_speak(what):
	print(f"BOT:  {what}")
	if not config.VA_VOICE:
		return
	engine = pyttsx3.init()
	ru_id = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_RU-RU_IRINA_11.0'
	engine.setProperty('voice', ru_id)
	engine.say(what)
	engine.runAndWait()