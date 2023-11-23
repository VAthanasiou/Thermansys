#######################################################################################
#              THIS MODULE PERFORMS THE IMAGE PATH FOR SINLGE                         #
#              OR MULTIPLE IMAGES AS AN USERS INPUT                    		          #
#       >  TAKES INPUT THE THRESHOLDED IMAGE                                          #
#       >  FIND THE SHAPE OF EACH IMAGE                                               #
#       >  APPEND THE RESULT (STRING VALUE) TO A LIST                                 #
#       >  RETURN THE APPENDED LIST                                                   #
#           				                                                          #
#           >  WRITTEN BY A.GKOURAS, V.ATHANASIOU, L.GERGIDIS					      #
#           						                                                  #
#	          *****************IMPORTANT*********************		                  #
#        IF IT FAILS TO LOAD IMAGES, CHECK THE NAMES AND THE TYPE OF EACH IMAGE       #
#######################################################################################


from tkinter import *

global path
global rectacnglesPath
global single_image_path
global icon_photo
global ir_icon_photo
global alg_enh_image

data_path =''

single_image_path= ''

# The directory where the images reside (user input)
path = ""
# Images for the 4 point Lock In
S1_path = ""
S2_path = ""
S3_path = ""
S4_path = ""
# Image path for the enhancment algorithms to work
alg_enh_image=""
# Various images for icons, backround images, e.t.c.
rectanglesPath = "" # ????
# Backround image used in main window
bgimgpath = 'images\\logo.png' 
# Image used in main window upper left corner 
icon_photo = 'images\\logo.png'
#
ir_icon_photo = 'images\\logo.png'
#
crop_png = 'images\\crop_image.png'
#
roi_image1 = 'images\\crop_image1.png'
#
icon_exit = 'images\\exit_icon.png'
#
manual_icon = 'images\\manual_icon.png'
#Image used for the about section in the menu
about_icon = 'images\\about_icon.png'
# Image used for the enhancment icon in the tools menu
img_enh = 'images\\image_en.png'

