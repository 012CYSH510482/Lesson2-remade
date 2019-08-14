import pygame
from os import path
from Env import *

ani_list = []

class Explosion(pygame.sprite.Sprite):
    
    for i in range(1,9):
        ani_list.append(pygame.image.load(path.join(img_dir,"explosion/regularExplosion0{0}.png".format(i))))
    
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = ani_list[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
        self.last_ani = pygame.time.get_ticks()
        self.ani_delay = 100
        self.ani_ind = 0
    
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_ani > self.ani_delay:
            self.ani_ind += 1
            self.image = ani_list[self.ani_ind]
        if self.ani_ind >= 7:
            self.kill()
    
    def play(self):
        pass