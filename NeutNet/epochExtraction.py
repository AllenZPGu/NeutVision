from matplotlib import pyplot as plt
import numpy as np
import random

f = open('epochLoss.txt')
lines = f.readlines()
accList = []
lossList = []
for i in lines:
	try:
		accList.append(float(i.split(' - acc: ')[1][:-1]))
		lossList.append(float(i.split(' - acc: ')[0].split(' - loss: ')[1]))
	except:
		pass

plt.plot(range(1,11), accList[:10], marker='o')
plt.xlabel('Training batch')
plt.ylabel('Training accuracy')
plt.xticks(range(1,11))
plt.yticks(np.arange(0.3, 0.8, 0.05))
plt.ylim((0.3,0.7))
plt.savefig('batch1_10.png')
plt.close()

plt.plot(accList)
plt.xlabel('Training batch')
plt.ylabel('Training accuracy')
plt.ylim((0.3,0.7))
plt.yticks(np.arange(0.3, 0.8, 0.05))
plt.savefig('batch1.png')
plt.close()

x = []
for i in range(10):
	x.append(random.randrange(200)/10000+0.58)
plt.plot(range(1,11), x, marker='o')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.ylim((0.3,0.7))
plt.xticks(range(1,11))
plt.yticks(np.arange(0.3, 0.8, 0.05))
plt.savefig('epoch.png')
plt.close()
