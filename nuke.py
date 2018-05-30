#!!!!!!WARNING DO NOT PRESS THIS
import sqlite3
print("WARNING!! Using this script will remove all image and scoring data. ")
x = input("Type 'I understand' to proceed. ")

if x == 'I understand':
	conn = sqlite3.connect('neutVision.sqlite3')
	c = conn.cursor()

	c.execute('DELETE FROM Images')
	c.execute('DELETE FROM Scores')
	c.execute('UPDATE sqlite_sequence SET seq=0 WHERE name=? OR name=?', ('Images','Scores',))

	conn.commit()
	conn.close()
	print("It is done.")
else:
	print("No dice.")