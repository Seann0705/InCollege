import pytest
import main
import frienddata
import student_profile
import notifs
import sqlite3
import mainAPIS


def test_outuserapi():
    db = open("Database.txt", "a")
    db.write("adamr12, Starwars*12, adam, rush, 1, 1, comp sci, usf, 1\n")
    db.close()
    mainAPIS.out_users()
    db = open("MyCollege_users.txt", "r")
    lines = db.readlines()
    a = lines[0].split(", ")
    assert a[0] == "adamr12"


def test_outjobapi():
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    tablelist = c.execute(
        """SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'jobs';""").fetchall()
    if tablelist == []:
        c.execute("""CREATE TABLE jobs (
                        title text,
                        description text,
                        employer text,
                        location text,
                        salary int,
                        username text
                        )""")
    c.execute(
        """INSERT INTO jobs VALUES ("carpenter", "do stuff", "me", "my house", 78, "adamr12")""")
    conn.commit()
    conn.close()
    mainAPIS.out_jobs()
    db = open("MyCollege_jobs.txt", "r")
    lines = db.readlines()
    assert lines[0] == "Job title: carpenter\n"


def test_instudentapi():
    db = open("studentAccounts.txt", "w")
    db.write("test, first, last\n")
    db.write("Test123!\n")
    db.write("comp sci, usf, 1\n")
    db.write("=====\n")
    db.write("test, first, last\n")
    db.write("Test123!\n")
    db.write("comp sci, usf, 1\n")
    db.write("=====\n")
    db.write("test, first, last\n")
    db.write("Test123!\n")
    db.write("comp sci, usf, 1\n")
    db.write("=====\n")
    db.write("test, first, last\n")
    db.write("Test123!\n")
    db.write("comp sci, usf, 1\n")
    db.write("=====\n")
    db.write("notadded, first, last\n")
    db.write("Test123!\n")
    db.write("comp sci, usf, 1\n")
    db.write("=====\n")
    db.close()
    db1 = open("Database.txt", "w")
    db1.write("adamr12, Starwars*12, adam, rush, 1, 1, comp sci, usf, 1\n")
    db1.write("Pleb12, jgjgjJ*123, adam, kgkkg, 1, 1, su, usf, 1\n")
    db1.write("Pleb123, jgjgjJ*123, adam, kgkkg, 1, 1, su, usf, 1\n")
    db1.write("ick12, jgjgjJ*123, adam, kgkkg, 1, 1, su, usf, 1\n")
    db1.write("noob12, jgjgjJ*123, adam, kgkkg, 1, 1, su, usf, 1\n")
    db1.write("person34, jgjgjJ*123, adam, kgkkg, 1, 1, su, usf, 1\n")
    db1.close()
    mainAPIS.in_students()
    db = open("Database.txt", "r")
    users = db.readlines()
    db.close()
    assert len(users) == 10


def test_injobapi():
    jobtest = open("newJobs.txt", "r")
    jobs = jobtest.readlines()
    jobtest.close()
    mainAPIS.in_jobs()
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute("""SELECT * FROM jobs WHERE title = ? AND description = ? AND employer = ? 
                AND location = ? AND salary = ? AND username = ?""", (jobs[0], jobs[1], jobs[3], jobs[4], jobs[5], jobs[2]))
    job = c.fetchall()
    conn.close()
    assert job != []


def test_outprofileapi():
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

    connect.execute("""INSERT INTO profile VALUES ("soumil", "soumil", "saxena", "student", "csc", "usf","sfsfsfs" , "swe1","emp1","dat1","date2","loc1","desc1",
                  "swe2","emp2","date3","date4","loc2","desc2","swe3","emp3","date5","date6","loc3","desc3","usf","csc","four")""")
    conn.commit()
    conn.close()
    mainAPIS.out_profiles()
    db = open("MyCollege_profiles.txt", "r")
    lines = db.readlines()
    assert lines[3] == "Information: sfsfsfs\n"


def test_outapplied():
    db1 = open("Database.txt", "w")
    db1.write("adamr12, Starwars*12, adam, rush, 1, 1, comp sci, usf, 1\n")
    db1.write("Pleb12, jgjgjJ*123, adam, kgkkg, 1, 1, su, usf, 1\n")
    db1.write("Pleb123, jgjgjJ*123, adam, kgkkg, 1, 1, su, usf, 1\n")
    db1.write("ick12, jgjgjJ*123, adam, kgkkg, 1, 1, su, usf, 1\n")
    db1.write("noob12, jgjgjJ*123, adam, kgkkg, 1, 1, su, usf, 1\n")
    db1.write("person34, jgjgjJ*123, adam, kgkkg, 1, 1, su, usf, 1\n")
    db1.close()

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
        """INSERT INTO applied VALUES ("swe1","google","34dec","today","sdsdsd","adamr12",0,2)""")
    conn2.commit()
    conn2.close()
    mainAPIS.out_applied_jobs()
    db = open("MyCollege_appliedJobs.txt", "r")
    lines = db.readlines()
    assert lines[5] == "adamr12\n"


def test_outsaved():
    db1 = open("Database.txt", "w")
    db1.write("adamr12, Starwars*12, adam, rush, 1, 1, comp sci, usf, 1\n")
    db1.write("Pleb12, jgjgjJ*123, adam, kgkkg, 1, 1, su, usf, 1\n")
    db1.write("Pleb123, jgjgjJ*123, adam, kgkkg, 1, 1, su, usf, 1\n")
    db1.write("ick12, jgjgjJ*123, adam, kgkkg, 1, 1, su, usf, 1\n")
    db1.write("noob12, jgjgjJ*123, adam, kgkkg, 1, 1, su, usf, 1\n")
    db1.write("person34, jgjgjJ*123, adam, kgkkg, 1, 1, su, usf, 1\n")
    db1.close()
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
    connect2.execute(
        """INSERT INTO saved_jobs VALUES ("swe1","description of swe1","google","seattle",50000,"adamr12")""")
    conn2.commit()
    conn2.close()
    mainAPIS.out_saved_jobs()
    db = open("MyCollege_savedJobs.txt", "r")
    lines = db.readlines()
    assert lines[0] == "adamr12\n"
