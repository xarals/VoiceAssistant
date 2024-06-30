import tkinter as tk
from threading import Thread
from tkinter import ttk
from modules import config
from modules import command
from modules import emotion

def open_menu():
	root = tk.Tk()
	root.geometry("800x600")
	root.title(f"Ассистент {config.VA_NAME}")

	label1 = tk.Label(root, text="Изменить имя ассистента: ")
	label1.grid(row=0, column=0)

	entry = tk.Entry(root)
	entry.grid(row=1, column=0)

	def button1_clicked():
		config.VA_NAME = entry.get()
		config.VA_ALIAS = entry.get().lower()
		config.update_file()
		root.title(f"Ассистент {config.VA_NAME}")

	button1 = tk.Button(root, text="Изменить имя", command=button1_clicked)
	button1.grid(row=2, column=0)

	label2 = tk.Label(root, text="", font=("Arial", 20))
	label2.grid(row=3, column=0)

	def button2_clicked():
		command.voice()
		if not config.VA_VOICE:
			button2.config(text="Включить звук ассистента")
		else:
			button2.config(text="Отключить звук ассистента")

	button2 = tk.Button(root, text="Отключить звук ассистента", width=25, command=button2_clicked)
	if not config.VA_VOICE:
	    button2.config(text="Включить звук ассистента")
	button2.grid(row=4, column=0)

	label3 = tk.Label(root, text="", font=("Arial", 20))
	label3.grid(row=5, column=0)

	def button3_clicked():
		th = Thread(target=command.ctime)
		th.start()

	button3 = tk.Button(root, text="Назвать время", width=25, command=button3_clicked)
	button3.grid(row=6, column=0)

	label4 = tk.Label(root, text="", font=("Arial", 20))
	label4.grid(row=5, column=0)

	def button4_clicked():
		th = Thread(target=command.news)
		th.start()

	button4 = tk.Button(root, text="Открыть новости", width=25, command=button4_clicked)
	button4.grid(row=6, column=0)

	label5 = tk.Label(root, text="", font=("Arial", 20))
	label5.grid(row=7, column=0)

	def button5_clicked():
		th = Thread(target=command.weather)
		th.start()

	button5 = tk.Button(root, text="Назвать погоду", width=25, command=button5_clicked)
	button5.grid(row=8, column=0)

	def button6_clicked():
		if not command.music.play:
			th = Thread(target=command.start_music)
			th.start()
			button6.config(text="Отключить музыку")
		else:
			th = Thread(target=command.stop_music)
			th.start()
			button6.config(text="Включить музыку")

	button6 = tk.Button(root, text="Включить музыку", width=25, command=button6_clicked)
	if command.music.play:
		button6.config(text="Отключить музыку")
	button6.grid(row=0, column=1)

	label5 = tk.Label(root, text="", font=("Arial", 20))
	label5.grid(row=1, column=1)

	def button7_clicked():
		if not command.music.play:
			return
		if not command.music.pause:
			th = Thread(target=command.pause_songs)
			th.start()
			button7.config(text="Продолжить музыку")
		else:
			th = Thread(target=command.continue_songs)
			th.start()
			button7.config(text="Приостановить музыку")

	button7 = tk.Button(root, text="Приостановить музыку", width=25, command=button7_clicked)
	if command.music.pause:
		button7.config(text="Продолжить музыку")
	button7.grid(row=2, column=1)

	label6 = tk.Label(root, text="", font=("Arial", 20))
	label6.grid(row=3, column=1)

	label7 = tk.Label(root, text="Громкость музыки: ")
	label7.grid(row=4, column=1)

	scale = tk.Scale(root, from_=0, to=100, length=230, width=10, orient=tk.HORIZONTAL)
	scale.set(int(command.music.volume * 100))
	scale.grid(row=5, column=1)

	def button8_clicked():
		value = scale.get() / 100
		command.change_volume(value)

	button8 = tk.Button(root, text="Применить", command=button8_clicked)
	button8.grid(row=6, column=1)

	label8 = tk.Label(root, text="", font=("Arial", 20))
	label8.grid(row=7, column=1)

	def button9_clicked():
		if not command.music.play:
			return
		th = Thread(target=command.next_song)
		th.start()

	button9 = tk.Button(root, text="Cледующуя музыка", width=25, command=button9_clicked)
	button9.grid(row=8, column=1)

	def button10_clicked():
		if not command.music.play:
			return
		th = Thread(target=command.previous_song)
		th.start()

	button10 = tk.Button(root, text="Предыдущая музыка", width=25, command=button10_clicked)
	button10.grid(row=9, column=1)


	label9 = tk.Label(root, text="Шахматы: ")
	label9.grid(row=10, column=0)

	def button11_clicked():
		command.play_chess(0)

	button11 = tk.Button(root, text="Играть за белых", width=25, command=button11_clicked)
	button11.grid(row=11, column=0)

	def button12_clicked():
		command.play_chess(1)

	button12 = tk.Button(root, text="Играть за черных", width=25, command=button12_clicked)
	button12.grid(row=12, column=0)

	label8 = tk.Label(root, text="", font=("Arial", 20))
	label8.grid(row=13, column=0)

	label10 = tk.Label(root, text="Ваши эмоции - ")
	label10.grid(row=14, column=0)

	def button13_clicked():
		emot = emotion.camera_emotions()
		label10.config(text=f'Ваши эмоции - {emot}.')

	button13 = tk.Button(root, text="Прочитать эмоции по камере", width=25, command=button13_clicked)
	button13.grid(row=15, column=0)

	def button14_clicked():
		emot = emotion.text_emotions()
		label10.config(text=f'Ваши эмоции - {emot}.')

	button14 = tk.Button(root, text="Прочитать эмоции по речи", width=25, command=button14_clicked)
	button14.grid(row=16, column=0)

	root.grid_columnconfigure(0, minsize=400)
	root.grid_columnconfigure(1, minsize=400)

	root.mainloop()
