import re
import os
import sys
import csv
import sqlite3


def in_students():
    fileTest = os.path.exists("studentAccounts.txt")
    
    if(fileTest == False):     #Checking if file exists
        return

    currentUsers = []

    db = open("studentAccounts.txt", "r")
    lines = db.readlines()
    db.close()

    testdb = open("Database.txt", "r")
    test = testdb.readlines()

    for user in test:
        if user != "":
            a, b, c, d, e, g, h, i, j = user.split(", ")        #gets all current usernames in database
        a = a.strip()
        currentUsers.append(a)

    testdb.close()

    db1 = open("Database.txt", "a")

    buffer = []
    index = 0

    length = len(test)          #Keeps track of current amount of accounts in database

    for line in lines:
        if line != "":
            if length == 10:
                return 
            elif index == 0:
                a, b, c = line.split(", ")
                a = a.strip()
                
                isIn = 0

                for user in currentUsers:
                    if(user == a):
                        isIn = 1            #skips current account from text file if already in system
                
                buffer.append(a)
                buffer.append(b)
                buffer.append(c[:-1])
                index += 1
            elif index == 1:
                buffer.append(line[:-1])
                index += 1
            elif index == 2:
                a, b, c = line.split(", ")
                buffer.append(a)
                buffer.append(b)
                buffer.append(c[:-1])
                index += 1
            elif index == 3:
                index = 0
                if(isIn != 1):
                    db1.write(buffer[0]+ ", " + buffer[3] + ", " + buffer[1] + ", " + buffer[2] + ", 1" + 
                    ", 1" + ", " + buffer[4] + ", " + buffer[5] + ", " + buffer[6] + "\n")
                length += 1
                buffer.clear()
    db1.close()

def in_jobs():
    db = open("newJobs.txt", "r")
    lines = db.readlines()
    db.close()
    currentJobList = []
    conn = sqlite3.connect('jobs.db')
    connect = conn.cursor()
    jobs = connect.execute("""SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'jobs';""").fetchall()
    rows_count = connect.execute("SELECT * FROM jobs")
    connect.execute("""SELECT * FROM jobs""")
    currentJobs = connect.fetchall()
    buffer = []
    for job_num in range(len(currentJobs)):
        if currentJobs[job_num] != []:
            currentJobList.append(currentJobs[job_num][0])  # gets all current usernames in database

    if len(rows_count.fetchall()) >= 10:
        print("No more Job creations possible.")
    index = 0
    isIn = 0
    for line in lines:
        for title in currentJobList:
            if title == line:
                isIn = 1
        if len(rows_count.fetchall()) >= 10:
            print("No more Job creations possible.")
        if line != "" and isIn != 1:
            # print(line)
            if index == 0:
                buffer.append(line)
                index += 1
            elif index == 1:
                buffer.append(line)
                index += 1
            elif index == 2:
                buffer.append(line)
                index += 1
            elif index == 3:
                buffer.append(line)
                index += 1
            elif index == 4:
                buffer.append(line)
                index += 1
            elif index == 5:
                buffer.append(line)
                index += 1
            elif index == 6:
                if isIn != 1:
                    connect.execute("""INSERT INTO jobs VALUES (?, ?, ?, ?, ?, ?)""",
                                    (buffer[0], buffer[1], buffer[3], buffer[4], buffer[5], buffer[2]))
                    conn.commit()
                    buffer.clear()
                    index = 0
                else:
                    buffer.clear()
                    index = 0

