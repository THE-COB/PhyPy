import math

grid = []
for i in range(10):
    grid.append([None]*10)

class force:
    def __init__(self,m, d):
        self.mag = m
        self.theta = d

class obj:
    def __init__(self, m, c):
        self.mass = m
        self.coord = c
        grid[self.coord[0]][self.coord[1]] = self
        self.forces = []
        self.forces.append(force(10*self.mass, -1*math.pi/2))

    def getMass(self):
        return self.mass
    def getCoord(self):
        return self.coord
    def getForces(self):
        return self.forces
    def addForce(self, f):
        self.forces.append(f)

thing = obj(10, (9,3))
print(thing.getForces())
