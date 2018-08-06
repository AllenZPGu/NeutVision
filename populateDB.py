import os
import sqlite3

conn = sqlite3.connect('neutVision.sqlite3')
c = conn.cursor()

dayDirs = os.listdir('NVapp/static/NVapp/cells')

for dayDir in [i for i in dayDirs if '.DS_Store' not in i]:
	#day = 'Day '+dayDir[1:-1].replace('#','')
	cellDirs = os.listdir('NVapp/static/NVapp/cells/'+dayDir)
	for img in [j for j in cellDirs if '.DS_Store' not in j]:
		c.execute('SELECT * FROM Images WHERE name=? AND source=?;', (img,dayDir,))
		if c.fetchone() == None:
			c.execute('INSERT INTO Images (name, count, source) VALUES (?,?,?)', (img,0,dayDir,))
			print("Inserted %s"%img)
		else:
			print("%s already exists"%img)

conn.commit()
conn.close()