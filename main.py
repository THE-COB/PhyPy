import math
import pygame

grid = []
for i in range(20):
	grid.append([None]*20)

class force:
	def __init__(self,m, d, n):
		self.mag = m
		self.theta = d
		self.name = n

	def __str__(self):
		return "Magnitude: "+str(self.mag)+"\nAngle(radians): "+str(self.theta)+"\nName: "+self.name

class obj:
	def __init__(self, m, c):
		self.screenCoord = []
		self.mass = m
		self.coord = c
		grid[self.coord[0]][self.coord[1]] = self
		self.forces = []
		self.forces.append(force(10*self.mass, -1*math.pi/2, "gravity"))
		if(self.coord[1] is 0):
			self.forces.append(force(10*self.mass,math.pi/2, "normal"))
		self.vel = (0,0)
		self.acc = (0,0)

	def __str__(self):
		strForces = ""
		for i in self.forces:
			strForces+=i.name+","
		strForces = strForces[:-1]
		return "Mass: "+str(self.mass)+"\nCoordinate: "+str(self.coord)+"\nForces: "+strForces+"\nVelocity: "+str(self.vel)+"\nAcceleration: "+str(self.calcAcc())

	def getMass(self):
		return self.mass
	def getCoord(self):
		return self.coord
	def getForces(self):
		return self.forces
	def addForce(self, f):
		self.forces.append(f)

	def calcTotalFs(self):
		xComps = 0
		yComps = 0
		for i in self.forces:
			xComps+=(math.cos(i.theta)*i.mag)
			yComps+=(math.sin(i.theta)*i.mag)
		return (round(xComps, 3),round(yComps, 3))

	def calcAcc(self):
		fs = self.calcTotalFs()
		self.acc = (fs[0]/self.mass,fs[1]/self.mass)
		return self.acc
	
	def calcPos(self, t):
		xfX = self.coord[0] + self.vel[0]*t + self.calcAcc()[0]*math.pow(t,2)//2
		xfY = self.coord[1] + self.vel[1]*t + self.calcAcc()[1]*math.pow(t,2)//2
		self.vel = self.calcAcc()*t
		return (round(xfX),round(xfY))

	def passTime(self):
		newPos = self.calcPos(1)
		if(newPos[0]<0):
			newPos = (0,newPos[1])
		if(newPos[1]<0):
			newPos = [newPos[0],0]
		grid[self.coord[0]][self.coord[1]] = None
		grid[newPos[0]][newPos[1]] = self
		self.coord = (newPos[0],newPos[1])
		if(newPos[1] is 0):
			hasNorm = False
			for i in self.forces:
				if(i.name is "normal"):
					i.mag = 10*self.mass
					i.theta = math.pi/2
					hasNorm = True
					break
			if(not hasNorm):
				self.forces.append(force(10*self.mass,math.pi/2, "normal"))

black = (0,0,0)
white = (255,255,255)
gridOn = True

pygame.init()

WINDOW_SIZE = [800,800]
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("PhyPy")
done = False
clock = pygame.time.Clock()
objects = []

boi = obj(10, (12,8))
objects.append(boi)

def drawObj(thing):
	width = WINDOW_SIZE[0]/len(grid)
	height = WINDOW_SIZE[1]/len(grid[0])
	scrX = (thing.coord[0]*width)
	scrY = WINDOW_SIZE[1]-(thing.coord[1]*height)
	pygame.draw.rect(screen,black,(scrX,scrY,-1*width,-1*height))
	thing.screenCoord = [round(scrX),round(scrY),round(scrX-width),round(scrY-height)]

while(not done):
	ev = pygame.event.get()
	screen.fill(white)
	for event in pygame.event.get():
		if(event.type == pygame.QUIT):
			done = True

	if(gridOn):
		xInt = WINDOW_SIZE[0]//len(grid)
		yInt = WINDOW_SIZE[1]//len(grid[0])
		for i in range(0,WINDOW_SIZE[0]):
			if(i>=len(grid) and i%xInt is 0):
				pygame.draw.line(screen, black, (i,0), (i,WINDOW_SIZE[0]))
		for i in range(0,WINDOW_SIZE[1]):
			if(i>=len(grid[0]) and i%yInt is 0):
				pygame.draw.line(screen, black, (0,i), (WINDOW_SIZE[1],i))

	for i in objects:
		drawObj(i)

	for event in ev:
		if(event.type is pygame.MOUSEBUTTONUP and event.button is 1):
			for i in grid:
				for j in i:
					if(j != None):
						j.passTime()
		if(event.type is pygame.MOUSEBUTTONUP and event.button is 3):
			alterObj = True
			mousePos = pygame.mouse.get_pos()
			for i in objects:
				objPos = i.screenCoord
				if(mousePos[0]>objPos[2] and mousePos[0]<objPos[0] and mousePos[1]>objPos[3] and mousePos[1]<objPos[1]):
					alterObj = True
					print("Would you like to change the force the object(c) or see information about it(r)?")
					inp = input()
					if(inp is "r"):
						print(i)
					elif(inp is "c"):
						print("Would you like to delete(d) or add(a) a force")
						inp0 = input()
						if(inp0 is "d"):
							strForces = ""
							for j in i.forces:
								strForces += j.name
							strForces = strForces[:-1]
							print("Which force would you like to delete(0, "+str(len(i.forces)-1)+")")
							i.forces.pop(int(input()))
							print("done")
						if(inp0 is "a"):
							print("Type in magnitude(Newtons), direction(degrees), name. ex: 5,180,applied")
							pI = input().split(",")
							i.addForce(force(int(pI[0]),math.radians(int(pI[1])),pI[2]))
							print("Done")
				else:
					alterObj = False

			if(not alterObj):
				print("Would you like to add an object (y/n)")
				if(input() is "y"):
					print("What is the mass? ex: 12")
					mass = int(input())
					print("What is the coordinate ex: 6,3")
					strCoord = input().split(",")
					coord = (int(strCoord[0]),int(strCoord[1]))
					objects.append(obj(mass,coord))
					print("done")

	pygame.display.flip()
