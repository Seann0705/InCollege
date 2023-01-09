import re
import os
import sys
import csv
import sqlite3
from pathlib import Path
from frienddata import displayrequests
from frienddata import showfriends
from frienddata import sendrequest
from student_profile import create_profile
from student_profile import display_profile
from notifs import checknotifs
from notifs import datetime_to_int
from notifs import newusers
from notifs import jobalert
from notifs import jobdelete
from datetime import datetime
from mainAPIS import out_users
from mainAPIS import out_jobs
from mainAPIS import out_profiles
from mainAPIS import in_students
from mainAPIS import out_applied_jobs
from mainAPIS import in_jobs
from mainAPIS import out_saved_jobs

def Merge(dict1, dict2):
    return (dict2.update(dict1))


def login():
    print("--------------Login---------------\n")
    db = open("Database.txt", "a")
    db.close()
    filesize = os.path.getsize("Database.txt")
    if filesize == 0:
        print("The file is empty: " + str(filesize))
        return
    # creating a username and password dictionary
    file = 'Database.txt'
    path = Path(file)
    if path.is_file():
        db = open("Database.txt", "r")
    else:
        print("No accounts created")
        main()
    u = []
    p = []
    f = []
    l = []
    for i in db:
        a = i.split(", ")
        user = a[0]
        pas = a[1]
        firs = a[2]
        las = a[3]
        u.append(user)
        p.append(pas)
        f.append(firs)
        l.append(las)
    data = dict(zip(u, p))
    name = dict(zip(f, l))
    # Merge(name, data)
    # print(data)
    username = input("Please Enter Your Username: ")
    password = input("Please Enter Your Password: ")

    # Login Access Check
    if username in data:
        if password == data[username]:
            print("Login Successful! ")
            db.close()
            LoginSuccess(username, password)
        else:
            print("Incorrect password. Try Again!\n")
            login()
    else:
        print("Incorrect username. Try Again:")
        login()


def LoginSuccess(username, password):
    while True:
        conn = sqlite3.connect('profile.db')
        connect = conn.cursor()
        tablelist = connect.execute(
        """SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'profile';""").fetchall()
        if tablelist == []:
            print("\nDon't forget to create a profile")
        else:
            connect.execute("""SELECT * FROM profile WHERE user = ?""", (username,))
            profiles = connect.fetchall()
            if profiles == []:
                print("\nDon't forget to create a profile")
        conn.close()
        checknotifs(username)
        print("\nPlease enter a number to select an option below: ")
        print("\n1. Search for a job or an internship")
        print("2. Find someone you know")
        print("3. Learn a new skill.")
        print("4. Useful links")
        print("5. Important links")
        print("6. Show my network")
        print("7. Show pending friend requests")
        print("8. Create/Edit your profile")
        print("9. View your profile")
        print("10. Messaging")
        print("11. Change tier")
        print("12. Logout\n")

        # if(pending_friend):
        # print("8. Pending Friend Request(s)")

        option = input("\nEnter a number: ")

        if option == '1':
            conn3 = sqlite3.connect('jobs.db')
            connect3 = conn3.cursor()
            connect3.execute(
                """SELECT * FROM notifications WHERE username=?""", (username, ))
            data = connect3.fetchall()
            for x in data:

                if x[1] == 1:
                    notifications(username, 1)
                    connect3.execute(
                        """UPDATE notifications SET employer = 0 WHERE username = ?""", (username,))
                    conn3.commit()
                conn3.close()
            job_search(username, password)

        elif option == '2':
            find_someone(username, password)

        elif option == '3':
            learn_a_skill(username, password)

        elif option == '4':
            useful_links_from_login(username, password)

        elif option == '5':
            imp_links(username, password)

        elif option == '6':
            show_network(username, password)

        elif option == '7':
            displayrequests(username)
            LoginSuccess(username, password)
        elif option == '8':
            create_profile(username)
            LoginSuccess(username, password)
        elif option == '9':
            display_profile(username)
            LoginSuccess(username, password)
        elif option == '10':
            # message
            message_prompt(username, password)
            pass
        elif option == '11':
            tier = input(
                "Enter 1 to downgrade to standard, 2 to upgrade to premium, or 3 to not change: ")
            while tier != '1' and tier != '2' and tier != '3':
                tier = input("Invalid input, enter 1, 2, or 3: ")
            if tier == '3':
                LoginSuccess(username, password)
            else:
                changetier(username, tier)
                LoginSuccess(username, password)
        elif option == '12':
            main()
            return

        elif option == 1 or option == 2 or option == 3:
            break
        else:
            print("Wrong input, try again\n")
            LoginSuccess(username, password)


def create_acc(name, pwd, first, last, major, university, tier):

    # password:
    check_pwd = 0
    check2 = 0
    check3 = 0
    check4 = 0
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')

    # password validation
    for x in pwd:

        # checking if it contains at least a capital letter
        if x >= 'A' and x <= 'Z':
            check2 = check2 + 1

        # checking if it contains at least a number
        if x.isnumeric():
            check3 = check3 + 1

    # checking if it meets the 2 conditions above
    if check2 and check3:
        check_pwd = check_pwd + 2

    # checking if it contains at least a special character
    if (regex.search(pwd) != None):
        check_pwd = check_pwd + 1

    # checking if the length is between 8 and 12
    if len(pwd) >= 8 and len(pwd) <= 12:
        check_pwd = check_pwd + 1

    # checking if the username already exists in the text file

# find_word = open('Database.txt', "r")
# check_name = False
# if name in find_word:
#     check_name = True

    check_name = False
    db = open("Database.txt", "r")
    u = []
    for i in db:
        a = i.split(", ")
        user = a[0]
        u.append(user)

    if name in u:
        check_name = True

    if (check_name == False) and (check_pwd == 4):

        append_ = open("Database.txt", "a")

        append_.write(name + ", " + pwd + ", " + first + ", " + last + ", 1" +
                      ", 1" + ", " + major + ", " + university + ", " + tier + "\n")
        # default alert notifications for account creation is 1 for ON
        # default language for account creation is 1 for english
        append_.close()

        print("")
        print("Your account has been successfully created.")
        print("")
        conn3 = sqlite3.connect('jobs.db')
        connect3 = conn3.cursor()
        applylist = connect3.execute(
            """SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'notifications';""").fetchall()
        if applylist == []:
            connect3.execute("""CREATE TABLE notifications (
                        username text,
                        employer int,
                        newuser int,
                        newjob int
                        )""")
        connect3.execute("""INSERT INTO notifications VALUES (?, 0, 0, 0)""", (name,))
        connect3.execute("""UPDATE notifications SET newuser = newuser + 1 WHERE NOT username = ?""", (name,))
        conn3.commit()
        conn3.close()

   
        #data = connect3.fetchall()

        # friendApp = open("FriendList.txt", "a")

        # friendApp.write(name + ", " + "\n")
        # default alert notifications for account creation is 1 for ON
        # default language for account creation is 1 for english
        # friendApp.close()
        out_users()

        LoginSuccess(name, pwd)
    else:
        print("")
        print("Please choose another username or password.")
        print(
            "Password must contain at least 1 capital letter, 1 number, and 1 special character with a size between 8 and 12 letters!\n"
        )
        username = input("Please Enter Your Username: ")
        password = input("Please Enter Your Password: ")
        first = input("Please Enter Your First Name: ")
        last = input("Please Enter Your Last Name: ")
        major = input("Please Enter Your Major: ")
        university = input("Please Enter your University: ")
        tier = input(
            "Enter 1 to sign up as standard or 2 to sign up as premium for $10 a month: ")
        while tier != '1' and tier != '2':
            tier = input("Invalid input, enter 1 or 2: ")
        create_acc(username, password, first, last, major, university, tier)


