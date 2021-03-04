import random

inventory = ['Sword']
#-------------------- COMBAT SYSTEM --------------------

print("You walk through the woods...")
print("The Battle has engaged!")

#PLAYER & ENEMY HEALTH
player_health = random.randint(10, 20)
text = ("Player health: ",player_health)
print(text)
enemy_health = random.randint(10, 15)
text = ("Enemy health: ",enemy_health)
print(text)

#PLAYER & ENEMY ATTACK
player_attack = random.randint(3, 6)
enemy_attack = random.randint(3, 6)

#METHOD: SPAWN ENEMY
def spawnEnemy():
	enemy = random.choice (['Bone Walker', 'Imp', 'Dark Phoenix', 'Shadow Soldier'])
	chance = random.randrange(1,3)
	if chance == 1:
		return enemy
	else:
		return "none"

def assignTreasure(enemy):
	if enemy == "Bone Walker":
		return "Bone Oil"
	elif enemy == "Imp":
		return "Hatchet"
	elif enemy == "Dark Phoenix":
		return "Blackened Wing"
	elif enemy == "Shadow Soldier":
		return "Shadow Helmet"
	else:
		return "nothing"

#CHANCE OF ENCOUNTERING ENEMY
enemy = spawnEnemy()
if enemy != "none":
	print(("You are attacked by a ",enemy))
	fightEnemy = True

#THE BATTLE
fighting = True
while (fighting):

	#CHOOSE ITEM FROM INVETORY
	print(("Invetory:", inventory))
	item = input("Choose an item from your invetory. >> ")
	if item in inventory:
		if item == 'Sword':
			player_attack = random.randint(3,8)
	else:
		print("That item is not in your invetory! Given penalty!")
		player_attack = random.randint(-5, 0)
	
	#PLAYER ATTACK
	print(("Player deals ", player_attack, " damage with ", item, "!"))
	enemy_health -= player_attack
	print(("Player health: ", player_health))
	print(("Enemy health: ", enemy_health))
	if enemy_health<= 0:
		break
		
	#ENEMY ATTACK
	print("The Enemy attacks!")
	print(("Enemy deals ", enemy_attack, " damage!"))
	player_health -= enemy_attack
	print(("Player health: ", player_health))
	print(("Enemy health: ", enemy_health))
	if player_health<= 0:
		break
 
 #THE BATTLE IS OVER
print("The battle is done...")
print(("Player health: ", player_health))
print(("Enemy health: ", enemy_health))

#COLLECT TREASURE
if player_health >0:
	print("You have won! choose an item to add to your invetory...")
	text = ("'Boar Meat' or ", assignTreasure(enemy), " >> ")
	item = input(text)
	if item == 'Bone Oil' or item == 'Hatchet' or 'Blackened Wing' or 'Shadow Helmet':
		inventory.append (item)
		print(("Inventory: ", inventory))
	else:
		print("You leave empty handed!")
