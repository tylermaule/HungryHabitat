# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 13:01:01 2017

@author: mauletj
"""

import random
import pygame

#Just some ideas on implementation of simulation
#very object oriented. we could go other directions
w,h = 20, 20
board = [[[] for x in range(w)] for y in range(h)] #array of array of arrays
#print(board)

class Plant(object):

	def __init__(self,x,y):
		self.x=x
		self.y=y

	def update(self):
		if (random.randint(0,1000) > 975):
			if (random.random<=.5):
				plant_x = (self.x+1)%20
			else:
				plant_x = (self.x-1)%20
			if (random.random<=.5):
				plant_y = (self.y+1)%20
			else:
				plant_y = (self.y-1)%20
			plant = Plant(plant_x,plant_y)
			board[plant_x][plant_y].append(plant)
			characters.append(plant)
		return

class Prey(object):

	def __init__(self,x,y,repro):
		self.count = 200
		self.x=x
		self.y=y
		self.repro=repro

	def update(self):
		rand=random.randint(1,4) #needs collisions checks.
		try:
			board[self.x][self.y].remove(self) #think about modulo looping around maybe
		except ValueError:
			return

		if (self.count <= 0):
			characters.remove(self)
			return


		if(rand==1 and self.x+1<20):
			self.x=self.x+1
		if(rand==2 and self.x-1>-1):
			self.x=self.x-1
		if(rand==3 and self.y+1<20):
			self.y=self.y+1
		if(rand==4 and self.y-1>-1):
			self.y=self.y-1

		if (len(board[self.x][self.y]) > 0):
			for u in (board[self.x][self.y]):
				if type(u) == Predator:
					print('prey eaten')
					characters.remove(self)
					return
				if type(u) == Plant:
					print('prey eat plant')
					board[self.x][self.y].remove(u)
					characters.remove(u)
					self.count = 300
					board[self.x][self.y].append(self)
					#plant=Plant(self.x, self.y)
					#characters.append(plant)
					plant_countdown = 25
					plant_locations.append((self.x,self.y))
					return
				elif type(u) == Prey:
					board[self.x][self.y].append(self)
					self.count -= 1
					if (random.random() > self.repro) and (self.count > 200):
						child_x = (self.x + random.randint(-3,3)) % 20
						child_y = (self.y + random.randint(-3,3)) % 20
						child_prey = Prey(child_x,child_y,0.7)
						board[child_x][child_y].append(child_prey)
						characters.append(child_prey)
					return
		else:
			board[self.x][self.y].append(self)
			self.count -= 1
		

class Predator(object):

	def __init__(self,x,y,repro):
				self.count = 200
				self.x=x
				self.y=y
				self.repro=repro

	def update(self):
				rand=random.randint(1,4) #needs collisions checks.
				try:
					board[self.x][self.y].remove(self) #think about modulo looping around maybe
				except ValueError:
					return

				
				if (self.count <= 0):
					characters.remove(self)
					return


				if(rand==1 and self.x+1<20):
						self.x=self.x+1
				if(rand==2 and self.x-1>-1):
						self.x=self.x-1
				if(rand==3 and self.y+1<20):
						self.y=self.y+1
				if(rand==4 and self.y-1>-1):
						self.y=self.y-1

				if (len(board[self.x][self.y]) > 0):
					for u in (board[self.x][self.y]):
						if type(u) == Prey:
							board[self.x][self.y].remove(u)
							characters.remove(u)
							self.count = 300
							board[self.x][self.y].append(self)
							return
						elif type(u) == Predator:
							print('endless')
							board[self.x][self.y].append(self)
							self.count -= 1
							if (random.random() > self.repro) and (self.count > 200):
								child_x = (self.x + random.randint(-3,3)) % 20
								child_y = (self.y + random.randint(-3,3)) % 20
								if(self.y != child_y) and (self.x != child_x):
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
time_tot=1000
dt=0.01
current_t=0

#randomly initalize 10 plants, 5 prey, 2 predators
plant_locations = []
for i in range(20): #plant=1
	x=random.randint(0, 19)
	y=random.randint(0, 19)
	plant_locations.append((x,y))
	plant=Plant(x,y)
	characters.append(plant)
	board[x][y].append(plant)

for i in range(15): #prey =2
		x=random.randint(0, 19)
		y=random.randint(0, 19)
		prey=Prey(x,y,0.7)
		characters.append(prey)
		board[x][y].append(prey)

for i in range(3):#predator =3
		x=random.randint(0, 19)
		y=random.randint(0, 19)
		predator=Predator(x,y,.5)
		characters.append(predator)
		board[x][y].append(predator)


pygame.init()
screen = pygame.display.set_mode((800,800))
done = False

chicken = pygame.image.load('chicken2.png')

def draw_background():
	for i in range(0,800,40):
		for j in range(0,800,40):
			r_color = 0 + random.randint(0,60)
			g_color = 60 + random.randint(0,50)
			b_color = 0 + random.randint(0,60)
			pygame.draw.rect(screen, (0,60,0),
					pygame.Rect(i,j,40,40))
plant_countdown = 10

while not done:
	for event in pygame.event.get():
		plant_countdown = max(plant_countdown-1,0)
		if plant_countdown == 0:
			for l in plant_locations:
				if(len(board[l[0]][l[1]])==0) and (random.randint(0,1000)>990):
					print('plant regrowing')
					plant = Plant(l[0],l[1])
					board[plant.x][plant.y].append(plant)
					characters.append(plant)
				else:
					plant_countdown = 10
			plant_locations = []	
			plant_countdown = 10
		for p in range(1):
			draw_background()
			current_t+=+dt
			for i in characters:
                            i.update()
                            color = (0,0,0)
                            if type(i) == Prey:
                                screen.blit(chicken, (i.x * 40,i.y * 40))
                            elif type(i) == Predator:
                                print('count',i.count)
                                color = (60,0,0,50)
				pygame.draw.rect(screen,(color),pygame.Rect(i.x * 40,i.y * 40,40,40))

                            elif type(i) == Plant:
                                color = (100,0,100,50)
                            	pygame.draw.rect(screen,(color),pygame.Rect(i.x * 40,i.y * 40,40,40))
                            pygame.display.update()

		if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT and ((current_t<time_tot)):
			pass
		if event.type == pygame.QUIT:
			done = True
		pygame.display.update()
		pygame.display.flip()

endnum = 0
for j in range(20):
	print(board[j])
print (endnum)
