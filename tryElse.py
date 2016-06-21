import Tkinter
import itertools
from math import sqrt
import time
from numpy.random import random
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageEnhance

W=800
H=800
FractalOriginX=0.5
FractalOriginY=0.6
scalingX=50
scalingY=50

AxisX= 10.0
AxisY= 10.0

window= Tkinter.Tk()
window.title("Iterated Function System Editor")
FractalWindow= Tkinter.Toplevel()
FractalWindow.title("Attractor")
fractalCanvas = Tkinter.Canvas(FractalWindow, width=W, height=H, background="black")

canvas = Tkinter.Canvas(window, width=W, height=H, background="black")
coords = Tkinter.Label(window, width="10")




global tick
global quads
global matrices
global XYC



global Barnsley
global Triangle
global Pythagorean_tree
global Snowflake



XYC=[[],[],[]]


square_count={0:'#00FFFF', 1:'#FF00FF', 2:'#FFFF00', 3: '#90FF00',
		4:'#FF9000', 5:'#00FF90', 6:'#0090FF', 7:'#9000FF'}

drag_data = {"x": 0, "y": 0, "item": None}

tick=0
quads =[[0,0,0,0],
	[0,0,0,0],
	[0,0,0,0],
	[0,0,0,0]]

#gives probabilities for each iterated function in pdf form.  The Default is 1/4 for each vector

P=[1, 1, 1, 1]

#number of points to be generated, default set at 10000
pointnum=10000;


colors=["red","green","yellow","orange"]

#a collection of sample fractals
Barnsley=[[0.85, 0.04,-0.04,.85,0,1.6], #lists linear transformations, 
	[0.2,-0.26,0.23,0.22,0,1.60],	#values 1,2, 5 give a,b,c with a*x+b*y +c = new_x
	[-0.15,0.28,0.26,0.24,0,0.44],	#values 3,4, 6 give a,b,c with a*x+b*y +c = new_y
	[0,0,0,.16,0,0], [85,7,7,1]]   	 
					

Triangle=[[0.5,0,0,0.5,0,0],
	[0.5,0,0,0.5,0.5, 0],
	[0.5,0,0,0.5,0.25,sqrt(3)*0.25],
	[0,0,0,0,0,0], [1,1,1,0]]

Pythagorean_tree=[[0,0,0,1.0/3,-0.5,-1],
		[0.5,-0.5,0.5,0.5,-1,0.5],
		[0,0,0,0,0,0],
		[0.5,0.5,-0.5,0.5,0.5,0], [1,2,0,2]]

snowflake=[[1.0/3,0,0,1.0/3,0,0],
		[1.0/3,0,0,1.0/3,2.0/3,0],
		[-1.0/6,sqrt(3)/6,sqrt(3)/6,1.0/6,2.0/3,0],
		[-1.0/6,-sqrt(3)/6,-sqrt(3)/6,1.0/6,0.5,sqrt(3)/6],[1,1,1,1]]

matrices=np.zeros((4,6))

def barnsley_fern():
	
	m=Barnsley[0:4]
	P=Barnsley[4]
	originsX.set(0.5)
	originsY.set(0.9)
	Xscale.set(50)
	Yscale.set(50)
	for i in range(4):
		create_case()
	for i in range(24):
		function_entries[i].set(m[i/6][i%6])
	entry_case()
	for i in range(4):
		probEntry[i].set(P[i])
		reset_entries(i)
	
def serpinski_triangle():
	
	m=Triangle[0:4]
	P=Triangle[4]

	originsX.set(0.3)
	originsY.set(0.6)
	Xscale.set(300)
	Yscale.set(300)
	
	for i in range(4):
		create_case()
	for i in range(24):
		function_entries[i].set(m[i/6][i%6])
	entry_case()
	for i in range(4):
		probEntry[i].set(P[i])
		reset_entries(i)
	
def pyth_tree():
	
	m=Pythagorean_tree[0:4]
	P=Pythagorean_tree[4]
	originsX.set(0.6)
	originsY.set(0.5)
	Xscale.set(150)
	Yscale.set(150)
	for i in range(4):
		create_case()
	for i in range(24):
		function_entries[i].set(m[i/6][i%6])
	entry_case()
	for i in range(4):
		probEntry[i].set(P[i])
		reset_entries(i)
	
	
