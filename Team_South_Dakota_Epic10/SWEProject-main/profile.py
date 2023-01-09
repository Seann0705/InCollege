import csv
def createprofile(username, pwd):
  print("Which part of the profile would you like to update?")
  print("1. Title")
  print("2. Major")
  print("3. University")
  print("4. About")
  print("5. Experience")
  print("6. Education")
  print("7. Exit")
  sel = input("Enter number: ")
  if sel == '1':
    title = input("Enter profile title: ")
  elif sel == '2':
    major = input("Enter major: ")
  elif sel == '3':
    univ = input("Enter university name: ")
  elif sel == '4':
    about = input("Enter information about yourself: ")