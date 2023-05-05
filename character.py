import math

import pygame
import constants
import weapon


class Character():
    def __init__(self, x, y, health, mob_animations, char_type, boss, size):
        self.char_type = char_type
        self.boss = boss
        self.score = 0
        self.flip = False
        self.animation_list = mob_animations[char_type]
        self.frame_index = 0
        self.action = 0 # 0 is IDLE, 1 is RUNNING
        self.update_time = pygame.time.get_ticks()
        self.running = True
        self.health = health
        self.alive = True
        self.hit = False
        self.last_hit = pygame.time.get_ticks()
        self.last_attack = pygame.time.get_ticks()
        self.stunned = False  # when an arrow hits the enemy, make him a little stop

        self.image = self.animation_list[self.action][self.frame_index]
        # a bit of difference in the rect to let the characters pass betwen tiles
        self.rect = pygame.Rect(0, 0, constants.TILE_SIZE*size -3, constants.TILE_SIZE*size -3)
        self.rect.center = (x, y)


    def move(self, dx, dy, obstacle_tiles, exit_tile):
        screen_scroll = [0, 0]
        level_complete = False
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

        #check for collision with map in X direction
        self.rect.x += dx
        for obstacle in obstacle_tiles:
            #check for collision
            if obstacle[1].colliderect(self.rect):
                #check which side the collision is from
                if dx > 0:#moving to the right
                    self.rect.right = obstacle[1].left
                if dx < 0:#moving to the left
                    self.rect.left = obstacle[1].right

        #check for collision with map in Y direction
        self.rect.y += dy
        for obstacle in obstacle_tiles:
            #check for collision
            if obstacle[1].colliderect(self.rect):
                #check which side the collision is from
                if dy > 0:#moving down
                    self.rect.bottom = obstacle[1].top
                if dy < 0:#moving up
                    self.rect.top = obstacle[1].bottom

        #logic only applicable to player, not the enemies
        if self.char_type == 0:
            #check collision with exit ladder but not just collision, player needs to be upon the ladder
            if exit_tile[1].colliderect(self.rect):
                #ensure player is close to the center of the exit ladder
                exit_dist = math.sqrt(((self.rect.centerx - exit_tile[1].centerx) ** 2) + ((self.rect.centery - exit_tile[1].centery) ** 2))
                if exit_dist < 20:
                    level_complete = True

            #update scroll based on player position
            #move camera left and right
            if self.rect.right > (constants.SCREEN_WIDTH - constants.SCROLL_THRESHOLD):
                screen_scroll[0] = (constants.SCREEN_WIDTH - constants.SCROLL_THRESHOLD) - self.rect.right
                self.rect.right = constants.SCREEN_WIDTH - constants.SCROLL_THRESHOLD
            if self.rect.left < constants.SCROLL_THRESHOLD:
                screen_scroll[0] = constants.SCROLL_THRESHOLD - self.rect.left
                self.rect.left = constants.SCROLL_THRESHOLD

            #move camera up and down
            if self.rect.bottom > (constants.SCREEN_HEIGHT - constants.SCROLL_THRESHOLD):
                screen_scroll[1] = (constants.SCREEN_HEIGHT - constants.SCROLL_THRESHOLD) - self.rect.bottom
                self.rect.bottom = constants.SCREEN_HEIGHT - constants.SCROLL_THRESHOLD
            if self.rect.top < constants.SCROLL_THRESHOLD:
                screen_scroll[1] = constants.SCROLL_THRESHOLD - self.rect.top
                self.rect.top = constants.SCROLL_THRESHOLD
        return screen_scroll, level_complete

    def ai(self, player, obstacle_tiles, screen_scroll, fireball_image): #enemies movement
        clipped_line = ()
        stun_cooldown = 200
        ai_dx = 0
        ai_dy = 0
        fireball = None
        #reposition the mobs based on screen scroll
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        #create a line of sight from the enemy to the player
        line_of_sight = ((self.rect.centerx, self.rect.centery), (player.rect.centerx, player.rect.centery))
        #check if line of sight passes through an obstacle tile
        for obstacle in obstacle_tiles:
            if obstacle[1].clipline(line_of_sight):#clipline, collision with a line, not a rect
                clipped_line = obstacle[1].clipline(line_of_sight)


        #check distance to player
        dist = math.sqrt(((self.rect.centerx - player.rect.centerx)**2) + ((self.rect.centerx - player.rect.centerx)**2))
        if not clipped_line and dist > constants.RANGE:
            if self.rect.centerx > player.rect.centerx:
                ai_dx = -constants.ENEMY_SPEED
            if self.rect.centerx < player.rect.centerx:
                ai_dx = constants.ENEMY_SPEED
            if self.rect.centery > player.rect.centery:
                ai_dy = -constants.ENEMY_SPEED
            if self.rect.centery < player.rect.centery:
                ai_dy = constants.ENEMY_SPEED

        if self.alive:
            if not self.stunned:
                #move towards player
                self.move(ai_dx, ai_dy, obstacle_tiles, exit_tile=None)
                #attack player
                if dist < constants.ATTACK_RANGE and player.hit == False:
                    player.health -= 10
                    player.hit = True
                    player.last_hit = pygame.time.get_ticks()
                #boss enemies shoot fireballs
                fireball_cooldown = 800
                if self.boss:
                    if dist < 500:
                        if pygame.time.get_ticks() - self.last_attack >= fireball_cooldown:
                            fireball = weapon.Fireball(fireball_image, self.rect.centerx, self.rect.centery, player.rect.centerx, player.rect.centery)
                            self.last_attack = pygame.time.get_ticks()



            #check if hit
            if self.hit == True:
                self.hit = False
                self.last_hit = pygame.time.get_ticks()
                self.stunned = True
                self.running = False
                self.update_action(0)
            if (pygame.time.get_ticks() - self.last_hit > stun_cooldown):
                self.stunned = False

        return fireball
    # updating the state of the moving and flipped image
    def update(self):
        #check if character has died
        if self.health <= 0:
            self.health = 0
            self.alive = False
        #timer to reset player taking a hit
        hit_cooldown = 1600
        if self.char_type == 0:
            if self.hit == True and (pygame.time.get_ticks() - self.last_hit) > hit_cooldown:
                self.hit = False
        #check what action the player is performing
        if self.running == True:
            self.update_action(1)# 1 = RUN
        else:
            self.update_action(0)# 0 = IDLE


        #handle animation and update image
        animation_cooldown = 80
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
        if self.char_type == 0:
            surface.blit(flipped_image, (self.rect.x, self.rect.y - constants.SCALE*constants.OFFSET))
        else:
            surface.blit(flipped_image, self.rect)
        #show a rect object over the character to visualize collisions etc...
        #pygame.draw.rect(surface, (constants.RED), self.rect, 1)