def koch_curve():
	m=snowflake[0:4]
	P=snowflake[4]
	originsX.set(0.2)
	originsY.set(0.6)
	Xscale.set(500)
	Yscale.set(500)
	for i in range(4):
		create_case()
	for i in range(24):
		function_entries[i].set(m[i/6][i%6])
	entry_case()
	for i in range(4):
		probEntry[i].set(P[i])
		reset_entries(i)

def generate_image():
	global save_entry
	global image_save_window
	image_save_window=Tkinter.Toplevel()
	picture_name=Tkinter.StringVar()
	picture_name.set("fractal.jpg")
	save_entry=Tkinter.Entry(image_save_window,width="15",textvariable=picture_name)
	save_button=Tkinter.Button(image_save_window, text= "Save",command=save_picture)
	save_entry.pack()
	save_button.pack()
		

	#fig = plt.figure(1)
	#ax = fig.add_subplot(111, axisbg='black')
	#plt.figure()
	#ax.scatter(XYC[0],XYC[1], s=.1,edgecolor=XYC[2])
	#plt.show()

def save_picture():
	global save_entry
	global image_save_window
	fractalCanvas.postscript(file=save_entry.get(), colormode='color')
	save_image=Image.new("RGB",(W,H))
	draw=ImageDraw.Draw(save_image)
	startingX=float(start_X_point.get())*W
	startingY=float(start_Y_point.get())*H
	for i in range(len(XYC[0])):
		x=startingX+float(scale_X_point.get())*XYC[0][i]
		y=startingY-float(scale_X_point.get())*XYC[1][i]
		draw.point([x,y],XYC[2][i])

	save_image=ImageEnhance.Color(save_image).enhance(1.0)
	save_image=ImageEnhance.Sharpness(save_image).enhance(1.5)
	filename=save_entry.get()

	
	save_image.save(filename)

	image_save_window.destroy()	

samples=Tkinter.Menubutton(FractalWindow, text="samples")
samples.menu=Tkinter.Menu(samples, tearoff = 0)
samples["menu"]=samples.menu
samples.menu.add_command(label="Barnsley Fern", command = barnsley_fern)
samples.menu.add_command(label="Serpinski Triangle", command = serpinski_triangle)
samples.menu.add_command(label="Pythagorean Tree", command = pyth_tree)
samples.menu.add_command(label="Koch Curve", command = koch_curve)

File=Tkinter.Menubutton(FractalWindow, text= "File")
File.menu=Tkinter.Menu(File, tearoff = 0)
File["menu"]=File.menu
File.menu.add_command(label="Save as picture", command=generate_image)

 #generates an identical image that can be saved as a jpeg file.


def motion(event): #monitors current location of mouse in cartesian coordinates
	x,y= event.x, event.y
	AxisX=float(AxisX_entry.get())
	AxisY=float(AxisY_entry.get())
	coordinates = "%.2f , %.2f" %((x-W/2)*AxisX/W,(-y+H/2)*AxisY/H)

	#drag_data["item"] = canvas.find_closest(event.x, event.y)[0]
        
	coords.configure(text = coordinates)
	

def clear(): #clears all squares in the plane
	global matrices
	global P
	

	canvas.delete("square")
	quads =[[0,0,0,0],
		[0,0,0,0],
		[0,0,0,0],
		[0,0,0,0]]

	matrices=np.zeros((4,6))
	for i in range(24):
		function_entries[i].set(0)
	
	create_square.configure(bg="gray85")
	stretch_square.configure(bg="gray85")
	move_square.configure(bg="gray85")
	skew_square.configure(bg="gray85")
	rotate_square.configure(bg="gray85")


	create_square.configure(activebackground="#ececec")
	stretch_square.configure(activebackground="#ececec")
	move_square.configure(activebackground="#ececec")
	skew_square.configure(activebackground="#ececec")
	rotate_square.configure(activebackground="#ececec")




#Gives settings for mouse clicks, indicates settings by color

FunctionLabels=[] #labels for functions, will match the transformations represented by
			#the four squares
for i in range(4):
	FunctionLabels=FunctionLabels+[Tkinter.Label(window,text="f"+str(i+1))]
	FunctionLabels[i].grid(row = 3+i, column= 0)

function_entries=[]

