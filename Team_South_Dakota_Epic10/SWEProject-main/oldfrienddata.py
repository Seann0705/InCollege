import sqlite3
def createfriend(username):
  conn = sqlite3.connect("incollege.db")
  f = conn.cursor()
  tablelist = f.execute("""SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'friends';""").fetchall()
  blankspot = "NA"
  if tablelist == []:
    f.execute("""CREATE TABLE friends (
            user TEXT PRIMARY KEY,
            f1 TEXT,
            f2 TEXT,
            f3 TEXT,
            f4 TEXT,
            f5 TEXT,
            f6 TEXT,
            f7 TEXT,
            f8 TEXT,
            f9 TEXT
            )""")
  #f.execute("""INSERT INTO friends VALUES("{username}", 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA')""")
  #f.execute('INSERT INTO friends VALUES("{username}", "NA", "NA", "NA", "NA", "NA", "NA", "NA", "NA", "NA")')
  f.execute("""INSERT INTO friends VALUES(?, null, null, null, null, null, null, null, null, null)""", (username,))
  conn.commit()
  conn.close()

def creatependfriend(username):
  conn = sqlite3.connect("incollege.db")
  f = conn.cursor()
  tablelist = f.execute("""SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'pendfriends';""").fetchall()
  blankspot = "NA"
  if tablelist == []:
    f.execute("""CREATE TABLE pendfriends (
            user TEXT PRIMARY KEY,
            f1 TEXT,
            f2 TEXT,
            f3 TEXT,
            f4 TEXT,
            f5 TEXT,
            f6 TEXT,
            f7 TEXT,
            f8 TEXT,
            f9 TEXT
            )""")
    #f.execute("""CREATE TABLE pendfriends(user TEX")
  f.execute("""INSERT INTO pendfriends VALUES(?, null, null, null, null, null, null, null, null, null)""", (username,))
  conn.commit()
  conn.close()
#Just trying things out
#        user1  user2
#user1            2
#user2     0

def createfriend(username):
  conn = sqlite3.connect("incollege.db")
  f = conn.cursor()
  tablelist = f.execute("""SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'friendsys';""").fetchall()
  if tablelist == []:
    f.execute("""CREATE TABLE friendsys(user TEXT)""")
  f.execute("""ALTER TABLE friendsys ADD COLUMN """)
  f.execute("""INSERT INTO friendsys VALUES""")

  
def sendrequest(sender, receiver):
  conn = sqlite3.connect("incollege.db")
  f = conn.cursor()
  f.execute("""UPDATE pendfriends SET f1 = null WHERE user = "sdfafd";""")
  f.execute("""UPDATE pendfriends SET f1 = (CASE WHEN f1 IS null THEN ? ELSE f1 end), f2 = (CASE WHEN f2 IS null AND f1 IS NOT null THEN ? ELSE f2 END), f3 = (CASE WHEN f3 IS null AND f2 IS NOT null THEN ? ELSE f3 END), f4 = (CASE WHEN f4 IS null AND f3 IS NOT null THEN ? ELSE f4 END), f5 = (CASE WHEN f5 IS null AND f4 IS NOT null THEN ? ELSE f5 END), f6 = (CASE WHEN f6 IS null AND f5 IS NOT null THEN ? ELSE f6 END), f7 = (CASE WHEN f7 IS null AND f6 IS NOT null THEN ? ELSE f7 END), f8 = (CASE WHEN f8 IS null AND f7 IS NOT null THEN ? ELSE f8 END), f9 = (CASE WHEN f9 IS null AND f8 IS NOT null THEN ? ELSE f9 END) WHERE user = ?""", (sender, sender, sender, sender, sender, sender, sender, sender, sender, receiver))
  conn.commit()
  friendslist = f.execute('''SELECT * from pendfriends''')
  for i in friendslist:
    print(i)
  #conn.commit()
  conn.close()