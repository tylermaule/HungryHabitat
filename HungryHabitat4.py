# -*- coding: utf-8 -*-
"""
Jai Ahuja, Lucas Napolitano, Tyler Maule
Created on Thu Nov 30 13:01:01 2017
@author: mauletj
"""

import random
import pygame

#Just some ideas on implementation of simulation
#very object oriented. we could go other directions
BOARD_W, BOARD_H = 20, 20
board = [[[] for x in range(BOARD_W)] for y in range(BOARD_H)]

#chance that a plant grows a new plant nearby
PLANT_REPRO = 0.01

class Plant(object):
	"""
	A plant object/'character' that can be eaten by prey. Takes an x-pos,
	y-pos, and may generate new plant objects nearby upon update.
	"""
	def __init__(self,x,y):
		self.x=x
		self.y=y

	def update(self):
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
		#count is number of 'turns' remaining before 'death'
		self.count = 200
		self.x=x
		self.y=y
		self.repro=repro

	def update(self):
		#remove character from board prior to potential movement
		try:
			board[self.x][self.y].remove(self)
		except ValueError:
			return

		#character dies if food count has run to 0
		if (self.count <= 0):
			characters.remove(self)
			return

		#random movement, up/down/left/right/diagonal
		self.x = (self.x + random.randint(-1,1))%20
		self.y = (self.y + random.randint(-1,1))%20

		#check for, and respond to, character object collisions
		if (len(board[self.x][self.y]) > 0):
			for u in (board[self.x][self.y]):
				if type(u) == Predator:
					print('prey eaten')

					#prey character eaten
					characters.remove(self)
					u.count == 300

					return

				elif type(u) == Plant:
					print('prey eat plant')

					#remove plant
					board[self.x][self.y].remove(u)
					characters.remove(u)

					#allow plants to regrow in same location
					plant_countdown = 25
					#plant_locations.append((self.x,self.y))

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

	def __init__(self,x,y,repro):
				self.count = 200
				self.x=x
				self.y=y
				self.repro=repro

	def update(self):
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

							#eat prey, restore food
							board[self.x][self.y].remove(u)
							characters.remove(u)
							board[self.x][self.y].append(self)
							self.count = 300

							return

						elif type(u) == Predator:
							print('endless')
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


characters=[]
time_tot=10000
dt=1
current_t=0

#randomly initalize 10 plants, 5 prey, 2 predators
#plant_locations = []

def char_migration(plant_no, prey_no, predator_no):
	for i in range(plant_no): #plant=1
		x=random.randint(0, 19)
		y=random.randint(0, 19)
		#plant_locations.append((x,y))
		plant=Plant(x,y)
		characters.append(plant)
		board[x][y].append(plant)

	for i in range(prey_no): #prey =2
			x=random.randint(0, 19)
			y=random.randint(0, 19)
			prey=Prey(x,y,0.7)
			characters.append(prey)
			board[x][y].append(prey)

	for i in range(predator_no):#predator =3
			x=random.randint(0, 19)
			y=random.randint(0, 19)
			predator=Predator(x,y,.9)
			characters.append(predator)
			board[x][y].append(predator)


pygame.init()
screen = pygame.display.set_mode((800,800))
done = False

chicken = pygame.image.load('chicken2.png')
cat = pygame.image.load('276-cat.png')
plant_img = pygame.image.load('plant.png')
background = pygame.image.load('grasses2.png')


def draw_background():
	for i in range(0,800,40):
		for j in range(0,800,40):
			r_color = 0 + random.randint(0,60)
			g_color = 60 + random.randint(0,50)
			b_color = 0 + random.randint(0,60)
			pygame.draw.rect(screen, (r_color,g_color,b_color),
					pygame.Rect(i,j,40,40))

plant_countdown = 10
char_migration(45,30,3)


while not done:
	for event in pygame.event.get():
		"""plant_countdown = max(plant_countdown-1,0)
		if plant_countdown == 0:
			for l in plant_locations:
				if(len(board[l[0]][l[1]])==0) and (random.randint(0,1000)>900):
					print('plant regrowing')
					#plant = Plant(l[0],l[1])
					#board[plant.x][plant.y].append(plant)
					#characters.append(plant)
				else:
					plant_countdown = 10
			plant_locations = []
			plant_countdown = 10"""

		screen.blit(background,(0,0))
		current_t+=+dt

		if(current_t % 100 == 0):
			char_migration(5,6,2)

		for i in characters:
			i.update()
			color = (0,0,0)
			if type(i) == Prey:
					screen.blit(chicken, (i.x * 40,i.y * 40))
			elif type(i) == Predator:
					screen.blit(cat, (i.x * 40,i.y * 40))
			elif type(i) == Plant:
					screen.blit(plant_img, (i.x * 40,i.y * 40))
		pygame.display.update()

		if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT and ((current_t<time_tot)):
			pass
		if event.type == pygame.QUIT:
			done = True
		pygame.display.update()
		pygame.display.flip()

"""endnum = 0
for j in range(20):
	print(board[j])
print (endnum)"""