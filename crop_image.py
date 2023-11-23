#######################################################################################
#              THIS MODULE PERFORMS THE CROP OF AN IMAGE                              #
#              AND APPLIES THE SELECTED COORDINATES TO THE 		                     #
#              DESIRED DATASET BY THE REGION OF INTEREST                              #
#                                       &                                             #
#              CONTAINS THE TOOLBOX OF GUI                                            #
#                                                                                     #
#       >  USER INPUTS THE ORIGINAL (RESULT) IMAGE                                    #
#       >  SELECTS THE COORDINATES AS THE REGION OF INTEREST                          #
#       >  APPLIES THE SELECTED COORDINATES TO THE DATASET                            #                                                   #
#           				                                                        #
#           >  WRITTEN BY A.GKOURAS, V.ATHANASIOU, L.GERGIDIS			           #
#           						                                              #
#	          *****************IMPORTANT*********************		                #
#        IF IT FAILS TO RUN, CHECK DIRECTORIES AND TYPE OF SELECTED FILES             #
#######################################################################################
#######################################################################################
#										                                    #
#                              CODE FOR THERMANSYS	                               #
#								                                              #
#                                  Flow chart                                         #
#       User selects the coordinates from a thermal image as the region of interest   #
#       applies the selected coordinates to the desired dataset                       #
#       saves a detailed report of the progress                                       #
#                                                                                     #
#                                                                                     #
#                                                                                     #
#######################################################################################

import cv2
import glob
import os
import Img_path
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Progressbar
from Information import *
from tkinter.messagebox import showinfo
import Img_path
from Img_path import crop_png
import time
from datetime import date
from datetime import datetime

def image_path():
     #global path
     Img_path.single_image_path = filedialog.askopenfilename()
     return

def folder_path():
     #global path
     Img_path.path = filedialog.askdirectory()
     return

def popup_showinfo():
     showinfo('Manual for the code','here goes the manual')

