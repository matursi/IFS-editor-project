import Tkinter
import itertools
from math import sqrt
import time
from numpy.random import random
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageEnhance
import os


#lists of variables:

#	W: width of screens in pixels
#	H: height of screens in pixels
# 	FractalOriginX: gives starting X point of attractor from range of 0 to 1
# 	FractalOriginY: gives starting Y point of attractor from range of 0 to 1
# 	ScalingX and ScalingY: scales attractors from calculate coordinates to pixel friendly coordinates
#	Axis X and Axis Y: gives number of units from left to right, top to bottom of cartesian plane

#	window: a window widget for setting up IFS
#	FractalWindow: a window widget for generating attractor
#	fractalCanvas:	canvas for attractor
#	canvas: canvas for IFS
#	widgetCanvas: canvas for which to place matrix entries to enable scrolling
#	frame: placed inside widgetCanvas, contains widgets
#	frame2: contains widgetCanvas, localizes scrolling
#	scroll: placed in frame 2, a scroll bar for the entries

#	tick: tells which square to create
#	quads
#	matrices
#	number_functions
#	XYC
#	records
#	front_records



#	Barnsley
#	Triangle
#	Pythagorean_tree
#	Snowflake
#	serpinski_carpet
#	P
#	square_count
#	drag_data
#	pointnum
#	

	

W=800
H=800
FractalOriginX=0.5
FractalOriginY=0.6
scalingX=50
scalingY=50

AxisX= 10.0
AxisY= 10.0

#creates window for the Iterated function Editor with the default width and height specifications.
#TKinter.Canvas enables space where graphic activity occurs
window= Tkinter.Tk()
window.title("Iterated Function System Editor")
canvas = Tkinter.Canvas(window, width=W, height=H, background="black")

#creates window where attractor will appear
FractalWindow= Tkinter.Toplevel()
FractalWindow.title("Attractor")
fractalCanvas = Tkinter.Canvas(FractalWindow, width=W, height=H, background="black")


# Create frame for IFS window.  Frames allow the grouping of different kinds of "widgets" into more complex formats.
# this frame will be on the top, with color gray85, and borderwidth = 0
frame2=Tkinter.Frame(window,background="gray85", bd=0)

#Create frames where entries and scrollbar will appear.  
widgetCanvas=Tkinter.Canvas(frame2,borderwidth=0, bg="gray85",height = 75)

#frame specifically for the entries
frame=Tkinter.Frame(widgetCanvas,background="gray85",bd=0)
frame.rowconfigure(1, weight=1)
frame.columnconfigure(1, weight=1)

#make scrollbar: this is to keep the size of the IFS window the same, but to allow for more functions in IFS
scroll=Tkinter.Scrollbar(frame2, orient="vertical", command=widgetCanvas.yview)

#configure command for scrolling, place it on left hand side of entries general frame
widgetCanvas.configure(yscrollcommand=scroll.set)
widgetCanvas.create_window((0,0), window=frame, anchor="nw")
frame2.grid_rowconfigure(0, weight=1)
frame2.grid_columnconfigure(0, weight=1)


#make entire region of canvases visible (otherwise real window size is smaller than height and width specified)
def onFrameConfigure(Canvas_X):
	Canvas_X.configure(scrollregion=Canvas_X.bbox("all"))

frame.bind("<Configure>", lambda event, Canvas_X=widgetCanvas: onFrameConfigure(Canvas_X))
frame.update_idletasks()

#widgetCanvas.configure(scrollregion=frame.bbox("all"), height =100)

#make a box that shows coordinates of point where mouse is on the cartesian plane in IFS editor
coords = Tkinter.Label(window, width="10")




global tick
global quads
global matrices
global number_functions
global XYC
global records
global front_records



global Barnsley
global Triangle
global Pythagorean_tree
global Snowflake
global serpinski_carpet

# sets initial number of functions in IFS
number_functions=4

matrices=np.zeros((4,6))

#gives probabilities for each iterated function in p.d.f. form.  The Default is 1/4 for each vector

P=[0, 0, 0, 0]

# gives x coordinates, y coordinates, and colors of points in attractor
XYC=[[],[],[]]

#latest IFS configurations.  If you undo from records, will record the last bit before the undoing and will be used
#if you want to redo a previously undone actions
front_records=[]

#records will contain a history of all configurations.  (This is to allow undoing and redoing
records=[[np.zeros((4,6)),P,number_functions]]

# gives colors of squares giving graphic representation of IFS
square_count={0:'#00FFFF', 1:'#FF00FF', 2:'#FFFF00', 3: '#90FF00',
		4:'#FF9000', 5:'#00FF90', 6:'#0090FF', 7:'#9000FF'}

#tracks position of mouse on x and y axes of canvas when clcking on an object
drag_data = {"x": 0, "y": 0, "item": None}

#when using create button, tick tells which function to make into "idenity" function, represented by square.
# tick = n makes n+1 ^th function identity.  
tick=0

# quads will contain info on graphic representations of functions
quads =[[0,0,0,0],
	[0,0,0,0],
	[0,0,0,0],
	[0,0,0,0]]



#number of points to be generated, default set at 10000
pointnum=10000;

#colors that will be used throughout
colors=["red","green","yellow","orange"]

#a collection of sample fractals.  These will be loaded into the IFS window

