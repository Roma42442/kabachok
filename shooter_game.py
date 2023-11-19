from pygame import *
from random import randint
'''Необходимые классы'''

#класс-родитель для спрайтов 
class GameSprite(sprite.Sprite):
    #конструктор класса
    def __init__(self, player_image, player_x, player_y, player_speed, w, h):
        super().__init__()
 
        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (w, h))
        self.speed = player_speed
 
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#класс-наследник для спрайта-игрока (управляется стрелками)
class Player(GameSprite):
    reload = 0
    def update(self):
        self.reload += 1
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
        if keys[K_SPACE]:
            self.fire()

    def fire(self):
        if self.reload >= 30:
            shot = Shot('bullet.png', self.rect.x+40-15, self.rect.y, 4, 30,30)
            shots.add(shot)
            self.reload = 0




class Shot(GameSprite):
    
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < -60:
            self.kill()


class Star(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            stars.remove(self)

class Ufo(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            ufos.remove(self)
            global ufo_miss
            ufo_miss += 1



def creat_star():
    star = Star('asteroid.png', randint(0, win_width), -30, randint(3,15), 30, 30)
    stars.add(star)
    
def creat_ufo():
    ufo = Ufo('ufo.png', randint(0, win_width-60), -100, 2, 90, 70)
    ufos.add(ufo)
    



font.init()
font1 = font.Font(None, 36)


#Игровая сцена:
win_width = 1000
win_height = 600
window = display.set_mode((win_width, win_height))
display.set_caption("GALAXY")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

#Персонажи игры:

ship = Player('rocket.png', win_width/2 - 40, win_height - 80, 5, 80,80)

stars = sprite.Group()
ufos = sprite.Group()
shots = sprite.Group()
booms = sprite.Group()


game = True
finish = False
win = False
ticks = 0
ufo_miss = 0


clock = time.Clock()
FPS = 60

#музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.set_volume(0.3)
mixer.music.play(-1)
fire = mixer.Sound('fire.ogg  ')




while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                game = quit()
    
    if finish != True:

        if ticks % 10 == 0:
            creat_star() 

        if ticks % 120 == 0:
            creat_ufo() 

        window.blit(background,(0, 0))

        window.blit(
            font1.render("Пропущено: " + str(ufo_miss), 1, 
            (255, 255, 255)), (10,10)
        )
     


        stars.update()
        ufos.update()
        ship.update()
        shots.update()
        
        collisions = sprite.groupcollide(shots,ufos, True,True)

        stars.draw(window)
        ufos.draw(window)   
        ship.reset()
        shots.draw(window)

        if ufo_miss >= 3:
            finish = True

        
            
    
    else:
        if win:
            go = GameSprite('win.jpg', 0,0, 0, 700, 500)
            go.reset()
        else:
            # если конец игры
            go = GameSprite('gameover.jpg', 0,0, 0, 700, 500)
            go.reset()


    ticks += 1
    display.update()
    clock.tick(FPS)