def out_profiles():
    conn = sqlite3.connect('profile.db')

    connect = conn.cursor()

    tablelist = connect.execute(
        """SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'profile';""").fetchall()
    if tablelist == []:
        return              #No database to fetch data from

    connect.execute("""SELECT * FROM profile""")

    data = connect.fetchall()

    db = open("MyCollege_profiles.txt", "w")

    if data == []:
        test = 0
    else:
        for x in data:
            db.write("Title: " + str(x[3]) + '\n')
            db.write("Major: " + str(x[4]) + '\n')
            db.write("University: " + str(x[5]) + '\n')
            db.write("Information: " + str(x[6]) + '\n')
            db.write("")
            db.write("First Job: " + str(x[7]) + '\n')
            db.write("First Job Employer: " + str(x[8]) + '\n')
            db.write("Starting Date: " + str(x[9])+ '\n')
            db.write("Ending Date: " + str(x[10]) + '\n')
            db.write("Location: " + str(x[11]) + '\n')
            db.write("Description About The Job: " + str(x[12]) + '\n')
            db.write("")
            db.write("Second Job: " + str(x[13]) + '\n')
            db.write("Second Job Employer: " + str(x[14]) + '\n')
            db.write("Starting Date: " + str(x[15]) + '\n')
            db.write("Ending Date: " + str(x[16]) + '\n')
            db.write("Location: " + str(x[17]) + '\n')
            db.write("Description About The Job: " + str(x[18]) + '\n')
            db.write("")
            db.write("Third Job: " + str(x[19]) + '\n')
            db.write("Third Job Employer: " + str(x[20]) + '\n')
            db.write("Starting Date: " + str(x[21]) + '\n')
            db.write("Ending Date: " + str(x[22]) + '\n')
            db.write("Location: " + str(x[23]) + '\n')
            db.write("Description About The Job: " + str(x[24]) + '\n')
            db.write("")
            db.write("School Name: " + str(x[25]) + '\n')
            db.write("Degree: " + str(x[26]) + '\n')
            db.write("Years: " + str(x[27]) + '\n')
            db.write("=====" + '\n')
    conn.close()
    db.close()


def out_jobs():
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()

    db = open("MyCollege_jobs.txt", "w")
    tablelist = c.execute(
        """SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'jobs';""").fetchall()
    if tablelist == []:
        test = 0
    else:
        c.execute("""SELECT * FROM jobs""")
        data = c.fetchall()

        if data == []:
            test = 0
        else:
            for x in data:
                db.write("Job title: " + x[0] + '\n')
                db.write("Job description: " + x[1] + '\n')
                db.write("Employer: " + x[2] + '\n')
                db.write("Location: " + x[3] + '\n')
                db.write("Salary: " + str(x[4]) + '\n')
                db.write("=====" + '\n')

    conn.commit()
    conn.close()
    db.close()


def out_users():
    db = open("Database.txt", "r")
    lines = db.readlines()
    db.close()
    db1 = open("MyCollege_users.txt", "w")
    for line in lines:
        if line != "":
            a, b, c, d, e, g, h, i, j = line.split(", ")
        j = j.strip()
        if j == '1':
            db1.write(a + ", " + "Standard" + "\n")
        elif j == '2':
            db1.write(a + ", " + "Plus" + "\n")
    db1.close()

def out_applied_jobs():
    conn = sqlite3.connect('jobs.db')
    connect = conn.cursor()
    outputfile = open("MyCollege_appliedJobs.txt", "w")
    applylist = connect.execute(
        """SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'applied';""").fetchall()
    if applylist == []:
        test = 0
    else:
        users = open("Database.txt", "r")
        lines = users.readlines()
        for line in lines:
            if line != "":
                a, b, c, d, e, g, h, i, j = line.split(", ")
            username = a.strip()
            if applylist != []:
                connect.execute("""SELECT * FROM applied WHERE username = ?""", (username,))
                data = connect.fetchall()
                if len(data) > 0:
                    for x in range(len(data)):
                        if data != []:
                            outputfile.write(str(data[x][0]) + "\n" + str(data[x][5]) + "\n" + str(data[x][4]) + "\n" + "=====" + "\n")
                        else:
                            test = 0
    conn.close()
    outputfile.close()

def out_saved_jobs():
    outputfile = open("MyCollege_savedJobs.txt", "w")
    conn = sqlite3.connect('saved_jobs.db')
    connect = conn.cursor()
    savelist = connect.execute(
        """SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'saved_jobs';""").fetchall()
    users = open("Database.txt", "r")
    lines = users.readlines()
    for line in lines:
        if line != "":
            a, b, c, d, e, g, h, i, j = line.split(", ")
        username = a.strip()
        outputfile.write(username + "\n")
        if savelist != []:
            connect.execute("""SELECT * FROM saved_jobs""")
            data = connect.fetchall()
            numIndices = len(data) - 1
            for x in range(numIndices):
                outputfile.write(str(data[x][0]) + "\n")
            outputfile.write("=====\n")
    conn.close()
    outputfile.close()
        