def changetier(username, tier):
    if tier == '1':
        print("Downgraded down to standard, you will no longer be charged")
    else:
        print("Upgraded to premium, you will be charged $10 a month")
    db = open("Database.txt", "r")
    lines = db.readlines()
    db.close()
    db1 = open("Database.txt", "w")
    for line in lines:
        if line != "":
            a, b, c, d, e, g, h, i, j = line.split(", ")
        if a != username:
            db1.write(a + ", " + b + ", " + c + ", " + d + ", " + e +
                      ", " + g + ", " + h + ", " + i + ", " + j)
        else:
            db1.write(a + ", " + b + ", " + c + ", " + d + ", " + e +
                      ", " + g + ", " + h + ", " + i + ", " + tier)


def guest_controls(username, password):
    print("Do you want text, email, and targetted advertising")
    print("features on or off")
    print("1. On")
    print("2. Off")
    alerts = input("Enter a number: ")
    if alerts == '1' or alerts == '2':
        db = open("Database.txt", "r")
        lines = db.readlines()
        db.close()
        db1 = open("Database.txt", "w")
        for line in lines:
            if line != "":
                a, b, c, d, e, g, h, i, j = line.split(", ")
            if a != username:
                db1.write(a + ", " + b + ", " + c + ", " + d + ", " + e +
                          ", " + g + ", " + h + ", " + i + ", " + j)
            else:
                db1.write(a + ", " + b + ", " + c + ", " + d + ", " + alerts +
                          ", " + g + ", " + h + ", " + i + ", " + j)
        db1.close()


def languages(username, password):
    print("Do you want to view the app in english or spanish")
    inp = input("Enter 1 for english 2 for spanish: ")
    if inp == '1' or inp == '2':
        db = open("Database.txt", "r")
        lines = db.readlines()
        db.close()
        db1 = open("Database.txt", "w")
        for line in lines:
            if line != "":
                a, b, c, d, e, g, h, i, j = line.split(", ")
            if a != username:
                db1.write(a + ", " + b + ", " + c + ", " + d + ", " + e +
                          ", " + g + ", " + h + ", " + i + ", " + j)
            else:
                if g == '1':
                    print("Your language was english")
                elif g == '2':
                    print("Your language was spanish")
                db1.write(a + ", " + b + ", " + c + ", " + d + ", " + e +
                          ", " + inp + ", " + h + ", " + i + ", " + j)
        # db1.write("")
        if inp == '1':
            print("Your current language is now english")
        elif inp == '2':
            print("Your current language is now spanish")
        db1.close()
        """
        db2 = open("Database.txt", "r")
        for i in db2:
          a = i.split(", ")
          lang = a[6]
        db2.close()
        if(lang == 1):
          print("Your language is now English")
        else:
          print("Your language is now Spanish")
        """


def imp_linksnolog():
    print("")
    print("Select a link to navigate to")
    print("1. Copyright Notice")
    print("2. About")
    print("3. Accessibility")
    print("4. User Agreement")
    print("5. Privacy Policy")
    print("6. Cookie Policy")
    print("7. Copyright Policy")
    print("8. Brand Policy")
    print("9. Go back")
    inp = input("Enter a number: ")
    if inp == '1':
        print(
            "\nPlease do not use our stuff without us knowing, and if you do we will get some money out of you. Potentially a sum of money of the large variety."
        )
    elif inp == '2':
        print(
            "\nIn College: Welcome to InCollege, the world's largest college student network with many users in many countries and territories worldwide."
        )
    elif inp == '3':
        print(
            "\nHere are some accessibilities to those that have visual, motor, auditory, and intellectual impairments."
        )
    elif inp == '4':
        print(
            "\nBy using our platform, you agree to share with us your personal information, address, date of birth, favorite color, your family's names, social security number, bank information, and several other details. We will be selling this information for lots of money, and we don't care about telling you about it right here. Who reads these things anyway."
        )
    elif inp == '5':
        print("")
        print("Select a link to navigate to")
        print("1. Guest Controls")
        val = input("Enter a number: ")
        if val == '1':
            print("You must be logged in to access Guest Controls.")
            imp_linksnolog()
        else:
            print("Invalid Input. Please try again.")
            imp_linksnolog()
    elif inp == '6':
        print(
            "\nOur policy on cookies is that you should bake them for 10-12 minutes or until golden brown."
        )
    elif inp == '7':
        print(
            "\nOur copyright policy identifies any action that utilizes intellectual property or content owned by InCollege as copyright infringement, and will be followed up on by our extensive, intimidating, and formidable legal team."
        )
    elif inp == '8':
        print(
            "\nThe InCollege brand policy is that we are InCollege, a platform for college students to interact and form professional connections."
        )
    elif inp == '9':
        main()
    imp_linksnolog()


def imp_links(username, password):
    print("")
    print("Select a link to navigate to")
    print("1. Copyright Notice")
    print("2. About")
    print("3. Accessibility")
    print("4. User Agreement")
    print("5. Privacy Policy")
    print("6. Cookie Policy")
    print("7. Copyright Policy")
    print("8. Brand Policy")
    print("9. Guest Controls")
    print("10. Languages")
    inp = input("Enter a number: ")
    if inp == '1':
        print(
            "Please do not use our stuff without us knowing, and if you do we will get some money out of you. Potentially a sum of money of the large variety."
        )
    elif inp == '2':
        print(
            "In College: Welcome to InCollege, the world's largest college student network with many users in many countries and territories worldwide."
        )
    elif inp == '3':
        print(
            "Here are some accessibilities to those that have visual, motor, auditory, and intellectual impairments."
        )
    elif inp == '4':
        print(
            "By using our platform, you agree to share with us your personal information, address, date of birth, favorite color, your family's names, social security number, bank information, and several other details. We will be selling this information for lots of money, and we don't care about telling you about it right here. Who reads these things anyway."
        )
    elif inp == '5':
        # do stuff
        guest = input("Go to guest controls? 1 for Yes 2 for No: ")
        if guest == '1':
            guest_controls(username, password)
        else:
            imp_links(username, password)
    elif inp == '6':
        print(
            "Our policy on cookies is that you should bake them for 10-12 minutes or until golden brown."
        )
    elif inp == '7':
        print(
            "Our copyright policy identifies any action that utilizes intellectual property or content owned by InCollege as copyright infringement, and will be followed up on by our extensive, intimidating, and formidable legal team."
        )
    elif inp == '8':
        print(
            "The InCollege brand policy is that we are InCollege, a platform for college students to interact and form professional connections."
        )
    elif inp == '9':
        guest_controls(username, password)
    elif inp == '10':
        languages(username, password)