#Barnsley fern
Barnsley=[[0.85, 0.04,-0.04,.85,0,1.6], #lists linear transformations, 
	[0.2,-0.26,0.23,0.22,0,1.60],	#values 1,2, 5 give a,b,c with a*x+b*y +c = new_x
	[-0.15,0.28,0.26,0.24,0,0.44],	#values 3,4, 6 give a,b,c with a*x+b*y +c = new_y
	[0,0,0,.16,0,0], [85,7,7,1]]   	 #The last line gives relative probabilities
					
#Serpinski triangle
Triangle=[[0.5,0,0,0.5,0,0],
	[0.5,0,0,0.5,0.5, 0],
	[0.5,0,0,0.5,0.25,sqrt(3)*0.25],[1,1,1]]

# Pythagorean tree
Pythagorean_tree=[[0,0,0,1.0/3,-0.5,-1],
		[0.5,-0.5,0.5,0.5,-1,0.5],
		[0,0,0,0,0,0],
		[0.5,0.5,-0.5,0.5,0.5,0], [1,2,0,2]]
# Koch snowflake (with four functions)
snowflake=[[1.0/3,0,0,1.0/3,0,0],
		[1.0/3,0,0,1.0/3,2.0/3,0],
		[-1.0/6,sqrt(3)/6,sqrt(3)/6,1.0/6,2.0/3,0],
		[-1.0/6,-sqrt(3)/6,-sqrt(3)/6,1.0/6,0.5,sqrt(3)/6],[1,1,1,1]]
# seprinski carpet
serpinski_carpet=[[1.0/3, 0 , 0, 1.0/3 , 1, 0],
		[1.0/3, 0 , 0, 1.0/3 , 1, 1],
		[1.0/3, 0 , 0, 1.0/3 , 0, 1],
		[1.0/3, 0 , 0, 1.0/3 , -1, 1],
		[1.0/3, 0 , 0, 1.0/3 , -1, 0],
		[1.0/3, 0 , 0, 1.0/3 , -1, -1],
		[1.0/3, 0 , 0, 1.0/3 , 0, -1],
		[1.0/3, 0 , 0, 1.0/3 , 1, -1], [1,1,1,1,1,1,1,1]]

#function calls for generations of sample functions.  I will document only the Barnsley fern, but the others have
#similar configurations

def barnsley_fern():
	global P #take in Probability vector, to change values
	while number_functions < 4: #This adds missing function entries if the current amount is less than 4
		add_function()
	m=Barnsley[0:4]  #The matrix representing configuration of barnsley fern
	P=Barnsley[4]+[0]*(number_functions-4) # changes probability entries.  If number_functions > 4, probabilities of the
						# fifth and beyond functions is set to 0
	originsX.set(0.5)		#gives starting x,y pixel coordinates of attractor.  
	originsY.set(0.9)
	Xscale.set(50)			#gives scale for sizing the barnsley fern
	Yscale.set(50)
	for i in range(4):		#creates 4 unit squares, but does not record them in record history
		create_case()
		records.pop()
	for i in range(24):		#provides barnsley fern configuration for entries in first few functions
		function_entries[i].set(m[i/6][i%6])
	for j in function_entries[24:]: #sets entries of other functions to 0
		j.set(0)
	
	
	for i in range(number_functions): #sets probability entries with new probabilities
		probEntry[i].set(P[i])
	entry_case()
	for i in range(number_functions): #
		reset_entries(i)
	#records=records+[[m, P, number_functions]]
	
def serpinski_triangle():
	global P
	global records
	global front_records
	while number_functions<3:
		add_function()

	m=Triangle[0:3]
	P=Triangle[3]+[0]*(number_functions-3)

	originsX.set(0.3)
	originsY.set(0.6)
	Xscale.set(300)
	Yscale.set(300)
	
	for i in range(3):
		create_case()
		records.pop()
	for i in range(18):
		function_entries[i].set(m[i/6][i%6])
	for j in function_entries[18:]:
		j.set(0)

	for i in range(number_functions):
		probEntry[i].set(P[i])
	entry_case()
	for i in range(number_functions):
		reset_entries(i)
	#records=records+[[m, P,number_functions]]
def pyth_tree():
	global P
	global records
	global front_records
	while number_functions<4:
		add_function()

	m=Pythagorean_tree[0:4]
	P=Pythagorean_tree[4]+[0]*(number_functions)
	originsX.set(0.6)
	originsY.set(0.5)
	Xscale.set(150)
	Yscale.set(150)
	for i in range(4):
		create_case()
		records.pop()
	for i in range(24):
		function_entries[i].set(m[i/6][i%6])
	for j in function_entries[24:]:
		j.set(0)
	for i in range(number_functions):
		probEntry[i].set(P[i])
	entry_case()
	for i in range(number_functions):
		reset_entries(i)
	#records=records+[[m, P, number_functions]]
	
def koch_curve():
	global P
	global records
	global front_records

	while number_functions <4:
		add_function()
	m=snowflake[0:4]
	P=snowflake[4]+[0]*(number_functions-4)
	originsX.set(0.2)
	originsY.set(0.6)
	Xscale.set(500)
	Yscale.set(500)
	for i in range(4):
		create_case()
		records.pop()
	for i in range(24):
		function_entries[i].set(m[i/6][i%6])
	for j in function_entries[24:]:
		j.set(0)
	
	
	for i in range(number_functions):
		probEntry[i].set(P[i])
	entry_case()
	for i in range(number_functions):
		reset_entries(i)
	#records=records+[[m, P,number_functions]]
	#front_records=[]

