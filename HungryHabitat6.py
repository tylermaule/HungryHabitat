# -*- coding: utf-8 -*-
"""
Jai Ahuja, Lucas Napolitano, Tyler Maule
Created on Thu Nov 30 13:01:01 2017
@author: mauletj
"""

import random, pygame, time, sys
import matplotlib.pyplot as plt
import numpy as np

BOARD_W, BOARD_H = 20, 20
board = [[[] for x in range(BOARD_W)] for y in range(BOARD_H)]

characters = [] #stores all plant/predator/prey objects

#chance that a plant grows a new plant nearby
PLANT_REPRO = 0.01
#time between window updates
wait_time=0.01

prey_eat_chance=0.0 #chance to not get eaten
pred_repro=0.9 #chance to not reproduce
prey_repro=0.7 #chance to not reproduce

class Plant(object):
	"""
	A plant object/'character' that can be eaten by prey. Takes an x-pos,
	y-pos, and may generate new plant objects nearby upon update.
	"""
	def __init__(self,x,y):
		#initialize a plant object
		self.x=x
		self.y=y
		self.dead=False

	def update(self):
		"""
		Upon each timestep of the simulation, determines whether a plant has been eaten. If not,
		offers a chance for the plant to reproduce (create a new plant object) in a 2x2 radius
		"""
		if(self.dead):
			characters.remove(self)
			board[self.x][self.y].remove(self)
		if (random.randint(0,100) > 100 - (PLANT_REPRO * 100)):
			#randomly pick a location for new plant related to current plant
			plant_x = (self.x + random.randint(-2,2))%20
			plant_y = (self.y + random.randint(-2,2))%20

			#place new plant
			plant = Plant(plant_x,plant_y)
			board[plant_x][plant_y].append(plant)
			characters.append(plant)
		return

class Prey(object):
	"""
	A prey object/'character' that eats plants and can be eaten by prey. Takes
	an x-pos, y-pos, chance of reproduction and moves upon update.
	If on movement shares a space with another character, interacts with
	said character object.
	"""
	def __init__(self,x,y,repro):
		#initialize prey object
		#count is number of 'turns' remaining before 'death'
		self.count = 200
		self.x=x
		self.y=y
		self.repro=repro

	def update(self):
		"""
		Update the prey object's status (includes movement, reproduction, death)
		upon each timestep of the simulation
		"""
		#remove character from board prior to potential movement
		try:
			board[self.x][self.y].remove(self)
		except ValueError:
			return

		#character dies if food count has run to 0
		if (self.count <= 0):
			characters.remove(self)
			if(self in board[self.x][self.y]):
				board[self.x][self.y].remove(self)
			return

		#random movement, up/down/left/right/diagonal
		self.x = (self.x + random.randint(-1,1))%20
		self.y = (self.y + random.randint(-1,1))%20

		#check for, and respond to, character object collisions
		if (len(board[self.x][self.y]) > 0):
			for u in (board[self.x][self.y]):
				if type(u) == Predator:
					if(random.random() >prey_eat_chance):

					#prey character eaten
						characters.remove(self)
						u.count = 300

						return

				elif type(u) == Plant:
					#print('prey eat plant')

					#remove plant
					board[self.x][self.y].remove(u)
					characters.remove(u)

					#allow plants to regrow in same location
					plant_countdown = 25

					#update prey object
					self.count = 300
					board[self.x][self.y].append(self)

					return

				elif type(u) == Prey:

					#reproduction
					board[self.x][self.y].append(self)
					self.count -= 10

					if (random.random() > self.repro) and (self.count > 200):
						for a in range(0,random.randint(1,3)):
							child_x = (self.x + random.randint(-3,3)) % 20
							child_y = (self.y + random.randint(-3,3)) % 20
							child_prey = Prey(child_x,child_y,0.7)
							board[child_x][child_y].append(child_prey)
							characters.append(child_prey)

					return
		else:
			#no collisions
			board[self.x][self.y].append(self)
			self.count -= 1


