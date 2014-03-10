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

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class BallFollowModel:
    """ This encodes the game state of our Ball Drawing Game """
    def __init__(self):
        self.width = 640    # Window's width
        self.height = 480   # Window's height
        self.balls = []
        self.click1_set = True
        self.num_clicks = 0
        new_ball = Ball((self.width/2), (self.height/2), [0,0])
        self.balls.append(new_ball)
        self.score = 0
        self.basicFont = pygame.font.SysFont(None, 48)
        self.text = self.basicFont.render('', True, GREEN)
        self.textRect = self.text.get_rect()
  
    def get_score(self, scr):
        for i in range(self.width - 1):
            for j in range(self.height - 1):
                rgb = tuple(scr.get_at((i, j)))
                if rgb == WHITE or rgb == BLACK:
                    self.score += 1

        self.score = (1 - (self.score / (self.width*self.height)))*100.0 - 1.5*self.num_clicks
        self.text = self.basicFont.render('Score: ' + str(self.score), True, GREEN)
        self.textRect = self.text.get_rect()

class Ball:
    """ This is the ball the the user controls """
  
    def __init__(self, x, y, speed):
        self.pos = [x, y]
        self.color = WHITE
        self.sprite = pygame.image.load('paul.gif')
        self.rect = self.sprite.get_rect()
        self.rect.topleft = (int(self.pos[0]), int(self.pos[1]))
        self.speed = speed
      

class BallFollowView:
    """ This renders the BallFollowModel to a pygame window """
  
    def __init__(self, model, screen):
        self.model = model
        self.screen = screen

    def draw(self):
        #self.screen.fill(pygame.Color(0,0,0))
        for ball in self.model.balls:
            self.screen.blit(ball.sprite, ball.rect)
        self.screen.blit(self.model.text, self.model.textRect)
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
                self.model.click1_set = False
            elif self.model.click1_set == False:
                self.model.click1_set = True
                self.set_speed()
            self.model.num_clicks += 1
    
    def handle_key_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                self.model.get_score(screen)
  
    def set_speed(self):
        target = self.mouse_pos
        org = self.model.balls[0].pos
        vx = (target[0] - org[0])/math.sqrt((target[0]-org[0])**2 + (target[1]-org[1])**2)
        vy = (target[1] - org[1])/math.sqrt((target[0]-org[0])**2 + (target[1]-org[1])**2)
        self.model.balls[0].speed = [vx, vy]
  
    def move_ball(self):
        scr = self.screen
        scr.fill((255, 105, 180), model.balls[0].rect)
        
        self.model.balls[0].pos[0] += 2*self.model.balls[0].speed[0]
        self.model.balls[0].pos[1] += 2*self.model.balls[0].speed[1]
        error = [self.model.balls[0].pos[0] - self.model.balls[0].rect.topleft[0], self.model.balls[0].pos[1] - self.model.balls[0].rect.topleft[1]]
      
        self.model.balls[0].rect = self.model.balls[0].rect.move(self.model.balls[0].speed)
        self.model.balls[0].rect = self.model.balls[0].rect.move(error)

        if self.model.balls[0].pos[0] < 0 or self.model.balls[0].pos[0]+35 > self.model.width:
            self.model.balls[0].speed[0] = -self.model.balls[0].speed[0]
            pygame.mixer.music.play(0)
        if self.model.balls[0].pos[1] < 0 or self.model.balls[0].pos[1]+35 > self.model.height:
            self.model.balls[0].speed[1] = -self.model.balls[0].speed[1]
            pygame.mixer.music.play(0)

background = pygame.image.load('cool_pic5.png')
background_rect = background.get_rect()

model = BallFollowModel()

screen = pygame.display.set_mode((model.width, model.height))
screen.blit(background,background_rect)
pygame.display.flip()
pygame.display.update()

view = BallFollowView(model, screen)
controller = BallFollowController(model,screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        controller.handle_mouse_event(event)
        controller.handle_key_event(event)
    
    if model.click1_set == False:
        controller.move_ball()
    
    view.draw()
    time.sleep(0.0001)
