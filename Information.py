#######################################################################################
#              THIS MODULE PERFORMS THE IMPORT OF THE INFROMATION                     #
#              ABOUT THE COMPUTER PROGRAM THERMANSYS 		                          #
#       >                                                                             #
#       >                                                                             #
#       >                                                                             #
#       >                                                                             #
#           				                                                          #
#           >  WRITTEN BY A.GKOURAS, V.ATHANASIOU, L.GERGIDIS					      #
#           						                                                  #
#######################################################################################


# import the necessary packages
import argparse
import os
import cv2
import glob
import ctypes 
import numpy as np 


def information():
 ctypes.windll.user32.MessageBoxW(0, "Written by Arsenios Gkourras, Vassilis Athanasiou, Leonidas Gergidis \
 http://www.materials.uoi.gr/simlab/", 
"ThermAnsys", 1)
    