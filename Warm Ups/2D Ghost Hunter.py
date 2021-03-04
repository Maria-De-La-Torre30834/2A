print("        GHOST HUNT NOW IN 2D!")
print("  Find the ghost hiding in the forest!")
print("         There are 8 trees.")
print("           Rows: 0, 1, 2")
print("          Columns: 0, 1, 2")

#          0      1      2
forest = [
				["0,0", "0,1", "0,2"],       #INDEX 0
				["1,0", "1,1", "1,2"],       #INDEX 1
				["2,0", "2,1", "2,2"]        #INDEX 2
]
ghost = ("G")
guess = (row, col)

#FIND THE GHOST
looking = True
while looking:
	guess = int(input("Where is the ghost? >> "))
	if guess == ghost:
		print ("You found it!")
		looking = False
	else:
		print("Keep guessing...")

for row in forest:
	print (row)
