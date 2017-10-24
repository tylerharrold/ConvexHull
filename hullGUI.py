#!/usr/bin/env python
# if using python 3, swap the next two lines
# from tkinter import *
from Tkinter import *
import copy
import random
from convexhull import computeHull


def hello(event):
    print("Single Click, Button-l") 

def addPoint(event):
	drawPoint(w, event.x, event.y)
	points.append((event.x,event.y))

def drawPoint(canvas,x,y):
	# r = 4
	# id = canvas.create_oval(x-r,y-r,x+r,y+r)
        id = canvas.create_text(x , y , text=str(x) + "," + str(y))
	#id = canvas.create_image((x,y),image=x + "," + y,state=NORMAL)
	return id

def showPoints(event):
	print points

def generate_randos():
    points = [0] * 500
    for i in range(0 , len(points)):
        x = random.randint(100,900)
        y = random.randint(100 , 600)
        points[i] = (x,y)
    return points
 

def drawHull():
        bigtest = generate_randos()
        for b in bigtest:
            x = b[0]
            y = b[1]
            r = 2
	    w.create_oval(x-r,y-r,x+r,y+r)
	hull = copy.copy(computeHull(bigtest))
	hull.append(hull[0])
	for i in range(0,len(hull)-1):
		x1 = hull[i][0]
		y1 = hull[i][1]
		x2 = hull[i+1][0]
		y2 = hull[i+1][1]
		w.create_line(x1, y1, x2, y2, width=3)


master = Tk()
points = []
colintest = [(200,200) , (200,300) , (200,400) , (400,400) , (300 , 200) , (300, 400) , (400, 200)]

submit_button = Button(master, text="Draw Hull", command=drawHull)
submit_button.pack()
quit_button = Button(master, text="Quit", command=master.quit)
quit_button.pack()

canvas_width = 1000
canvas_height = 800
w = Canvas(master, 
           width=canvas_width,
           height=canvas_height)
ram = PhotoImage(file="ram-sm.gif")
w.pack()
w.bind('<Button-1>', addPoint)

w.mainloop()

       

bigtest = generate_randos()
