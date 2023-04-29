import math

import pygame
import constants

class Character():
    def __init__(self, x, y):
        self.rect = pygame.Rect(0, 0, 40, 40)
        self.rect.center = (x, y)

    def move(self, dx, dy):

        #control diagonal speed
        if dx != 0 and dy != 0: #if one coord is 0, movement is horizontal or vertical
            dx = dx * (math.sqrt(2)/2)
            dy = dy * (math.sqrt(2)/2)

        self.rect.x += dx
        self.rect.y += dy


    def draw(self, surface):
        pygame.draw.rect(surface, (constants.RED), self.rect)

