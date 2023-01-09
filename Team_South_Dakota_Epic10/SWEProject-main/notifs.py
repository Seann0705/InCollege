import sqlite3
import os
import sys
from datetime import datetime

def checknotifs(username):
    # this function checks all notifications here
    newusers(username)
    jobalert(username)
    jobdelete(username)
    checklazy(username)

def newusers(username):
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute("""SELECT * FROM notifications WHERE username = ?""", (username,))
    newuse = c.fetchone()
    new_users = newuse[2]
    if new_users == 0:
        conn.close()
        return
    with open("Database.txt") as file:
        for line in (file.readlines() [-new_users:]):
            a = line.split(", ")
            print(a[2] + " " + a[3] + " has joined inCollege.")
    c.execute("""UPDATE notifications SET newuser = 0 WHERE username = ?""", (username, ))
    conn.commit()
    conn.close()

def jobalert(username):
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute("""SELECT * FROM notifications WHERE username = ?""", (username,))
    jobs = c.fetchall()
    for job in jobs:
        jobnots = job[3]
    if jobnots == 0:
        return
    else:
        print(str(jobnots) + " new job(s) have been posted.")
    c.execute("""UPDATE notifications SET newjob = 0 WHERE username = ?""", (username,))
    conn.commit()
    conn.close()

def jobdelete(username):
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    appliedlist = c.execute(
        """SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'applied';""").fetchall()
    if appliedlist == []:
        return
    else:
        c.execute("""SELECT * FROM applied WHERE username = ? AND to_be_deleted = 1""", (username,))
        outgoing_apps = c.fetchall()
        for apps in outgoing_apps:
            print("Job " + apps[0] + " has been deleted.")
        c.execute("""DELETE from applied WHERE username = ? AND to_be_deleted = 1""", (username,))
        conn.commit()
    conn.close()

def checklazy(username):
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    appliedList = c.execute(
        """SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'applied';""").fetchall()
    if appliedList == []:
        return
    else:
        c.execute("""SELECT apply_date FROM applied WHERE username = ?""", (username,))
        recent_apps = c.fetchall()
        if recent_apps == []:
            print("Remember – you're going to want to have a job when you graduate. Make sure that you start to apply for jobs today!")
            return
        current_date = datetime_to_int(datetime.now())
        most_recent = max(recent_apps)[0]
        if current_date - most_recent > 604799:
            print("Remember – you're going to want to have a job when you graduate. Make sure that you start to apply for jobs today!")
        
    conn.close()

def datetime_to_int(date):
    total = int(date.strftime('%S'))
    total += int(date.strftime('%M')) * 60
    total += int(date.strftime('%H')) * 60 * 60
    total += (int(date.strftime('%j')) - 1) * 60 * 60 * 24
    total += (int(date.strftime('%Y')) - 1970) * 60 * 60 * 24 * 365
    return total