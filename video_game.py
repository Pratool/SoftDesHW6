# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 10:59:53 2014

@authors: Pratool, Nitya, Gabrielle
"""

import sys, pygame

pygame.init()

from pygame.locals import *
import pdb
import time
import math

pygame.mixer.music.load('meow.mp3')

class BallFollowModel:
    """ This encodes the game state of our Ball Drawing Game """
    def __init__(self):
        self.width = 640    # Window's width
        self.height = 480   # Window's height
        self.balls = []
        self.click1_set = True
        new_ball = Ball((self.width/2), (self.height/2), [0,0])
        self.balls.append(new_ball)
    def update(self):
        self.ball.update()


class Ball:
    """ This is the ball the the user controls """
    
    def __init__(self, x, y, speed):
        self.pos = [x, y]
        self.color = (255, 255, 255)
        self.sprite = pygame.image.load('paul.gif')
        self.rect = self.sprite.get_rect()
        self.rect.topleft = (int(self.pos[0]), int(self.pos[1]))
        self.speed = speed
    
#    def update(self):
#        self.x += self.vx
#        self.y += self.vy
        

class BallFollowView:
    """ This renders the BallFollowModel to a pygame window """
    
    def __init__(self, model, screen):
        self.model = model
        self.screen = screen

    def draw(self):
        #self.screen.fill(pygame.Color(0,0,0))
        for ball in self.model.balls:
            self.screen.blit(ball.sprite, ball.rect)
        pygame.display.flip()
        pygame.display.update()
        
        

class BallFollowController:
    """ This manipulates the objects of BallFollowModel """
    def __init__(self, model, screen):
        self.model = model
        self.mouse_pos = (0, 0)
        self.screen = screen
    
    def handle_mouse_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            self.mouse_pos = pygame.mouse.get_pos()
            if self.model.click1_set == True:
                self.set_speed()
#                self.model.speed = [0, 0]
                self.model.click1_set = False
            elif self.model.click1_set == False:
                self.model.click1_set = True
                self.set_speed()
    
    def set_speed(self):
        target = self.mouse_pos
        org = self.model.balls[0].pos
        vx = (target[0] - org[0])/math.sqrt((target[0]-org[0])**2 + (target[1]-org[1])**2)
        vy = (target[1] - org[1])/math.sqrt((target[0]-org[0])**2 + (target[1]-org[1])**2)
        self.model.balls[0].speed = [vx, vy]
    
    def move_ball(self):
        scr = self.screen
        scr.fill((255, 105, 180), model.balls[0].rect)
        #scr.fill((255, 255, 255), model.balls[0].rect)

#        self.model.balls[0].rect = self.model.balls[0].rect.move(self.model.balls[0].speed)
        self.model.balls[0].pos[0] += 2*self.model.balls[0].speed[0]
        self.model.balls[0].pos[1] += 2*self.model.balls[0].speed[1]
        error = [self.model.balls[0].pos[0] - self.model.balls[0].rect.topleft[0], self.model.balls[0].pos[1] - self.model.balls[0].rect.topleft[1]]
        
        self.model.balls[0].rect = self.model.balls[0].rect.move(self.model.balls[0].speed)
        self.model.balls[0].rect = self.model.balls[0].rect.move(error)
        
#        if self.model.balls[0].rect.left < 0 or self.model.balls[0].rect.right > self.model.width:
#            self.model.balls[0].speed[0] = -self.model.balls[0].speed[0]
#        if self.model.balls[0].rect.top < 0 or self.model.balls[0].rect.bottom > self.model.height:
#            self.model.balls[0].speed[1] = -self.model.balls[0].speed[1]

        if self.model.balls[0].pos[0] < 0 or self.model.balls[0].pos[0]+35 > self.model.width:
            self.model.balls[0].speed[0] = -self.model.balls[0].speed[0]
            pygame.mixer.music.play(0)
        if self.model.balls[0].pos[1] < 0 or self.model.balls[0].pos[1]+35 > self.model.height:
            self.model.balls[0].speed[1] = -self.model.balls[0].speed[1]
            pygame.mixer.music.play(0)
        print self.model.height, self.model.width
        
        #scr.make_trail()
#        pygame.self.screen.fill((212,175,55), model.balls[0].rect)
#         Debugging
#        print 'Target', self.mouse_pos
#        print 'Speed', self.model.balls[0].speed
#        print 'Position', self.model.balls[0].rect.topleft



model = BallFollowModel()
screen = pygame.display.set_mode((model.width, model.height))
view = BallFollowView(model, screen)
controller = BallFollowController(model,screen)

while True:
    for event in pygame.event.get():
        if event.type  == pygame.QUIT:
            #pygame.image.save(screen,'cool_pic6.png')
            sys.exit()
        controller.handle_mouse_event(event)
    if model.click1_set == False:
        controller.move_ball()
        print 'Have not clicked to stop'
    view.draw()
    time.sleep(0.0001)