class Predator(object):
	"""
	A predator object that moves, 'eats' the prey object, can reproduce if landing on another
	predator object, and will 'die' if not fed. 
	"""
	def __init__(self,x,y,repro):
				#initializes a predator object
				self.count = 200
				self.x=x
				self.y=y
				self.repro=repro

	def update(self):
				"""
				Allows for the movement, death/reproduction/eating of predator objects
				upon each timestep of the simulation
				"""
				try:
					board[self.x][self.y].remove(self)
				except ValueError:
					return

				if (self.count <= 0):
					characters.remove(self)
					return

				#random movement, up/down/left/right/diagonal
				self.x = (self.x + random.randint(-1,1))%20
				self.y = (self.y + random.randint(-1,1))%20

				if (len(board[self.x][self.y]) > 0):
					for u in (board[self.x][self.y]):
						if type(u) == Prey:
							if  random.random() > prey_eat_chance:

								#eat prey, restore food
								board[self.x][self.y].remove(u)
								characters.remove(u)
								board[self.x][self.y].append(self)
								self.count = 220

								return

						elif type(u) == Predator:
							
							board[self.x][self.y].append(self)
							self.count -= 1
							if (random.random() > self.repro) and (self.count > 200):
									child_x = (self.x + random.randint(-3,3)) % 20
									child_y = (self.y + random.randint(-3,3)) % 20
									child_pred = Predator(child_x,child_y,self.repro)
									board[child_x][child_y].append(child_pred)
									characters.append(child_pred)
							return

						else:
							board[self.x][self.y].append(self)
							self.count -= 1
				else:
					board[self.x][self.y].append(self)
					self.count -= 1
					return


def char_migration(plant_no, prey_no, predator_no):
	"""
	Initializes and places a given number of plant, prey, predator objects
	"""
	for i in range(plant_no):
		x=random.randint(0, 19)
		y=random.randint(0, 19)
		plant=Plant(x,y)
		characters.append(plant)
		board[x][y].append(plant)

	for i in range(prey_no):
			x=random.randint(0, 19)
			y=random.randint(0, 19)
			prey=Prey(x,y,prey_repro)
			characters.append(prey)
			board[x][y].append(prey)

	for i in range(predator_no):
			x=random.randint(0, 19)
			y=random.randint(0, 19)
			predator=Predator(x,y,pred_repro)
			characters.append(predator)
			board[x][y].append(predator)


#prepare the screen on which visuals for the simulation run
pygame.init()
screen = pygame.display.set_mode((800,800))
done = False

#load the images for the visuals of the simulation
chicken = pygame.image.load('chicken2.png')
cat = pygame.image.load('276-cat.png')
plant_img = pygame.image.load('plant.png')
background = pygame.image.load('grasses2.png')

#Setup pygame inputs
pygame.event.set_allowed(None)
pygame.event.set_allowed(pygame.KEYDOWN)
pygame.event.set_allowed(pygame.KEYUP)