def carpet():
	global P
	global records
	global front_records

	while number_functions < 8:
		add_function()
	m=serpinski_carpet[0:8]
	P=serpinski_carpet[8]
	originsX.set(0.5)
	originsY.set(0.5)
	Xscale.set(150)
	Yscale.set(150)
	numpoints.set(40000)

	for i in range(8):
		create_case()
		records.pop()
	for i in range(48):
		function_entries[i].set(m[i/6][i%6])
	
	for i in range(number_functions):
		probEntry[i].set(P[i])
	entry_case()
	for i in range(number_functions):
		reset_entries(i)
	#records=records+[[m, P,number_functions]]
	#front_records=[]

# this function will be used as part of the process of saving functions.  It creates a window where you can enter the name of
# the fractal you generated in the attractor and save the image.
def generate_image():
	global save_entry #name of entry widget
	global image_save_window #name of save window
	image_save_window=Tkinter.Toplevel() #creates window for inputting name of function and saving.
	picture_name=Tkinter.StringVar() #creates name of of string accessed in save_entry
	picture_name.set("fractal.png") #sets default name as fractal.png
	save_entry=Tkinter.Entry(image_save_window,width="15",textvariable=picture_name)
	save_button=Tkinter.Button(image_save_window, text= "Save",command=save_picture) #calls the save_picture function
											#defined below
	#puts entry space for name and save button into window
	save_entry.pack()
	save_button.pack()
		

	#fig = plt.figure(1)
	#ax = fig.add_subplot(111, axisbg='black')
	#plt.figure()
	#ax.scatter(XYC[0],XYC[1], s=.1,edgecolor=XYC[2])
	#plt.show()

def save_picture():
	global save_entry #calls in save_entry and image_save_window
	global image_save_window
	fractalCanvas.postscript(file=save_entry.get(), colormode='color') #gets name inside save_entry that user typed
									#which will be used as name of image file
	#gives name of image, with coordinates in RGB form, and width and height default
	save_image=Image.new("RGB",(W,H))
	draw=ImageDraw.Draw(save_image)
	
	#converts [0,1] coordinates into pixel coordinates
	startingX=float(start_X_point.get())*W
	startingY=float(start_Y_point.get())*H
	for i in range(len(XYC[0])): #draws each point in the attractor
		x=startingX+float(scale_X_point.get())*XYC[0][i]  #x values are left to right.
		y=startingY-float(scale_X_point.get())*XYC[1][i] #y values are up to down, hence subtraction
		draw.point([x,y],XYC[2][i]) #draws point of cover

	save_image=ImageEnhance.Color(save_image).enhance(1.0)  #image enhancements to make picture look more like that
								# of the image in the attractor
	save_image=ImageEnhance.Sharpness(save_image).enhance(1.5)
	
	#saves image and then closes save window
	filename=save_entry.get()
	save_image.save(filename)
	image_save_window.destroy()	

# creates a menu in the attractor window that contains buttons, which when pressed, will give the configuration of the
# chosen fractal in the IFS window. 
samples=Tkinter.Menubutton(FractalWindow, text="samples")
samples.menu=Tkinter.Menu(samples, tearoff = 0)
samples["menu"]=samples.menu
samples.menu.add_command(label="Barnsley Fern", command = barnsley_fern)
samples.menu.add_command(label="Serpinski Triangle", command = serpinski_triangle)
samples.menu.add_command(label="Pythagorean Tree", command = pyth_tree)
samples.menu.add_command(label="Koch Curve", command = koch_curve)
samples.menu.add_command(label="Serpinski Carpet", command=carpet)

# Adds a "file" menu in the attractor window, where you can save pictures
File=Tkinter.Menubutton(FractalWindow, text= "File")
File.menu=Tkinter.Menu(File, tearoff = 0)
File["menu"]=File.menu
File.menu.add_command(label="Save as picture", command=generate_image)


# puts entries for the probabilities of linear transformations in entry frame
#and sets points to default P (here it was just a row of 0s)
probEntry=[]
prob=[]
for i in range(4):
	V=Tkinter.StringVar()
	probEntry.append(V)
	prob.append(Tkinter.Entry(frame, width= "5", textvariable = V))
	V.set(P[i])
	prob[i].grid(row=1+i,column=7)
	
#creates a label for probability 
probLabel=Tkinter.Label(frame, width="9")
probLabel.configure(text="probabilities")

#Gives settings for mouse clicks, indicates settings by color

FunctionLabels=[] #labels for functions, will match the transformations represented by
			#the four squares
for i in range(number_functions):
	FunctionLabels=FunctionLabels+[Tkinter.Label(frame,text="f"+str(i+1))]
	FunctionLabels[i].grid(row = 1+i, column= 0) #label location in entry frame

# function_entries is a list that will contain TKinter entry variables that you can call to get string inputs
function_entries=[]
# func is a list of the actual entry widgets
func=[]
for i in range(number_functions):
	for j in range(6):
        	s_var=Tkinter.StringVar()
        	function_entries.append(s_var)
       		func.append(Tkinter.Entry(frame, width="5", textvariable = s_var, bg=square_count[i%4]))
		s_var.set(matrices[i][j])
		func[-1].grid(row=1+i,column=j+1)


