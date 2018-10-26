import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
import cv2
import os
import sqlite3

model = keras.models.load_model('neutNetModel.h5')

outputPath = '../../NeutNuke/Backups/14dDoxYes/output'

slides = sorted([i for i in os.listdir(outputPath) if '.DS_Store' not in i], key=lambda x:10*int(x[1:][:-2])+int(x[-1]))

print(slides)

for slide in slides:
	conn = sqlite3.connect('{}/{}/outputDB_0.db'.format(outputPath, slide))
	c = conn.cursor()

	c.execute('''SELECT name FROM Cells WHERE acceptable=?;''', (True,))
	acceptables = c.fetchall()
	print(acceptables[0])
	
	#loadImage
	img = cv2.imread('{}/{}/{}/cell.png'.format(outputPath, slide, acceptables[0][0]))
	img = img.astype(np.uint8)
	grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	ret, cellThresh = cv2.threshold(grey, 200, 255, cv2.THRESH_BINARY_INV)
	img2, rawCellCon, hierarchy = cv2.findContours(cellThresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cellCon = sorted(rawCellCon, key=lambda x:-cv2.contourArea(x))
	x, y, width, height = cv2.boundingRect(cellCon[0])
	
	#cellManipulation
	cell = img[y:y+height, x:x+width]
	cellGrey = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)
	cellCol = cv2.cvtColor(cellGrey, cv2.COLOR_GRAY2BGR)
	cellCol = cv2.resize(cellCol, (64,64))

	z = model.predict(np.expand_dims(cellCol, axis=0), batch_size=None, verbose=1, steps=None)
	print(z)

	conn.close()






#model.fit(x_train)