for i in range(4):
	for j in range(6):
        	s_var=Tkinter.StringVar()
        	function_entries.append(s_var)
       		k=Tkinter.Entry(window, width="5", textvariable = s_var, bg=square_count[i%4])
		s_var.set(matrices[i][j])
		k.grid(row=3+i,column=j+1)



def create_case(): #makes a new square, 
		#or resets the square of some color to the unit square
	
	create_square.configure(bg="gold")

	create_square.configure(activebackground="light goldenrod")
	stretch_square.configure(activebackground="#ececec")
	move_square.configure(activebackground="#ececec")
	skew_square.configure(activebackground="#ececec")
	rotate_square.configure(activebackground="#ececec")

	global tick
	global quads

	#deletes old rectangle

	canvas.delete(quads[tick][0])
	canvas.delete(quads[tick][1])
	canvas.delete(quads[tick][2])
	canvas.delete(quads[tick][3])

	#creates new unit square in place of the old rectangle
	quads[tick]=[canvas.create_line(W/2, H/2, W/2+W/AxisX, H/2, 
		fill=square_count[tick], tags= ["square",tick, "bottom line"] ),
	canvas.create_line(W/2+W/AxisX, H/2, W/2+W/AxisX, H/2-W/AxisY, 
		fill=square_count[tick], tags= ["square",tick, "right line"] ),
	canvas.create_line( W/2+W/AxisX, H/2-W/AxisY,  W/2, H/2-W/AxisY, 
                fill=square_count[tick], tags= ["square", tick, "top line"] ),
	canvas.create_line(W/2, H/2 -W/AxisY, W/2, H/2, fill=square_count[tick], tags= ["square",tick, "left line"]) ]

	matrices[tick]=[1,0,0,1,0,0]
	for i in range(6):
		function_entries[6*tick+i].set(matrices[tick][i])

	
	tick=(tick+1)%4
	
def stretch_case(): #indicates choice to set transformations on canvas to stretch
	create_square.configure(bg="gray85")
	stretch_square.configure(bg="LightBlue2")
	move_square.configure(bg="gray85")
	skew_square.configure(bg="gray85")
	rotate_square.configure(bg="gray85")

	create_square.configure(activebackground="#ececec")
	stretch_square.configure(activebackground="LightBlue1")
	move_square.configure(activebackground="#ececec")
	skew_square.configure(activebackground="#ececec")
	rotate_square.configure(activebackground="#ececec")


def move_case(): #indicates choice to set transformations to translations of rectangles

	create_square.configure(bg="gray85")
	stretch_square.configure(bg="gray85")
	move_square.configure(bg="green3")
	skew_square.configure(bg="gray85")
	rotate_square.configure(bg="gray85")

	create_square.configure(activebackground="#ececec")
	stretch_square.configure(activebackground="#ececec")
	move_square.configure(activebackground="green2")
	skew_square.configure(activebackground="#ececec")
	rotate_square.configure(activebackground="#ececec")


def skew_case(): #indicates choice to set transformations to skewing of rectangles

	create_square.configure(bg="gray85")
	stretch_square.configure(bg="gray85")
	move_square.configure(bg="gray85")
	skew_square.configure(bg="orchid3")
	rotate_square.configure(bg="gray85")
	
	create_square.configure(activebackground="#ececec")
	stretch_square.configure(activebackground="#ececec")
	move_square.configure(activebackground="#ececec")
	skew_square.configure(activebackground="orchid1")
	rotate_square.configure(activebackground="#ececec")


def rotate_case(): #indicates choice to set tranformations to rotation
	create_square.configure(bg="gray85")
	stretch_square.configure(bg="gray85")
	move_square.configure(bg="gray85")
	skew_square.configure(bg="gray85")
	rotate_square.configure(bg="dark orange")

	create_square.configure(activebackground="#ececec")
	stretch_square.configure(activebackground="#ececec")
	move_square.configure(activebackground="#ececec")
	skew_square.configure(activebackground="#ececec")
	rotate_square.configure(activebackground="orange")

