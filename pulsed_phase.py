#######################################################################################
#              THIS MODULE PERFORMS THE FAST FOURIER TRANSFORM                        #
#              ON THE INPUTED DATASET FOR PULSE PHASE METHOD         		          #
#       >  CREATES TOOLBOX FOR GUI                                                    #
#       >  TAKES INPUT THE DATASET IMAGES FROM USER                                   #
#       >  NORMALIZE IMAGES                                                           #
#       >  PERFORM FAST FOURIER TRANSFORM TO THE NORMALIZED IMAGES                    #
#       >  CALCULATES AMPLITUDE AND PHASE AND SAVES THE FINAL REULTS                  #
#           				                                                          #
#           >  WRITTEN BY A.GKOURAS, V.ATHANASIOU, L.GERGIDIS					      #
#           						                                                  #
#	          *****************IMPORTANT*********************		                  #
#                   IF IT FAILS TO RUN, CHECK DIRECTORIES                             #
#######################################################################################
#######################################################################################
#										                                              #
#                             CODE FOR PV_AUTO SCOUT	                              #
#								                                                      #
#                                 Flow chart                                          #
#       Creates Grafical User Interface                                               #
#       reads images as user input and calculates standard deviation of them          #
#       normalize the images and perform fft and inverse fourier transform            #
#       calculates phase and amplitude and saves the final results                    #
#                                                                                     #
#                                                                                     #
#                                                                                     #
#######################################################################################

from tkinter.ttk import Progressbar
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
import Img_path
import ctypes
import time
from datetime import date
from datetime import datetime

def image_path():
    #global path
    Img_path.path = filedialog.askdirectory()
    return

def popup_showinfo():
    showinfo('Manual for the code','here goes the manual')

########################################   TOOLBOX   ##############################################
def Pulse_Phase():
    global PPT_root
    PPT_root = Toplevel()
    PPT_root.geometry("320x180")
    PPT_root.resizable(False,False)
    PPT_root.title("Pulse Phase Calculator")
    #Second window will stay always on top
    PPT_root.wm_attributes("-topmost", 1)
    crop_icon = PhotoImage(file=bgimgpath)
    PPT_root.tk.call('wm', 'iconphoto', PPT_root._w, crop_icon)
    # Read the optionDB.py file
    # This file contains the template 
    # For the Graphical User Interface
    PPT_root.option_readfile('optionDB.py')
    # Read imageas a small icon 
    menu = Menu(PPT_root)
    PPT_root.config(menu=menu)
    filemenu = Menu(menu)
    menu.add_cascade(label="File", menu=filemenu)
    filemenu.add_command(label="Select Image Directory", command=image_path)
    filemenu.add_separator()
    filemenu.add_command(label='Exit', command=PPT_root.quit)
    
    helpmenu = Menu(menu)
    menu.add_cascade(label="Help", menu=helpmenu)
    helpmenu.add_command(label="About", command=information)
    helpmenu.add_command(label='Manual',command=popup_showinfo)

    global percent
    global text
    global bar
    percent = StringVar()
    text = StringVar()

    bar = Progressbar(PPT_root, orient=HORIZONTAL, length=200, mode='determinate')
    bar.pack(pady=11)
     
    percentlabel = Label(PPT_root, textvariable=percent)
    percentlabel.pack()
          
    textlabbl = Label(PPT_root, textvariable=text)
    textlabbl.pack()

    bar['value']=0
    percent.set(str( "0 %"))
    text.set("0 " + " Images have Processed")

    Run_Code_button = Button(PPT_root, 
                              text="Pulsed Phase Results", 
                              bg='blue2', 
                              fg='white', 
                              command=pulse_phase_therm, 
                              height = 2, 
                              width = 28
                              )
    Run_Code_button.pack(side='bottom', padx=50, pady=12)
    PPT_root.mainloop()
     

     ########################################   METHOD   ##############################################

