#######################################################################################
#              THIS MODULE PERFORMS THE DIGITAL LOCKING CORRELATION METHOD &          #
#               INCLUDES THE TOOLBOX OF GUI                          		          #
#       >  CREATES THE TOOLBOX OF GUI                                                 #
#       >  TAKES INPUT THE DATASET                                                    #
#       >  APPENDS THE IMAGES INTO A LIST                                             #
#       >  DEVIDE THE LIST DEPENDING TO THE NUMBER OF PERIODS                         #
#       >  CALCULATES THE K0 & K90 OF EACH THERMAL FRAME                              #
#       >  CALCULATES THE S0 & S90 OF EACH THERMAL FRAME                              #
#       >  CALCULATES AMPLITUDE AND PHASE                                             #
#       >  SAVES THE FINAL RESULTS AND CREATES A PROCESS REPORT                       #
#           				                                                          #
#           >  WRITTEN BY A.GKOURAS, V.ATHANASIOU, L.GERGIDIS					      #
#           						                                                  #
#	          *****************IMPORTANT*********************		                  #
#                IF IT FAILS TO RUN, CHECK DIRECTORIES                                #
#######################################################################################
#######################################################################################
#										                                              #
#                             CODE FOR THERMANSYS   	                              #
#								                                                      #
#                                  Flow chart                                         #
#       Takes the dataset from user input and append them into a list                 #
#       devide the list depending to number of periods                                #
#       saves the final results and create a detailed process report                  #
#                                                                                     #
#######################################################################################

from tkinter import *
from tkinter import filedialog
from Information import *
from tkinter.messagebox import showinfo
import Img_path
from Img_path import bgimgpath
import os
import numpy as np
import glob
import cv2 
from tkinter.ttk import Progressbar
import Img_path
import ctypes
import math
import time
from datetime import date
from datetime import datetime

def image_path():
     #global path
     Img_path.path = filedialog.askdirectory()
     return

def popup_showinfo():
     showinfo('Manual for the code','here goes the manual')

##################################   TOOLBOX     ##############################################
def Lock_in_periods():
    global Lock_in_prd_root
    Lock_in_prd_root = Toplevel()
    Lock_in_prd_root.geometry("320x230")
    Lock_in_prd_root.resizable(False,False)
    Lock_in_prd_root.title("IR Lock-in periods Calculator")
    #Second window will stay always on top
    Lock_in_prd_root.wm_attributes("-topmost", 1)
    crop_icon = PhotoImage(file=bgimgpath)
    Lock_in_prd_root.tk.call('wm', 'iconphoto', Lock_in_prd_root._w, crop_icon)
    # Read the optionDB.py file
    # This file contains the template 
    # For the Graphical User Interface
    Lock_in_prd_root.option_readfile('optionDB.py')
    # Read imageas a small icon 
    menu = Menu(Lock_in_prd_root)
    Lock_in_prd_root.config(menu=menu)
    filemenu = Menu(menu)
    menu.add_cascade(label="File", menu=filemenu)
    filemenu.add_command(label="Select Image Directory", command=image_path)
    filemenu.add_separator()
    filemenu.add_command(label='Exit', command=Lock_in_prd_root.quit)
    helpmenu = Menu(menu)
    menu.add_cascade(label="Help", menu=helpmenu)
    helpmenu.add_command(label="About", command=information)
    helpmenu.add_command(label='Manual',command=popup_showinfo)
    
    #ProgessBar
    global percent
    global text
    global bara
    percent = StringVar()
    text = StringVar()

    bara = Progressbar(Lock_in_prd_root, orient=HORIZONTAL, length=200, mode='determinate')
    bara.place(x=60, y=53)
     
    percentlabel = Label(Lock_in_prd_root, textvariable=percent)
    percentlabel.place(x=150, y=85)
          
    tasklabel = Label(Lock_in_prd_root, textvariable=text)
    tasklabel.place(x=80, y=105)

    bara['value']=0
    percent.set(str( "0 %"))
    text.set("0 " + " Images has proccessed")

    # USER INPUT
    text_input = StringVar()
    textlabel = Label(Lock_in_prd_root, textvariable=text_input)
    textlabel.place(x=60, y=20)
    text_input.set("Input the number of periods N :")
    global entry
    global N
    N = StringVar()
    entry = Entry(Lock_in_prd_root,
                    textvariable = N, 
                    bg="white", 
                    borderwidth=3,
                    width = 2)
    entry.place(x=235 ,y=20)

    # Main button for results
    Run_Code_button = Button(Lock_in_prd_root, 
                                text="IR Lock-in periods Results",
                                bg='blue2', 
                                fg='white', 
                                command=lock_in_periods_methd,
                                height = 2, 
                                width = 28)
    Run_Code_button.place(x=57, y=140)
    Lock_in_prd_root.mainloop()
    