def useful_links():
    print("")
    print("Select a link to navigate to")
    print("1. General Links")
    print("2. Browse InCollege")
    print("3. Business Solutions")
    print("4. Directories")
    print("5. To Go Back")
    value = input("Enter a number: ")
    if value == '1':
        general_links()
    elif value == '2':
        print("Under Construction.")
        useful_links()
    elif value == '3':
        print("Under Construction.")
        useful_links()
    elif value == '4':
        print("Under Construction.")
        useful_links()
    elif value == '5':
        main()
    else:
        print("Invalid Input. Please Try Again")
        useful_links()


def useful_links_from_login(username, password):
    print("")
    print("Select a link to navigate to")
    print("1. General Links")
    print("2. Browse InCollege")
    print("3. Business Solutions")
    print("4. Directories")
    print("5. To Go Back")
    value = input("Enter a number: ")
    if value == '1':
        general_links_from_login(username, password)
    elif value == '2':
        print("Under Construction.")
        useful_links_from_login(username, password)
    elif value == '3':
        print("Under Construction.")
        useful_links_from_login(username, password)
    elif value == '4':
        print("Under Construction.")
        useful_links_from_login(username, password)
    elif value == '5':
        LoginSuccess(username, password)
    else:
        print("Invalid Input. Please Try Again")
        useful_links_from_login(username, password)


def general_links():
    print("")
    print("Select a link to navigate to")
    print("1. Sign Up")
    print("2. Help Center")
    print("3. About")
    print("4. Press")
    print("5. Blog")
    print("6. Careers")
    print("7. Developers")
    print("8. To Go Back")
    value = input("Enter a number: ")
    if value == '1':
        db = open("Database.txt", "a")
        db = open("Database.txt", "r+")
        count = len(db.readlines())
        if count >= 10:
            print("No More account creations acceptable\n")
            general_links()
        else:
            username = input("Please Enter Your Username: ")
            pwd = input("Please Enter Your Password: ")
            first = input("Please Enter Your First Name: ")
            last = input("Please Enter Your Last Name: ")
            major = input("Please Enter Your Major: ")
            university = input("Please Enter your University: ")
            create_acc(username, pwd, first, last, major, university)
    elif value == '2':
        print("We're here to help.")
        general_links()
    elif value == '3':
        print(
            "In College: Welcome to InCollege, the world's largest college student network with many users in many countries and territories worldwide."
        )
        general_links()
    elif value == '4':
        print(
            "In College Pressroom: Stay on top of the latest news, updates, and reports"
        )
        general_links()
    elif value == '5':
        print("Under Construction.")
        general_links()
    elif value == '6':
        print("Under Construction.")
        general_links()
    elif value == '7':
        print("Under Construction.")
        general_links()
    elif value == '8':
        useful_links()
    else:
        print("Invalid Input. Please Try Again")
        general_links()


def general_links_from_login(username, password):
    print("")
    print("Select a link to navigate to")
    print("1. Help Center")
    print("2. About")
    print("3. Press")
    print("4. Blog")
    print("5. Careers")
    print("6. Developers")
    print("7. To Go Back")
    value = input("Enter a number: ")
    if value == '1':
        print("We're here to help.")
        general_links_from_login(username, password)
    elif value == '2':
        print(
            "In College: Welcome to InCollege, the world's largest college student network with many users in many countries and territories worldwide."
        )
        general_links_from_login(username, password)
    elif value == '3':
        print(
            "In College Pressroom: Stay on top of the latest news, updates, and reports"
        )
        general_links_from_login(username, password)
    elif value == '4':
        print("Under Construction.")
        general_links_from_login(username, password)
    elif value == '5':
        print("Under Construction.")
        general_links_from_login(username, password)
    elif value == '6':
        print("Under Construction.")
        general_links_from_login(username, password)
    elif value == '7':
        useful_links_from_login(username, password)
    else:
        print("Invalid Input. Please Try Again")
        general_links_from_login(username, password)


def addjob(username, password):

    conn = sqlite3.connect('jobs.db')
    connect = conn.cursor()

    tablelist = connect.execute(
        """SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'jobs';""").fetchall()
    if tablelist == []:
        connect.execute("""CREATE TABLE jobs (
                        title text,
                        description text,
                        employer text,
                        location text,
                        salary int,
                        username text
                        )""")

    rows_count = connect.execute("SELECT * FROM jobs")

    if len(rows_count.fetchall()) >= 10:
        print("No more Job creations possible.")
        job_search(username, password)
    else:
        title = input("Enter job title: ")
        description = input("Enter job description: ")
        employer = input("Enter employer name: ")
        location = input("Enter job location: ")
        salary = input("Enter salary: ")

        connect.execute("""INSERT INTO jobs VALUES (?, ?, ?, ?, ?, ?)""",
                        (title, description, employer, location, salary, username))

        connect.execute("""SELECT * FROM jobs""")
        # data = connect.fetchall()
        # print(data)

        conn.commit()
        connect.execute("""UPDATE notifications SET newjob = newjob + 1 WHERE NOT username = ?""", (username,))
        conn.commit()
        conn.close()  
        print("")
        out_jobs()
        job_search(username, password)