# function that generates a new line of function entries (these are six entries, representing a linear function
def add_function():
	global matrices
	global quads
	global tick
	global number_functions
	global FunctionLabels
	global P
	global records
	#?

	#sets limit of adding new functions at 8
	if number_functions==8:
		return 1

	number_functions+=1
	P=np.append(P,0)
	matrices=np.append(matrices,[0,0,0,0,0,0]).reshape(number_functions,6) #adds new function data
	
	#adds new line for "line" objects representing the quadrilateral formed by the linear function configuration
	quads=quads+[[0,0,0,0]]
	
	a=tick
	
	
	#adds new entry string variables to function_entries, adds new entry widgets to func
	for j in range(6):
        	s_var=Tkinter.StringVar()
        	function_entries.append(s_var)
       		func.append(Tkinter.Entry(frame, width="5", textvariable = s_var, bg=square_count[number_functions-1]))
		func[-1].grid(row=number_functions+4,column=j+1)
		
	#generates new label for latest function
	FunctionLabels=FunctionLabels+[Tkinter.Label(frame,text="f"+str(number_functions))]
	FunctionLabels[-1].grid(row = 4+number_functions, column= 0)

	#generates new probability entry, and adds new element to probability matrix
	V=Tkinter.StringVar()
	probEntry.append(V)
	prob.append(Tkinter.Entry(frame, width= "5", textvariable = V))
	V.set(P[number_functions-1])
	prob[-1].grid(row=number_functions+4,column=7)	
	
	#makes newest function, creates a square for it, removes latest configuration of identity square creation
	tick_number.set(number_functions-1)
	create_case()
	records.pop()

	#turns square into point, so it does not appear as image of an identity function
	matrices[number_functions-1]=np.array([0,0,0,0,0,0]) #gives configuration for point, sets entries all to 0
	for j in range(6*(number_functions-1),6*number_functions):
		function_entries[j].set(0)
	entry_case() #makes indentity square into point
	reset_entries(number_functions-1) 
	tick_number.set(a) #changes tick back to its original value
	records.pop() #remove  latest configuration for undoing records
	print records[-1]

	return 1
# removes a function entry line from the entry frame
def remove_function():
	global matrices
	global quads
	global number_functions
	global FunctionLabels
	global records
	global front_records
	global P

	#must maintain at least two function entriy lines
	if number_functions==2:
		return 1
	
	# set number of functions to 1 less, delete the square representing last function in IFS
	number_functions-=1
	canvas.delete(quads[-1][0])
	canvas.delete(quads[-1][1])
	canvas.delete(quads[-1][2])
	canvas.delete(quads[-1][3])

	quads.pop() #delete label names for last square
	matrices=matrices[0:-1] #remove last row in function entry data
	
	FunctionLabels[-1].destroy() #remove function label in window
	FunctionLabels.pop() 

	probEntry.pop() #remove last probablity entry widget
	prob[-1].destroy()
	prob.pop() #remove probability data for last function
	P=P[0:-1] 
	
	#remove function entries and records of them
	for k in range(6):
		func[-1].destroy()
		function_entries.pop()
		func.pop()

	
	# add function removal to records, since this can change the IFS
	records=records+[[temporary_matrix(), P,number_functions]]
	# set front records to empty since you just made latest action
	front_records=[]
	print len(records), ',', len(front_records)

# Function that undoes any configuration. 
def undo_transformation():
	global matrices
	global records
	global front_records
	global number_functions

	#can't undo if you're at the beginning
	if len(records)==1: return 1

	#adds latest configuration to front_records, in case user wants to redo transformation
	F=front_records+[records[-1]]
	
	#removes last configuration from record history
	records.pop()

	# this is to show that the record changes were successful
	print " \n"

	print " "
	print number_functions, ',', records[-1][2]

	#If the previous configuration had more functions, add whatever function lines are necessary
	while number_functions<records[-1][2]:
		print "yes"
		add_function()
		#records.pop()
		
	#If they are less, remove functions, but also erase history of removal, since function removal adds to the record
	while number_functions > records[-1][2]:
		print "no"
		remove_function()
		records.pop()

	#change data to match previous configuration
	matrices=records[-1][0]
	P=records[-1][1]

	#set entries to previous configuration
	for i in range(number_functions):
		for j in range(6):
			function_entries[6*i+j].set(matrices[i][j])

	
	# change squares to match entry configuration, but remove history of entry change.
	entry_case()
	records.pop()
	
	#set front records to have data of undone transformation
	front_records=F
	
	#for j in range(number_functions):
	#	if quads[j]!=[0,0,0,0]:
	#		reset_entries(j)
	#	probEntry[j].set(P[j])

	#print records[-1]

	print len(records), ',', len(front_records)
	return 1