def entry_case(): #changes linear transformations by changing the entries
	global matrices
	AxisX=float(AxisX_entry.get())
	AxisY=float(AxisY_entry.get())
	for i in range(4):
		if quads[i]!=[0,0,0,0]:
			Tx=float(function_entries[6*i+4].get())*W/AxisX +W/2
			Ty=-float(function_entries[6*i+5].get())*H/AxisY +H/2
			Dx1=float(function_entries[6*i].get())*W/AxisX
			Dy1=-float(function_entries[6*i+1].get())*H/AxisY
			Dx2=float(function_entries[6*i+2].get())*W/AxisX
			Dy2=-float(function_entries[6*i+3].get())*H/AxisY
		
			canvas.coords(quads[i][0],Tx,Ty,Tx+Dx1,Ty+Dy1)
			canvas.coords(quads[i][1],Tx+Dx1,Ty+Dy1,Tx+Dx1+Dx2,Ty+Dy1+Dy2)
			canvas.coords(quads[i][2],Tx+Dx1+Dx2,Ty+Dy1+Dy2,Tx+Dx2,Ty+Dy2)
			canvas.coords(quads[i][3],Tx+Dx2,Ty+Dy2,Tx,Ty)

			reset_entries(i)

	print matrices

def clickDown(event): #finds closest line or corner of rectangle

	
	
	drag_data["item"] = list(Tkinter.Canvas.find(canvas,'closest',event.x,event.y))[0]
       	drag_data["x"] = event.x
       	drag_data["y"] = event.y
	

def reset_entries(m):  #resets the matrix entries according to transformations

	AxisX=float(AxisX_entry.get())
	AxisY=float(AxisY_entry.get())
	
	global matrices
	matrices[m][0]=(canvas.coords(quads[m][0])[2]-canvas.coords(quads[m][0])[0])*AxisX/W
	matrices[m][1]=-(canvas.coords(quads[m][0])[3]-canvas.coords(quads[m][0])[1])*AxisY/H
	matrices[m][2]=-(canvas.coords(quads[m][3])[2]-canvas.coords(quads[m][3])[0])*AxisX/W
	matrices[m][3]=(canvas.coords(quads[m][3])[3]-canvas.coords(quads[m][3])[1])*AxisY/H
	matrices[m][4]=(canvas.coords(quads[m][0])[0]-W/2)*AxisX/W
	matrices[m][5]=-(canvas.coords(quads[m][0])[1]-H/2)*AxisY/H

	for i in range(6):
		function_entries[6*m+i].set(matrices[m][i])		 
	
