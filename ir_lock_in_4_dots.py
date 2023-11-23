#######################################################################################
#              THIS MODULE PERFORMS THE FOUR POINT CORRELATION METHOD &               #
#              INCLUDES THE TOOLBOX OF GUI                              		      #
#       >  TAKES 4 IMAGES AS AN INPUT                                                 #
#       >  CONVERT IMAGES TO ARRAYS                                                   #
#       >  CALCULATES AMPLITUDE AND PHASE                                             #
#       >  CREATES A DETAILED REPORT                                                  #
#           				                                                          #
#           >  WRITTEN BY A.GKOURAS, V.ATHANASIOU, L.GERGIDIS					      #
#           						                                                  #
#	          *****************IMPORTANT*********************		                  #
#                 IF IT FAILS TO RUN, CHECK DIRECTORIES                               #
#######################################################################################
#######################################################################################
#										                                              #
#                              CODE FOR THERMANSYS      	                          #
#								                                                      #
#                                 Flow chart                                          #
#       Takes the 4 imageS as input from user and convert them to array               #
#       calculates the aplitude and phase                                             #
#       creates a detailed report and saves the final results                         #
#                                                                                     #
#                                                                                     #
#######################################################################################

import cv2
import numpy as np
import os
import ctypes
from tkinter import *
from tkinter import filedialog
from Information import *
from tkinter.messagebox import showinfo
import Img_path
from Img_path import bgimgpath
from tkinter.ttk import Progressbar
import time
from datetime import date
from datetime import datetime


def image_path_S1():
    #global path
    Img_path.S1_path = filedialog.askopenfilename()
    return
def image_path_S2():
    #global path
    Img_path.S2_path = filedialog.askopenfilename()
    return
def image_path_S3():
    #global path
    Img_path.S3_path = filedialog.askopenfilename()
    return
def image_path_S4():
    #global path
    Img_path.S4_path = filedialog.askopenfilename()
    return
def popup_showinfo():
    showinfo('Manual for the code','here goes the manual')

