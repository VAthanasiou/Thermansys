#######################################################################################
#              THIS MODULE PERFORMS THE MAIN GRAPHICAL USER INTEFACE                  #
#                 OF THE COMPUTER PROGRAM THERMASYS, INCLUDES:                        #
#       >  A TASK BAR WITH TOOLS AND MANUAL                                           #
#       >  IR LOCK-IN PERIODS BUTTON                                                  #
#       >  PULSE PHASE BUTTON                                                         #
#       >  IR LOCK-IN 4 POINTS BUTTON                                                 #
#       >  STANDARD DEVIATION                                                         #
#           				                                                        #
#           >  WRITTEN BY A.GKOURAS, V.ATHANASIOU, L.GERGIDIS					 #
#           						                                              #
#	          *****************IMPORTANT*********************		                #
#                 IF IT FAILS TO RUN, RESTART THE PROGRAM                             #
#######################################################################################
#######################################################################################
#										                                    #
#                             CODE FOR THERMANSYS	                                    #
#								                                              #
#                                 Flow chart                                          #
#       Imports the Manual.pdf and required images                                    #
#       creates the the Graphical User Interface window &                             #
#       adds backround image, main buttons and methods to the GUI                     #
#                                                                                     #
#                                                                                     #
#                                                                                     #
#                                                                                     #
#######################################################################################

import tkinter as tk
from tkinter import *
from crop_image import tool_box
from Information import *
from tkinter.messagebox import showinfo
from Img_path import bgimgpath, roi_image1, icon_photo, manual_icon, about_icon, img_enh
from Img_path  import icon_exit
from ir_lock_in_4_dots import Lock_in
from standard_dev import Standard_Dev
from pulsed_phase import Pulse_Phase
from ir_lock_in_prds import Lock_in_periods
from PIL import ImageTk, Image
from img_alg_enh import call_algorithms
from img_alg_enh import enhancement

 

def read_pdf():
     pdf_path = "Manual\\Manual.pdf"
     os.startfile(pdf_path)
     #showinfo('Manual for the code','here goes the manual')


def image_path():
     #global path
     #Img_path.path = filedialog.askdirectory()
     pass
     return

# Create the the Graphical User Interface window   
root = tk.Tk()
# Pixel Geometry of the window created
root.geometry("640x512")
# False False means cannot resize manually the window
# The window will always have set values
root.resizable(False,False)
# Title on the window
root.title("Thermansys")
# Read the optionDB.py file
# This file contains the template 
# For the Graphical User Interface
root.option_readfile('optionDB.py')
# Read image to put as a small icon 
# To put in on the top left corner 
# as a logo for the software
icon = PhotoImage(file=icon_photo)
root.tk.call('wm', 'iconphoto', root._w, icon)

#create a menu for the main window
menu = Menu(root)
root.config(menu=menu)

im1 = Image.open(icon_exit)
ph1 = ImageTk.PhotoImage(im1)
filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label=' Exit', command=root.quit, image=ph1, compound="left")
# Need to keep the reference of the image to avoid garbage collection
filemenu.image=ph1

im2 = Image.open(roi_image1)
ph2 = ImageTk.PhotoImage(im2)
imen=Image.open(img_enh)
phen= ImageTk.PhotoImage(imen)
tool_menu = Menu(menu)
menu.add_cascade(label="Tools", menu=tool_menu)
tool_menu.add_command(label=" Crop Image", command=tool_box, image=ph2, compound="left")
tool_menu.add_command(label=" Image Enhancement", command=enhancement, image=phen, compound="left")
# Need to keep the reference of the image to avoid garbage collection
tool_menu.image=ph2

im3 = Image.open(manual_icon)
ph3 = ImageTk.PhotoImage(im3)
im4 = Image.open(about_icon)
ph4 = ImageTk.PhotoImage(im4)
helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label=" About", command=information, image=ph4, compound="left")
helpmenu.add_command(label=' Manual',command=read_pdf, image=ph3, compound="left")
# Need to keep the reference of the image to avoid garbage collection
#helpmenu.image=ph3
#helpmenu.image=ph4

# Add backround image to the Graphical User interface
C = Canvas(root, bg="blue", height=250, width=200)
backround_image = PhotoImage(file = bgimgpath)
background_label = Label(root, image=backround_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
C.pack()
root.config(bg='#49A')

# Main buttons and Methods
# Creates Lock-in 4 points button
IR_Lock_In_button = Button(root, 
                              text="4 dots IR Lock-in", 
                              font=("Comic Sans",10), 
                              bg='red2', 
                              fg='white', 
                              command=Lock_in, 
                              height = 2, 
                              width = 24
                              )
IR_Lock_In_button.place(x=421, y=350)

# Creates Standard Deviation button
Standard_Dev_button = Button(root, 
                              text="Standard Dev",
                              font=("Comic Sans",10), 
                              bg='red2', 
                              fg='white', 
                              command=Standard_Dev, 
                              height = 2, 
                              width = 24
                              )
Standard_Dev_button.place(x=421, y=400)

# Creates Pulse Phase button
Pulse_Phase_button = Button(root, 
                              text="Pulsed Phase",
                              font=("Comic Sans",10), 
                              bg='red2', 
                              fg='white', 
                              command=Pulse_Phase, 
                              height = 2, 
                              width = 24
                              )
Pulse_Phase_button.place(x=421, y=300)

# Creates Lock-in periods button
Lock_In_periods_button = Button(root,
                              text="IR Lock-in periods",
                              font=("Comic Sans",10), 
                              bg='red2', 
                              fg='white', 
                              command=Lock_in_periods, 
                              height = 2, 
                              width = 24
                              )
Lock_In_periods_button.place(x=421, y=250)
root.mainloop()


