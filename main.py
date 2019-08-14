import random
from os import path
import pygame

from Env import *
from explosion import *
from meteor import *
from player import *
from begin_state import *


font_name = pygame.font.match_font('arial')
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(path.join(sound_dir, "bgm.mp3"))
pygame.mixer.music.play(-1)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(path.join(img_dir, "laser_red.png"))
        self.rect = self.image.get_rect()
        self.rect.centerx = posx
        self.rect.centery = posy
        self.speedy = 30

    def update(self):
        self.rect.y -= self.speedy
        if self.rect.bottom < 0:
            self.kill()

def newMeteor():
    global all_sprites
    m = Meteor(meteors,all_sprites)
    meteors.add(m)
    all_sprites.add(m)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
bg = pygame.image.load(path.join(img_dir,'background.png'))
bg_rect = bg.get_rect()
clock = pygame.time.Clock()

meteors = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
supports = pygame.sprite.Group()

last_shot = pygame.time.get_ticks()
powertime = 0
now = 0
power = 1
score = 0
player = Player(WIDTH / 2, HEIGHT - 50)

for i in range(8):
    newMeteor()

all_sprites.add(bullets)
all_sprites.add(player)
all_sprites.add(meteors)

running = True
sound_pew = pygame.mixer.Sound(path.join(sound_dir, "pew.wav"))


def check_meteor_hit_player():
    global running, meteors, gamestate
    hits = pygame.sprite.spritecollide(player, meteors, False, pygame.sprite.collide_circle_ratio(0.7))
    if hits:
        for hit in hits:
            player.shield -= hit.speedy*3
            hit.kill()
            if player.shield <= 0:
                player.lifes -= 1
                if player.lifes < 0:
                    gamestate = 'begin'
                else:
                    player.shield = 100
                # print("check_meteor_hit_player")
            newMeteor()

def check_support_hit_player():
    global power
    hits = pygame.sprite.spritecollide(player, supports, True, pygame.sprite.collide_circle_ratio(0.7))
    if hits:
        for hit in hits:
            if hit.thing == 'bolt':
                power += 1
                powertime = pygame.time.get_ticks()
            elif hit.thing == 'pill':
                player.shield += 20
                if player.shield >=100:
                    player.shield = 100
            #elif hit.thing = 'shield':
                
            hit.kill()


class Support(pygame.sprite.Sprite):
    def __init__(self, x, y, speedy):
        pygame.sprite.Sprite.__init__(self)
        
        self.thing = random.choice(['bolt','pill','shield'])
        self.number = random.randint(1,3)
        
        self.image = pygame.image.load(path.join(img_dir,"powerUp/{0}_0{1}.png".format(self.thing, self.number)))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedy = speedy
    
    def update(self):
        self.rect.centery = self.rect.centery + self.speedy
        if self.rect.centery > HEIGHT:
            self.kill()


def check_bullets_hit_meteor():
    global  score
    hits = pygame.sprite.groupcollide(meteors, bullets, True, True, pygame.sprite.collide_circle_ratio(0.7))
    if hits:
        for hit in hits:
            score += (8 - hit.size)*hit.speedy/10
            hit.kill()
            # print("check_bullets_hit_meteor")
            newMeteor()
            explosion = Explosion(hit.rect.centerx,hit.rect.centery)
            all_sprites.add(explosion)
            if random.randint(0,1):
                support = Support(hit.rect.centerx, hit.rect.centerx, hit.speedy)
                supports.add(support)
                all_sprites.add(support)
            # TODO 06.擊破隕石會掉出武器或是能量包 武器可以改變攻擊模式 能量包可以回血

def draw_score():
    font = pygame.font.Font(font_name, 14)
    text_surface = font.render(str(score), True, YELLOW)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (WIDTH/2, 20)
    screen.blit(text_surface, text_rect)
    pass

def shoot():
    sound_pew.play()
    if power > 1:
        bullet1 = Bullet(player.rect.left, player.rect.centery)
        bullets.add(bullet1)
        all_sprites.add(bullet1)
        bullet2 = Bullet(player.rect.right, player.rect.centery)
        bullets.add(bullet2)
        all_sprites.add(bullet2)
    else:
        bullet = Bullet(player.rect.centerx, player.rect.centery)
        bullets.add(bullet)
        all_sprites.add(bullet)

def draw_shield():
    shield_bar = pygame.rect.Rect(10,10,player.shield,20)
    outline_rect = pygame.rect.Rect(10,10,100,20)
    pygame.draw.rect(screen,GREEN,shield_bar)
    pygame.draw.rect(screen,(255,255,255),outline_rect,2)

def draw_lifes(surf, x, y, player):
    img = pygame.transform.scale(player.image, (30,20))
    img_rect = img.get_rect()
    for i in range(player.lifes):
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img,img_rect)

begin_state = Begin_state(screen)
gamestate = 'begin'

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    if gamestate == 'begin':
        begin_state.keyhandle()
        begin_state.show()
        gamestate = begin_state.updateState()
        if gamestate == 'start':
            begin_state.reset()
            player.reset()
    
    elif gamestate == 'start':
        
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            if power >= 2 and (now - powertime >= 5000):
                power -= 1
                powertime = pygame.time.get_ticks()
            if now - last_shot > SHOT_DELAY:
                last_shot = now
                shoot()
        
        check_meteor_hit_player()
        check_support_hit_player()
        
        check_bullets_hit_meteor()

        all_sprites.update()
        
        screen.blit(bg,bg_rect)
        draw_shield()
        draw_lifes(screen, WIDTH - 100, 10, player)
        draw_score()
        all_sprites.draw(screen)
        # flip to display

    pygame.display.flip()

pygame.quit()