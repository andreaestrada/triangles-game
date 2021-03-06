import random
import math, cmath
from tkinter import *

def init(data):
    data.triangles = []
    data.triangleSize = 50
    for i in range(10):
        triangle = Triangle(data.triangleSize, random.randint(0, data.width-data.triangleSize), random.randint(0, data.height/2), random.randint(0,360))
        data.triangles.append(triangle)
    data.timerSeconds = 1000
    data.currTimer = 0
    data.score = 0

class Triangle(object):
    def __init__(self, size, x, y, startingRotation):
        self.size = size #side length of triangle
        self.x = x #bottom left x starting position
        self.y = y #bottom left y starting position
        self.color = "black"

        #animate triangle
        self.rotateDeg = 2 #rotation speed 
        self.dropSpeed = 1.5

        #define starting coordinates
        coor1 = [self.x, self.y]
        coor2 = [self.x+self.size, self.y]
        coor3 = [self.x+self.size/2, self.y-self.size*(3**0.5)/2]

        #set centroid 
        self.centroid = [(coor1[0] + coor2[0] + coor3[0])/3, (coor1[1] + coor2[1] + coor3[1])/3]

        #random rotation
        self.triangleCoors = self.rotate(startingRotation, self.centroid, [coor1, coor2, coor3])

    def rotate(self, angle, centroid, triangle):
        #rotate triangle around centroid
        cangle = cmath.exp(angle*1j*math.pi/180)
        offset = complex(centroid[0], centroid[1])
        rotated = []
        for x, y in triangle:
            v = cangle*(complex(x,y) - offset) + offset
            rotated.append([v.real, v.imag])
        return rotated
        
    def move(self, centroid, triangle, dropSpeed):
        for coordinate in triangle:
            coordinate[1] += dropSpeed
        centroid[1] += dropSpeed

    def hit(self, mouse,tri):
        #checks if mouse click is in triangle
        #uses barycentric coordinates 
        twiceArea = (-tri[1][1]*tri[2][0]+tri[0][1]*(-tri[1][0]+tri[2][0])+ 
            tri[0][0]*(tri[1][1]-tri[2][1])+tri[1][0]*tri[2][1])
        s = 1/twiceArea*(tri[2][0]*tri[0][1]-tri[0][0]*tri[2][1]+(tri[2][1]-tri[0][1])*mouse[0]+\
            (tri[0][0]-tri[2][0])*mouse[1])
        if s<0: return False
        t = 1/twiceArea*(tri[0][0]*tri[1][1]-tri[1][0]*tri[0][1]+(tri[0][1]-tri[1][1])*mouse[0]+\
            (tri[1][0]-tri[0][0])*mouse[1])
        return (t>0 and 1-s-t>0)

def redrawAll(canvas, data):
    for triangle in data.triangles:
        canvas.create_polygon(triangle.triangleCoors, fill = triangle.color) #draw triangle
    canvas.create_text(80,40, text = "Score: " + str(data.score), font = "Arial 22")

def timerFired(data):
    for triangle in data.triangles:
        triangle.triangleCoors = triangle.rotate(triangle.rotateDeg, triangle.centroid, triangle.triangleCoors)
        triangle.move(triangle.centroid, triangle.triangleCoors, triangle.dropSpeed)
    data.currTimer += 10
    if data.currTimer >= data.timerSeconds/4: #1000 milliseconds = 1 second
        data.currTimer = 0
        #add new triangle
        data.triangles.append(Triangle(data.triangleSize, random.randint(0, data.width-data.triangleSize), 0, random.randint(0,360)))

def mousePressed(event, data):
    mouseCoors = (event.x, event.y)
    maxHit = -1
    for i in range(len(data.triangles)): #eliminate hit triangles
        if data.triangles[i].hit(mouseCoors, data.triangles[i].triangleCoors): maxHit = i
    if maxHit > -1:
        data.triangles = data.triangles[:maxHit] + data.triangles[maxHit+1:]
        data.score += 1

def keyPressed(event, data): pass

####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 10 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed

def main():
	run (700, 700)

main()
