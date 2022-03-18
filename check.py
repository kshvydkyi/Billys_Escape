from pygame import *
from time import *
import pyganim
import os


MOB_WIDTH = 75
MOB_HEIGHT = 116
MOB_COLOR = "#FF6262"
ICON_DIR = os.path.dirname(__file__) #  Полный путь к каталогу с файлами

ANIMATION_MONSTERVRTICAL = [('%s/sprites/walk0.png' % ICON_DIR), ('%s/sprites/walk1.png' % ICON_DIR),('%s/sprites/walk2.png' % ICON_DIR),('%s/sprites/walk3.png' % ICON_DIR),('%s/sprites/walk4.png' % ICON_DIR),]
class Mob(sprite.Sprite):
     def __init__(self, x, y, left, up, maxLengthLeft,maxLengthUp):
            sprite.Sprite.__init__(self)
            self.image = Surface((MOB_WIDTH, MOB_HEIGHT))
            self.image.fill(Color(MOB_COLOR))
            self.rect = Rect(x, y, MOB_WIDTH, MOB_HEIGHT)
            self.image.set_colorkey(Color(MOB_COLOR))
            self.startX = x # начальные координаты
            self.startY = y
            self.maxLengthLeft = maxLengthLeft # максимальное расстояние, которое может пройти в одну сторону
            self.maxLengthUp= maxLengthUp # максимальное расстояние, которое может пройти в одну сторону, вертикаль
            self.xvel = left # cкорость передвижения по горизонтали, 0 - стоит на месте
            self.yvel = up # скорость движения по вертикали, 0 - не двигается
            boltAnim = []
            for anim in ANIMATION_MONSTERVRTICAL:
                boltAnim.append((anim, 0.1))
            self.boltAnim = pyganim.PygAnimation(boltAnim)
            self.boltAnim.play()
     def update(self, platforms): # по принципу героя
                    
        self.image.fill(Color(MOB_COLOR))
        self.boltAnim.blit(self.image, (0, 0))
       
        self.rect.y += self.yvel
        self.rect.x += self.xvel
 
        self.collide(platforms)
        
        if (abs(self.startX - self.rect.x) > self.maxLengthLeft):
            self.xvel =-self.xvel  # если прошли максимальное растояние, то идеи в обратную сторону
        if (abs(self.startY - self.rect.y) > self.maxLengthUp):
            self.yvel = -self.yvel # если прошли максимальное растояние, то идеи в обратную сторону, вертикаль

     def collide(self, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p) and self != p: # если с чем-то или кем-то столкнулись
               self.xvel = - self.xvel # то поворачиваем в обратную сторону
               self.yvel = - self.yvel

        




C_WIDTH = 70
C_HEIGHT = 70
C_COLOR = "#FF4312"
 
class Coin(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((C_WIDTH, C_HEIGHT))
        self.image.fill(Color(C_COLOR))
        self.image = image.load("%s/sprites/300$1.png" % ICON_DIR)
        self.image = transform.scale(self.image, (70, 40))
        self.rect = Rect(x, y, C_WIDTH, C_HEIGHT)
        self.startX = x
        self.startY = y
    def update(self, hero):
        if sprite.collide_rect(self, hero):
            self.rect.x = 999999
            self.rect.y = 999999
            
        

Q_WIDTH = 188
Q_HEIGHT = 311
Q_COLOR = "#aa4312"

 
class Quit(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((Q_WIDTH, Q_HEIGHT))
        self.image.fill(Color(Q_COLOR))
        self.rect = Rect(x, y, Q_WIDTH, Q_HEIGHT)
        self.image = image.load("%s/sprites/dver1 open.png" % ICON_DIR)
        self.image = transform.scale(self.image, (188, 311))





