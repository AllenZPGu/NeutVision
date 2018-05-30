import os
import sqlite3

conn = sqlite3.connect('neutVision.sqlite3')
c = conn.cursor()

cellDirs = os.listdir('NVapp/static/NVapp/cells')

for img in cellDirs:
	c.execute('SELECT * FROM Images WHERE name=?', (img,))

	if img == ".DS_Store":
		print("Skipped .DS_Store")
	elif c.fetchone() == None:
		c.execute('INSERT INTO Images (name, count) VALUES (?,?)', (img,0,))
		print("Inserted %s"%img)
	else:
		print("%s already exists"%img)

conn.commit()
conn.close()