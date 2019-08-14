import pygame
from Env import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load(path.join(img_dir, "ship.png"))
        self.image = pygame.transform.scale(image, (50,30))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedx = 0
        self.speedy = 0
        self.shield = 100
        self.lifes = 2
        self.ax = 0
        self.ay = 0

    def update(self):
        self.keyEventHandling()

    def keyEventHandling(self):
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.ax = -0.5
            # self.move(-self.speedx, 0)
        if keystate[pygame.K_RIGHT]:
            self.ax = 0.5
            # self.move(self.speedx, 0)
        if keystate[pygame.K_UP]:
            self.ay = -0.5
            # self.move(0, -self.speedy)
        if keystate[pygame.K_DOWN]:
            self.ay = 0.5
            # self.move(0, self.speedy)
        # vt = v0 + at
        self.speedx += self.ax
        if self.speedx > 10:
            self.speedx = 10
        elif self.speedx < -10:
            self.speedx = -10
        self.speedy += self.ay
        if self.speedy > 8:
            self.speedy = 8
        elif self.speedy < -8:
            self.speedy = -8
        self.ax = 0
        self.ay = 0
        self.move(self.speedx,self.speedy)
        
    def move(self, dx, dy):
        self.rect.x += dx
        if self.rect.x >= WIDTH - 50:
            self.rect.x = WIDTH - 50
            self.speedx = -2
        elif self.rect.x < 0:
            self.rect.x = 0
            self.speedx = 2
        self.rect.y += dy
        if self.rect.y >= HEIGHT - 30:
            self.rect.y = HEIGHT - 30
            self.speedy = -2
        elif self.rect.y <= 0:
            self.rect.y = 0
            self.speedy = 2
    
    def reset(self):
        self.shield = 100
        self.lifes = 2
