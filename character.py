import math

import pygame
import constants

class Character():
    def __init__(self, x, y, animation_list):
        self.flip = False
        self.animation_list = animation_list
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = animation_list[self.frame_index]
        self.rect = pygame.Rect(0, 0, 40, 40)
        self.rect.center = (x, y)

    def move(self, dx, dy):

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

    def update(self): #updating the state of the moving and flipped image
        #handle animation and update image
        animation_cooldown = 75
        self.image = self.animation_list[self.frame_index]
        #checking if enough time has passed since last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        #checking if animation range has finished, if not it gives an error
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0



    def draw(self, surface):
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(flipped_image, self.rect)
        pygame.draw.rect(surface, (constants.RED), self.rect, 1)

