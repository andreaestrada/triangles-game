####################################

from tkinter import *
import math, cmath

def init(data):
    data.size = 100 #side length of triangle
    data.x = data.width/2 #bottom left x starting position
    data.y = 200 #bottom left y starting position
    data.color = "black"

    #animate triangle
    data.rotateDeg = 2 #rotation speed 
    data.dropSpeed = 2

    #define coordinates
    coor1 = [data.x, data.y]
    coor2 = [data.x+data.size, data.y]
    coor3 = [data.x+data.size/2, data.y-data.size*(3**0.5)/2]

    #defining characteristics
    data.triangle = [coor1, coor2, coor3]
    data.centroid = [(coor1[0] + coor2[0] + coor3[0])/3, (coor1[1] + coor2[1] + coor3[1])/3]

def redrawAll(canvas, data):
    canvas.create_polygon(data.triangle, fill = data.color) #draw triangle

def timerFired(data):
    data.triangle = rotate(data.rotateDeg, data.centroid, data.triangle)
    moveTriangle(data.centroid, data.triangle, data.dropSpeed)

def rotateTriangle(angle, centroid, triangle):
    #rotate triangle around centroid
    cangle = cmath.exp(angle*1j*math.pi/180)
    offset = complex(centroid[0], centroid[1])
    rotatedTriangle = []
    for x, y in triangle:
        v = cangle*(complex(x,y) - offset) + offset
        rotatedTriangle.append([v.real, v.imag])
    return rotatedTriangle
    
def moveTriangle(centroid, triangle, dropSpeed):
    for coordinate in triangle:
        coordinate[1] += dropSpeed
    centroid[1] += dropSpeed

def mousePressed(event, data):
    mouseCoors = (event.x, event.y)
    if triangleHit(mouseCoors, data.triangle): data.color = "red"

def triangleHit(mouse,tri):
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

def keyPressed(event,data): pass

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
    data.timerDelay = 10 #100 times/second
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
