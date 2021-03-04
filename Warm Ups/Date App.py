def dateApp(day, month, year):
    if (month == "January" or month == "March" or month == "May" or month == "July" or month == "August" or month == "October" or month == "December"):
        if day>= 1 and day <= 31:
            print (str(day), month, year)
    elif (month == "April" or month == "June" or month == "September" or month == "November"):
        if day>= 1 and day <= 30:
            print (str(day), month, year)
    elif (month == ("February")):
          if day>= 1 and day <= 28:
            print (str(day), month, year)

day = int(input("Enter day>> "))
month = input("Enter month>> ")
year = input("Enter year>> ")

dateApp (day,month,year)

print(day,month,year)