##############################          METHOD         #######################################
def crop_():
     
     if os.path.exists(Img_path.path) and  os.path.exists(Img_path.single_image_path) :
          '''
          # Create Directories to current working directory
          current_directory = os.getcwd()
          # Create the Croped data directory
          CropDir = os.path.join(current_directory, r'Cropped Dataset')
          
          if not os.path.exists(CropDir):
               os.makedirs(CropDir)
          '''
          # Select an image for coordinates 
          directory = glob.glob(Img_path.path+'\\*.tif')
          # Create the Croped data directory
          desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop', r"Cropped Dataset")
          # If the above path doesnt exist create the directories below
           # In this directory we save the calculations
           # For the user to look at the now visible images
          if not os.path.exists(desktop):
                os.makedirs(desktop)

          # Read image
          im = cv2.imread(Img_path.single_image_path, -1)

          # Select ROI
          r = cv2.selectROI(im)

          # Crop image
          imCrop = im[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
          #---------#
          x = int(r[1])
          w = int(r[1]+r[3])
          y = int(r[0])
          h = int(r[0]+r[2])

          # Display cropped image
          cv2.imshow("Image", imCrop)
          cv2.waitKey(0)

          # n: a usefull counter for the calculations bellow
          total_of_images = len(directory)
          n = 0
          for file in directory :
               n += 1
               # Read each image from directory
               im_data = cv2.imread(file, -1)
               # Crop each image based on coordinates the user selected above
               im_dataCrop = im_data[int(x):int(w), int(y):int(h)]
               # Save each croped-image to final directory 
               cv2.imwrite(os.path.join(desktop,'CroppedImage.{}.tif'.format(n)), im_dataCrop)

               # Ιncrease the percent of progess bar by 1 devided by total number of images
               bar['value']+=(1/total_of_images)*100
               percent.set(str(int((n/total_of_images)*100)) + "%")
               # A text that reports the current amount of croped images
               text.set(str(n)+"/"+str(total_of_images)+ " Cropped images completed")
               # Update the window 
               roi_root.update_idletasks()

          ctypes.windll.user32.MessageBoxW(0, "Process has been finished, Check Results directory ", "Success !", 1)

          # Usefull to output the runtime
          start_time = time.time()
          # Creating the date object of today's date
          todays_date = date.today()
          # Current time
          now = datetime.now()
          current_time = now.strftime("%H:%M:%S")

          # Image Name for coordinates
          dir_image_name = os.path.basename(Img_path.single_image_path)
          # Path of chosen Image for coordinate
          dir_img_path_name = os.path.dirname(Img_path.single_image_path)

          # Folder Name from choosen directory
          dir_folder_name = os.path.basename(Img_path.path)
          # Path from choosen directory
          dir_path_name = os.path.dirname(Img_path.path)
          # Creates the final report
          with open("Crop-tool Report_{}.txt".format(todays_date), "a") as f:
               f.write("#############################      REPORT      #############################" + '\n'
               +"\n" +'Coordinates : ' + "(" + str(x) + "," + str(w) + ")" + "\t"  + 
                    "(" + str(y) + "," + str(h) + ")" + "\n"
               +"\n" +'Name of Chosen Image for Coordinates : ' + dir_image_name + "\n" 
               +"\n" +'Path of Chosen Image for Coordinates : ' + dir_img_path_name + "\n" 
               +"\n" +'Name of Chosen Folder for Crop : ' + dir_folder_name + "\n" 
               +"\n" +'Path of Chosen Folder for Crop : ' + dir_path_name + "\n" 
               +"\n" +'Number of Calculated Images : ' + str(total_of_images) + "\n" 
               +"\n" +'Program Runtime :' + " %s seconds" % (time.time() - start_time) + "\n"
               +"\n" + 'Date : ' + str(todays_date) + "\n" 
               +"\n" + 'Time : ' + str(current_time) + "\n"
               )
     
     else :
        ctypes.windll.user32.MessageBoxW(0, "Choose image path or Directory path !", "Error", 1)      

##############################          TOOLBOX         #######################################
def tool_box():
     global roi_root
     roi_root = Toplevel()
     roi_root.geometry("320x180")
     roi_root.resizable(False,False)
     roi_root.title("Crop Image")
     #Second window will stay always on top
     roi_root.wm_attributes("-topmost", 1)
     crop_icon = PhotoImage(file=crop_png)
     roi_root.tk.call('wm', 'iconphoto', roi_root._w, crop_icon)
     # Read the optionDB.py file
     # This file contains the template 
     # For the Graphical User Interface
     roi_root.option_readfile('optionDB.py')
            # Read imageas a small icon 
     menu = Menu(roi_root)
     roi_root.config(menu=menu)
     filemenu = Menu(menu)
     menu.add_cascade(label="File", menu=filemenu)
     filemenu.add_command(label="Select Image Directory for Coordinates", command=image_path)
     filemenu.add_command(label="Select Dataset for Crop", command=folder_path)
     filemenu.add_separator()
     filemenu.add_command(label='Exit', command=roi_root.quit)
               
     helpmenu = Menu(menu)
     menu.add_cascade(label="Help", menu=helpmenu)
     helpmenu.add_command(label="About", command=information)
     helpmenu.add_command(label='Manual',command=popup_showinfo)

     global percent
     global text
     global bar
     percent = StringVar()
     text = StringVar()

     bar = Progressbar(roi_root, orient=HORIZONTAL, length=200, mode='determinate')
     bar.pack(pady=11)
     
     percentlabel = Label(roi_root, textvariable=percent)
     percentlabel.pack()
          
     tasklabel = Label(roi_root, textvariable=text)
     tasklabel.pack()

     bar['value']=0
     percent.set(str( "0 %"))
     text.set("0 " + " Cropped images completed")
     
     Run_Code_button = Button(roi_root, 
                              text="Crop Dataset", 
                              font=("Comic Sans",11),
                              bg='blue2', 
                              fg='white', 
                              command=crop_, 
                              height = 2, 
                              width = 18 )

     Run_Code_button.pack(side='bottom', padx=50, pady=12)
     roi_root.mainloop()
    