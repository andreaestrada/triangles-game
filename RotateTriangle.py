####################################

from tkinter import *
import math, cmath

def init(data):
    data.size = 100
    data.x = data.width/2
    data.y = 200
    data.rotateDeg = 2

    data.coor1 = (data.x, data.y)
    data.coor2 = (data.x+data.size, data.y)
    data.coor3 = (data.x+data.size/2, data.y-data.size*(3**0.5)/2)
    data.triangle = [data.coor1, data.coor2, data.coor3]
    data.centroid = ((data.coor1[0] + data.coor2[0] + data.coor3[0])/3, (data.coor1[1] + data.coor2[1] + data.coor3[1])/3)

def redrawAll(canvas, data):
    canvas.create_polygon(data.triangle, fill = "black")
    canvas.create_oval(data.centroid, data.centroid, width = 5, fill = "red")

def timerFired(data):
    data.triangle = rotateTriangle(data.rotateDeg, data.centroid, data.triangle)


def rotateTriangle(angle, centroid, triangle):
    cangle = cmath.exp(angle*1j*math.pi/180)
    offset = complex(centroid[0], centroid[1])
    rotatedTriangle = []
    for x, y in triangle:
        v = cangle*(complex(x,y) - offset) + offset
        rotatedTriangle.append((v.real, v.imag))
    return rotatedTriangle
    

def mousePressed(event, data): pass

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
