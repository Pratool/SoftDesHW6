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

pygame.mixer.music.load('meow.mp3')     # Cat's meow sound

# Commonly used RGB color tuples
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class BallFollowModel:
    """ This encodes the game state of our Ball Drawing Game self refers to the
        implicit object parameter
    """
    def __init__(self):
        """ This initializes the model attributes of the model include:
            width       integer
            height      integer
            balls       list
            click1_set  boolean
        """
        self.width = 640    # Window's width
        self.height = 480   # Window's height
        self.balls = []
        self.click1_set = True
        self.num_clicks = 0
        
        # Sets the first ball's top-left corner at the center of the window
        new_ball = Ball((self.width/2), (self.height/2), [0,0])
        self.balls.append(new_ball)
        
        self.score = 0
        
        # Sets up the rendering of the final score text
        self.basicFont = pygame.font.SysFont(None, 48)
        self.text = self.basicFont.render('', True, GREEN)
        self.textRect = self.text.get_rect()
  
    def get_score(self, scr):
        """ This function judges the user drawn picture against the provided image to see how
            close the user drawn picture is to the provided image.
        """
        
        # Loops through all the pixels and checks how many white and black pixels are
        # left in the background
        white = 0
        black = 0
        for i in range(self.width - 1):
            for j in range(self.height - 1):
                rgb = tuple(scr.get_at((i, j)))
                if rgb == (255, 255, 255, 255):
                    white += 1
                if rgb == (0, 0, 0, 255):
                    black += 1
        
        # Score calculation
        self.score = round((1 - float(white)/(black+white))*100.0 - 1.5*self.num_clicks)
        
        # PyGame setup for the text to be drawn
        self.text = self.basicFont.render('Score: ' + str(self.score), True, GREEN)
        self.textRect = self.text.get_rect()

class Ball:
    """This is the initializing function for the ball and contains all the properties
        the ball needs to have.
        input:
            width   integer             width of the image of the ball
            height  integer             height of the image of the ball
            x       floating point      x position of the ball
            y       floating point      y position of the ball
            speed   list                x and y vectors of velocity, respectively

        Ball attributes:
            pos         list
            color       tuple
            sprite      surface
            rectangle   object
            speed       list
    """
  
    def __init__(self, x, y, speed):
        self.pos = [x, y]
        self.width = 35
        self.height = 35
        self.color = WHITE
        self.sprite = pygame.image.load('paul.gif')
        self.rect = self.sprite.get_rect()
        self.rect.topleft = (int(self.pos[0]), int(self.pos[1])) # The topleft is a tuple of integers only
        self.speed = speed
      

class BallFollowView:
    """ This renders the BallFollowModel to a pygame window """
  
    def __init__(self, model, screen):
        """ The initializing function for the view takes in the model (an object)
            and the screen (a surface) and sets them equal to the model and screen
            used in the class.
        """
        self.model = model
        self.screen = screen

    def draw(self):
        """ This function draws the ball on the screen where it needs to go and
            updates the position of the ball each time the function is called.
        """
        for ball in self.model.balls:
            self.screen.blit(ball.sprite, ball.rect)
        self.screen.blit(self.model.text, self.model.textRect)
        pygame.display.flip()
        pygame.display.update()

class BallFollowController:
    """ This manipulates the objects of BallFollowModel """
    
    def __init__(self, model, screen):
        """ The initializing function for the controller takes in the model and
            screen as inputs and sets them equal to the model and screen used in
            the class.  It also keeps track of the mouse position
        """
        self.model = model
        self.mouse_pos = (0, 0)
        self.screen = screen
  
    def handle_mouse_event(self, event):
        """ This function handles the mouse event input. When the mouse is clicked,
            the position of the click is stored, and the function figures out which
            click it is and either stops the ball if the ball is moving or sends the
            ball in the direction of the click if the ball is stopped.
        """
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
        """ Handles and event in which a key is pressed. If that key is the 'Enter'
            button, it displays the score.
        """
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                self.model.get_score(screen)
  
    def set_speed(self):
        """ This function sets the velocity of the ball in the direction it needs to go using vector math. The
            direction of the velocity is from the origin (org) pointing to the target
        """
        target = self.mouse_pos
        org = self.model.balls[0].pos
        
        # Computes the direction of 'speed' (really velocity) by taking each of the
        # components of the displacement and dividing it by the displacement's magnitude
        vx = (target[0] - org[0])/math.sqrt((target[0]-org[0])**2 + (target[1]-org[1])**2)
        vy = (target[1] - org[1])/math.sqrt((target[0]-org[0])**2 + (target[1]-org[1])**2)
        
        self.model.balls[0].speed = [vx, vy]
  
    def move_ball(self):
        """ This function moves the ball by adding the speed to the position."""
        scr = self.screen
        scr.fill((255, 105, 180), model.balls[0].rect)
        
        V_factor = 2
        
        self.model.balls[0].pos[0] += V_factor*self.model.balls[0].speed[0]
        self.model.balls[0].pos[1] += V_factor*self.model.balls[0].speed[1]
        error = [self.model.balls[0].pos[0] - self.model.balls[0].rect.topleft[0], self.model.balls[0].pos[1] - self.model.balls[0].rect.topleft[1]]
      
        self.model.balls[0].rect = self.model.balls[0].rect.move(self.model.balls[0].speed)
        self.model.balls[0].rect = self.model.balls[0].rect.move(error)
        
        # If the ball's position goes out of the window's view, negate either
        # the x or y component of the speed. Every time it hits the window's edge
        # it emits a sound
        if self.model.balls[0].pos[0] < 0 or self.model.balls[0].pos[0]+self.model.balls[0].width > self.model.width:
            self.model.balls[0].speed[0] = -self.model.balls[0].speed[0]
            pygame.mixer.music.play(0)
        if self.model.balls[0].pos[1] < 0 or self.model.balls[0].pos[1]+self.model.balls[0].height > self.model.height:
            self.model.balls[0].speed[1] = -self.model.balls[0].speed[1]
            pygame.mixer.music.play(0)

#----------------------------------------------------------------------------#

model = BallFollowModel()

screen = pygame.display.set_mode((model.width, model.height))

# Sets the background that the player must attempt to recreate
background = pygame.image.load('cool_pic5.png')
background_rect = background.get_rect()
screen.blit(background,background_rect)
pygame.display.flip()
pygame.display.update()

view = BallFollowView(model, screen)
controller = BallFollowController(model, screen)

# Infinite loop that the game runs in
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        controller.handle_mouse_event(event)
        controller.handle_key_event(event)
    
    if model.click1_set == False:
        controller.move_ball()
    
    view.draw()
    time.sleep(0.0001)  # Sets the time between frames to be 0.1 ms
