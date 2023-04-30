import math

import pygame
import constants

class Character():
    def __init__(self, x, y, mob_animations, char_type):
        self.char_type = char_type
        self.flip = False
        self.animation_list = mob_animations[char_type]
        self.frame_index = 0
        self.action = 0 # 0 is IDLE, 1 is RUNNING
        self.update_time = pygame.time.get_ticks()
        self.running = True
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect(0, 0, 40, 40)
        self.rect.center = (x, y)

    def move(self, dx, dy):
        self.running = False

        if dx != 0 or dy != 0: #if this coords are not 0, there is movement
            self.running = True
        if dx < 0: #player moves to the left
            self.flip = True #player flips to the left side
        if dx > 0:
            self.flip = False

        #control diagonal speed
        if dx != 0 and dy != 0: #if one coord is 0, movement is horizontal or vertical
            dx = dx * (math.sqrt(2)/2)
            dy = dy * (math.sqrt(2)/2)

        self.rect.x += dx
        self.rect.y += dy

    # updating the state of the moving and flipped image
    def update(self):
        #check what action the player is performing
        if self.running == True:
            self.update_action(1)# 1 = RUN
        else:
            self.update_action(0)# 0 = IDLE


        #handle animation and update image
        animation_cooldown = 75
        self.image = self.animation_list[self.action][self.frame_index]
        #checking if enough time has passed since last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        #checking if animation range has finished, if not it gives an error
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    #helper function to define if character is IDLE or RUNNING
    def update_action(self, new_action):
        #check if new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            #update animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
    def draw(self, surface):
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(flipped_image, self.rect)
        pygame.draw.rect(surface, (constants.RED), self.rect, 1)

