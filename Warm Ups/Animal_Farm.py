def animalFarm(num, animal):
    if animal == "cow":
        sound = "moo "
    elif animal == "pig":
        sound = "oink "
    elif animal == "chicken":
        sound = "cluck "
    else:
        print ("I don't know that animal")
        sound = " " + input ("Enter new animal sound >> ")
    print (sound*num)

num = int (input("Number >> "))
animal = input ( "Animal >> ")

animalFarm (num, animal)
