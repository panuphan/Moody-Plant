# sudo apt-get install mpg321
#import os
#os.system('mpg321 Ave-maria-instrumental.mp3 &')

import pygame
pygame.mixer.init()
pygame.mixer.music.load("Ave-maria-instrumental.mp3")
pygame.mixer.music.play(-1) # note -1 for playing in loops
# do whatever
# when ready to stop do:
#pygame.mixer.unpause()

""" https://www.youtube.com/watch?v=m_y66_b1Edc """
