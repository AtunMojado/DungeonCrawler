import pygame.sprite
import pygame


class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type, animation_list, dummy_coin = False):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type #0 is coin, 1 is health potion
        self.animation_list = animation_list
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.dummy_coin = dummy_coin

    def update(self, screen_scroll, player):
        #doesnt apply to the dummy coin that is always displayed on top of the screen
        if not self.dummy_coin:
            #reposition based on screen scroll
            self.rect.x += screen_scroll[0]
            self.rect.y += screen_scroll[1]
        #check to see if item has been collected by the player
        if self.rect.colliderect(player.rect):
            #coin collected
            if self.item_type == 0:#coin
                player.score += 1
            elif self.item_type == 1:#potion
                player.health += 10
                if player.health > 100:
                    player.health = 100
            self.kill()




        #handle animation
        animation_cooldown = 100
        #update image
        self.image = self.animation_list[self.frame_index]
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        #check if the animation has finished
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0
    def draw(self, surface):
        surface.blit(self.image, self.rect)