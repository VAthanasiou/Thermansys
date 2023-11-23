#######################################################################################
#              THIS MODULE PERFORMS THE STANDARD DEVIATION OF SELECTED                #
#              DATASET/IMAGES                                          		          #
#       >  READS .TIF IMAGES FROM USER INPUT                                          #
#       >  CONVERT IMAGES TO ARRAYS FOR CALCULATIONS                                  #
#       >  CALCULATES THE AVERAGE/MEAN OF IMAGES                                      #
#       >  CALCULATES STD AND SAVES FINAL RESULTS                                     #
#           				                                                          #
#           >  WRITTEN BY A.GKOURAS, V.ATHANASIOU, L.GERGIDIS	                      #
#           						                                                  #
#	          *****************IMPORTANT*********************		                  #
#                  IF IT FAILS TO RUN, CHECK DIRECTORIES                              #
#######################################################################################
#######################################################################################
#										                                              #
#                             CODE FOR PV_AUTO SCOUT       	                          #
#								                                                      #
#                                  Flow chart                                         #
#       Reads each image and calculates average for standard deviation                #
#       normalaze final image and convert it to uint8 to apply colormap               #
#       save final results and create report                                          #
#       create toolbox for GUI                                                        #
#                                                                                     #
#                                                                                     #
#                                                                                     #
#######################################################################################

import os
import numpy as np
import glob
import cv2
import Img_path
import ctypes
from tkinter import filedialog
from tkinter.messagebox import showinfo
from tkinter import *
from Img_path import bgimgpath
from Information import *
from tkinter.ttk import Progressbar
import time
from datetime import date
from datetime import datetime

def image_path():
     #global path
     Img_path.path = filedialog.askdirectory()
     return

def popup_showinfo():
     showinfo('Manual for the code','here goes the manual')

######################################   METHOD    ################################################### 
def stand_dev_meth():

    # Check if the path of the images exist if not go to error message
    if os.path.exists(Img_path.path) :

        # Create Directories to current working directory
        current_directory = os.getcwd()
        # Desktop directory
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop', r"Standard Deviation Results")
        # If the above path doesnt exist create the directories below
        # In this directory we save the calculations
        # For the user to look at the now visible images
        if not os.path.exists(desktop):
            os.makedirs(desktop)


        # The path where the thermographig images reside
        # We only need .tif images for the calculation thus the *.tif extension 
        # If anything comes up we add more extensions 
        images_path = glob.glob(Img_path.path+'\\*.tif')

        ttl_of_images = len(images_path)

        #Set counter n, and sums mean_im and std_im , zero
        #initialize variables
        n = 0 
        mean_im = 0 
        std_im = 0
        for file in images_path:
            n += 1
            #Reading .tif images from Images Path
            image = cv2.imread(file, -1)
            #'Convert' images to arrays for the above calculations
            image = np.array(image, dtype=np.float64)
            #Sum each image to mean_im (Mean Image) to calculate the Average/Mean Image
            mean_im += image
            #Sum each image to std_im and rise to square for each sum result (Standard Deviation Image) 
            # to calculate the Standard Deviation Image
            std_im += (image - mean_im) ** 2

            # Ιncrease the percent of progess bar by 1 devided by total number of images
            bar['value']+=(1/ttl_of_images)*100
            percent.set(str(int((n/ttl_of_images)*100)) + "%")
            # A text that reports the current amount of calculated images
            text.set(str(n)+"/"+str(ttl_of_images)+ " Images Calculated")
            # Update the window 
            STD_root.update_idletasks()

        #Devide by n-1 the result of Standard Deviation Image sum
        std_im = np.sqrt(std_im / n-1)
        #Devide the result by n of Mean Image sum
        #n = the number of images
        mean_im = mean_im/n
        #Giving names to each images.
        
        Std_Image_Name = "Standard Deviation Results.png"
        # Normalize the calculated image
        norm_image = cv2.normalize(std_im, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
        # Convert image to uint8
        norm_image = np.uint8(norm_image)
        # Apply color_map to image
        norm_image = cv2.applyColorMap(norm_image, cv2.COLORMAP_INFERNO)

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

        with open("Standard Deviation Report_{}.txt".format(todays_date), "a") as f:
            f.write("#############################      REPORT      #############################" + '\n'
                +"\n" +'Folder Name : ' + dir_folder_name + "\n" 
                +"\n" +'Directory Path : ' + dir_path_name + "\n" 
                +"\n" +'Number of Calculated Images : ' + str(ttl_of_images) + "\n" 
                +"\n" +'Program Runtime :' + " %s seconds" % (time.time() - start_time) + "\n"
                +"\n" + 'Date : ' + str(todays_date) + "\n" 
                +"\n" + 'Time : ' + str(current_time) + "\n"
                )

        #Save mean_im & std_im Images to Results directory
        cv2.imwrite(os.path.join(desktop , Std_Image_Name), norm_image)
        ctypes.windll.user32.MessageBoxW(0, "Process has been finished, Check Results directory ", "Success !", 1)

#If the image path doesnt exist point it out with the error window
    else :
        ctypes.windll.user32.MessageBoxW(0, "Choose image path", "Error", 1)

##################################   TOOLBOX     ##############################################
def Standard_Dev():
    global STD_root
    STD_root = Toplevel()
    STD_root.geometry("320x180")
    STD_root.resizable(False,False)
    STD_root.title("Standard Deviation Calculator")
    #Second window will stay always on top
    STD_root.wm_attributes("-topmost", 1)
    crop_icon = PhotoImage(file=bgimgpath)
    STD_root.tk.call('wm', 'iconphoto', STD_root._w, crop_icon)
    # Read the optionDB.py file
    # This file contains the template 
    # For the Graphical User Interface
    STD_root.option_readfile('optionDB.py')
    # Read imageas a small icon 
    menu = Menu(STD_root)
    STD_root.config(menu=menu)
    filemenu = Menu(menu)
    menu.add_cascade(label="File", menu=filemenu)
    filemenu.add_command(label="Select Image Directory", command=image_path)
    filemenu.add_separator()
    filemenu.add_command(label='Exit', command=STD_root.quit)

    helpmenu = Menu(menu)
    menu.add_cascade(label="Help", menu=helpmenu)
    helpmenu.add_command(label="About", command=information)
    helpmenu.add_command(label='Manual',command=popup_showinfo)

    global percent
    global text
    global bar
    percent = StringVar()
    text = StringVar()

    bar = Progressbar(STD_root, orient=HORIZONTAL, length=200, mode='determinate')
    bar.pack(pady=11)
     
    percentlabel = Label(STD_root, textvariable=percent)
    percentlabel.pack()
          
    tasklabel = Label(STD_root, textvariable=text)
    tasklabel.pack()

    bar['value']=0
    percent.set(str( "0 %"))
    text.set("0 " + " Images Calculated")

    Run_Code_button = Button(STD_root, 
                              text="Standard Deviation Results",
                              bg='blue', 
                              fg='white', 
                              command=stand_dev_meth, 
                              height = 2, 
                              width = 28
                              )
    Run_Code_button.pack(side='bottom', padx=50, pady=12)
    STD_root.mainloop()