# Epic 6
def delete_job(username, password):

    #job_title = input("Enter a job title you want to delete: ")


    ##############
    conn = sqlite3.connect('jobs.db')
    connect = conn.cursor()

    tablelist = connect.execute(
        """SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'jobs';""").fetchall()
    if tablelist == []:
        connect.execute("""CREATE TABLE jobs (
                        title text,
                        description text,
                        employer text,
                        location text,
                        salary int,
                        username text
                        )""")

    connect.execute("""SELECT * FROM jobs WHERE username =?""", (username, ))
    data = connect.fetchall()
    i = 0
    if data == []:
        print("\nNo Jobs added by you!\n")
        job_search(username, password)
    else:
        print("\n-----------------------------Enter Title and Employer of the job to Delete-----------------------------\n")
        for x in data:
            print("")
            print("------Job " + str(i) + "-------")
            print("Job title: " + x[0])
            print("Job description: " + x[1])
            print("Employer: " + x[2])
            print("Location: " + x[3])
            print("Salary: " + str(x[4]))
            print("------------------")
            print("")
            i = i + 1

    job_title = input("Enter a job title you want to delete: ")
    for x in data:
        if job_title == x[0]:
            employer_title = input(
                "Enter the employer of "+job_title+" to delete: ")

    # applied
    conn2 = sqlite3.connect('jobs.db')
    connect2 = conn2.cursor()
    checklist = []
    appliedlist = connect2.execute(
        """SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'applied';""").fetchall()

    if appliedlist == []:

        check = 0
        for x in data:
            if job_title == x[0]:
                if employer_title == x[2]:
                    check = 1
                    break

        if check == 0:
            print("\nYou don't have this job uploaded in the list.\n")
            job_search(username, password)
        else:
            connect.execute(
                """DELETE from jobs WHERE title=? and employer=?""", (job_title, employer_title))
            conn.commit()
            connect.execute("""UPDATE applied SET to_be_deleted = 1 WHERE title = ?""", (job_title,))
            conn.commit()
            print("\nJob deleted successfully.\n")
            conn.close()
            out_jobs()
            job_search(username, password)
            return

    connect2.execute(
        """SELECT * FROM applied WHERE NOT username=?""", (username, ))
    data2 = connect2.fetchall()
    check = 0
    for x in data:
        if job_title == x[0]:
            if employer_title == x[2]:
                check = 1
                break

    if check == 0:
        print("\nYou don't have this job uploaded in the list.\n")
        job_search(username, password)
    else:
        connect.execute(
            """DELETE from jobs WHERE title=? and employer=?""", (job_title, employer_title))
        conn.commit()
        out_jobs()
        print("Job deleted")
        for x in data2:  # applied table
            if job_title == x[0]:
                if employer_title == x[1]:
                    checklist.append(x[5])
                    #connect2.execute(
                    #    """DELETE from applied WHERE title=? and employer=?""", (job_title, employer_title))
                    #conn2.commit()
                    connect2.execute("""UPDATE applied SET to_be_deleted = 1 WHERE title = ?""", (job_title,))
                    conn2.commit()
                    # Notifications
                    conn3 = sqlite3.connect('jobs.db')
                    connect3 = conn3.cursor()
                    templist = connect3.execute(
                        """SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'notifications';""").fetchall()
                    if templist == []:
                        connect3.execute("""CREATE TABLE notifications (
                                                            username text,
                                                            employer int
                                            )""")

                    connect3.execute(
                        """UPDATE notifications SET employer = 1 WHERE username = ?""", (x[5],))
                    conn3.commit()

                    conn3.close()
                    # print("\nJob deleted succesfully.\n")
        # deleting saved jobs
        conn4 = sqlite3.connect('saved_jobs.db')
        connect4 = conn4.cursor()

        saved_list = connect4.execute(
            """SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'saved_jobs';""").fetchall()
        if saved_list == []:
            connect4.execute("""CREATE TABLE saved_jobs (
                        title_save text,
                        description_save text,
                        employer_save text,
                        location_save text,
                        salary_save int,
                        username_save text
                        )""")

        connect4.execute(
            """SELECT * FROM saved_jobs""")
    # connect.execute("""SELECT * FROM saved_jobs""")
        data4 = connect4.fetchall()
        for x in data4:  # applied table
            if job_title == x[0]:
                if employer_title == x[2]:
                    connect4.execute(
                        """DELETE from saved_jobs WHERE title_save=? and employer_save=?""", (job_title, employer_title))
                    conn4.commit()

        conn4.close()


        job_search(username, password)

    conn2.commit()
    conn3.close()
    # check if a job is in the list


def notifications(username, inte):
    if inte == 1:
        print("\nA Job that you applied has been removed!!!!!\n")


def display_jobs(username, password):
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()

    tablelist = c.execute(
        """SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'jobs';""").fetchall()
    if tablelist == []:
        "There is no jobs in the system right now."
    else:
        c.execute("""SELECT * FROM jobs""")
        data = c.fetchall()
        i = 1

        if data == []:
            print("Thre is no jobs in the system right now.")
        else:
            print("\nAll jobs in our system right now: \n")
            for x in data:
                print("")
                print("Job " + str(i) + ":")
                print("Job title: " + x[0])
                print("Job description: " + x[1])
                print("Employer: " + x[2])
                print("Location: " + x[3])
                print("Salary: " + str(x[4]))
                i = i + 1

    conn.commit()
    conn.close()

    value = input(
        "\nEnter 1 to save a job, 2 to apply for a job, and 3 to exit: ")
    if value == '1':
        save_job(username, password)

    elif value == '2':
        apply_for_job(username, password)

    elif value == '3':
        job_search(username, password)
    else:
        display_jobs(username, password)


def save_job(username, password):

    job_title = input("Enter the title of the job you want to save: ")
    employer = input("Enter the employer's name: ")

    # getting data from jobs.db
    conn1 = sqlite3.connect('jobs.db')
    connect1 = conn1.cursor()

    tablelist = connect1.execute(
        """SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'jobs';""").fetchall()
    if tablelist == []:
        connect1.execute("""CREATE TABLE jobs (
                        title text,
                        description text,
                        employer text,
                        location text,
                        salary int,
                        username text
                        )""")

    connect1.execute(
        """SELECT * FROM jobs WHERE title=? AND employer =?""", (job_title, employer, ))
    data = connect1.fetchall()

    # print(data)
    if len(data) == 0:
        print("This job is not in the system. Make sure you input the exact job's title and employer's name\n")
        save_job(username, password)
    else:
        for x in data:
            path_title = x[0]
            path_description = x[1]
            path_employer = x[2]
            path_location = x[3]
            path_salary = x[4]
            path_username = x[5]

    conn1.commit()
    conn1.close()

    # saving a job part
    conn2 = sqlite3.connect('saved_jobs.db')
    connect2 = conn2.cursor()

    tablelist = connect2.execute(
        """SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'saved_jobs';""").fetchall()
    if tablelist == []:
        connect2.execute("""CREATE TABLE saved_jobs (
                        title_save text,
                        description_save text,
                        employer_save text,
                        location_save text,
                        salary_save int,
                        username_save text
                        )""")

    connect2.execute("""INSERT INTO saved_jobs VALUES (?, ?, ?, ?, ?, ?)""", (path_title,
                     path_description, path_employer, path_location, path_salary, path_username))

    connect2.execute("""SELECT * FROM saved_jobs""")
    # data2 = connect2.fetchall()

    print("\nJob saved successfully!\n")
    # print(data2)

    conn2.commit()
    conn2.close()

    out_saved_jobs()
    print("")
    job_search(username, password)

# MESSAGING


