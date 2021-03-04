import time

running = True
while running:
    #Create a program that measures seconds...
    print("Hit ENTER when you think 21 seconds has elapsed.")
    start = time.time()
    input(">> ")
    end = time.time()

    print("Number of seconds that elapsed:", int(end - start))
