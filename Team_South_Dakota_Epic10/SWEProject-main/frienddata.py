import sqlite3 
from student_profile import *
def addfriend(use1, use2):
    conn = sqlite3.connect("incollege.db")
    f = conn.cursor()
    tablelist = f.execute("""SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'friends';""").fetchall()
    if tablelist == []:
        f.execute("""CREATE TABLE friends(user1 TEXT, user2 TEXT)""")
    f.execute("""INSERT INTO friends VALUES(?, ?)""", (use1, use2))
    f.execute("""INSERT INTO friends VALUES(?, ?)""", (use2, use1))
    # friendslist = f.execute('''SELECT * from pendfriends''')
    # # for i in friendslist:
    # #     print(i)
    conn.commit()
    conn.close()

def sendrequest(send, receive):
    conn = sqlite3.connect("incollege.db")
    f = conn.cursor()
    friends = []
    tablelist = f.execute("""SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'friends';""").fetchall()
    if tablelist != []:
        f.execute("""SELECT user1 FROM friends WHERE user1 = ? AND user2 = ?""", (send, receive))
        friends = f.fetchall()
    if friends == []:
        tablelist2 = f.execute("""SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'pendfriends';""").fetchall()
        if tablelist2 == []:
            f.execute("""CREATE TABLE pendfriends(sender TEXT, receiver TEXT)""")
        f.execute("""SELECT sender FROM pendfriends WHERE sender = ? AND receiver = ?""", (send, receive))
        req1 = f.fetchall()
        f.execute("""SELECT sender FROM pendfriends WHERE sender = ? AND receiver = ?""", (receive, send))
        req2 = f.fetchall()
        if req1 == [] and req2 == []:
            f.execute("""INSERT INTO pendfriends VALUES(?, ?)""", (send, receive))
        else:
            print("There is already a request between you 2")
        # friendslist = f.execute('''SELECT * from pendfriends''')
        # # for i in friendslist:
        # #     print(i)
    else:
        print("You are already friends.")
    conn.commit()
    conn.close()

def deleterequest(send, receive):
    conn = sqlite3.connect("incollege.db")
    f = conn.cursor()
    f.execute("""DELETE FROM pendfriends WHERE sender = ? AND receiver = ?""", (send, receive))
    # friendslist = f.execute('''SELECT * from pendfriends''')
    # for i in friendslist:
    #     print(i)
    conn.commit()
    conn.close()

def deletefriend(use1, use2):
    conn = sqlite3.connect("incollege.db")
    f = conn.cursor()
    f.execute("""DELETE FROM friends WHERE user1 = ? AND user2 = ?""", (use1, use2))
    f.execute("""DELETE FROM friends WHERE user1 = ? AND user2 = ?""", (use2, use1))
    # friendslist = f.execute('''SELECT * from friends''')
    # for i in friendslist:
    #     print(i)
    conn.commit()
    conn.close()

def showfriends(user):
    conn = sqlite3.connect("incollege.db")
    f = conn.cursor()
    tablelist = f.execute("""SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'friends';""").fetchall()
    if tablelist != []:
        f.execute("""SELECT user1 FROM friends WHERE user2 = ?""", (user,))
        friends = f.fetchall()
        n = 1
        
        if friends == []:
            print("No connections with anyone at this current time")
        else:
            print("Your friends:\n")
            for i in friends:
                print(str(n) + ". " + i[0])
                n = n + 1
            print("Would you like to delete a friend or view a profile?")
            opt = input("Enter 1 for delete 2 for view profile 3 for neither: ")
            if opt == '1':
                frien = input("Which friend would you like to delete: ")
                deletefriend(user, friends[int(frien)-1][0])
            if opt == '2':
                frien = input("Which profile would you like to view: ")
                while int(frien) > len(friends):
                    frien = input("Invalid option, select friend's number from list: ")
                display_profile(friends[int(frien)-1][0])
    else:
        print("No connections with anyone at this current time")
    conn.close()

def displayrequests(user):
    conn = sqlite3.connect("incollege.db")
    f = conn.cursor()
    tablelist = f.execute("""SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'pendfriends';""").fetchall()
    if tablelist != []:
        f.execute("""SELECT sender FROM pendfriends WHERE receiver = ?""", (user,))
        requestlist = f.fetchall()
        n = 1
        if requestlist == []:
            print("No requests at this current time")
        else:
            for i in requestlist:
                print(str(n) + ". " + i[0])
                n = n + 1
            print("Would you like to accept/reject one?")
            opt = input("Enter 1 for yes 2 for no: ")
            if opt == '1':
                frien = input("Enter number of request you would like: ")
                acc = input("1 for accept 2 for reject: ")
                if acc == '1':
                    addfriend(user, requestlist[int(frien)-1][0])
                    deleterequest(requestlist[int(frien)-1][0], user)
                elif acc == '2':
                    deleterequest(requestlist[int(frien)-1][0], user)
    else:
        print("No requests at this current time")
    
    conn.close()