def pulse_phase_therm():

    if os.path.exists(Img_path.path) :
        # Create the Croped data directory        
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop', r"Pulsed Phase Results")
        # If the above path doesnt exist create the directories below
        # In this directory we save the calculations
        # For the user to look at the now visible images
        if not os.path.exists(desktop):
            os.makedirs(desktop)

        # Usefull to output the runtime
        start_time = time.time()
        # Creating the date object of today's date
        todays_date = date.today()
        # Current time
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        # The path where the thermographig images reside
        # We only need .tif images for the calculation thus the *.tif extension 
        # If anything comes up we add more extensions 
        images_path = glob.glob(Img_path.path+'\\*.tif')
        #Set counter n, and sums mean_im and std_im , zero
        n = 0 
        mean_im = 0 
        std_im = 0
        total_of_imgs = len(images_path)
        # reading images in for loop
        for file in images_path:
            n += 1
            #Reading .tif images from Images Path
            image = cv2.imread(file, -1)
            #'Convert' images to arrays for the above calculations
            image = np.array(image, dtype=np.float64)
            #Sum each image to mean_im (Mean Image) to calculate the Average/Mean Image
            mean_im += image
            std_im += (image - mean_im) ** 2
            # Ιncrease the percent of progess bar by 1 devided by total number of images
            bar['value']+=(1/total_of_imgs)*100
            percent.set(str(int((n/total_of_imgs)*100)) + "%")
            # A text that reports the current amount of croped images
            text.set(str(n)+"/"+str(total_of_imgs)+ " Images Calculated")
            # Update the window 
            PPT_root.update_idletasks()


        #Devide by n-1 the result of Standard Deviation Image sum
        std_im = np.sqrt(std_im / n-1)
        #Devide the result by n of Mean Image sum
        #n = the number of images
        mean_im = mean_im/n
        #normalize image to process for the fast fourrier transform
        norm_image = cv2.normalize(std_im, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
        #Perform FFT to the normalized image 
        f = np.fft.fft2(norm_image)
        # shift low frequencies
        fshift = np.fft.fftshift(f)
        # Calculate the magnitute_spectrum
        magnitude_spectrum = 20*np.log(np.abs(fshift))
        #Extract the real part from the shifted low frequencies
        dft_real = np.real(fshift)
        #Extract the imaginay part from the shifted low frequencies
        dft_imag = np.imag(fshift)
        # Perform the inverse fourier transform
        f_ishift = np.fft.ifftshift(fshift)
        # Perform the inverse fourier to the shifted low frequencies
        img_back = np.fft.ifft2(f_ishift)
        # Calculate the amplitute of the image
        img_back = np.abs(img_back)
        #calculate the phase of the image
        Phase = np.arctan(dft_imag,dft_real)
        # Convert image to np.uint8 to apply the colormaps
        ampl = np.uint8(img_back)
        # apply colomarps to the amplitute image
        ampl_image = cv2.applyColorMap(ampl, cv2.COLORMAP_INFERNO)
        ampl_image2 = cv2.applyColorMap(ampl, cv2.COLORMAP_BONE)
        # convert phase image
        phase_img = ~ampl_image2
        phase_img = cv2.applyColorMap(phase_img, cv2.COLORMAP_INFERNO)

        # assign names for the saved images
        phase_img_name= 'Phase.png'
        amplitude_img_name = 'Amplitute.png'
        # Folder Name from choosen directory
        dir_folder_name = os.path.basename(Img_path.path)
        # Path from choosen directory
        dir_path_name = os.path.dirname(Img_path.path)
        #Write & Save results from the calculations to file  (Report.txt)
        with open("Pulsed Phase Report_{}.txt".format(todays_date), "a") as f:
            f.write("#############################      REPORT      #############################" + '\n'
                    +"\n" +'Folder Name : ' + dir_folder_name + "\n" 
                    +"\n" +'Directory Path : ' + dir_path_name + "\n" 
                    +"\n" +'Number of Calculated Images : ' + str(total_of_imgs) + "\n" 
                    +"\n" +'Program Runtime :' + " %s seconds" % (time.time() - start_time) + "\n"
                    +"\n" + 'Date : ' + str(todays_date) + "\n" 
                    +"\n" + 'Time : ' + str(current_time) + "\n"
                    )
       
        # save images to the the results directory
        cv2.imwrite(os.path.join(desktop , phase_img_name), phase_img)
        cv2.imwrite(os.path.join(desktop , amplitude_img_name), ampl_image)
        ctypes.windll.user32.MessageBoxW(0, "Process has been finished, Check Results directory ", 
"Success !", 1)

#If the image path doesnt exist point it out with the error window
    else :
        ctypes.windll.user32.MessageBoxW(0, "Choose image path", 
"Error", 1)