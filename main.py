#!/usr/bin/env python


from sys import argv
from os import system
import zbar
import Image
import cv
import cv2


import os
import pygame
import libardrone
import numpy as np
from PIL import Image
import cv2
import sys, qrcode
from qrtools import QR
 
def scanner():
	SEPARATOR = ' '
	TERMINATOR = ' '

	image = cv2.imread('temp.png',1)
	
	cv_img_color=cv.fromarray(image)
	
	width = cv_img_color.width
	
	height = cv_img_color.height
	
	cv_img = cv.CreateImage((width, height), cv.IPL_DEPTH_8U, 1)
	
	cv.CvtColor(cv_img_color, cv_img, cv.CV_RGB2GRAY)
	
	raw = cv_img.tostring()
	
	scanner = zbar.ImageScanner()
	
	scanner.parse_config('enable')

	image = zbar.Image(width, height, 'Y800', raw)
	
	scanner.scan(image)

	strings = [symbol.data for symbol in image.symbols]
	
	output = SEPARATOR.join(strings) + TERMINATOR

		
	
	del(image)
	return strings

def main():
    pygame.init()
    W, H = 320, 240
    screen = pygame.display.set_mode((W, H))
    drone = libardrone.ARDrone()

    clock = pygame.time.Clock()
    running = True
    test=True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
		drone.land()

                running = False
	    if event.type == pygame.KEYDOWN:
                           if event.key == pygame.K_SPACE:
				drone.land()
 
                           if event.key == pygame.K_m:
                                drone.takeoff()
				drone.hover()

                           if event.key == pygame.K_s:
				drone.move_forward()
				pygame.time.wait(1000)
				drone.hover()

           

        try:
            surface = pygame.image.fromstring(drone.image, (W, H), 'RGB')
            
            screen.blit(surface, (0, 0))

	    pygame.image.save(surface,'temp.png')
	    
	    strings=scanner()
            if strings==[]:
		test=True
	    if strings==['takeoff']:
		drone.takeoff()
		drone.hover()
    

	    if strings==['forward']:
		
		drone.move_forward()
		pygame.time.wait(1000)
		drone.hover()
		
		
	    if strings==['back']:
		
		drone.move_backward()
		pygame.time.wait(1000)
		drone.hover()


	    if strings==['left']:
		
		drone.turn_left()
		pygame.time.wait(1000)
		drone.hover()


	    if strings==['right']:
		
		drone.turn_right()
		pygame.time.wait(1000)
		drone.hover()



	    if strings==['land'] :
		drone.land()		

	
		



        except:
            pass

        pygame.display.flip()
        clock.tick(20)
        pygame.display.set_caption("FPS: %.2f" % clock.get_fps())

    print "Shutting down...",
    drone.halt()
    print "Ok."

if __name__ == '__main__':
    main()


