import math

grid = []
for i in range(50):
    grid.append([None]*50)

class force:
    def __init__(self,m, d, n):
        self.mag = m
        self.theta = d
        self.name = n

class obj:
    def __init__(self, m, c):
        self.mass = m
        self.coord = c
        grid[self.coord[0]][self.coord[1]] = self
        self.forces = []
        self.forces.append(force(10*self.mass, -1*math.pi/2, "gravity"))
        if(self.coord[1] is 0):
            self.forces.append(force(10*self.mass,math.pi/2, "normal"))
        self.vel = (0,0)

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
        return (fs[0]/self.mass,fs[1]/self.mass)
    
    def calcPos(self, t):
        xfX = self.coord[0] + self.vel[0]*t + self.calcAcc()[0]*math.pow(t,2)//2
        xfY = self.coord[1] + self.vel[1]*t + self.calcAcc()[1]*math.pow(t,2)//2
        self.vel = self.calcAcc()*t
        return (round(xfX),round(xfY))

    def passTime(self):
        newPos = self.calcPos(1)
        grid[self.coord[0]][self.coord[1]] = None
        grid[newPos[0]][newPos[1]] = self
        self.coord = newPos
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
        
            

thing = obj(10, (3,42))
print(thing.getCoord())
thing.passTime()
print(thing.getCoord())