def message_prompt(username, password):
    conn = sqlite3.connect('jobs.db')
    connect = conn.cursor()

    tablelist = connect.execute(
        """SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'messaging';""").fetchall()
    if tablelist == []:
        connect.execute("""CREATE TABLE messaging (
                        sender text,
                        reciever text,
                        message text,
                        notif int
                        )""")
    connect.execute(
        """SELECT * FROM messaging WHERE reciever = ? AND notif = 1""", (username,))
    data1 = connect.fetchall()
    print("")
    print("You have "+str(len(data1))+" new messages\n")

    print("Enter from the Following\n ")
    print("1. Display All Messages")
    print("2. Send Message")
    print("3. Delete Message")
    print("4. Go back\n")

    option = input("Enter value: ")
    if option == '1':
        display_messages_recieved(username)
        message_prompt(username, password)
    elif option == '2':
        send_message(username, password)
    elif option == '3':
        delete_sent_message(username)
        message_prompt(username, password)
    elif option == '4':
        LoginSuccess(username, password)
    else:
        print("Wrong Input!! Enter again: ")
        message_prompt(username, password)


def send_message(username, password):
    conn = sqlite3.connect('jobs.db')
    connect = conn.cursor()

    tablelist = connect.execute(
        """SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'messaging';""").fetchall()
    if tablelist == []:
        connect.execute("""CREATE TABLE messaging (
                        sender text,
                        reciever text,
                        message text,
                        notif int
                        )""")

    # connect.execute(
       # """SELECT * FROM messaging WHERE username=?""", (username, ))
    # data = connect.fetchall()
    # conn.commit()
    #i = 1
    # if data == []:
    # print("There is no jobs in the system right now.\n")
    # job_search(username, password)
    # exit(0)
    db = open("Database.txt", "a")
    db.close()
    filesize = os.path.getsize("Database.txt")

    if filesize == 0:
        print("The file is empty: " + str(filesize))
        return
    # creating a username and password dictionary
    file = 'Database.txt'
    path = Path(file)
    if path.is_file():
        db = open("Database.txt", "r")
    else:
        print("No accounts created")
        main()
    u = []
    p = []
    f = []
    l = []
    t = []
    for i in db:
        a = i.split(", ")
        user = a[0]
        pas = a[1]
        firs = a[2]
        las = a[3]
        tier_tab = a[8]
        u.append(user)
        p.append(pas)
        f.append(firs)
        l.append(las)
        t.append(tier_tab)
    data = dict(zip(u, t))
    x = 0

    while (x != len(u)):
        if u[x] == username:
            temp = x
            tempx = int(t[x])
            if tempx == 1:
                # messaging for standard
                # messaging from friends
                conn2 = sqlite3.connect("incollege.db")
                connect2 = conn2.cursor()
                tablelist = connect2.execute(
                    """SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'friends';""").fetchall()
                if tablelist != []:
                    connect2.execute(
                        """SELECT user2 FROM friends WHERE user1 = ?""", (username,))
                    requestlist = connect2.fetchall()
                    i = 1
                    if requestlist == []:
                        print("\nNo Friends to send messages to\n")
                        LoginSuccess(username, password)
                    else:

                        for w in requestlist:
                            print("")
                            print(str(i) + ". " + w[0])
                            print("-------------")
                            print("")
                            i = i + 1
                        frien = input(
                            "Which friend would you like to send a message to, Enter the number: ")
                        recieverx = requestlist[0][int(frien)-1]
                        messagex = input(
                            "Enter the message you want to send: ")
                        connect.execute("""INSERT INTO messaging VALUES (?, ?,?,?)""", (
                            username, recieverx, messagex, 1))
                        conn.commit()

            if tempx == 2:
                # messaging for premiums
                j = 1
                for w in u:
                    if username != w:
                        print(str(j) + ". "+w)
                        j += 1

                frien = input(
                    "Which person would you like to send a message to, Enter the number: ")
                while True:
                    try:
                        frien = input(
                        "Which person would you like to send a message to, Enter the number: ")
                    except ValueError:
                        print("Enter number value for friend: ")
                        continue
                    else:
                        break
                receiverx = u[int(frien)-1]
                messagex = input(
                    "Enter the message you want to send: ")
                connect.execute("""INSERT INTO messaging VALUES (?, ?,?,?)""", (
                    username, receiverx, messagex, 1))
                conn.commit()

        x = x + 1

    conn.close()


def delete_sent_message(username):
    conn = sqlite3.connect('jobs.db')
    connect = conn.cursor()

    connect.execute(
        """SELECT * FROM messaging WHERE reciever = ?""", (username,))
    data = connect.fetchall()
    if data == []:
        print("empty list of messages")
    else:
        i = 1
        for x in data:
            print("")
            print("Message " + str(i))
            print("Sender: ", x[0])
            print("message: ", x[2])
            print("")
        connect.execute(
            """UPDATE messaging SET notif = 0 WHERE reciever = ?""", (username,))
        conn.commit()

        checker1 = input(
            "Enter the number of the message you would like to delete: ")
        connect.execute("""DELETE FROM messaging WHERE sender = ? AND reciever = ? AND message = ? """,
                        (data[int(checker1)-1][0], data[int(checker1)-1][1], data[int(checker1)-1][2]))
        conn.commit()
        print("Message deleted! ")


def delete_sent_message(username):
    pass


def display_messages_recieved(username):
    conn = sqlite3.connect('jobs.db')
    connect = conn.cursor()

    connect.execute(
        """SELECT * FROM messaging WHERE reciever = ?""", (username,))
    data = connect.fetchall()
    if data == []:
        print("empty list of messages")
    else:
        i = 1
        for x in data:
            print("")
            print("Message " + str(i))
            print("Sender: ", x[0])
            print("message: ", x[2])
            print("")
        connect.execute(
            """UPDATE messaging SET notif = 0 WHERE reciever = ?""", (username,))
        conn.commit()
        print("Would you like to delete a message or reply to a message")
        opt = input("Enter 1 for delete 2 for reply 3 for neither: ")
        if opt == '1':
            while True:
                try:
                    checker1 = int(input(
                        "Enter the number of the message you would like to delete: "))
                except ValueError:
                    print("Enter number value for message")
                    continue
                else:
                    break
            while (int(checker1) > len(data)):
                print("Invalid message number")
                while True:
                    try:
                        checker1 = int(input(
                            "Select the number of message to delete again: "))
                    except ValueError:
                        print("Enter valid integer")
                        continue
                    else:
                        break

            connect.execute("""DELETE FROM messaging WHERE sender = ? AND reciever = ? AND message = ? """,
                            (data[int(checker1)-1][0], data[int(checker1)-1][1], data[int(checker1)-1][2]))
            conn.commit()
            print("Message deleted! ")
        elif opt == '2':
            while True:
                try:
                    checker2 = int(input(
                        "Enter the number of the message you would like to reply to: "))
                except ValueError:
                    print("Enter number value for message")
                    continue
                else:
                    break
            while (int(checker2) > len(data)):
                print("Invalid message number")
                while True:
                    try:
                        checker2 = int(input(
                            "Select the number of message to reply to again: "))
                    except ValueError:
                        print("Enter valid integer")
                        continue
                    else:
                        break
            receiverx = data[int(checker2)-1][0]
            messagex = input("Enter the message: ")
            connect.execute("""INSERT INTO messaging VALUES (?, ?,?,?)""", (
                username, receiverx, messagex, 1))
            conn.commit()

    conn.close()