# If user wants to redo something undone, this function is called
def redo_transformation():
	global matrices
	global records
	global front_records 
	global number_functions

	#can't redo something if there is nothing to redo
	if front_records==[]: return 1
	
	#set A to be the last undone configuration which was recorded in front_records
	# let F be used as a place-holder for front_records, since later functions will make front_records empty
	A=front_records[-1]
	F=[]
	for a in front_records[0:-1]:
		F=F+[a]
	records=records+[front_records[-1]]
	front_records.pop()

	print "length of front records is ", len(front_records)

	#Simlar to undo case, if last configuration undone has more functions, add as many as necessary
	while number_functions<A[2]:
		print number_functions, ',', A[2]
		print "yes"
		add_function()
		#records.pop()
		
	# otherwise, if less, remove functions, and remove record history of function removal
	while number_functions > A[2]:
		print number_functions, ',', A[2]
		print "no"
		remove_function()
		records.pop()

	print "length of F is ", len(F), len(records)

	#set front_records to F, which preserved the undo history that we wanted
	front_records=F
	
	# set data configurations
	matrices=A[0]
	P=A[1]

	#change entry values
	for i in range(number_functions):
		for j in range(6):
			function_entries[6*i+j].set(matrices[i][j])

	#change squares to mathc entries, but remove record history
	entry_case()
	records.pop()
	
	front_records=F	

	print len(records), ',', len(front_records)

	return 1	

# a function call to save IFS data, so that you can recall it after having closed the IFS editor.  
# This function in particular opens the save window
def save_IFS():
	global function_name #name given to IFS configuration
	global Function_window #name of window

	#create save window and entry variable
	Function_window=Tkinter.Toplevel()
	function_name=Tkinter.StringVar()
	function_name.set("function") #give default name as "function"
	save_entry=Tkinter.Entry(Function_window,width="15",textvariable=function_name)
	savef_button=Tkinter.Button(Function_window, text= "Save",command=save_function)
	save_entry.pack()
	savef_button.pack()
		
	return 1
# function call to save a function.  The saved functions go into a file
def save_function():
	global function_name #name of function
	global number_functions
	global Function_window # function window that was created with save_IFS
	print 1
	
	#the following makes sure that function names form a single string
	A=function_name.get()
	print A
	#for i in range(A):
	#	if A[i]==' ': A[i]='_'

	#records function data: 
	#function_data contains the name and the number of functions in the IFS, 
	#the function data, and the probabilities for each function in the IFS.
	# these data points are separated by a space, which is why the function name should be a single string.
	
	function_data=[A+' ', str(number_functions)+' ']
	for a in function_entries:
		function_data=function_data+[str(a.get())+' ']
	for b in prob:
		function_data=function_data+[str(b.get())+' ']
	
	print function_data
	#Opens the saved function data file, 
	lines = open("Iterated_Function_Systems.txt", 'r').readlines()
	check=0
	
	#checks if IFS name was already used: if so, replaces old function data line with new one
	for i in range(len(lines)):
		if lines[i].split()[0]==A:
			lines[i]=''.join(tuple(function_data+['\n']))
			check=1
			break
	
	#writes new function data line into function, or overwrites file with edited data line
	if check==0:
		fo=open("Iterated_Function_Systems.txt",'a')
		fo.writelines(function_data+['\n'])
		fo.close()
	else:
		fo=open("Iterated_Function_Systems_tmp.txt",'w')
		fo.writelines(lines)
		fo.close()
		os.rename("Iterated_Function_Systems_tmp.txt","Iterated_Function_Systems.txt")
		
	#closes save window
	Function_window.destroy()
	return 1

#Creates loading window for loading IFSs.  
# type in the name of an IFS, and it will change the IFS configuration of the editor to 
# the configuration you loaded.
def load_IFS():
	global names			 #list of names of functions
	global Load_function_window 	 #name of load window
	global line_data 		 #lines of currently saved IFS data
	global load_entry_instance	 #stringvar containing load IFS name
	line_data=open("Iterated_Function_Systems.txt",'r').readlines()
	names=[]
	for line in line_data:
		names=names+[line.split()[0]]
	Load_function_window=Tkinter.Toplevel()
	print names
	
	#creates a frame containing the names of available saved functions
	function_big_grid=Tkinter.Frame(Load_function_window,background="white", bd=1)
	function_canvas=Tkinter.Canvas(function_big_grid,borderwidth=0,bg="white", height=150,width=450)
	
	#enables creation of grid where labels containing names will be placed
	function_grid=Tkinter.Frame(function_canvas,background="white", bd = 0)
	function_grid.rowconfigure(1,weight=1)
	function_grid.columnconfigure(1,weight=1)
	
	#creates scrollbars to scroll through IFS names
	name_vscroll=Tkinter.Scrollbar(function_big_grid, orient="vertical",command=function_canvas.yview)
	name_hscroll=Tkinter.Scrollbar(function_big_grid,orient="horizontal",command=function_canvas.xview)

	#enables function of both scrollbars
	function_canvas.configure(yscrollcommand=name_vscroll.set,xscrollcommand=name_hscroll.set)
	function_canvas.create_window((0,0), window=function_grid,anchor="nw")
	function_big_grid.grid_rowconfigure(0,weight=1)
	function_big_grid.grid_columnconfigure(0,weight=1)
	
	function_grid.bind("<Configure>", lambda event, Canvas_X=function_canvas: onFrameConfigure(Canvas_X))
	function_grid.update_idletasks()

	name_entry_strings=[] 	#list of stringvars for entries of labels
	name_entries=[]		# list of labels containing IFS names
	
	for i in range(len(names)):
		name_entry_strings=name_entry_strings+[Tkinter.StringVar()]
		name_entries=name_entries+[Tkinter.Label(function_grid, width="20",textvariable=name_entry_strings[i])]
		name_entry_strings[i].set(names[i])
		name_entries[-1].grid(column=i%3, row=int(i/3)) #layer names into three columns

	#puts grid into windows, with visible dimensions set
	function_big_grid.grid(row=0,column=0, columnspan=3, sticky="nsew")
	function_canvas.grid(row=0,column=0,rowspan=3,sticky="we")
	function_grid.place()
	name_vscroll.grid(row=0,column=1,sticky="ns")
	name_hscroll.grid(row=1,column=0, columnspan=2,sticky="ew")

	#creates entry for loading IFS name
	load_entry_instance=Tkinter.StringVar()
	load_entry=Tkinter.Entry(Load_function_window,width="20",textvariable=load_entry_instance)
	load_entry.grid(row=1,column=1)
	
	#creates load button for load window
	load_button=Tkinter.Button(Load_function_window, text="load IFS", width="20",command=load_function)
	load_button.grid(row=2,column=1)
	return 1