def holdButtonDown(event): #defines transformations for each case

	if move_square['bg']=="green3" and drag_data["item"] not in [1,2]:
	#translates chosen rectangle in the direction of the mouse

		m=int(canvas.gettags(drag_data["item"])[1])
		delta_x = event.x - drag_data["x"]
        	delta_y = event.y - drag_data["y"]
		n = drag_data["item"]%4

		for i in range(4):	
        		canvas.move(quads[m][i], delta_x, delta_y)
		matrices[m][4]=matrices[m][4]+delta_x*AxisX/W
		function_entries[6*m+4].set(matrices[m][4])
		matrices[m][5]=matrices[m][5]-delta_y*AxisY/H
		function_entries[6*m+5].set(matrices[m][5])
        	drag_data["x"] = event.x
        	drag_data["y"] = event.y

	elif stretch_square['bg']=="LightBlue2": 
	#stretches transformation in vertical and horizontal directions, may give diagonal direction as well

		if  drag_data["item"] not in [1,2]:
			m=int(canvas.gettags(drag_data["item"])[1])
			delta_x = event.x - drag_data["x"]
        		delta_y = event.y - drag_data["y"]
			[px,py]=Projection(drag_data["item"],delta_x,delta_y)
			n = drag_data["item"]%4			

			if n==3:
				[x1,y1,x2,y2]=canvas.coords(drag_data["item"])
				[a1,b1,a2,b2]=canvas.coords(drag_data["item"]+1)
				[c1,d1,c2,d2]=canvas.coords(drag_data["item"]+3)
				canvas.coords(drag_data["item"],x1+px,y1+py,x2+px,y2+py)
				canvas.coords(drag_data["item"]+1,a1+px,b1+py,a2,b2)
				canvas.coords(drag_data["item"]+3,c1,d1,c2+px,d2+py)
				reset_entries(m)
				
			elif n==2:
				[x1,y1,x2,y2]=canvas.coords(drag_data["item"])
				[a1,b1,a2,b2]=canvas.coords(drag_data["item"]-3)
				[c1,d1,c2,d2]=canvas.coords(drag_data["item"]-1)
				canvas.coords(drag_data["item"],x1+px,y1+py,x2+px,y2+py)
				canvas.coords(drag_data["item"]-3,a1+px,b1+py,a2,b2)
				canvas.coords(drag_data["item"]-1,c1,d1,c2+px,d2+py)
				reset_entries(m)

			else:
				[x1,y1,x2,y2]=canvas.coords(drag_data["item"])
				[a1,b1,a2,b2]=canvas.coords(drag_data["item"]+1)
				[c1,d1,c2,d2]=canvas.coords(drag_data["item"]-1)
				canvas.coords(drag_data["item"],x1+px,y1+py,x2+px,y2+py)
				canvas.coords(drag_data["item"]+1,a1+px,b1+py,a2,b2)
				canvas.coords(drag_data["item"]-1,c1,d1,c2+px,d2+py)
				reset_entries(m)
			

			drag_data["x"] = event.x
        		drag_data["y"] = event.y
	elif rotate_square['bg']=="dark orange" and drag_data["item"] not in [1,2]: 		#rotates figure around its center clockwise, so far can't do counterclockwise

		m=int(canvas.gettags(drag_data["item"])[1])
		c=center(quads[m][0],quads[m][2])
		c1=[drag_data["x"]-c[0], c[1]-drag_data["y"]]
		c2=[event.x-c[0], c[1]-event.y]
		[cs,sn]=trigs(c1,c2)

		a=[]
		for i in range(4):
			a=a+[canvas.coords(quads[m][i])]
		
		for i in range(4):	
			canvas.coords(quads[m][i],(a[i][0]-c[0])*cs-(a[i][1]-c[1])*sn+c[0],
						(a[i][0]-c[0])*sn +(a[i][1]-c[1])*cs+c[1],
						(a[i][2]-c[0])*cs-(a[i][3]-c[1])*sn+c[0],
						(a[i][2]-c[0])*sn +(a[i][3]-c[1])*cs+c[1])
		reset_entries(m)
        	drag_data["x"] = event.x
        	drag_data["y"] = event.y
		
	elif skew_square['bg']=="orchid3" and type(drag_data["item"])==int:
	#skews rectangle by moving chosen side with the mouse, while fixing opposite side,
	#and stretching adjacent sides in the same direction as mouse

		m=int(canvas.gettags(drag_data["item"])[1])
		delta_x = event.x - drag_data["x"]
        	delta_y = event.y - drag_data["y"]
		n = drag_data["item"]%4

		if n==3:
			[a1,b1,a2,b2]=canvas.coords(drag_data["item"]+1)
			[c1,d1,c2,d2]=canvas.coords(drag_data["item"]+3)
			canvas.move(drag_data["item"], delta_x, delta_y)
			canvas.coords(drag_data["item"]+1,a1+delta_x,b1+delta_y,a2,b2)
			canvas.coords(drag_data["item"]+3,c1,d1,c2+delta_x,d2+delta_y)
			
		elif n==2:
			[a1,b1,a2,b2]=canvas.coords(drag_data["item"]-3)
			[c1,d1,c2,d2]=canvas.coords(drag_data["item"]-1)
			canvas.move(drag_data["item"], delta_x, delta_y)
			canvas.coords(drag_data["item"]-3,a1+delta_x,b1+delta_y,a2,b2)
			canvas.coords(drag_data["item"]-1,c1,d1,c2+delta_x,d2+delta_y)
			

		else:
			
			[a1,b1,a2,b2]=canvas.coords(drag_data["item"]+1)
			[c1,d1,c2,d2]=canvas.coords(drag_data["item"]-1)
			canvas.move(drag_data["item"], delta_x, delta_y)
			canvas.coords(drag_data["item"]+1,a1+delta_x,b1+delta_y,a2,b2)
			canvas.coords(drag_data["item"]-1,c1,d1,c2+delta_x,d2+delta_y)

		reset_entries(m)
		drag_data["x"] = event.x
        	drag_data["y"] = event.y
		
		
		
def ButtonRelease(event):
        '''End drag of an object'''
        # reset the drag information
        drag_data["item"] = None
        drag_data["x"] = 0
        drag_data["y"] = 0

