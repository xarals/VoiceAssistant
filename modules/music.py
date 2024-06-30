import os
import pygame
import time
from threading import Thread
from modules import tts

class Music:
	def __init__(self, directory):
		self.directory = directory
		self.play = False
		self.number = 0
		self.pause = False
		self.songs = None
		self.volume = 0.5
		self.get_songs()
		pygame.init()
	def get_songs(self):
		if not os.path.exists(self.directory):
			return
		songs_list = os.listdir(self.directory)
		for i in range(len(songs_list)):
			songs_list[i] = self.directory + "\\" + songs_list[i]
		self.songs = songs_list
	def __play_songs(self):
		self.get_songs()
		if len(self.songs) == 0:
			text = "В данный момент в папке нет музыки."
			tts.va_speak(text)
			return
		if self.number >= len(self.songs):
			self.number = 0
		while True:
			self.play = True
			self.pause = False
			try:
				pygame.mixer.music.load(self.songs[self.number])
			except:
				self.number += 1
				continue
			if self.number >= len(self.songs) - 1:
				self.number = 0
			pygame.mixer.music.set_volume(self.volume)
			pygame.mixer.music.play()
			while pygame.mixer.music.get_busy():
				time.sleep(2)
				if self.pause:
					while self.pause:
						pass
				if not self.play:
					pygame.mixer.music.stop()
					return
			self.number += 1
		self.play = False
	def start_songs(self):
		th = Thread(target=self.__play_songs)
		th.start()
	def stop_songs(self):
		pygame.mixer.music.stop()
		self.play = False
	def pause_songs(self):
		pygame.mixer.music.pause()
		self.pause = True
	def continue_songs(self):
		pygame.mixer.music.unpause()
		self.pause = False
	def next_song(self):
		self.number += 1
		self.stop_songs()
		th = Thread(target=self.__play_songs)
		th.start()
	def previous_song(self):
		self.number -= 1
		self.stop_songs()
		if self.number < 0:
			self.number = len(self.songs) - 1
		th = Thread(target=self.__play_songs)
		th.start()
	def reduce_songs(self):
		self.volume -= 0.2
		if self.volume < 0:
			self.volume = 0
		pygame.mixer.music.set_volume(self.volume)
	def increase_songs(self):
		self.volume += 0.2
		if self.volume > 1:
			self.volume = 1
		pygame.mixer.music.set_volume(self.volume)
	def more_reduce_songs(self):
		self.volume -= 0.5
		if self.volume < 0:
			self.volume = 0
		pygame.mixer.music.set_volume(self.volume)
	def more_increase_songs(self):
		self.volume += 0.5
		if self.volume > 1:
			self.volume = 1
		pygame.mixer.music.set_volume(self.volume)
	def change_volume(self, volume):
		self.volume = volume
		pygame.mixer.music.set_volume(self.volume)
