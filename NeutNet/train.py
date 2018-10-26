import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
import cv2
import os

def tupify(max, no):
	x = [0]*max
	x[int(no)] = 1
	return x

model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=(64, 64, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

# model.add(Conv2D(64, (3, 3)))
# model.add(Activation('relu'))
# model.add(MaxPooling2D(pool_size=(2, 2)))
# model.add(Dropout(0.25))

# model.add(Conv2D(128, (3, 3)))
# model.add(Activation('relu'))
# model.add(MaxPooling2D(pool_size=(2, 2)))
# model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(3, activation='softmax'))

model.summary()

model.compile(loss='categorical_crossentropy', optimizer=keras.optimizers.SGD(lr=0.01, momentum=0.0, decay=0.0, nesterov=True), metrics=['accuracy'])

testing = True

#images = sorted([i for i in os.listdir('scoredCells') if i[-4:] == '.jpg'], key=lambda x:int(x[:-4]))
#imageArray = np.asarray([cv2.imread('scoredCells/'+i) for i in images])

scoreFile = open('scoreCells/scores.txt', 'r')
scoreInputArray = [x.replace('\n','').split('$$$') for x in scoreFile]
print('readingImages')

if not testing:
	trainArray = np.asarray([cv2.imread('scoreCells/'+i[0]+'.jpg')/255 for i in scoreInputArray if i[2]=='0'])
	print(trainArray.shape)
	trainScoreArray = np.asarray([tupify(3, i[1]) for i in scoreInputArray if i[2]=='0'])
	print(trainScoreArray.shape)

	testArray = np.asarray([cv2.imread('scoreCells/'+i[0]+'.jpg')/255 for i in scoreInputArray if i[2]=='1'])
	print(testArray.shape)
	testScoreArray = np.asarray([tupify(3, i[1]) for i in scoreInputArray if i[2]=='1'])
	print(testScoreArray.shape)

	evalArray = np.asarray([cv2.imread('scoreCells/'+i[0]+'.jpg')/255 for i in scoreInputArray if i[2]=='2'])
	print(evalArray.shape)
	evalScoreArray = np.asarray([tupify(3, i[1]) for i in scoreInputArray if i[2]=='2'])
	print(evalScoreArray.shape)

else:
	length = 500
	trainArray = np.asarray([cv2.imread('scoreCells/'+i[0]+'.jpg')/255 for i in scoreInputArray[:length] if i[2]=='0'])
	print(trainArray.shape)
	trainScoreArray = np.asarray([tupify(3, i[1]) for i in scoreInputArray[:length] if i[2]=='0'])
	print(trainScoreArray.shape)

	testArray = np.asarray([cv2.imread('scoreCells/'+i[0]+'.jpg')/255 for i in scoreInputArray[length:6*length] if i[2]=='1'])
	print(testArray.shape)
	testScoreArray = np.asarray([tupify(3, i[1]) for i in scoreInputArray[length:6*length] if i[2]=='1'])
	print(testScoreArray.shape)

	evalArray = np.asarray([cv2.imread('scoreCells/'+i[0]+'.jpg')/255 for i in scoreInputArray[6*length:20*length] if i[2]=='2'])
	print(evalArray.shape)
	evalScoreArray = np.asarray([tupify(3, i[1]) for i in scoreInputArray[6*length:20*length] if i[2]=='2'])
	print(evalScoreArray.shape)

model.fit(trainArray, trainScoreArray, batch_size=32, epochs=50, verbose=1,
		validation_data=(testArray, testScoreArray))

score = model.evaluate(evalArray, evalScoreArray, verbose=0)
print('Test loss: ', score[0])
print('Test accuracy: ', score[1])

if not testing:
	model.save('neutNetModel.h5')

#model.fit(x_train)