def Projection(side,cx,cy): #gives direction for proper stretching of rectangle:
# u is the closest side,  c0 is the starting point, c is current cursor position
	s=canvas.coords(side)
	[ux,uy]=[s[3]-s[1],s[0]-s[2]]
	m=ux*cx+uy*cy
	n=ux*ux+uy*uy
	return [m*ux/n,m*uy/n]

def center(l1,l3): #computes the center of the parallelogram 
		#representing the transformation
	[x1,y1]=canvas.coords(l1)[0:2]
	[a1,b1]=canvas.coords(l3)[0:2]
	return [(x1+a1)/2,(y1+b1)/2]

def trigs(c1,c2): #computes the sin(theta) and cos(theta) for rotations
	nc1=c1[0]*c1[0]+c1[1]*c1[1]
	nc2=c2[0]*c2[0]+c2[1]*c2[1]
	dotc12=c1[0]*c2[0]+c1[1]*c2[1]
	orient_check=-c1[1]*c2[0]+c1[0]*c2[1]
	cosine=dotc12/sqrt(nc1*nc2)
	if orient_check>=0: return [cosine, -sqrt(1-cosine*cosine)]
	return [cosine, sqrt(1-cosine*cosine)]	
		
def createPoint(fractalCanvas, x0, y0, c):
	p=fractalCanvas.create_line(x0, y0+1, x0+1, y0, fill=c)
	return p



#function for generating the points of the fractal

def f(x,y,Probs):
	m=random();
	
	if m<Probs[0]: 
		return 	[matrices[0][0]*x+matrices[0][1]*y +matrices[0][4], 
					matrices[0][2]*x+matrices[0][3]*y +matrices[0][5], 						square_count[0]]
	

	for i in range(1,4):				
		if m>= sum(Probs[0:i]) and m<sum(Probs[0:i+1]):
			return [matrices[i][0]*x+matrices[i][1]*y +matrices[i][4], 
					matrices[i][2]*x+matrices[i][3]*y +matrices[i][5],
					 square_count[i]]
	

#generates the points on the fractalCanvas
def animate():
	global XYC
	#gives starting point, translates it to a starting point on the fractalCanvas
	xpoints=[0]  
	ypoints=[0]
	point_color=["black"]
	items=np.zeros(int(numpoints.get()))
	startingX=float(start_X_point.get())*W
	startingY=float(start_Y_point.get())*H
	

	Probs=[float(prob[0].get()),
		float(prob[1].get()),
		float(prob[2].get()),
		float(prob[3].get())]
	if sum(Probs) != 0: Probs=[p/sum(Probs) for p in Probs]
	
	fractalCanvas.update()

	for i in range(int(numpoints.get())):
		[x,y,c]=f(xpoints[-1],ypoints[-1],Probs);
		xpoints=xpoints+[x];
		ypoints=ypoints+[y];
		point_color=point_color+[c]
		items[i]=createPoint(fractalCanvas,startingX+float(scale_X_point.get())*x,
		startingY-float(scale_Y_point.get())*y, c)
		fractalCanvas.update()
	XYC[0]=XYC[0]+xpoints 
	XYC[1]=XYC[1]+ypoints 
	XYC[2]=XYC[2]+point_color


#removes all points from the Fractal canvas		
def clearFractal():
	global XYC
	fractalCanvas.delete("all")
	XYC=[[],[],[]]

# buttons on fractal canvas
clearFractal_button = Tkinter.Button(FractalWindow, text="clear", command=clearFractal)
start = Tkinter.Button(FractalWindow, text="start", command=animate)

# entries for number of generated points
numpoints=Tkinter.StringVar()
numpoints.set(`pointnum`)
stepLabel=Tkinter.Label(FractalWindow, width="15")
stepLabel.configure(text="Num Points= ")
stepentry=Tkinter.Entry(FractalWindow, width="15", textvariable=numpoints)

#entries for starting point of fractal, in terms of percentage of length/ width of canvas
originsX=Tkinter.StringVar()
originsX.set(FractalOriginX)
originsY=Tkinter.StringVar()
originsY.set(FractalOriginY)
start_X_point=Tkinter.Entry(FractalWindow, width="5",textvariable=originsX)
start_Y_point=Tkinter.Entry(FractalWindow, width="5",textvariable=originsY)
start_point_label=Tkinter.Label(FractalWindow, width="15",text="Start Point")