# END of MESSAGING


def display_saved_jobs(username, password):
    conn = sqlite3.connect('saved_jobs.db')
    c = conn.cursor()

    tablelist = c.execute(
        """SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'saved_jobs';""").fetchall()
    if tablelist == []:
        "\nYou haven't saved any jobs yet.\n"
    else:
        c.execute("""SELECT * FROM saved_jobs""")
        data = c.fetchall()
        i = 1

        if data == []:
            print("\nYou haven't saved any jobs yet.\n")
            job_search(username, password)
        else:
            print("\nAll job(s) you have saved: \n")
            for x in data:
                print("")
                print("-------Job " + str(i) + "--------")
                print("Job title: " + x[0])
                print("Job description: " + x[1])
                print("Employer: " + x[2])
                print("Location: " + x[3])
                print("Salary: " + str(x[4]))
                i = i + 1

    conn.commit()
    conn.close()

    value = input("\nDo you want to delete a job? \n1 for yes and 2 for no: ")
    if value == '1':
        delete_saved_job(username, password)

    elif value == '2':
        job_search(username, password)
    else:
        display_saved_jobs(username, password)


def delete_saved_job(username, password):

    job_title = input("Enter the job's title you want to delete: ")

    conn = sqlite3.connect('saved_jobs.db')
    connect = conn.cursor()

    tablelist = connect.execute(
        """SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'saved_jobs';""").fetchall()
    if tablelist == []:
        connect.execute("""CREATE TABLE saved_jobs (
                        title_save text,
                        description_save text,
                        employer_save text,
                        location_save text,
                        salary_save int,
                        username_save text
                        )""")

    connect.execute(
        """SELECT * FROM saved_jobs WHERE username_save =?""", (username, ))
    # connect.execute("""SELECT * FROM saved_jobs""")
    data = connect.fetchall()

    # check if a job is in the list
    check = 0
    for x in data:
        if job_title == x[0]:
            check = 1
            break

    if check == 0:
        print("\nYou don't have this job saved in the list.\n")
        job_search(username, password)
    else:
        connect.execute(
            """DELETE from saved_jobs WHERE title_save=? and username_save=?""", (job_title, username))
        conn.commit()
        print("\nJob deleted succesfully.\n")

    out_saved_jobs()
    conn.close()
    job_search(username, password)


def apply_for_job(username, password):

    # job_title = input("Enter a job title you want to apply: ")
    conn = sqlite3.connect('jobs.db')
    connect = conn.cursor()

    tablelist = connect.execute(
        """SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'jobs';""").fetchall()
    if tablelist == []:
        connect.execute("""CREATE TABLE jobs (
                        title text,
                        description text,
                        employer text,
                        location text, 
                        salary int,
                        username text
                        )""")

    connect.execute(
        """SELECT * FROM jobs WHERE NOT username=?""", (username, ))
    data = connect.fetchall()
    conn.commit()
    i = 1
    if data == []:
        print("There is no jobs in the system right now.\n")
        job_search(username, password)
        exit(0)
    else:
        for x in data:
            print("")
            print("------Job " + str(i) + "-------")
            print("Job title: " + x[0])
            print("Job description: " + x[1])
            print("Employer: " + x[2])
            print("Location: " + x[3])
            print("Salary: " + str(x[4]))
            print("------------------")
            print("")
            i = i + 1
    conn2 = sqlite3.connect('jobs.db')
    connect2 = conn2.cursor()
    applylist = connect2.execute(
        """SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'applied';""").fetchall()
    if applylist == []:
        connect2.execute("""CREATE TABLE applied (
                        title text,
                        employer text,
                        graduation text,
                        start_date text,
                        coverletter text,
                        username text,
                        to_be_deleted int,
                        apply_date int
                        )""")
    connect2.execute(
        """SELECT * FROM applied WHERE username=?""", (username, ))
    applied_data = connect2.fetchall()
    jobtitle = input("Enter title of the job you want to apply for: ")
    for x in data:
        if jobtitle == x[0]:
            jobemployee = input("Enter Employer for " + jobtitle+": ")
            for y in applied_data:
                if y[0] == jobtitle:
                    if y[1] == jobemployee:
                        if y[5] == username:
                            print("You have already applied for this job")
                            job_search(username, password)
                            exit(0)

    for x in data:
        if jobtitle == x[0] and jobemployee == x[2]:
            print("")
            current_date = datetime_to_int(datetime.now())
            graduation_date = input("Enter you graduation date: ")
            startdate = input("Enter the date you can start working: ")
            coverletter = input(
                "Enter a short paragraph explaining why you deserve the job: ")
            connect2.execute("""INSERT INTO applied VALUES (?, ?, ?, ?, ?, ?, 0, ?)""", (
                jobtitle, jobemployee, graduation_date, startdate, coverletter, username, current_date))
            conn2.commit()
            connect2.execute("""SELECT * FROM applied""")
            print("\nApplied!!\n")

            conn2.close()

            job_search(username, password)
            exit(0)
    conn.close()
    conn2.close()
    out_applied_jobs()


def not_applied_display(username, password):
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    data_display = []
    appliedlist = c.execute(
        """SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'applied';""").fetchall()
    if appliedlist == []:
        print("You don't have any applied jobs in the list.")
        application_prompt(username, password)
    else:
        c.execute(
            """SELECT * FROM applied WHERE username=?""", (username, ))
        data1 = c.fetchall()
    conn.commit()
    conn2 = sqlite3.connect('jobs.db')
    c2 = conn2.cursor()

    joblist = c2.execute(
        """SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'jobs';""").fetchall()
    if joblist == []:
        print("No Jobs Available")
        application_prompt(username, password)
        exit()
    else:
        c2.execute(
            """SELECT * FROM jobs WHERE NOT username=?""", (username, ))
        data2 = c2.fetchall()
    conn2.commit()
    # print(data2)
    print("")
    # print(data1)
    i = 1
    for x in data2:
        title_jobtable = x[0]
        employee_jobtable = x[2]
        if data1 == []:
            print("")
            print("------Job " + str(i) + "-------")
            print("Job title: " + x[0])
            print("Job description: " + x[1])
            print("Employer: " + x[2])
            print("Location: " + x[3])
            print("Salary: " + str(x[4]))
            print("------------------")
            print("")
            i = i + 1
            z = 0
        else:
            for y in data1:
                title_applied = y[0]
                employee_applied = y[1]
                if title_jobtable != title_applied:
                    if employee_jobtable != employee_applied:
                        list1 = [x[0], x[1], x[2], x[3], str(x[4])]
                        data_display.append(list1)

    # removing same jobs
    new_list = []
    for x in data_display:
        if x not in new_list:
            new_list.append(x)

    for x in new_list:
        print("")
        print("------Job " + str(i) + "-------")
        print("Job title: " + x[0])
        print("Job description: " + x[1])
        print("Employer: " + x[2])
        print("Location: " + x[3])
        print("Salary: " + str(x[4]))
        print("------------------")
        print("")
        i = i + 1

    # print("\nnew list")
    # print(new_list)
    conn.close()
    conn2.close()
    application_prompt(username, password)

