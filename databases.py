import sqlite3

db = sqlite3.connect("albumtracker.sqlite")
tester = db.execute("SELECT * FROM albums")
print(tester)

test2 = []
cursor = db.cursor()
for each in tester:
    test2.append(each)
print(test2)

db.close()