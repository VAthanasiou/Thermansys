import cv2
import glob
import os
import Img_path
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Progressbar
from Information import *
from tkinter.messagebox import showinfo
from Img_path import crop_png
from Img_path import bgimgpath
import time
from datetime import date
from datetime import datetime
import numpy as np
from matplotlib import pyplot as plt
import math



def popup_showinfo():
    showinfo('Manual for the code','here goes the manual')



def image_path():
     #global path
     Img_path.alg_enh_image = filedialog.askopenfilename()
     return




def histequal ():
                                                       # Path of original image
    img_orig = cv2.imread(Img_path.alg_enh_image)                         # Creates an image object

    img = cv2.cvtColor(img_orig, cv2.COLOR_BGR2GRAY )   # Converting RGB to gray


    #Histogram Equalization using inbuilt function--------------------------------
    equ = cv2.equalizeHist(img)


    #performing histogram equalization manually-----------------------------------

    origfreq = np.zeros((256,),dtype=np.float16)        # vector consisting of initial frequencies of gray scale values
    newgrayval = np.zeros((256,),dtype=np.float16)      # vector consisting of final gray scale values

    height, width = img.shape                           # Find height and width of image 


    # for loop to count frequency of gray scale values
    for i in range(width):                         
        for j in range(height):
            g = img[j,i]                                # g is grayscale value of pixel
            origfreq[g] = origfreq[g]+1                 # add 1 to count of frequency

    # reciprocal of total number of pixels
    tmp = 1.0/(height*width)                       

    # for loop to calculate final gray scale values
    for i in range(256):                           
        for j in range(i+1):                            # calculates cdf value  
            newgrayval[i] += origfreq[j] * tmp;                    
        newgrayval[i] = round(newgrayval[i] * 255)      # final gray scale value = cdf*(L-1)

    # b now contains the equalized histogram
    newgrayval=newgrayval.astype(np.uint8)

    # Re-map values from equalized histogram into the image   
    for i in range(width):                         
        for j in range(height):
            g = img[j,i]
            img[j,i]= newgrayval[g]
            
    #plot histograms--------------------------------------------------------------

    hist,bins = np.histogram(img.flatten(),256,[0,256]) # Create histogram of original image

    cdf = hist.cumsum()                                 # Computes cumulative sum of array elements
    cdf_normalized = cdf * hist.max()/ cdf.max()        # Normalize cdf value

    plt.hist(img.flatten(),256,[0,256], color = 'r')    # Converts image into 1D array and plot histogram
    plt.xlim([0,256])                                   # Limits the x axis values to 256
    plt.title("Histogram of original image")            # Title of histogram
    #plt.savefig("./hist.png", dpi=200)                # Save histogram
    #plt.show()                                          # Display histogram

    #perform histogram equalization
    cdf_temp = np.ma.masked_equal(cdf,0)                # Checks validity of cdf values and store in cdf_m ( temporary cdf for new image )
    cdf_temp = (cdf_temp - cdf_temp.min())*255/(cdf_temp.max()-cdf_temp.min()) # Formula for histogram equalisation
    cdf = np.ma.filled(cdf_temp,0).astype('uint8')      # Store value from cdf_m back into cdf

    img2 = cdf[img]                                     # Final image
    cdf_normalized = cdf * hist.max()/ cdf.max()        # Normalize cdf values

    plt.hist(img2.flatten(),256,[0,256], color = 'r')   # Converts image into 1D array and plot histogram
    plt.xlim([0,256])                                   # Limits the x axis value to 256
    plt.title("Histogram of equalized image")           # Title of histogram
    #plt.savefig("./8-equalized-hist.png", dpi=200)      # Save histogram
    #plt.show()                                          # Display histogram


    #Display all images-----------------------------------------------------------

    #cv2.imshow("Original Image", img_orig)                           # To display the image
    #cv2.imshow("After manual Histogram Equalization", img)           # To display the enhanced image (manual Histogram equalization)
    #cv2.imshow("After Histogram Equalization using inbuilt function", equ)   # To display the enhanced image (Histogram equalization using inbuilt function )
    #cv2.waitKey(0)
    color1 = cv2.applyColorMap(equ,cv2.COLORMAP_INFERNO)
    color2 = cv2.applyColorMap(img,cv2.COLORMAP_INFERNO)


    cv2.imwrite("Manual-histogram-equalization.png", color2)
    cv2.imwrite("Funcional-histogram-equalization.png", color1)

    # References:
    # 
    # 1. Manual histogram equalization algorithm:-
    # https://stackoverflow.com/questions/50578876/histogram-equalization-using-python-and-opencv-without-using-inbuilt-functions
    #
    # 2. Plot histograms:-
    # https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_histograms/py_histogram_equalization/py_histogram_equalization.html





