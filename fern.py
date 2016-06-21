from numpy.random import random
import matplotlib.pyplot as plt

import Tkinter
import math
import time

#Gives dimension of canvas

W=800
H=600

#creates a point 

def createPoint(canvas, x0, y0, c):
   canvas.create_line(x0, y0+1, x0+1, y0, fill=c)

#gives probabilities for each iterated function in pdf form.  The Default is the traditional Barnsley fern

P=[.85, .07, .07, .01]

#number of points to be generated, default set at 10000
pointnum=10000;


#function for generating the points of the fern

def f(x,y,Probs):
	m=random();
	
	#creates the top part of the fern
	if m<sum(Probs[0:1]): return 	[0.85*x+0.04*y, 
					-0.04*x+0.85*y+1.6,
					"red"]
	#creates the left bottom leaf of the fern
	elif m<sum(Probs[0:2]): return 	[0.2*x-0.26*y, 
					 0.23*x+0.22*y +1.6,
					"green"]
	#creates the right bottom leaf of the fern
	elif m<sum(Probs[0:3]): return  [-0.15*x+0.28*y, 
					  0.26*x+0.24*y+0.44, 
					"yellow"]
	#creates the bottom stem of the ferm
	return [0,0.16*y, "orange"]

#generates the points on the canvas
def animate():
	xpoints=[0]  #gives starting point, translates it to a starting point on the canvas
	ypoints=[0]
	startingX=W/2
	startingY=0.9*H

	Probs=[float(probs1.get()),
		float(probs2.get()),
		float(probs3.get()),
		float(probs4.get())]
	if sum(Probs) != 0: Probs=[p/sum(Probs) for p in Probs]
	
	canvas.update()
	for i in range(int(numpoints.get())):
		[x,y,c]=f(xpoints[-1],ypoints[-1],Probs);
		xpoints=xpoints+[x];
		ypoints=ypoints+[y];
		createPoint(canvas,startingX+70*x,startingY-50*y, c)
		canvas.update()


		
def clear():
	canvas.delete("all")


FractalWindow= Tkinter.Tk()
FractalWindow.title("Barnsley Fern")

clear_button = Tkinter.Button(FractalWindow, text="clear", command=clear)
start = Tkinter.Button(FractalWindow, text="start", command=animate)
numpoints=Tkinter.StringVar()
numpoints.set(`pointnum`)
stepLabel=Tkinter.Label(FractalWindow, width="15")
stepLabel.configure(text="Num Points= ")
stepentry=Tkinter.Entry(FractalWindow, width="15", textvariable=numpoints)

canvas = Tkinter.Canvas(FractalWindow, width=W, height=H, background="black")

probs1=Tkinter.StringVar()
probs1.set(P[0])
probs2=Tkinter.StringVar()
probs2.set(P[1])
probs3=Tkinter.StringVar()
probs3.set(P[2])
probs4=Tkinter.StringVar()
probs4.set(P[3])
probLabel=Tkinter.Label(FractalWindow, width="15")
probLabel.configure(text="probabilities= ")
probEntry1=Tkinter.Entry(FractalWindow, width= "5", textvariable = probs1)
probEntry2=Tkinter.Entry(FractalWindow, width= "5", textvariable = probs2)
probEntry3=Tkinter.Entry(FractalWindow, width= "5", textvariable = probs3)
probEntry4=Tkinter.Entry(FractalWindow, width= "5", textvariable = probs4)


canvas.pack(side="top")
start.pack(side="right")
clear_button.pack(side = "right")
stepLabel.pack(side="left")
stepentry.pack(side="left")

probLabel.pack(side="left")
probEntry1.pack(side="left")
probEntry2.pack(side="left")
probEntry3.pack(side="left")
probEntry4.pack(side="left")

FractalWindow.mainloop()
#plt.figure()
#plt.scatter(xpoints,ypoints, s=0.25, c='blue')
#plt.show()