# End Epic 6

# End Epic 6


def application_prompt(username, password):
    print("Enter from the Following\n ")
    print("1. Apply for a Job")
    print("2. Show Applied Jobs")
    print("3. Show Jobs not applied yet")
    print("4. Go back\n")

    option = input("Enter value: ")
    if option == '1':
        apply_for_job(username, password)
    elif option == '2':
        applied_display(username, password)
    elif option == '3':
        not_applied_display(username, password)
    elif option == '4':
        job_search(username, password)
    else:
        print("Wrong Input!! Enter again: ")
        application_prompt(username, password)


def applied_display(username, password):
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()

    appliedlist = c.execute(
        """SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'applied';""").fetchall()
    if appliedlist == []:
        print("You don't have any applied jobs in the list.")
        application_prompt(username, password)
    else:
        c.execute(
            """SELECT * FROM applied WHERE username=?""", (username, ))
        data = c.fetchall()
        i = 1

        if data == []:
            print("You don't have any applied jobs in the list.")
        else:
            print("\nJob(s) you have applied:\n")
            for x in data:
                print("")
                print("------Job " + str(i) + "-------")
                print("Job title: " + x[0])
                print("Employer: " + x[1])
                print("Graduation Date: " + x[2])
                print("Start Date: " + x[3])
                print("Cover Letter " + x[4])
                print("-------------")
                print("")
                i = i + 1

    conn.commit()
    conn.close()
    application_prompt(username, password)


def job_search(username, password):
    conn3 = sqlite3.connect('jobs.db')
    connect3 = conn3.cursor()
    applylist = connect3.execute(
        """SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'applied';""").fetchall()
    apps = 0
    if (applylist != []):
        connect3.execute("""SELECT COUNT(*) from applied WHERE username = ?""", (username,))
        apps2 = connect3.fetchall()
        apps = apps2[0][0]
    print("You have currently applied for " + str(apps) + " job(s).")
    applylist = connect3.execute(
        """SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'notifications';""").fetchall()
    if applylist == []:
        connect3.execute("""CREATE TABLE notifications (
                        username text,
                        employer int
                        )""")
    connect3.execute(
        """SELECT employer FROM notifications WHERE username=?""", (username, ))
    data = connect3.fetchall()
    for x in data:

        if x == 1:
            notifications(username, 1)
            connect3.execute(
                """UPDATE notifications SET employer = 0 WHERE username = ?""", (username,))
            conn3.commit()
        conn3.close()

    job = input("Enter 1 to add a job\n      2 for Job Applications\n      3 to search for a job\n      4 to delete a job\n      5 to display all jobs\n      6 to display saved jobs\n      7 to go back: ")
    # job = int(jobx)
    if job == '1':
        addjob(username, password)
    elif job == '2':
        application_prompt(username, password)
    elif job == '3':
        searchjob(username, password)
    elif job == '4':
        delete_job(username, password)
    elif job == '5':
        display_jobs(username, password)
    elif job == '6':
        display_saved_jobs(username, password)
    elif job == '7':
        LoginSuccess(username, password)
    else:
        print("Wrong input, try again\n")
        job_search(username, password)


def searchjob(username, password):
    print("under construction")
    job_search(username, password)


def find_someone_notlogged():
    print("Enter first and last name of person you want to connect with")
    first = input("First Name: ")
    last = input("Last Name: ")
    db = open("Database.txt", "r")
    found = 0
    db = open("Database.txt", "r")
    u = []
    p = []
    f = []
    l = []
    for i in db:
        a, b, c, d, e, g, h, i, j = i.split(", ")
        b = b.strip()
        c = c.strip()
        d = d.strip()
        u.append(a)
        p.append(b)
        f.append(c)
        l.append(d)
    data1 = dict(zip(u, p))
    data2 = dict(zip(u, f))
    data3 = dict(zip(f, l))

    if first in data3:
        if last == data3[first]:
            found = 1
    if found == 1:
        print("This person is in the inCollege system, join them!")
        main()
    else:
        print("This person is not in the inCollege system")
    main()


def show_network(username, password):
    showfriends(username)
    LoginSuccess(username, password)


def find_someone(username, password):
    print("Please choose how you would like to search for a student:\n ")
    print("1. By Last name")
    print("2. By Major")
    print("3. By University\n")

    option = input("Enter value: ")

    found = 0  # change to 1 if user is found
    index = 1
    test = []

    """
    This code generates an empty array to store the usernames of users that match the criteria for each option (last name, major, university)
    In which after printing out all of the users that match the criteria of the search the user is prompted to choose which person they want to
    befriend if any. Then based on the number of the option they chose, the username stored within the array at the index of the number will be sent
    to the friend request function
    """
    db = open("Database.txt", "r")
    if option == '1':
        last = input("Last Name: ")
        print('\n')
        for i in db:
            a, b, c, d, e, g, h, j, k = i.split(", ")
            b = b.strip()
            c = c.strip()
            d = d.strip()
            if (d == last):
                found = 1
                if (a == username):
                    test.append(a)
                    print("Yourself" + ". " + c + " " + d)
                    index += 1
                else:
                    test.append(a)
                    print(str(index) + ". " + c + " " + d)
                    index += 1
        if (found == 1):
            print('\n')
            print("Would you like to send a friend request to any of these users?")
            print("1. Yes")
            print("2. No")
            sel = input("Enter choice: ")
            while sel != '1' and sel != '2':
                sel = input("Invalid choice, enter 1 or 2: ")
            if sel == '1':
                requestSelect = input(
                    "Type the number of the person would you like to befriend: ")
                sendrequest(username, test[int(requestSelect) - 1])
        else:
            print("User not found")

    elif option == '2':
        major = input("Major: ")
        print('\n')
        for i in db:
            a, b, c, d, e, g, h, j, k = i.split(", ")
            b = b.strip()
            c = c.strip()
            d = d.strip()
            e = e.strip()
            g = g.strip()
            h = h.strip()
            j = j.strip()
            k = k.strip()
            if (h == major):
                found = 1
                if (a == username):
                    test.append(a)
                    print("Yourself" + ". " + c + " " + d)
                    index += 1
                else:
                    test.append(a)
                    print(str(index) + ". " + c + " " + d)
                    index += 1
        if (found == 1):
            print('\n')
            print("Would you like to send a friend request to any of these users?")
            print("1. Yes")
            print("2. No")
            sel = input("Enter choice: ")
            while sel != '1' and sel != '2':
                sel = input("Invalid choice, enter 1 or 2: ")
            if sel == '1':
                requestSelect = input(
                    "Type the number of the person would you like to befriend: ")
                sendrequest(username, test[int(requestSelect) - 1])
        else:
            print("User not Found")

    elif option == '3':
        university = input("University: ")
        print('\n')
        for i in db:
            a, b, c, d, e, g, h, j, k = i.split(", ")
            b = b.strip()
            c = c.strip()
            d = d.strip()
            e = e.strip()
            g = g.strip()
            h = h.strip()
            j = j.strip()
            k = k.strip()
            if (j == university):
                found = 1
                if (a == username):
                    test.append(a)
                    print("Yourself" + ". " + c + " " + d)
                    index += 1
                else:
                    test.append(a)
                    print(str(index) + ". " + c + " " + d)
                    index += 1
        if (found == 1):
            print('\n')
            print("Would you like to send a friend request to any of these users?")
            print("1. Yes")
            print("2. No")
            sel = input("Enter choice: ")
            while sel != '1' and sel != '2':
                sel = input("Invalid choice, enter 1 or 2: ")
            if sel == '1':
                requestSelect = input(
                    "Type the number of the person would you like to befriend: ")
                sendrequest(username, test[int(requestSelect) - 1])
        else:
            print("User not found")

    # if found == 1:
    #   print(a)
    #   print("User found")
    #   print("Would you like to send a friend request to this user?")
    #   print("1. Yes")
    #   print("2. No")
    #   sel = input("Enter choice: ")
    #   while sel != '1' and sel != '2':
    #     sel = input("Invalid choice, enter 1 or 2: ")
    #   if sel == '1':
    #     sendrequest(username, a)
    # elif found == 0:
    #   print("User not found")
    # #first = input("First Name: ")
    # #last = input("Last Name: ")

    db.close()
    LoginSuccess(username, password)


