import keras
import keras.utils as image
import numpy as np
import cv2
import os
from PIL import Image

camera = True

last_message = ""

camera_model = keras.models.load_model('camera_emotion_model.h5')
text_model = keras.models.load_model("text_emotion_model")

with open("dictionary.txt", "r", encoding="utf-8") as f:
	dictionary = f.read().split("\n")
	f.close()

camera_emotion = ["злой", "отвращение", "напуган", "счастливый", "нейтральный", "грустный", "удивлен"]
text_emotion = ["грустный", "злой", "симпатия", "удивлен", "напуган", "счастливый"]

def camera_emotions():
	global camera
	try:
		cap = cv2.VideoCapture(0)
	except:
		camera = False
	if not camera:
		return -1
	for i in range(30):
		cap.read()
	ret, frame = cap.read()
	cv2.imwrite('cam.png', frame)
	img = cv2.imread('cam.png')
	gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	haar_cascade = cv2.CascadeClassifier('Haarcascade_frontalface_default.xml')
	faces_rect = haar_cascade.detectMultiScale(gray_img, 1.1, 9)
	for (x, y, w, h) in faces_rect:
		cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
		im = Image.open("cam.png")
		im_crop = im.crop((x, y, x+w, y+h))
		im_crop.save('cam.jpg', quality=100)
	if not os.path.exists("cam.jpg"):
		os.remove("cam.png")
		return -1
	img = image.load_img("cam.jpg",target_size = (48,48),color_mode = "grayscale")
	img = np.array(img) / 255
	img = np.expand_dims(img,axis = 0)
	img = img.reshape(1,48,48,1)
	result = camera_model.predict(img)
	result = list(result[0])
	index = np.argmax(result)
	os.remove("cam.png")
	os.remove("cam.jpg")
	return camera_emotion[index]

def correct_sentence(sentence):
	words = sentence.lower().replace("!", "").replace("?", "").replace(".", "").replace(",", "").split(" ")
	num_words = []
	for word in words:
		if word in dictionary:
			num_words.append(dictionary.index(word))
		else:
			num_words.append(0)
	while len(num_words) < 100:
		num_words.append(0)
	return num_words

def text_emotions():
	model_predict = text_model.predict(np.array([correct_sentence(last_message)]).astype("float32"))[0]
	index = np.argmax(model_predict)
	return text_emotion[index]