def simulation(init_plant,init_prey,init_pred,mig_plant,mig_prey,mig_pred,freeplay=False):
	#initial migration
	char_migration(init_plant,init_prey,init_pred)

	#time parameters
	current_t=0
	time_tot=1000
	dt=1

	#count arrays
	prey_array = []
	pred_array = []
	plant_array = []

	while (current_t<time_tot):
		#dummy action, to keep the loop running and time gap
		pygame.event.post(pygame.event.Event(pygame.KEYUP))
		time.sleep(wait_time)
		for event in pygame.event.get():
			screen.blit(background,(0,0))
			current_t=current_t+dt

			#Additional Migration
			if(current_t % 100 == 0):
				char_migration(mig_plant,mig_prey,mig_pred)

			#adding and removing characters during run
			if event.type == pygame.KEYDOWN and freeplay:
				if(event.key == pygame.K_q):
					x=random.randint(0, 19)
					y=random.randint(0, 19)
					prey=Prey(x,y,prey_repro)
					characters.append(prey)
					board[x][y].append(prey)
					print("chicken added")
				if(event.key == pygame.K_w):
					x=random.randint(0, 19)
					y=random.randint(0, 19)
					predator=Predator(x,y,pred_repro)
					characters.append(predator)
					board[x][y].append(predator)
					print("cat added")
				if(event.key == pygame.K_e):
					x=random.randint(0, 19)
					y=random.randint(0, 19)
					plant=Plant(x,y)
					characters.append(plant)
					board[x][y].append(plant)
					print("plant added")
				if(event.key ==pygame.K_a):
					for i in characters:
						if(type(i)==Prey):
							i.count=0
							print("chicken removed")
							break
				if(event.key ==pygame.K_s):
					for i in characters:
						if(type(i)==Predator):
							i.count=0
							print("cat removed")
							break
				if(event.key ==pygame.K_d):
					for i in characters:
						if(type(i)==Plant):
							i.dead=True
							print("plant removed")
							break
			#updating characters and screen
			count_prey = 0
			count_pred = 0
			count_plant = 0

			for i in characters:
				i.update()
				color = (0,0,0)
				if type(i) == Prey:
					screen.blit(chicken, (i.x * 40,i.y * 40))
					count_prey += 1
				elif type(i) == Predator:
					screen.blit(cat, (i.x * 40,i.y * 40))
					count_pred += 1
				elif type(i) == Plant:
					screen.blit(plant_img, (i.x * 40,i.y * 40))
					count_plant += 1
			pygame.display.update()

			prey_array.append(count_prey)
			pred_array.append(count_pred)
			plant_array.append(count_plant)

			if event.type == pygame.QUIT:
				done = True
			pygame.display.update()
			pygame.display.flip()


	#creates matplotlib plots of prey, predator, plant populations over time
	plt.subplot(4, 1, 1)
	plt.plot(np.arange(len(prey_array)),np.asarray(prey_array), color ='blue')
	plt.title('Prey Count')
	plt.ylim(0,np.asarray(prey_array).max()+5)
	plt.savefig('prey_c.png')

	plt.subplot(4, 1, 2)
	plt.plot(np.arange(len(pred_array)),pred_array, color='purple')
	plt.title('Predator Count')
	plt.ylim(0,np.asarray(pred_array).max()+5)
	plt.savefig('pred_c.png')

	plt.subplot(4, 1, 3)
	plt.plot(np.arange(len(plant_array)),plant_array, color='green')
	plt.title('Plant Count')
	plt.ylim(0,np.asarray(plant_array).max()+5)
	plt.savefig('plant_c.png')

	plt.subplot(4, 1, 4)
	plt.plot(np.arange(len(prey_array)),np.asarray(prey_array), color ='blue')
	plt.plot(np.arange(len(pred_array)),pred_array, color='purple')	
	plt.plot(np.arange(len(plant_array)),plant_array, color='green')
	plt.title('Total Count')
	plt.ylim(0,max(np.asarray(plant_array).max()+5,np.asarray(pred_array).max()+5,np.asarray(prey_array).max()+5))
	plt.savefig('plant_c.png')


	plt.show()

#To display for users at the start of the simulation

print("           Welcome to Hungry Habitat!          ")
print("-----------------------------------------------")
print("This is a tool developed to help teach children")
print("basic ecological and mathematical concepts     ")
print("through simulations of predator/prey/plant     ")
print("scenarios that are easy to understand, visually")
print("interesting and most importantly fun!          ")
print()
print("---------------------------------------------------")
print("There are currently six simulations to choose from ")
print("1: Chicken carrying capacity   ")
print("2: Introduction of predators   ")
print("3: Cat carrying capacity       ")
print("4: Drought                     ")
print("5: Chicken population Explosion")
print("6: Free-play                   ")
print("In free play you can design your own simulation")
print("adding characters with the Q,W and E keys, and ")
print("removing characters with the A, S and D keys")
print()
print("--------------------------------------------------")

#Program loop, exits with sys.exit()
while True:
	#reset
	board = [[[] for x in range(BOARD_W)] for y in range(BOARD_H)]
	characters=[]
	#Input Validation of num between 0 and 6
	while True:
		value= input("Please enter the number for the \nsimulation you'd like to see: (enter 0 to quit) ")
		try:
			sim_num= int(value)
		except ValueError:
			print ("\nRemember to enter a number between 0 and 6 \n")
			continue
		if ( sim_num>-1 and sim_num<7):
			break
		else:
			print("\nRemember to enter a number between 0 and 6 \n")
#exit app
	if(sim_num==0):
		print("Thanks for using Hungry Habitat!")
		sys.exit()

#Chicken Carry capacity
	if(sim_num==1):
		simulation(45,30,0,8,0,0)

#Introduction of predators
	if(sim_num==2):
		simulation(45,30,0,1,0,3)

#Cat carrying capacity
	if(sim_num==3):
		simulation(0,20,10,0,8,0)

#Drought
	if(sim_num==4):
		simulation(50,30,3,0,0,0)

#Chicken Explosion
	if(sim_num==5):
		simulation(60,0,0,0,2,0)

#free-play
	if(sim_num==6):
		simulation(0,0,0,0,0,0,freeplay=True)
