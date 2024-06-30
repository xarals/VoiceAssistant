import json

VA_NAME = "Ева"

VA_ALIAS = ("ева", "его", "дела", "дева")

VA_CMD_LIST = {
    "ctime": ["время", "текущее время", "сколько сейчас времени", "который час"],
	"news": ["новости", "покажи новости", "включи новости", "последние новости", "какие последние новости"],
	"weather": ["какая погода", "какая сегодня погода", "какая сейчас погода", "погода", "что за погода", "что сегодня за погода"],
	"start_music": ["включи музыку", "запусти музыку", "давай послушаем музыку", "вруби музыку"],
	"stop_music": ["выключи музыку", "выруби музыку", "стоп музыка", "стоп музыку", "останови музыку"],
	"pause_songs": ["приостанови музыку", "пауза музыки", "пауза музыка"],
	"continue_songs": ["продолжи музыку", "продолжай музыку"],
	"next_song": ["включи следующую музыку", "запусти следующую музыку", "давай послушаем следующую музыку", "вруби следующую музыку", "следующуя музыка", "следующую музыку", "некст музыка"],
	"previous_song": ["включи предыдущую музыку", "запусти предыдущую музыку", "давай послушаем предыдущую музыку", "вруби предыдущую музыку", "предыдущуя музыка", "предыдущую музыку"],
	"reduce_songs": ["тише", "потише", "тише музыку", "потише музыку", "сделай тише", "сделай потише", "сделай тише музыку", "сделай потише музыку"],
	"increase_songs": ["громче", "погромче", "громче музыку", "погромче музыку", "сделай громче", "сделай погромче", "сделай громче музыку", "сделай погромче музыку"],
	"more_reduce_songs": ["намного тише", "намного тише музыку", "сделай намного тише", "сделай намного тише музыку"],
	"more_increase_songs": ["намного громче", "намного громче музыку", "сделай намного громче", "сделай намного громче музыку"],
	"open_menu": ["меню", "открой меню", "главное меню"],
	"play_chess": ["шахматы", "поиграем в шахматы", "открой шахматы", "играть в шахматы", "запусти шахматы"],
	"emotions": ["эмоции", "какие эмоции", "считай эмоции", "прочитай эмоции"]
}

VA_CITY = ["Киев", 703448]

VA_VOICE = True

conf = None

try:
	with open('config.json', 'r', encoding='utf-8') as f:
		conf = json.load(f)
		f.close()
except:
	pass

if conf != None:
	try:
		VA_NAME = conf['VA_NAME']
	except:
		pass
	try:
		VA_ALIAS = conf['VA_ALIAS']
	except:
		pass
	try:
		VA_CMD_LIST = conf['VA_CMD_LIST']
	except:
		pass
	try:
		VA_CITY = conf['VA_CITY']
	except:
		pass
	try:
		VA_VOICE = conf['VA_VOICE']
	except:
		pass


def reload_cfg():
	global VA_NAME
	global VA_ALIAS
	global VA_CMD_LIST
	global VA_CITY
	global VA_VOICE
	conf = None
	try:
		with open('config.json', 'r', encoding='utf-8') as f:
			conf = json.load(f)
			f.close()
	except:
		return
	if conf != None:
		try:
			VA_NAME = conf['VA_NAME']
		except:
			pass
		try:
			VA_ALIAS = conf['VA_ALIAS']
		except:
			pass
		try:
			VA_CMD_LIST = conf['VA_CMD_LIST']
		except:
			pass
		try:
			VA_CITY = conf['VA_CITY']
		except:
			pass
		try:
			VA_VOICE = conf['VA_VOICE']
		except:
			pass

def update_file():
	text = "{\n"
	text += f"\"VA_NAME\": \"{VA_NAME}\",\n"
	text += f"\"VA_ALIAS\": \"{VA_ALIAS}\",\n"
	text += f"\"VA_CMD_LIST\": {VA_CMD_LIST},\n"
	text += f"\"VA_CITY\": {VA_CITY},\n"
	text += f"\"VA_VOICE\": {VA_VOICE}\n"
	text += "}"
	text = text.replace("\'", "\"")
	try:
		with open('config.json', 'w+', encoding='utf-8') as f:
			f.write(text)
			f.close()
	except:
		pass