def hismatch ():
    
    target_img = cv2.imread()           # Target image
    #print(target_img.shape)                       # Check the size of the image
    
    target_img = cv2.cvtColor(target_img, cv2.COLOR_BGR2GRAY )    # Converting RGB to gray
    target_img1=target_img
    target_img2=target_img

    path_ref=target_img
    img1 = cv2.imread()                               
    ref_img = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY )    # Reference image

    #Display target and reference images
    #cv2.imshow("Target image original", target_img) 
    #cv2.imshow("Reference image original", ref_img)

    plt.hist(target_img.flatten(),256,[0,256], color = 'r')     # Converts image into 1D array and plot histogram
    plt.xlim([0,256])                                           # Limits the x axis value to 256
    plt.title("Histogram of orig target image")                 # Title of histogram
    #plt.savefig("./target-orig-hist.png", dpi=200)              # Save histogram
    #plt.show()                                                  # Display histogram


    # Performing Equalisation on original image-----------------------------------

    target_freq = np.zeros((256,),dtype=np.float16)             # vector consisting of initial frequencies of gray scale values
    target_new_grayval = np.zeros((256,),dtype=np.float16)      # vector consisting of final gray scale values

    height, width = target_img.shape                            # Find height and width of image 

    max1 = 0
    # for loop to count frequency of gray scale values
    for i in range(width):                         
        for j in range(height):
            g = target_img[j,i]                                 # g is grayscale value of pixel
            target_freq[g] = target_freq[g]+1                   # adds 1 to count of frequency     
            if g>max1:
                max1=g
                
    #print(max1)
    # reciprocal of total number of pixels
    tmp = 1.0/(height*width)                       

    # for loop to calculate final gray scale values
    for i in range(256):                           
        for j in range(i+1):                                            # calculates cdf value  
            target_new_grayval[i] += target_freq[j] * tmp;                    
        target_new_grayval[i] = round(target_new_grayval[i] * 255)      # final gray scale value = cdf(L-1)

    # b now contains the equalized histogram
    target_new_grayval=target_new_grayval.astype(np.uint8)

    # Re-map values from equalized histogram into the image   
    for i in range(width):                         
        for j in range(height):
            g = target_img[j,i]
            target_img1[j,i]= target_new_grayval[g]
            

    #cv2.imshow("Target image after eq", target_img1)        

    """

    plt.hist(target_img1.flatten(),256,[0,256], color = 'r')   # Converts image into 1D array and plot histogram
    plt.xlim([0,256])                                   # Limits the x axis value to 256
    plt.title("Histogram of target image after eq")            # Title of histogram
    plt.show()                                          # Display histogram
    """


    # Histogram Equalisation of Reference Image-----------------------------------------------

    ref_freq = np.zeros((256,),dtype=np.float16)                # vector consisting of initial frequencies of gray scale values
    ref_new_grayval = np.zeros((256,),dtype=np.float16)         # vector consisting of final gray scale values

    height, width = ref_img.shape                               # Find height and width of image 

    max1 = 0
    # for loop to count frequency of gray scale values
    for i in range(width):                         
        for j in range(height):
            g = ref_img[j,i]                                    # g is grayscale value of pixel
            ref_freq[g] = ref_freq[g]+1                         # adds 1 to count of frequency     
            if g>max1:
                max1=g
    #print(max1)
    # reciprocal of total number of 
    tmp = 1.0/(height*width)                       

    # for loop to calculate final gray scale values
    for i in range(256):                           
        for j in range(i+1):                                    # calculates cdf value  
            ref_new_grayval[i] += ref_freq[j] * tmp;                    
        ref_new_grayval[i] = round(ref_new_grayval[i] * 255)    # final gray scale value = cdf(L-1)

    # b now contains the equalized histogram
    ref_new_grayval=ref_new_grayval.astype(np.uint8)

    # Re-map values from equalized histogram into the image   
    for i in range(width):                         
        for j in range(height):
            g = ref_img[j,i]
            ref_img[j,i]= ref_new_grayval[g]

    #cv2.imshow("Reference image after eq", ref_img)
    # Histogram matching----------------------------------------------------------

    target_match_intensity = np.zeros((256,),dtype=np.float16)  # vector consisting of final gray scale values

    for i in range(256):
        j=0
        #print(i,ref_new_grayval[i])
        while j<256 and ref_new_grayval[i]>target_new_grayval[j]:
            j+=1
        target_match_intensity[i]=j
        #print(i,ref_new_grayval[i])
        
    for i in range(width):                         
        for j in range(height):
            g = target_img[j,i]
            target_img2[j,i]= target_match_intensity[g]

    #plot histograms--------------------------------------------------------------


    plt.hist(ref_img.flatten(),256,[0,256], color = 'r')        # Converts image into 1D array and plot histogram
    plt.xlim([0,256])                                           # Limits the x axis value to 256
    plt.title("Histogram of orig reference image")              # Title of histogram
    #plt.savefig("./ref-hist.png", dpi=200)                     # Save histogram
    #plt.show()                                                  # Display histogram


    plt.hist(target_img2.flatten(),256,[0,256], color = 'r')    # Converts image into 1D array and plot histogram
    plt.xlim([0,256])                                           # Limits the x axis value to 256
    plt.title("Histogram of target image after histogram matching")            # Title of histogram
    #plt.savefig("./target-match-hist.png", dpi=200)            # Save histogram
    #plt.show()                                                  # Display histogram

    # ------------------------------------------------------------------------------------

    color1 = cv2.applyColorMap(target_img2,cv2.COLORMAP_INFERNO)

    #cv2.imshow("Target image after matching", target_img2)
    cv2.imwrite("Histogram-Matching.png", color1)

    #cv2.imwrite("target-after-hist-match.jpeg", target_img2)
    #cv2.waitKey(0)

    # References:
    #
    # 1. Manual histogram equalization algorithm:-
    # https://stackoverflow.com/questions/50578876/histogram-equalization-using-python-and-opencv-without-using-inbuilt-functions
    #
    # 2. Plot histograms:-
    # https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_histograms/py_histogram_equalization/py_histogram_equalization.html
    #
    # 3. Histogram matching algorithm:-
    # https://youtu.be/WXHFmJVHvag


