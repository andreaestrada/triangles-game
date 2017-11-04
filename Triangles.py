import random
from tkinter import *

def init(data):
    data.triangles = []
    for i in range(15):
        triangle = Triangle(data.width, random.randint(0, windowHeight))
        data.triangles.append(triangle)
    data.timerMove = 0
    data.currTimer = 5 

class Triangle(object):
    def init(self, windowWidth, yPosition = 0):
        self.sideLen = windowWidth/20
        self.xPosition = random.randint(0, windowWidth) 
        self.yPosition = yPosition
        self.coor1 = (self.xPosition, yPosition)
        self.coor2 = (self.xPosition + self.sideLen, yPosition)
        self.coor3 = (self.xPosition + self.sideLen/2, yPosition)
                

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
    data.timerDelay = 1000 # milliseconds
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
