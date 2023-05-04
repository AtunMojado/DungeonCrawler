import random
import pygame
import math
import constants


class Weapon():
    def __init__(self, image, arrow_image):
        self.original_image = image
        self.angle = 0
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.arrow_image = arrow_image
        self.rect = self.image.get_rect()
        self.fired = False
        self.last_shot = pygame.time.get_ticks()
        #time between arrow shots the player is able to do
    def update(self, player):
        shot_cooldown = 300 #time between an arrow is shot
        arrow = None #if nothings clicked, we return nothing

        self.rect.center = player.rect.center

        pos = pygame.mouse.get_pos()#gives an X and Y coord on screen for where mouse is sitting
        x_dist = pos[0] - self.rect.centerx
        y_dist = -(pos[1] - self.rect.centery)#bcs pygame Y coords increase the way down the screen
        self.angle = math.degrees(math.atan2(y_dist, x_dist))

        #get mouse clicks
        if pygame.mouse.get_pressed()[0] and self.fired == False and (pygame.time.get_ticks()- self.last_shot >= shot_cooldown):
            #index 0 to indicate the mouse left button
            arrow = Arrow(self.arrow_image, self.rect.centerx, self.rect.centery, self.angle)
            self.fired = True #just to leave one arrow
            self.last_shot = pygame.time.get_ticks()#resets timer to 0
        #reset mouse click
        if pygame.mouse.get_pressed()[0] == False: #while mouse is not clicked
            self.fired = False
        return arrow #if somethings clicked, we return one arrow


    def draw(self, surface):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/2)), self.rect.centery - int(self.image.get_height()/2)))

class Arrow(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = image
        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image, self.angle - 90)#-90 degrees because of the Sprite rotation of the arrow
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        #calculate the horizontal and vertical speeds based on angle
        self.dx = math.cos(math.radians(self.angle)) * constants.ARROW_SPEED
        self.dy = -(math.sin(math.radians(self.angle)) * constants.ARROW_SPEED)#negative because Ycoord increases down screen

    def update(self, screen_scroll, obstacle_tiles, enemy_list):
        #reset variables
        damage = 0
        damage_pos = None
        #reposition based on speed
        self.rect.x += screen_scroll[0] + self.dx
        self.rect.y += screen_scroll[1] + self.dy

        #check for collision arrow/tile wall
        for obstacle in obstacle_tiles:
            if obstacle[1].colliderect(self.rect):
                self.kill()


        #check if arrow has gone off screen
        if self.rect.right < 0 or self.rect.left > constants.SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > constants.SCREEN_HEIGHT:
            self.kill()

        #check collision between arrow and enemies
        for enemy in enemy_list:
            if enemy.rect.colliderect(self.rect) and enemy.alive:
                damage = 10 + random.randint(-5, 5)#cause damage between 5 and 15
                damage_pos = enemy.rect
                enemy.health -= damage
                enemy.hit = True
                self.kill()#makes the arrow stop
                break

        return damage, damage_pos

    def draw(self, surface):
        surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width() / 2)), self.rect.centery - int(self.image.get_height() / 2)))