#call function for loading IFS
def load_function():
	global names
	global load_entry_instance
	global Load_function_window
	global number_functions
	global line_data
	global records
	global front_records
	global matrices
	global P

	chosen_name=load_entry_instance.get() #name of desired IFS
	
	#Gives error if chosen name not in list of saved IFS data
	warning_1_box=Tkinter.Text(fg="red")
	warning_1_box.tag_config("t",wrap="word",justify="center")
	if chosen_name not in names:
		text="chosen name is not in list of saved IFS's.  Type new entry."
		warning_1_box.insert(text, ("t"))
		warning_1_box.grid(row=3,sticky="ew")

	else:
		warning_1_box.forget()		#gets rid of warning_1_box, since there is no need for error
		i=names.index(chosen_name)	# locates inserted name among the IFS saved data lines
		function_data=line_data[i].split(' ')  #numerical data for IFS
		nf=int(function_data[1])		#number of functions for IFS

		while number_functions < nf:  #changes number of functions to those of chosen IFS
			add_function()
		while number_functions > nf:
			remove_function()
			records.pop()
		print function_data
		
		#change IFS data, change entries for probabilities and IFS data
		for i in range(number_functions):
			for j in range(6):
				matrices[i][j]=float(function_data[2+6*i+j])
				function_entries[6*i+j].set(matrices[i][j])
			P[i]=float(function_data[2+6*number_functions+i])
			probEntry[i].set(P[i])

		#change squares representing IFS data, empty undo history
		entry_case()
		print len(records)
		front_records=[]
	return 1

#these were functions that I wanted to create before I got too busy with school work.
#rotation settings would have allowed different loci for rotation, for example,
#color settings would have allowed for different color combinations to come up when
#the attractor is generated. 

def rotation_settings():
	return 1

def dilation_settings():
	return 1

def skew_settings():
	return 1

def color_settings():
	return 1

# creates a menu in the IFS window containing buttons to call several functions
options=Tkinter.Menubutton(window,text="Options")
options.menu=Tkinter.Menu(options, tearoff=0)
options["menu"]=options.menu
options.menu.add_command(label="undo transformation", command=undo_transformation)
options.menu.add_command(label="redo transformation", command=redo_transformation)
options.menu.add_command(label="add function",command = add_function)
options.menu.add_command(label="remove function",command = remove_function)
options.menu.add_command(label="save IFS", command= save_IFS)
options.menu.add_command(label="load IFS", command = load_IFS)

#creates a menu for transformation settings (which I didn't define yet)
formatting=Tkinter.Menubutton(window, text="format")
formatting.menu=Tkinter.Menu(formatting, tearoff=0)
formatting["menu"]=formatting.menu
formatting.menu.add_command(label="rotation settings",command=rotation_settings)
formatting.menu.add_command(label="dilation settings",command=dilation_settings)
formatting.menu.add_command(label="skew settings", command=skew_settings)
formatting.menu.add_command(label="color settings", command=color_settings)


def motion(event): #monitors current location of mouse in cartesian coordinates
	x,y= event.x, event.y
	AxisX=float(AxisX_entry.get())  #gets x and y axis ranges to provide correct cartesian coordinates
	AxisY=float(AxisY_entry.get())
	coordinates = "%.2f , %.2f" %((x-W/2)*AxisX/W,(-y+H/2)*AxisY/H) #calculates cartesian coordinates

	#drag_data["item"] = canvas.find_closest(event.x, event.y)[0]
        
	coords.configure(text = coordinates) #shows the coordinate point on the bottom left of the plane
	

def clear(): #clears all squares in the plane
	global matrices
	global P
	global quads
	global records
	global front_records
	

	canvas.delete("square")
	quads =[[0,0,0,0]]*number_functions #makes line markers all 0
	
	#set all data to 0
	P=[0]*number_functions 
	matrices=np.zeros((number_functions,6))

	#set all entries to 0
	for i in range(6*number_functions):
		function_entries[i].set(0)
		
	for i in range(number_functions):
		prob[i].set(0)
	
	#transformation buttons are all made gray, with grey highlighting, to show none is activated
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

	#updates records
	records=records+[[np.zeros((number_functions,6)), P, number_functions]]
	front_records=[]