#entries for scaling.  The scaling takes the calculated values and scales them to a more reasonable pixel range.
Xscale=Tkinter.StringVar()
Xscale.set(scalingX)
Yscale=Tkinter.StringVar()
Yscale.set(scalingY)
scale_X_point=Tkinter.Entry(FractalWindow, width="5",textvariable=Xscale)
scale_Y_point=Tkinter.Entry(FractalWindow, width="5",textvariable=Yscale)
scale_label=Tkinter.Label(FractalWindow, width="15",text="Scaling")

# entries for axis ranges in the main window.  the values correspond to the number of units ranging accross the canvas both horizontally and vertically
XAxis=Tkinter.DoubleVar()
XAxis.set(AxisX)
YAxis=Tkinter.DoubleVar()
YAxis.set(AxisY)
AxisX_entry=Tkinter.Entry(window, width="5",textvariable=XAxis)
AxisY_entry=Tkinter.Entry(window, width="5",textvariable=YAxis)
Axes_label=Tkinter.Label(window, width="15",text="Axes")


#entries for the probabilities of linear transformations
probEntry=[]
prob=[]
for i in range(4):
	V=Tkinter.StringVar()
	probEntry.append(V)
	prob.append(Tkinter.Entry(window, width= "5", textvariable = V))
	V.set(P[i])
	prob[i].grid(row=3+i,column=7)
	

probLabel=Tkinter.Label(window, width="9")
probLabel.configure(text="probabilities")


#puts widgets in the Attractor window
samples.grid(row=0)
File.grid(row=0, column=1)
fractalCanvas.grid(row=1, columnspan=11,sticky="nsew")
start.grid(row=2, column=10)
clearFractal_button.grid(row=2,column=9)
stepLabel.grid(row=2,column=0)
stepentry.grid(row=2,column=1)
start_point_label.grid(row=2,column=2)
start_X_point.grid(row=2,column=3)
start_Y_point.grid(row=2,column=4)
scale_label.grid(row=2,column=5)
scale_X_point.grid(row=2,column=6)
scale_Y_point.grid(row=2,column=7)




# binds mouse events to specific windows and canvas
window.bind('<Motion>',motion)
canvas.bind('<ButtonPress-1>',clickDown)
canvas.bind('<B1-Motion>', holdButtonDown)
canvas.bind('<ButtonRelease-1>', ButtonRelease)

# defines buttons in the transformation window
clear_button = Tkinter.Button(window, text="clear", command=clear)
create_square = Tkinter.Button(window, text="square", width= "7", command=create_case)
stretch_square = Tkinter.Button(window, text="stretch", width= "7", command=stretch_case)
move_square = Tkinter.Button(window, text="move", width ="7", command=move_case)
skew_square = Tkinter.Button(window, text="skew", width= "7", command=skew_case)
rotate_square = Tkinter.Button(window, text="rotate", width = "7", command=rotate_case)
entry_square= Tkinter.Button(window, text="entries", width = "7",command=entry_case)




s=canvas.create_line(W/2, 0, W/2, H, fill="#FFFFFF", tags = "line")
s2=canvas.create_line(0, H/2, W, H/2, fill="#FFFFFF", tags = "line")
canvas.grid(row=0, columnspan=13, sticky="nsew")
coords.grid(row = 1,column=0,sticky="w")

create_square.grid(row = 1, column = 1,columnspan=2, sticky="we")
stretch_square.grid(row =1, column=3,columnspan=2, sticky="we")
move_square.grid(row =1, column=5, columnspan=2, sticky="we")
skew_square.grid(row =1, column=7, columnspan=2, sticky="we")
rotate_square.grid(row =1, column=9, columnspan=2, sticky="we")
entry_square.grid(row = 2, column = 11,columnspan=2)

probLabel.grid(row=2, column=7)

clear_button.grid(row=1, column=11,columnspan=2, sticky="e")
Axes_label.grid(row=3,column=11,columnspan=2)
AxisX_entry.grid(row=4,column=11)
AxisY_entry.grid(row=4,column=12)

print type(AxisX_entry.get())
print type(AxisX_entry['textvariable'])



window.mainloop()


