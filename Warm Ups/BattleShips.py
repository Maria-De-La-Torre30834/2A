import random

print("                BATTLESHIP")
print("         Find the ships on the water!")
print("    Rows: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9")
print(" Columns: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9")
print("      There are 5 ships in the water")
print("          Choose your placement")
#SHIPS
carrier = ("C")
battleship = ("B")
cruiser = ("r")
submarine = ("s")
destroyer = ("d")

ships = [carrier, battleship, cruiser, submarine, destroyer]

def printGrid():
    for row in grid:
        for elem in row:
            print(elem + " ", end = " ")
        print()

grid = [
            ["*", "*", "*", "*", "*", "*", "*", "*", "*","*"],
            ["*", "*", "*", "*", "*", "*", "*", "*", "*","*"],
            ["*", "*", "*", "*", "*", "*", "*", "*", "*","*"],
            ["*", "*", "*", "*", "*", "*", "*", "*", "*","*"],
            ["*", "*", "*", "*", "*", "*", "*", "*", "*","*"],
            ["*", "*", "*", "*", "*", "*", "*", "*", "*","*"],
            ["*", "*", "*", "*", "*", "*", "*", "*", "*","*"],
            ["*", "*", "*", "*", "*", "*", "*", "*", "*","*"],
            ["*", "*", "*", "*", "*", "*", "*", "*", "*","*"],
            ["*", "*", "*", "*", "*", "*", "*", "*", "*","*"]
]
row = int(input("Enter row >> "))
col = int(input("Enter column >> "))
grid [row][col] = (carrier)

dir=input("Enter direction [r,l,u,d] >> ")
if dir == "r": # RIGHT
    for i in range(4):
        col += 1
        grid[row][col] = carrier
elif dir == "l": # LEFT
    for i in range(4):
        col += 1
        grid[row][col] = carrier
elif dir == "u": # UP
    for i in range(4):
        row += 1
        grid[row][col] = carrier
elif dir == "d": # DOWN
    for i in range(4):
        row += 1
        grid[row][col] = carrier

        
printGrid()

'''
#FIND THE SHIP
looking = True
while looking:
	gridRow = int(input("Enter Row >> "))
	gridCol = int(input("Enter Column >> "))
	if gridRow == row and gridCol == col:
		print ("You found it!")
		looking = False
	else:
		print("Keep guessing...")
	

for row in grid:
	print (row)
'''
