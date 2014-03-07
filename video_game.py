# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 10:59:53 2014

@authors: Pratool, Nitya, Gabrielle
"""

# -*- coding: utf-8 -*-

"""

Created on Wed Mar  5 22:29:57 2014

 

@author: gabrielle

"""

 

import sys, pygame

pygame.init()

from pygame.locals import *

 

w = 1000;

h = 1000;

speed = [0, 0]

black = 0,0,0

 

screen = pygame.display.set_mode((w, h))

 

sprite = pygame.image.load("elephant.gif")

el_rect = sprite.get_rect()

 

while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT: sys.exit()

        elif event.type == MOUSEBUTTONDOWN:

    el_rect = el_rect.move(speed)

    if el_rect.left < 0 or el_rect.right > w:

        speed[0] = -speed[0]

    if el_rect.top < 0 or el_rect.bottom > h:

        speed[1] = -speed[1]

    screen.fill(black)

    screen.blit(sprite, el_rect)

    pygame.display.flip()