def create_case(): #makes a new square, 
		   #or resets the square of some color to the unit square
	
	#color change will show that square creation was activated
	create_square.configure(bg="gold")
	create_square.configure(activebackground="light goldenrod")
	
	#all other transformations are made grey in highlighting
	stretch_square.configure(activebackground="#ececec")
	move_square.configure(activebackground="#ececec")
	skew_square.configure(activebackground="#ececec")
	rotate_square.configure(activebackground="#ececec")

	global tick
	global quads
	global records 
	global front_records

	tick=tick_number.get() #gets number designating which function you want to set to unit square

	#deletes old rectangle

	canvas.delete(quads[tick][0])
	canvas.delete(quads[tick][1])
	canvas.delete(quads[tick][2])
	canvas.delete(quads[tick][3])

	#creates new unit square in place of the old rectangle.
	#Quads becomes a list containing data on the bottom line of the square
	quads[tick]=[canvas.create_line(W/2, H/2, W/2+W/AxisX, H/2, 
		fill=square_count[tick], tags= ["square",tick, "bottom line"] ),
	canvas.create_line(W/2+W/AxisX, H/2, W/2+W/AxisX, H/2-W/AxisY, 
		fill=square_count[tick], tags= ["square",tick, "right line"] ),
	canvas.create_line( W/2+W/AxisX, H/2-W/AxisY,  W/2, H/2-W/AxisY, 
                fill=square_count[tick], tags= ["square", tick, "top line"] ),
	canvas.create_line(W/2, H/2 -W/AxisY, W/2, H/2, fill=square_count[tick], tags= ["square",tick, "left line"]) ]

	#sets up identity data and modifies entries
	matrices[tick]=[1,0,0,1,0,0]
	for i in range(6):
		function_entries[6*tick+i].set(matrices[tick][i])

	#changes the tick by one.  This is to enable several repeated clicks at a time making new functions squares
	#without changing the tick mark manually
	tick=(tick+1)%number_functions
	tick_number.set(tick)

	records=records+[[temporary_matrix(), P,number_functions]]
	#front_records=[]
	print len(records)
	print records[-1]
	print front_records
	
def stretch_case(): #indicates choice to set transformations on canvas to stretch:
	#non grey colors represent on a button indicate which transformation you will activate if you click on a square
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
	
	global records
	global front_records

	change_coordinates() #changes coordinates of squares to those in the entries

		
	records=records+[[temporary_matrix(), P, number_functions]]
	#front_records=[]
	print records[-1]
	print len(records)

def temporary_matrix(): #turns function_entries data into numerical matrix form
	global number_functions
	#global tick

	temp=np.zeros((number_functions,6))

	for i in range(number_functions):
		#a=tick
		for j in range(6):
			temp[i][j]=float(function_entries[6*i+j].get())

		#if quads[i]==[0,0,0,0]:
		#	tick=i
		#	create_case()
		#	for j in range(6):
		#		function_entries[6*i+j].set(temp[i][j])
		#tick=a

	return temp

def change_coordinates():
	global matrices
	global tick
	global P
	global records

	AxisX=float(AxisX_entry.get())
	AxisY=float(AxisY_entry.get())
	for i in range(number_functions):
		a=tick
		new_vals=[]
		for j in range(6):
			new_vals=new_vals+[float(function_entries[6*i+j].get())]

		if quads[i]==[0,0,0,0]:
			tick=i
			create_case()
			records.pop()
			for j in range(6):
				function_entries[6*i+j].set(new_vals[j])
		

		Tx=new_vals[4]*W/AxisX +W/2
		Ty=-new_vals[5]*H/AxisY +H/2
		Dx1=new_vals[0]*W/AxisX
		Dy1=-new_vals[1]*H/AxisY
		Dx2=new_vals[2]*W/AxisX
		Dy2=-new_vals[3]*H/AxisY
		
		canvas.coords(quads[i][0],Tx,Ty,Tx+Dx1,Ty+Dy1)
		canvas.coords(quads[i][1],Tx+Dx1,Ty+Dy1,Tx+Dx1+Dx2,Ty+Dy1+Dy2)
		canvas.coords(quads[i][2],Tx+Dx1+Dx2,Ty+Dy1+Dy2,Tx+Dx2,Ty+Dy2)
		canvas.coords(quads[i][3],Tx+Dx2,Ty+Dy2,Tx,Ty)
	

		reset_entries(i)
		tick=a

def clickDown(event): #finds closest line or corner of rectangle.  
		#This is to be able to transform graphically a single function without affecting the others

	drag_data["item"] = list(Tkinter.Canvas.find(canvas,'closest',event.x,event.y))[0]
       	drag_data["x"] = event.x
       	drag_data["y"] = event.y
	

def reset_entries(m):  #resets the matrix entries according to transformations
	global AxisX
	global AxisY	
	global matrices
	global P

	AxisX=float(AxisX_entry.get())
	AxisY=float(AxisY_entry.get())

	matrices[m]=vector_vals(m)
	P[m]=float(prob[m].get())

	for i in range(6):
		function_entries[6*m+i].set(matrices[m][i])		 

