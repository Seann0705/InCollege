from calendar import c
import sqlite3
from mainAPIS import out_profiles


# create a profile
# it will take first name and last name as parameters
def create_profile(username):

    conn = sqlite3.connect('profile.db')

    connect = conn.cursor()

    print("Whenever you want to quit and save please enter !q")

    proValues = {}
    startingDate2 = endingDate3 = years = jobEmployer1 = "None"
    firstname = lastname = title = major = university = information = jobTitle1 = jobEmployer1 = "None"
    startingDate1 = endingDate1 = location1 = description1 = jobTitle2 = jobEmployer2 = startingDate2 = startingDate2 = "None"
    endingDate2 = location2 = description2 = jobTitle3 = jobEmployer3 = startingDate3 = endingDate3 = "None"
    location3 = description3 = schoolName = degree = years = "None"

    firstname = input("Please enter first name: ")

    if firstname != "!q":  # all of these if statements are for to quit when the character is entered but it doesn't work yet
        proValues["firstname"] = firstname
        lastname = input("Please enter last name: ")

        if (lastname != "!q"):
            proValues["lastname"] = lastname
            title = input("Please enter your title: ")

            if (title != "!q"):
                proValues["title"] = title
                major = input("Please enter your major: ").title()

                if (major != "!q"):
                    proValues["major"] = major
                    university = input(
                        "Please enter your university name: ").title()

                    if (university != "!q"):
                        proValues["university"] = university
                        information = input(
                            "Please enter information about yourself:")

                        if (information != "!q"):
                            proValues["information"] = information
                            print("\nEnter your experience! \n")
                            jobTitle1 = input(
                                "Please enter your first past job: ")

                            if (jobTitle1 != "!q"):
                                proValues["jobTitle1"] = jobTitle1
                                jobEmployer1 = input(
                                    "Please enter your first past job employer: ")

                                if (jobEmployer1 != "!q"):
                                    proValues["jobEmployer1"] = jobEmployer1
                                    startingDate1 = input("Date started: ")

                                    if (startingDate1 != "!q"):
                                        proValues["startingDate1"] = startingDate1
                                        endingDate1 = input("Date ended: ")

                                        if (endingDate1 != "!q"):
                                            proValues["endingDate1"] = endingDate1
                                            location1 = input("Location: ")

                                            if (location1 != "!q"):
                                                proValues["location1"] = location1
                                                description1 = input(
                                                    "Enter description: ")

                                                if (description1 != "!q"):
                                                    proValues["description1"] = description1
                                                    jobTitle2 = input(
                                                        "Please enter your second past job: ")

                                                    if (jobTitle2 != "!q"):
                                                        proValues["jobTitle2"] = jobTitle2
                                                        jobEmployer2 = input(
                                                            "Please enter your Second past job employer: ")
                                                        if (jobEmployer2 != "!q"):
                                                            proValues["jobEmployer2"] = jobEmployer2
                                                            startingDate2 = input(
                                                                "Date started: ")

                                                            if (startingDate2 != "!q"):
                                                                proValues["startingDate2"] = startingDate2
                                                                endingDate2 = input(
                                                                    "Date ended: ")

                                                                if (endingDate2 != "!q"):
                                                                    proValues["endingDate2"] = endingDate2
                                                                    location2 = input(
                                                                        "Location: ")

                                                                    if (location2 != "!q"):
                                                                        proValues["location2 "] = location2
                                                                        description2 = input(
                                                                            "Enter description: ")

                                                                        if (description2 != "!q"):
                                                                            proValues["description2"] = description2
                                                                            jobTitle3 = input(
                                                                                "Please enter your third past job: ")

                                                                            if (jobTitle3 != "!q"):
                                                                                proValues["jobTitle3"] = jobTitle3
                                                                                jobEmployer3 = input(
                                                                                    "Please enter your Third past job employer: ")

                                                                                if (jobEmployer3 != "!q"):
                                                                                    proValues["jobEmployer3"] = jobEmployer3
                                                                                    startingDate3 = input(
                                                                                        "Date started: ")

                                                                                    if (startingDate3 != "!q"):
                                                                                        proValues["startingDate3"] = startingDate3
                                                                                        endingDate3 = input(
                                                                                            "Date ended: ")

                                                                                        if (endingDate3 != "!q"):
                                                                                            proValues["endingDate3"] = endingDate3
                                                                                            location3 = input(
                                                                                                "Location: ")

                                                                                            if (location3 != "!q"):
                                                                                                proValues["location3"] = location3
                                                                                                description3 = input(
                                                                                                    "Enter description: ")

                                                                                                if (description3 != "!q"):
                                                                                                    proValues["description3"] = description3
                                                                                                    print(
                                                                                                        "\nYour Education!\n")
                                                                                                    schoolName = input(
                                                                                                        "Enter your school name: ")

                                                                                                    if (schoolName != "!q"):
                                                                                                        proValues["schoolName"] = schoolName
                                                                                                        degree = input(
                                                                                                            "Enter your degree: ")

                                                                                                        if (degree != "!q"):
                                                                                                            proValues["degree"] = degree
                                                                                                            years = input(
                                                                                                                "Enter your years attended: ")
                                                                                                            proValues["years"] = years

    tablelist = connect.execute(
        """SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'profile';""").fetchall()
    if tablelist == []:
        connect.execute("""CREATE TABLE profile (
                    user text,
                    firstname text,
                    lastname text,
                    title text,
                    major text,
                    university text,
                    information text,
                    jobTitle1 text,
                    employer1 text,
                    startingDate1 text,
                    endingDate1 text,
                    location1 text,
                    description1 text,
                    jobTitle2 text,
                    employer2 text,
                    startingDate2 text,
                    endingDate2 text,
                    location2 text,
                    description2 text,
                    jobTitle3 text,
                    employer3 text,
                    startingDate3 text,
                    endingDate3 text,
                    location3 text,
                    description3 text,
                    schoolName text,
                    degree text,
                    years text

                    )""")

    connect.execute("""INSERT INTO profile VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (username, firstname, lastname, title, major, university, information, jobTitle1, jobEmployer1, startingDate1, endingDate1, location1, description1,
                     jobTitle2, jobEmployer2, startingDate2, endingDate2, location2, description2, jobTitle3, jobEmployer3, startingDate3, endingDate3,
                     location3, description3, schoolName, degree, years))

    # for i, j in proValues.items():
    #     connect.execute("""INSERT INTO profile(?) VALUES (?)""",          We are unable to make this work yet
    #     (i, j))

    # connect.execute("SELECT * FROM profile WHERE firstname_db = 'ABC' ")

    # print(connect.fetchall())

    conn.commit()

    conn.close()
    out_profiles()


# it may take first name or both first name and last name
def display_profile(username):

    # condition:
    # if they're friends, display below
    # if not, display nothing
    # if they're friends, but this person hasn't completed their profile, also display nothing

    # first_name = first_name.title()

    # new_firstname = (first_name,)
    conn = sqlite3.connect('profile.db')

    connect = conn.cursor()

    tablelist = connect.execute(
        """SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'profile';""").fetchall()
    if tablelist == []:
        connect.execute("""CREATE TABLE profile (
                    user text,
                    firstname text,
                    lastname text,
                    title text,
                    major text,
                    university text,
                    information text,
                    jobTitle1 text,
                    employer1 text,
                    startingDate1 text,
                    endingDate1 text,
                    location1 text,
                    description1 text,
                    jobTitle2 text,
                    employer2 text,
                    startingDate2 text,
                    endingDate2 text,
                    location2 text,
                    description2 text,
                    jobTitle3 text,
                    employer3 text,
                    startingDate3 text,
                    endingDate3 text,
                    location3 text,
                    description3 text,
                    schoolName text,
                    degree text,
                    years text

                    )""")

    connect.execute("""SELECT * FROM profile WHERE user =?""", (username, ))

    data = connect.fetchall()

    if data == []:
        print(username + " has no profile created.")
    else:
        for x in data:
            print("___________________________________")
            print("Name: " + x[1] + ' ' + x[2])
            print("")
            print("Title: " + x[3])
            print("Major: " + x[4])
            print("University: " + x[5])
            print("Information: " + x[6])
            print("")
            print("First Job: " + x[7])
            print("First Job Employer: " + x[8])
            print("Starting Date: " + x[9])
            print("Ending Date: " + x[10])
            print("Location: " + x[11])
            print("Description About The Job: " + x[12])
            print("")
            print("Second Job: " + x[13])
            print("Second Job Employer: " + x[14])
            print("Starting Date: " + x[15])
            print("Ending Date: " + x[16])
            print("Location: " + x[17])
            print("Description About The Job: " + x[18])
            print("")
            print("Third Job: " + x[19])
            print("Third Job Employer: " + x[20])
            print("Starting Date: " + x[21])
            print("Ending Date: " + x[22])
            print("Location: " + x[23])
            print("Description About The Job: " + x[24])
            print("")
            print("School Name: " + x[25])
            print("Degree: " + x[26])
            print("Years: " + x[27])
    conn.close()