def learn_a_skill(username, password):

    while True:
        print("\nPlease enter a number between 1 to 6: ")
        print("\n1. Python")
        print("2. Agile")
        print("3. HTML")
        print("4. PHP")
        print("5. JavaScript")
        print("6. Exit\n")

        skill_option = input("\nEnter here: ")

        if skill_option == '1':
            print("\nUnder construction!\n")
            learn_a_skill(username, password)
        elif skill_option == '2':
            print("\nUnder construction!\n")
            learn_a_skill(username, password)
        elif skill_option == '3':
            print("\nUnder construction!\n")
            learn_a_skill(username, password)
        elif skill_option == '4':
            print("\nUnder construction!\n")
            learn_a_skill(username, password)
        elif skill_option == '5':
            print("\nUnder construction!\n")
            learn_a_skill(username, password)
        elif skill_option == '6':
            LoginSuccess(username, password)
        else:
            print("Wrong input, try again: ")
            learn_a_skill(username, password)
       # if skill_option <= 6 and skill_option >= 1:
         #   break


def watchVideo():
    print("")
    print("Video is currently playing")
    print("")


# main:
def main():
    print("")
    print("-----------------------InCollege----------------------------")
    print("")
    print("Welcome to InCollege.")
    print("")
    print(
        "Meet Kyle. Kyle is a computer former computer science student at harvard university."
    )
    print(
        "He managed to use inCollege to find an internship after his sophomore year at google."
    )
    print(
        "He was very impressive at this internship and it helped him land a job with google when he finished his degree."
    )
    print("")

    #apis running at program start
    in_students()
    in_jobs()
    out_users()
    out_jobs()
    out_profiles()
    out_applied_jobs()
    out_saved_jobs()

    while True:
        # print(
        # "Please enter 1 to log in with an existing account\n             2 to create a new InCollege account\n             3 to watch a video on inCollege \n             4 to find a friend\n             5 to exit"
        # )
        print("Please enter")
        print("1 to log in with an existing account")
        print("2 to create a new InCollege account")
        print("3 to watch a video on inCollege")
        print("4 to find someone you know")
        print("5 to see useful links")
        print("6 to see inCollege important links")
        print("7 to exit")

        value = input("Enter a number: ")

        if value == '1':
            login()
            # if the password and username exist, it's logging in!

        elif value == '2':
            # Check whether the account limit has been exceeded or not
            db = open("Database.txt", "a")
            db = open("Database.txt", "r+")
            count = len(db.readlines())
            if count >= 10:
                print("No More account creations acceptable\n")
                main()
            else:
                username = input("Please Enter Your Username: ")
                password = input("Please Enter Your Password: ")
                first = input("Please Enter Your First Name: ")
                last = input("Please Enter Your Last Name: ")
                major = input("Please Enter Your Major: ")
                university = input("Please Enter your University: ")
                tier = input(
                    "Enter 1 to sign up as standard or 2 to sign up as premium for $10 a month: ")
                while tier != '1' and tier != '2':
                    tier = input("Invalid input, enter 1 or 2: ")
                create_acc(username, password, first,
                           last, major, university, tier)

        elif value == '3':
            watchVideo()
            main()
            return
        elif value == '4':
            find_someone_notlogged()
        elif value == '5':
            useful_links()
        elif value == '6':
            imp_linksnolog()
        elif value == '7':
            # return None
            sys.exit("Thank you for using InCollege")
        elif value == '1' or value == '2' or value == '3':
            break
        else:
            print("Incorrect Input: Try again\n")
            main()
            return None


def main2_without_findfriend():
    print("")
    print("-----------------------InCollege----------------------------")
    print("")
    print("Welcome to InCollege.")
    print("")
    print(
        "Meet Kyle. Kyle is a computer former computer science student at harvard university."
    )
    print(
        "He managed to use inCollege to find an internship after his sophomore year at google."
    )
    print(
        "He was very impressive at this internship and it helped him land a job with google when he finished his degree."
    )
    print("")

    #apis running at program start
    in_students()
    in_jobs()
    out_users()
    out_jobs()
    out_profiles()
    out_applied_jobs()
    out_saved_jobs()
    
    while True:
        print(
            "Please enter 1 to log in with an existing account\n             2 to create a new InCollege account\n             3 to watch a video on inCollege \n             4 to exit"
        )

        value = input("Enter a number: ")

        if value == '1':
            login()
            # if the password and username exist, it's logging in!

        elif value == '2':
            # Check whether the account limit has been exceeded or not
            db = open("Database.txt", "a")
            db = open("Database.txt", "r+")
            count = len(db.readlines())
            if count >= 10:
                print("No More account creations acceptable\n")
                main()
            else:
                username = input("Please Enter Your Username: ")
                password = input("Please Enter Your Password: ")
                first = input("Please Enter Your First Name: ")
                last = input("Please Enter Your Last Name: ")
                major = input("Please Enter Your Major: ")
                university = input("Please Enter your University: ")
                create_acc(username, password, first, last, major, university)

        elif value == '3':
            watchVideo()
            main()
        elif value == '4':
            sys.exit("Thank you for using InCollege\n")
        elif value == '1' or value == '2' or value == '3':
            break
        else:
            print("Incorrect Input: Try again\n")
            main()


# main()

if __name__ == "__main__":
    main()