######################################   METHOD    ###################################################  
def lock_in_periods_methd():
    # Check if the path of the images exist if not go to error message
    if os.path.exists(Img_path.path) :

        # Create the Croped data directory        
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop', r"IR Lock-in periods Results")
        # If the above path doesnt exist create the directories below
        # In this directory we save the calculations
        # For the user to look at the now visible images
        if not os.path.exists(desktop):
            os.makedirs(desktop)


        directory = glob.glob(Img_path.path+'\\*.tif')
        
        # A list that contains all the images that have been read
        list_of_images = []
        # "n" is the number of thermal images
        n = 0
        for file in directory:
            # Make a counter for the images
            # Useful for the calcultions of the K0 and K90
            n += 1
            # Reading the thermal images from the images directory
            frame_image = cv2.imread(file, -1)
            # Convert images to arrays 
            frame_image_array = np.array(frame_image)
            # Append images to the empty list
            list_of_images.append(frame_image_array)

        #print ('Number of images that exist in this folder are :', str(n),'images')

        # Usefull counter to read the multiples of the parts of the list
        cnt1 = 0
        cnt2 = 1
        S0 = 0
        S90 = 0
        j = 0
        #Numer of periods that user inputted
        N = entry.get()
        N = int(N)
        if N  <= 0 :
            ctypes.windll.user32.MessageBoxW (0,"Number of periods 'N' must be N>0 ",1)

        else:
            # Calculates the length of the list and divides it by the number of periods
            total_of_images = len(list_of_images)
            lenght = len(list_of_images) / N
            for i in range(1,N+1):
                for frame in list_of_images[int(cnt1*lenght):int(cnt2*lenght)] :
                    cnt1 += 1
                    cnt2 += 1
                    j += 1
                    # Calculates the K0 of each thermal frame-image
                    K0 = 2*math.sin((2*math.pi*(j-1))/n)
                    # Sum of S0 of each thermal frame-image
                    S0 += K0 * frame
                    # Calculates the K90 of each thermal frame-image
                    K90 = -2*math.cos((2*math.pi*(j-1))/n)
                    # Sum of S0 of each thermal frame-image
                    S90 += K90 * frame
                    # Ιncrease the percent of progess bar by 1 devided by total number of images
                    bara['value']+=(1/lenght)*100
                    percent.set(str(int((n/total_of_images)*100)) + "%")
                    # A text that reports the current amount of croped images
                    text.set(str(total_of_images)+ " Images has Processed")
                    # Update the window 
                    Lock_in_prd_root.update_idletasks()

            # Final S0 divided by the product of number of frames-images and number of periods as the theory suggests
            S0 = S0/(n*N)
            # Final S90 divided by the product of number of frames-images and number of periods as the theory suggests
            S90 = S90/(n*N)
            '''
            # Normalize S0 and S90 images from 0 to 255 pixs
            S0_norm_image = cv2.normalize(S0, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
            S90_norm_image = cv2.normalize(S90, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
            # Convert image to uint8
            S0_norm_image = np.uint8(S0_norm_image)
            S90_norm_image = np.uint8(S90_norm_image)
            # Apply color_map to image
            S0_norm_image = cv2.applyColorMap(S0_norm_image, cv2.COLORMAP_INFERNO)
            S90_norm_image = cv2.applyColorMap(S90_norm_image, cv2.COLORMAP_INFERNO)
                #print("S0_N-" + str(i) + "\n" , S0)
            #Save each output of the variables S0 and S90 with the opencv module
            #cv2.imwrite(os.path.join(S0_direc,'S0_N-{}.png'.format(i)), S0_norm_image)
            #cv2.imwrite(os.path.join(S90_direc,'S90_N-{}.png'.format(i)), S90_norm_image)
            '''
            # Call the module that calculates the Amplitude and Phase
            # Amplitude and Phase math-type
            Amplt = cv2.sqrt(S0**2 + S90**2)
            Phase = np.arctan(S90, S0)

            # Normalize image
            # Arcatan take values from -1 to 1
            # We normalise these values from 0 to 255 pixs
            Phase_norm = cv2.normalize(Phase, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
            Amplt_norm = cv2.normalize(Amplt, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)

            # Convert image to uint8
            Phase_norm = np.uint8(Phase_norm)
            Amplt_norm = np.uint8(Amplt_norm)
            # Apply color_map to image
            Phase_norm = cv2.applyColorMap(Phase_norm, cv2.COLORMAP_INFERNO)
            Amplt_norm = cv2.applyColorMap(Amplt_norm, cv2.COLORMAP_INFERNO)

            # Usefull to output the runtime
            start_time = time.time()
            # Creating the date object of today's date
            todays_date = date.today()
            # Current time
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")

            # Folder Name from choosen directory
            dir_folder_name = os.path.basename(Img_path.path)
            # Path from choosen directory
            dir_path_name = os.path.dirname(Img_path.path)

            with open("IR Lock-in periods Report_{}.txt".format(todays_date), "a") as f:
                f.write("#############################      REPORT      #############################" + '\n'
                    +"\n" +'Folder Name : ' + dir_folder_name + "\n" 
                    +"\n" +'Directory Path : ' + dir_path_name + "\n" 
                    +"\n" +'Number of Calculated Images : ' + str(total_of_images) + "\n" 
                    +"\n" +'Program Runtime :' + " %s seconds" % (time.time() - start_time) + "\n"
                    +"\n" + 'Date : ' + str(todays_date) + "\n" 
                    +"\n" + 'Time : ' + str(current_time) + "\n"
                    )

            # Save images to Results folder  
            cv2.imwrite(os.path.join(desktop ,'Amplitude_N-{}.png'.format(i)), Amplt_norm)
            cv2.imwrite(os.path.join(desktop ,'Phase_N-{}.png'.format(i)), Phase_norm)
            ctypes.windll.user32.MessageBoxW(0, "Process has been finished, Check Results directory ", "Success !", 1)
        
        #else : ctypes.windll.user32.MessageBoxW (0,"Number of periods 'N' must be a number and N > 0 ",1)
       

    else : ctypes.windll.user32.MessageBoxW(0, "Choose image path", "Error", 1)