def vector_vals(m):
	return np.array([(canvas.coords(quads[m][0])[2]-canvas.coords(quads[m][0])[0])*AxisX/W,
		-(canvas.coords(quads[m][0])[3]-canvas.coords(quads[m][0])[1])*AxisY/H,
		-(canvas.coords(quads[m][3])[2]-canvas.coords(quads[m][3])[0])*AxisX/W,
		(canvas.coords(quads[m][3])[3]-canvas.coords(quads[m][3])[1])*AxisY/H,
		(canvas.coords(quads[m][0])[0]-W/2)*AxisX/W,
		-(canvas.coords(quads[m][0])[1]-H/2)*AxisY/H,])
	

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
	elif rotate_square['bg']=="dark orange" and drag_data["item"] not in [1,2]: 		#rotates figure around its center

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
	global records
	global front_records

        '''End drag of an object'''
        # reset the drag information
        drag_data["item"] = None
        drag_data["x"] = 0
        drag_data["y"] = 0

	records=records+[[temporary_matrix(), P, number_functions]]
	front_records=[]
	print len(records)
	print records[-1]
	print front_records

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
		
def createPoint(fractalCanvas, x0, y0, c): #creates a point in the attractor window
	p=fractalCanvas.create_line(x0, y0+1, x0+1, y0, fill=c)
	return p



#function for generating the points of the fractal

def f(x,y,Probs):
	m=random();
	
	if m<Probs[0]: 
		return 	[matrices[0][0]*x+matrices[0][1]*y +matrices[0][4], 
					matrices[0][2]*x+matrices[0][3]*y +matrices[0][5], 						square_count[0]]
	

	for i in range(1,number_functions):				
		if m>= sum(Probs[0:i]) and m<sum(Probs[0:i+1]):
			return [matrices[i][0]*x+matrices[i][1]*y +matrices[i][4], 
					matrices[i][2]*x+matrices[i][3]*y +matrices[i][5],
					 square_count[i]]
	

#generates the points on the fractalCanvas
def animate():
	global XYC
	global number_functions
	if start["bg"]=="red":
		return 1
	start.configure(bg="red")
	start.configure(activebackground="pink")
	#gives starting point, translates it to a starting point on the fractalCanvas
	xpoints=[0]  
	ypoints=[0]
	point_color=["black"]
	items=np.zeros(int(numpoints.get()))
	startingX=float(start_X_point.get())*W
	startingY=float(start_Y_point.get())*H
	
	Probs=[]
	for i in range(number_functions):
		Probs=Probs+[float(prob[i].get())]
	
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

	start.configure(bg="gray85")
	start.configure(activebackground="#ececec")

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

#puts widgets in the Attractor window
File.grid(row=0, column=0)
samples.grid(row=0,column=1)
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


# entries for axis ranges in the main window.  the values correspond to the number of units ranging accross the canvas both horizontally and vertically
XAxis=Tkinter.DoubleVar()
XAxis.set(AxisX)
YAxis=Tkinter.DoubleVar()
YAxis.set(AxisY)
AxisX_entry=Tkinter.Entry(window, width="5",textvariable=XAxis)
AxisY_entry=Tkinter.Entry(window, width="5",textvariable=YAxis)
Axes_label=Tkinter.Label(window, width="15",text="Axes")

tick_number=Tkinter.IntVar()
tick_number.set(tick)
tick_entry=Tkinter.Entry(window, width ="5", textvariable=tick_number)


# binds mouse events to specific windows and canvas
window.bind('<Motion>',motion)
canvas.bind('<ButtonPress-1>',clickDown)
canvas.bind('<B1-Motion>', holdButtonDown)
canvas.bind('<ButtonRelease-1>', ButtonRelease)

# defines buttons in the transformation window
clear_button = Tkinter.Button(window, text="clear", command=clear)
create_square = Tkinter.Button(window, text="square", width= "5", command=create_case)


stretch_square = Tkinter.Button(window, text="stretch", width= "7", command=stretch_case)
move_square = Tkinter.Button(window, text="move", width ="7", command=move_case)
skew_square = Tkinter.Button(window, text="skew", width= "7", command=skew_case)
rotate_square = Tkinter.Button(window, text="rotate", width = "7", command=rotate_case)
entry_square= Tkinter.Button(window, text="entries", width = "7",command=entry_case)




s=canvas.create_line(W/2, 0, W/2, H, fill="#FFFFFF", tags = "line")
s2=canvas.create_line(0, H/2, W, H/2, fill="#FFFFFF", tags = "line")

options.grid(row=0,column=0)
formatting.grid(row=0, column =1) 
canvas.grid(row=1, columnspan=14, sticky="nsew")
coords.grid(row = 2,column=0, columnspan = 1)

frame2.grid(row=3,column=0,columnspan=8, rowspan=2, sticky= "we")
widgetCanvas.grid(row=0,column=1, rowspan=5, sticky= "we")
frame.place()

probLabel.grid(row=0, column=7)

scroll.grid(row=0,column=0, rowspan=3, sticky="ns")

create_square.grid(row = 2, column = 1,columnspan=1, sticky="we")
tick_entry.grid(row=2, column=2,sticky="we")
stretch_square.grid(row =2, column=3,columnspan=2, sticky="we")
move_square.grid(row =2, column=5, columnspan=2, sticky="we")
skew_square.grid(row =2, column=7, columnspan=2, sticky="we")
rotate_square.grid(row =2, column=9, columnspan=2, sticky="we")
entry_square.grid(row = 2, column = 11,columnspan=2,sticky="we")


clear_button.grid(row=2, column=13,columnspan=2, sticky="e")
Axes_label.grid(row=3,column=9,columnspan=2)
AxisX_entry.grid(row=4,column=9)
AxisY_entry.grid(row=4,column=10)

print type(AxisX_entry.get())
print type(AxisX_entry['textvariable'])



window.mainloop()