######################################   METHOD    ################################################### 
def ir_lock_in_meth ():
# Check if the path of the images exist if not go to error message
    if not os.path.exists(Img_path.S1_path):
        ctypes.windll.user32.MessageBoxW(0, "Choose image as S1", "Error", 1)

    elif not os.path.exists(Img_path.S2_path):
        ctypes.windll.user32.MessageBoxW(0, "Choose image as S2", "Error", 1)

    elif not os.path.exists(Img_path.S3_path):
        ctypes.windll.user32.MessageBoxW(0, "Choose image as S3", "Error", 1)

    elif not os.path.exists(Img_path.S4_path):
        ctypes.windll.user32.MessageBoxW(0, "Choose image as S4", "Error", 1)

    elif os.path.exists(Img_path.S1_path) and os.path.exists(Img_path.S2_path) \
        and os.path.exists(Img_path.S3_path) and os.path.exists(Img_path.S4_path):

        # Create Directories to current working directory
        current_directory = os.getcwd()
        # Create the results directory if not exist
        #results_directory = os.path.join(current_directory, r'IR Lock-In 4-dots Results')
        #Desktop path
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop', r"IR Lock-In 4-dots Results")
        # If the above path doesnt exist create the directories below
        # In this directory we save the calculations
        # For the user to look at the now visible images
        if not os.path.exists(desktop):
            os.makedirs(desktop)


        # Read 4 images: S1, S2, S3, S4
        S1 = cv2.imread(Img_path.S1_path, -1)
        S2 = cv2.imread(Img_path.S2_path, -1)
        S3 = cv2.imread(Img_path.S3_path, -1)
        S4 = cv2.imread(Img_path.S4_path, -1)

        # Convert images to arrays for calculations
        S1 = np.array(S1, dtype=np.float64)
        #print(S1)
        S2 = np.array(S2, dtype=np.float64)
        S3 = np.array(S3, dtype=np.float64)
        S4 = np.array(S4, dtype=np.float64)

        # Amplitude and Phase math-type
        Phase = np.arctan((S1-S3),(S2-S4))
        Ampl = cv2.sqrt((S1-S3)**2 + (S2-S4)**2)

        # Ιncrease the percent of progess bar by 1 devided by total number of images
        n = 0
        total_of_imgs = 4
        while n < total_of_imgs:
            n += 1
            # Progress of progess bar
            bar['value']+=(1/total_of_imgs)*100
            # Percent values
            percent.set(str(int((n/total_of_imgs)*100)) + "%")
            # A text that reports the current amount of croped images
            text.set(str(n)+"/"+str(total_of_imgs)+ " Images Processed")
            # Update the window 
            Lock_in_root.update_idletasks()


        # Normalize image
        # Arcatan take values from -1 to 1
        # We normalise these values from 0 to 255 pixs
        Ampl_norm = cv2.normalize(Ampl, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
        Phase_norm = cv2.normalize(Phase, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
        phase = np.uint8(Phase_norm)
        ampl = np.uint8(Ampl_norm)
        phase_image = cv2.applyColorMap(phase, cv2.COLORMAP_INFERNO)
        ampl_image = cv2.applyColorMap(ampl,cv2.COLORMAP_INFERNO)
        # Create names for each image
        Ampl_name = 'Ampltitude.jpg'
        Phase_name = 'Phase.jpg' 

        # Useful to output the runtime
        start_time = time.time()
        # Creating the date object of today's date
        todays_date = date.today()
        # Current time
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        # S1 File Name from choosen directory
        dir_S1file_name = os.path.basename(Img_path.S1_path)
        # S2 File Name from choosen directory
        dir_S2file_name = os.path.basename(Img_path.S2_path)
        # S3 File Name from choosen directory
        dir_S3file_name = os.path.basename(Img_path.S3_path)
        # S4 File Name from choosen directory
        dir_S4file_name = os.path.basename(Img_path.S4_path)
        # Path from choosen directory
        dir_path_name = os.path.dirname(Img_path.S1_path)

        with open("IR Lock-in 4 dots Report_{}.txt".format(todays_date), "a") as f:
            f.write("#############################      REPORT      #############################" + '\n'
                +"\n" +'S1 Image File Name : ' + dir_S1file_name + "\n" 
                +"\n" +'S2 Image File Name : ' + dir_S2file_name + "\n" 
                +"\n" +'S3 Image File Name : ' + dir_S3file_name + "\n" 
                +"\n" +'S4 Image File Name : ' + dir_S4file_name + "\n" 
                +"\n" +'Directory Path : ' + dir_path_name + "\n" 
                +"\n" +'Number of Calculated Images : ' + str(total_of_imgs) + "\n" 
                +"\n" +'Program Runtime :' + " %s seconds" % (time.time() - start_time) + "\n"
                +"\n" + 'Date : ' + str(todays_date) + "\n" 
                +"\n" + 'Time : ' + str(current_time) + "\n"
                )

        # Save images to Results folder  
        cv2.imwrite(os.path.join(desktop , Ampl_name), ampl_image)
        cv2.imwrite(os.path.join(desktop , Phase_name), phase_image)
        ctypes.windll.user32.MessageBoxW(0, "Process has been finished, Check Results directory ", "Sucess", 1)

##################################   TOOLBOX     ##############################################
def Lock_in():
    global Lock_in_root
    Lock_in_root = Toplevel()
    Lock_in_root.geometry("320x180")
    Lock_in_root.resizable(False,False)
    Lock_in_root.title("4 dots IR Lock-in Calculator")
    #Second window will stay always on top
    Lock_in_root.wm_attributes("-topmost", 1)
    crop_icon = PhotoImage(file=bgimgpath)
    Lock_in_root.tk.call('wm', 'iconphoto', Lock_in_root._w, crop_icon)
    # Read the optionDB.py file
    # This file contains the template 
    # For the Graphical User Interface
    Lock_in_root.option_readfile('optionDB.py')
    # Read imageas a small icon 
    menu = Menu(Lock_in_root)
    Lock_in_root.config(menu=menu)
    filemenu = Menu(menu)
    menu.add_cascade(label="File", menu=filemenu)
    filemenu.add_command(label="Select Image S1", command=image_path_S1)
    filemenu.add_command(label="Select Image S2", command=image_path_S2)
    filemenu.add_command(label="Select Image S3", command=image_path_S3)
    filemenu.add_command(label="Select Image S4", command=image_path_S4)
    filemenu.add_separator()
    filemenu.add_command(label='Exit', command=Lock_in_root.quit)

    helpmenu = Menu(menu)
    menu.add_cascade(label="Help", menu=helpmenu)
    helpmenu.add_command(label="About", command=information)
    helpmenu.add_command(label='Manual',command=popup_showinfo)

    global percent
    global text
    global bar
    percent = StringVar()
    text = StringVar()

    bar = Progressbar(Lock_in_root, orient=HORIZONTAL, length=200, mode='determinate')
    bar.pack(side='top', pady=14)
     
    percentlabel = Label(Lock_in_root, textvariable=percent)
    percentlabel.pack()
          
    tasklabel = Label(Lock_in_root, textvariable=text)
    tasklabel.pack()

    bar['value']=0
    percent.set(str( "0 %"))
    text.set("0 " + " Images Calculated")

    Run_Code_button = Button(Lock_in_root, 
                                text="4 dots IR Lock-in Results", 
                                bg='blue2', 
                                fg='white', 
                                command=ir_lock_in_meth, 
                                height = 2, 
                                width = 28
                                )
    Run_Code_button.pack(side='bottom', padx=50, pady=14)
    Lock_in_root.mainloop()