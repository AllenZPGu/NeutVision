import cv2
import sqlite3
import numpy as np
import imutils
import os
import random

def dice():
	x = random.random()
	if x < 0.80:
		return 0
	elif x < 0.95:
		return 1
	else:
		return 2

try:
	os.mkdir('scoreCells')
except:
	pass

wordDict = {'Unsegmented':0, 'Segmented':1, 'Hypersegmented':2}

scoreFile = open('scoreCells/scores.txt', 'w+')

conn = sqlite3.connect('../DBFromServer/neutVision.sqlite3')
c = conn.cursor()

c.execute('''SELECT * FROM Scores;''')

acceptables = [i for i in c.fetchall() if 'Good' in i[1] and 'Unknown' not in i[2] and 'Other' not in i[2]]

n = 0
k = 0
for score in acceptables:
	#Finding scells
	c.execute('''SELECT * FROM Images WHERE id=?;''',(score[-3],))
	x = c.fetchone()
	imgPath = '{}/{}'.format(x[3],x[1])
	diffScore = wordDict[score[2]]
	if score[2] == 'Segmented':
		k+=24
	
	#loadImage
	img = cv2.imread('../NVapp/static/NVapp/cells/{}'.format(imgPath))
	grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	ret, cellThresh = cv2.threshold(grey, 200, 255, cv2.THRESH_BINARY_INV)
	img2, rawCellCon, hierarchy = cv2.findContours(cellThresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cellCon = sorted(rawCellCon, key=lambda x:-cv2.contourArea(x))
	x, y, width, height = cv2.boundingRect(cellCon[0])
	
	#cellManipulation
	cell = img[y:y+height, x:x+width]
	cellNegGrey = 255-cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)

	for angle in np.arange(0, 360, 30):
		rawRotatedCell = 255-imutils.rotate_bound(cellNegGrey, angle)

		ret, rotatedCellThresh = cv2.threshold(rawRotatedCell, 200, 255, cv2.THRESH_BINARY_INV)
		img2, rawCellConRotated, hierarchy = cv2.findContours(rotatedCellThresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		cellConRotated = sorted(rawCellConRotated, key=lambda x:-cv2.contourArea(x))
		x, y, width, height = cv2.boundingRect(cellConRotated[0])
	
		#cellManipulation

		rotatedCell = 255-cv2.resize(rawRotatedCell[y:y+height, x:x+width], (64, 64))
		cv2.imwrite('scoreCells/{}.jpg'.format(str(n)), rotatedCell)
		scoreFile.write('{}$$${}$$${}\n'.format(n, diffScore, dice()))
		n+=1

		flippedRotatedCell = cv2.flip(rotatedCell, 0)
		cv2.imwrite('scoreCells/{}.jpg'.format(str(n)), flippedRotatedCell)
		scoreFile.write('{}$$${}$$${}\n'.format(n, diffScore, dice()))
		n+=1

conn.close()
scoreFile.close()

print(k/n)