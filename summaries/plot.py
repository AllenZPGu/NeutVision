import copy
import matplotlib
matplotlib.use('agg')
from matplotlib import pyplot as plt
import numpy as np
import os
import pandas as pd
import seaborn as sns
import scipy as sp
from scipy import signal
import sqlite3
import sys

# outputDir = sys.argv[1]
# outputDirDirs = os.listdir(sys.argv[1])

conn = sqlite3.connect('../DBFromServer/neutVision.sqlite3')
c = conn.cursor()

allScoresDict = {}
allShapeDict = {}
donutList = []

batches = ['D0#1', 'D0#2', 'D2#1', 'D2#2', 'D4#1', 'D4#2', 'D6#1', 'D6#2', 'D8#1', 'D8#2', 'D10#1', 'D10#2', 'D12#1', 'D12#2', 'D14#1', 'D14#2']
batches2 = ['D0', 'D2', 'D4', 'D6', 'D8', 'D10', 'D12', 'D14']

batchesDict = {i:{j:0 for j in ['Unsegmented', 'Segmented', 'Hypersegmented']} for i in batches}
batches2Dict = {i:{j:0 for j in ['Unsegmented', 'Segmented', 'Hypersegmented']} for i in batches2}
donutDict = {i:0 for i in batches2}

nDict = {i:0 for i in batches2}

for batch in batches:
	c.execute('''SELECT id FROM Images WHERE source=?;''', (batch,))
	cells = c.fetchall()

	for cell in cells:
		c.execute('''SELECT degree, shape FROM Scores WHERE img=? AND quality=?;''', (cell[0], 'Good: nucleus visible',))
		nucleiDegree = c.fetchall()
		if len(nucleiDegree) > 0:
			for i in nucleiDegree:
				if 'Other' not in i[0] and 'Unknown' not in i[0]:
					batchesDict[batch][i[0]] += 1
					batches2Dict[batch[:-2]][i[0]] += 1
					if i[1] == 'Donut':
						donutDict[batch[:-2]] += 1

c.close()
conn.close()

# #donuts
# ind = np.arange(16)    # the x locations for the groups
# width = 0.6       # the width of the bars: can also be len(x) sequence

# plt.figure(figsize=(14,8))

# pU = plt.bar(ind, donutList, width)
# plt.xlabel('Dox treatment day')
# plt.ylabel('Proportion of Donuts')
# plt.xticks(ind, batches)
# plt.yticks(np.arange(0, 1.2, 0.1))
# plt.legend((pU[0], pS[0], pH[0]), ('Unsegmented', 'Segmented', 'Hypersegmented'), bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
#        ncol=3, mode="expand", borderaxespad=0.)

# plt.savefig('replicates.png')

#replicates
totals = np.asarray([sum([batchesDict[i][j] for j in batchesDict[i]]) for i in batchesDict])
batchesLabel = ['{}\nn = {}'.format(batches[i], totals[i]) for i in range(len(batches))]
unsList = list(np.asarray([batchesDict[i]['Unsegmented'] for i in batchesDict])/totals)
segList = list(np.asarray([batchesDict[i]['Segmented'] for i in batchesDict])/totals)
hypList = list(np.asarray([batchesDict[i]['Hypersegmented'] for i in batchesDict])/totals)
hypBottom = list(np.asarray(unsList)+np.asarray(segList))

ind = np.arange(len(batches))    # the x locations for the groups
width = 0.6       # the width of the bars: can also be len(x) sequence

plt.figure(figsize=(14,8))

pU = plt.bar(ind, unsList, width)
pS = plt.bar(ind, segList, width, bottom=unsList)
pH = plt.bar(ind, hypList, width, bottom=hypBottom)

plt.xlabel('Dox treatment day')
plt.ylabel('Proportion')
plt.xticks(ind, batchesLabel)
plt.yticks(np.arange(0, 1.2, 0.1))
plt.legend((pU[0], pS[0], pH[0]), ('Unsegmented', 'Segmented', 'Hypersegmented'), bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
       ncol=3, mode="expand", borderaxespad=0.)

plt.savefig('replicates.png')
plt.close()

#pooled
totals2 = np.asarray([sum([batches2Dict[i][j] for j in batches2Dict[i]]) for i in batches2Dict])
batches2Label = ['{}\nn = {}'.format(batches2[i], totals2[i]) for i in range(len(batches2))]
unsList = list(np.asarray([batches2Dict[i]['Unsegmented'] for i in batches2Dict])/totals2)
segList = list(np.asarray([batches2Dict[i]['Segmented'] for i in batches2Dict])/totals2)
hypList = list(np.asarray([batches2Dict[i]['Hypersegmented'] for i in batches2Dict])/totals2)
print(unsList)
print(segList)
print(hypList)
hypBottom = list(np.asarray(unsList)+np.asarray(segList))

ind = np.arange(len(batches2))    # the x locations for the groups
width = 0.6       # the width of the bars: can also be len(x) sequence

plt.figure(figsize=(12,8))

pU = plt.bar(ind, unsList, width)
pS = plt.bar(ind, segList, width, bottom=unsList)
pH = plt.bar(ind, hypList, width, bottom=hypBottom)

plt.xlabel('Dox treatment day')
plt.ylabel('Proportion')
plt.xticks(ind, batches2Label)
plt.yticks(np.arange(0, 1.2, 0.1))
plt.legend((pU[0], pS[0], pH[0]), ('Unsegmented', 'Segmented', 'Hypersegmented'), bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
       ncol=3, mode="expand", borderaxespad=0.)

plt.savefig('pooled.png')
plt.close()

#donut
totals2 = np.asarray([sum([batches2Dict[i][j] for j in batches2Dict[i]]) for i in batches2Dict])
batches2Label = ['{}\nn = {}'.format(batches2[i], totals2[i]) for i in range(len(batches2))]
donutList = list(np.asarray([donutDict[i] for i in batches2])/totals2)

ind = np.arange(len(batches2))    # the x locations for the groups
width = 0.6       # the width of the bars: can also be len(x) sequence

plt.figure(figsize=(12,8))

pD = plt.bar(ind, donutList, width)
print(donutList)

plt.xlabel('Dox treatment day')
plt.ylabel('Donut proportion')
plt.xticks(ind, batches2Label)
plt.yticks(np.arange(0, 0.6, 0.05))

plt.savefig('donut.png')
plt.close()