def LTHM():
    # img = cv2.imread('clouds.jpg',0)
    #
    # # create a CLAHE object (Arguments are optional).
    # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    # cl1 = clahe.apply(img)
    #
    # cv2.imwrite('clahe_2.jpg',cl1)
    # cv2.imshow(mat,'clahe_2.jpg')
    # img_he = cv2.imread('clahe_2.jpg',0)
    # cv2.imshow('clahe_2.jpg')
    img = cv2.imread(Img_path.alg_enh_image,0)
    # cv2.imshow("input",img)
    equ = cv2.equalizeHist(img)
    # res = np.hstack((equ)) #stacking images side-by-side
    # cv2.imshow("hist eq",equ)
    #cv2.imwrite('res.jpg',equ)
    color = cv2.applyColorMap(equ,cv2.COLORMAP_INFERNO)
    cv2.imwrite('LTHM-Result.png',color)
    dft = cv2.dft(np.float32(equ),flags = cv2.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)

    magnitude_spectrum = 20*np.log(cv2.magnitude(dft_shift[:,:,0],dft_shift[:,:,1]))
    mag,angl = cv2.cartToPolar(dft_shift[:,:,0],dft_shift[:,:,1])

    #print(angl)
    #print(mag)
    plt.subplot(121),plt.imshow(img, cmap = 'gray')
    plt.title('Input Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(magnitude_spectrum, cmap = 'gray')
    plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
    #plt.show()       
    ctypes.windll.user32.MessageBoxW(0, "Process has been finished, Check Results directory ", "Sucess", 1)

def DPHE():
                                         # Path of original image
    img_orig = cv2.imread()                         # Creates an image object

    img = cv2.cvtColor(img_orig, cv2.COLOR_BGR2GRAY )   # Converting RGB to gray
    #cv2.imshow("Original", img)                         # Display original image

    # Plot Histogram of original image--------------------------------------------

    plt.hist(img.flatten(),256,[0,256], color = 'r')    # Converts image into 1D array and plot histogram
    plt.xlim([0,256])                                   # Limits the x axis values to 256
    plt.title("Histogram of original image")            # Title of histogram
    #plt.savefig("./1-orig-hist.png", dpi=200)               # Save histogram
    #plt.show()                                          # Show histogram


    # Double Plateus Histogram equalization---------------------------------------
    origfreq = np.zeros((256,),dtype=np.float16)        # vector consisting of initial frequencies of gray scale values
    newfreq = np.zeros((256,),dtype=np.float16)         # empty vector to store final frequencies of gray scale values
    newgrayval = np.zeros((256,),dtype=np.float16)      # vector consisting of final gray scale values
    height, width = img.shape                           # Find height and width of image 
    #print(img.shape)

    # for loop to count frequency of gray scale values
    for i in range(width):                         
        for j in range(height):
            g = img[j,i]                                # g is grayscale value of pixel
            origfreq[g] = origfreq[g]+1                 # add 1 to count of frequency

    # reciprocal of total number of pixels
    tmp = 1.0/(height*width)

    # Tup = Upper Threshold value
    # Tdown = Lower Threshold value
    # Calculate Tup
    count=0
    total=0
    not_zero=0
    for k in range(0,256):
        if origfreq[k]!=0:
            not_zero+=1
        if k<255 and k>=1 and origfreq[k+1]!=0 or origfreq[k-1]!=0:
            if (origfreq[k]>origfreq[k+1] or origfreq[k]>origfreq[k-1]):
                count+=1
                total+=origfreq[k]
            

    Tup = total/count
    Tup=2500
    #print('Tup',Tup)

    # Calculate Tdown using Tup
    Tdown = (np.min((1/tmp, not_zero*Tup )))/(255)
    #print('Tdown',Tdown)


    # Clipping
    excess=0                                        # no. of excess pixels (above Tup) for a bin
    deficit=0                                       # no. of deficit pixels (below Tdown) for a bin
    to_add=[]
    to_subtract=[]
    for k in range(0,256):
        if origfreq[k]==0:
            newfreq[k]=origfreq[k]
            to_add+=[k]
        elif origfreq[k]<Tdown:
            deficit += Tdown - origfreq[k]
            newfreq[k]=Tdown
        elif origfreq[k]>Tdown and origfreq[k]<Tup:
            newfreq[k]=origfreq[k]
            to_add+=[k]
            to_subtract+=[k]
        else:# origfreq[k] > Tup
            excess += origfreq[k] - Tup
            newfreq[k] = Tup
            
    # Redistribute excess pixels into other bins----------------------------------
    for i in to_add:
        if newfreq[i]<Tup:
            newfreq[i]+=excess/len(to_add)
            
    for i in to_subtract:
        if newfreq[i]>Tdown:
            newfreq[i]-=deficit/len(to_subtract)

    # Plot the new frequencies
    plt.plot(newfreq)
    plt.title("Clipped frequencies graph")
    #plt.savefig("./1-clipped-freq-graph.png", dpi=200)               # Save graph
    #plt.show()


    # for loop to calculate final gray scale values-------------------------------
    for i in range(256):                           
        for j in range(i+1):                            # calculates cdf value  
            newgrayval[i] += newfreq[j] * tmp;                    
        newgrayval[i] = round(newgrayval[i] * 255)      # final gray scale value = cdf*(L-1)

    # b now contains the equalized histogram
    newgrayval=newgrayval.astype(np.uint8)

    # Re-map values from equalized histogram into the image   
    for i in range(width):                         
        for j in range(height):
            g = img[j,i]
            img[j,i]= newgrayval[g]
            

    # Plot Histogram of enhanced image--------------------------------------------

    plt.hist(img.flatten(),256,[0,256], color = 'r')    # Converts image into 1D array and plot histogram
    plt.xlim([0,256])                                   # Limits the x axis value to 256
    plt.title("Histogram after DPHE")                   # Title of histogram
    #plt.savefig("./1-dphe-hist.png", dpi=200)     # Save histogram
    #plt.show()                                          # Display histogram

    '''
    # Plot Histogram of equalized image-------------------------------------------
    equ = cv2.equalizeHist(img)
    plt.hist(equ.flatten(),256,[0,256], color = 'r')    # Converts image into 1D array and plot histogram
    plt.xlim([0,256])                                   # Limits the x axis values to 256
    plt.title("Histogram after HE")                     # Title of histogram
    #plt.savefig("./8-hist.png", dpi=200)               # Save histogram
    plt.show()   
    #-----------------------------------------------------------------------------
    '''

    #Display all images-----------------------------------------------------------

    #cv2.imshow("After DPHE", img)             # To display the enhanced image (manual Histogram equalization)
    color1 = cv2.applyColorMap(img,cv2.COLORMAP_INFERNO)
    cv2.imwrite("DPHE.png", color1)
    # cv2.imshow("After HE", equ)             # To display the enhanced image (manual Histogram equalization)

    #cv2.waitKey(0)





##################################   TOOLBOX     ##############################################
def enhancement():
    global Enhancement_root
    Enhancement_root = Toplevel()
    Enhancement_root.geometry("320x180")
    Enhancement_root.resizable(False,False)
    Enhancement_root.title("Image Enhancement")
    #Second window will stay always on top
    Enhancement_root.wm_attributes("-topmost", 1)
    crop_icon = PhotoImage(file=bgimgpath)
    Enhancement_root.tk.call('wm', 'iconphoto', Enhancement_root._w, crop_icon)
    # Read the optionDB.py file
    # This file contains the template 
    # For the Graphical User Interface
    Enhancement_root.option_readfile('optionDB.py')
    # Read imageas a small icon 
    menu = Menu(Enhancement_root)
    Enhancement_root.config(menu=menu)
    filemenu = Menu(menu)
    menu.add_cascade(label="File", menu=filemenu)
    filemenu.add_command(label="Select image to enhance", command=image_path)
    filemenu.add_command(label='Exit', command=Enhancement_root.quit)

    helpmenu = Menu(menu)
    menu.add_cascade(label="Help", menu=helpmenu)
    helpmenu.add_command(label="About", command=information)
    helpmenu.add_command(label='Manual',command=popup_showinfo)
    
    
    
    global percent
    global text
    global bar
    percent = StringVar()
    text = StringVar()

    bar = Progressbar(Enhancement_root, orient=HORIZONTAL, length=200, mode='determinate')
    bar.pack(side='top', pady=14)
     
    percentlabel = Label(Enhancement_root, textvariable=percent)
    percentlabel.pack()
          
    tasklabel = Label(Enhancement_root, textvariable=text)
    tasklabel.pack()

    bar['value']=0
    percent.set(str( "0 %"))
    text.set("0 " + " Images Calculated")

    Run_Code_button = Button(Enhancement_root, 
                                text="Enhance Image", 
                                bg='blue3', 
                                fg='white', 
                                command=call_algorithms, 
                                height = 2, 
                                width = 28
                                )
    Run_Code_button.pack(side='bottom', padx=50, pady=14)
    Enhancement_root.mainloop()

def call_algorithms():

            # Create the Croped data directory        
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop', r"Enhanced Images")
        # If the above path doesnt exist create the directories below
        # In this directory we save the calculations
        # For the user to look at the now visible images
    if not os.path.exists(desktop):
            os.makedirs(desktop)
    
    if not os.path.exists(Img_path.alg_enh_image):
        ctypes.windll.user32.MessageBoxW(0, 'Choose image for enhancement', "Error", 1) 
        
        #hismatch(path)
    #LTHM WORKS 13/12/2022    
    LTHM()
    #Histogram Equalization works 13/12/2022
    histequal()
        #DPHE(path)
    


