import pygame
from pygame import *
from player import *
from blocks import *
from check import *
import sys



#Объявляем переменные
WIN_WIDTH = 1280 
WIN_HEIGHT = 720 
DISPLAY = (WIN_WIDTH, WIN_HEIGHT) 
BACKGROUND_COLOR = "#696969"

#Global
pygame.init()
pygame.mixer.init()
pygame.font.init()
screen = pygame.display.set_mode(DISPLAY) 
pygame.display.set_caption("Billy's escape")
timer = pygame.time.Clock()
coins = 0
lives = 1
#files
dir = os.path.dirname(__file__)
mixer.music.load('%s/music/theme.wav' % dir)
mixer.music.play(-1)
mixer.music.set_volume(0.3)
startbutton_sound = mixer.Sound("%s/sounds/1.wav" % dir)
quitbutton_sound = mixer.Sound("%s/sounds/woo.mp3" % dir)
bucks_sound = mixer.Sound("%s/sounds/300$.wav" % dir)
dead_sound = mixer.Sound("%s/sounds/deadsound1.wav" % dir)
game_background = image.load("%s/sprites/game_back.png" % dir)
game_background = transform.scale(game_background, (1280, 720))
gameIcon = pygame.image.load("%s/sprites/icon.png" % dir)
pygame.display.set_icon(gameIcon)
class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_clr = "#5519E0"
        self.active_clr = "#6F01F5"
    def draw(self, x, y, message, button_sound, action = None, font_size = 30):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(screen, self.active_clr, (x, y, self.width, self.height))
            if click[0] == 1:
                mixer.Sound.play(button_sound)
                pygame.time.delay(300)
                if action is not None:
                    if action == quit:
                        pygame.quit()
                        quit()
                    else:
                        action()

        else:
            pygame.draw.rect(screen, self.inactive_clr, (x, y, self.width, self.height))
        print_text(message = message, x = x + 10, y = y + 10, font_size=font_size)

def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l+WIN_WIDTH / 2, -t+WIN_HEIGHT / 2

    l = min(0, l)                           # Не движемся дальше левой правой нижней верхней границы
    l = max(-(camera.width-WIN_WIDTH), l)   
    t = max(-(camera.height-WIN_HEIGHT), t) 
    t = min(0, t)                           
    return Rect(l, t, w, h)        

def game():
    global coins, lives
    coins = 0
    lives = 1
    bg = Surface((WIN_WIDTH,WIN_HEIGHT)) 
    bg.fill(Color(BACKGROUND_COLOR))     
   
    
    entities = pygame.sprite.Group() # Все объекты
    platforms = []
    coins_array = []
    wrong_blocks = []
    lava_a = []
    enemies = []
    level = [
             "B                                                                                                            ",
             "B                                                                                                            ",
             "B                                                                                                            ",
             "B                                                                                                            ",
             "B                                                                                                            ",
             "B---r C                                                                                                      ",
             "BBBBB---r                                                                                                    ",
             "BBBBBBBBB       M                                                                                            ",
             "B                                                                                                            ",
             "B              l--r                M                                                                         ",
             "B              BBBB                  C                                                                       ",
             "B                                l----r                                                                      ",
             "B                          C     BBBBBB                                                                      ",
             "B                   l------r                                                                      Q           ",
             "B                   BBBBBBBB                                                                                 ",
             "B                                                                                                            ",
             "B               r                                                                          C                 ",
             "B               B                            l  r                          M            l-----------r        ",
             "B               B     C                     lB  Br                           C          BBBBBBBBBBBBB        ",
             "B               B-------r                  lBBCCBBr        M            l--------r      BBBBBBBBBBBBB        ",
             "B                                         lBBB  BBBr                    BBBBBBBBBB                           ",
             "B                             l-----------BBBBWWBBBB-------------r      BBBBBBBBBB                           ",
             "B                             BBBBBBBBBBBBBBBB  BBBBBBBBBBBBBBBBBB                                           ",
             "B                                                                                                            ",
             "B                                                                                                            ",
             "B                                                                                                            ",
             "B                                                                                                            ",
             "B                                                                                                            ",
             "B                                                                                                            ",
             "B                                                                                                            ",
             "B                                                                                                            ",
             "BLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL",
             "BLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL",
             "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
             "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
             "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"]
       
    x=y=0 # координаты
    for row in level: # вся строка
        for col in row: # каждый символ
            if col == "-":
                pf = Platform(x,y, "%s/sprites/castleMid1.png" % dir)
                entities.add(pf)
                platforms.append(pf)
            if col == "r":
                pf = Platform(x,y, "%s/sprites/castleRight.png" % dir)
                entities.add(pf)
                platforms.append(pf)
            if col == "l":
                pf = Platform(x,y, "%s/sprites/castleLeft.png" % dir)
                entities.add(pf)
                platforms.append(pf)
            if col == "L":
                lava = Platform(x,y, "%s/sprites/Lava.png" % dir)
                entities.add(lava)
                lava_a.append(lava)
            if col == "B":
                pf = Platform(x,y, "%s/sprites/castleCenter1.png" % dir)
                entities.add(pf)
                platforms.append(pf)
            if col == "W":
                wrong_ex = Wrong(x,y, "%s/sprites/WrongExit.png" % dir)
                entities.add(wrong_ex)
                wrong_blocks.append(wrong_ex)
            if col == "M":
                co = Mob(x, y, 2, 0, 110, 0)
                entities.add(co)
                enemies.append(co)
            if col == "Q":
                enter = Quit(x, y)
                entities.add(enter)
            if col == "C":
                coinn = Coin(x, y)
                entities.add(coinn)
                coins_array.append(coinn)

            x += PLATFORM_WIDTH #блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT    
        x = 0                   
    
    hero = Player(100,100)
    left = right = False # по умолчанию - стоим
    up = False
    
    entities.add(hero)
    total_level_width  = len(level[0])*PLATFORM_WIDTH # Высчитываем фактическую  и высоту ширину уровня
    total_level_height = len(level)*PLATFORM_HEIGHT  
    
    camera = Camera(camera_configure, total_level_width, total_level_height) 
    running = True
    while running: 
        timer.tick(60)
        keys = key.get_pressed()
        for e in pygame.event.get(): 
            if e.type == QUIT:
                running = False
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True


            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
        if keys[K_ESCAPE]:
                pause()
        
        screen.blit(game_background, (0,0))      
        

        camera.update(hero) # центризируем камеру относительно персонажа
        hero.update(left, right, up,platforms)
        for e in enemies:
            e.update(platforms)
            
        for c in coins_array:
            count_coins(c, hero)
            c.update(hero)
        # отображение
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        for l in  lava_a:
            if check_collision(hero, l):
                if HIT(hero, l) < 1:
                    mixer.Sound.play(dead_sound)
                    print_text("ЧЕЛ ТЫ....", 600, 200)
                    running = False
        for dead in enemies:
            if check_collision(hero, dead):
                if HIT(hero, dead) < 1:
                    mixer.Sound.play(dead_sound)
                    print_text("ПОМЯНЕМ", 600, 200)
                    running = False
        if check_collision(hero, enter):
            print_text("Вы нашли выход из этого Dungeon и Billy теперь может вернутся в gym.", 150, 180)
            print_text("Сделано на коленке Studios благодарит вас за прохождение.", 230, 130)
            running = False
        print_text("Lives: " + str(lives), 700, 10)
        print_text("Bucks: " + str(coins), 500, 10)
        pygame.display.update()
    return game_over()
        
def print_text(message, x, y, font_color = (255, 255, 255), font_type = "gogoia2.ttf", font_size = 40):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))

def pause():
    paused = True
    mixer.music.pause()
    while paused:
        for e in pygame.event.get(): 
            if e.type == QUIT:
                quit()
                
        
        print_text("Paused. Press enter to countinue", WIN_WIDTH / 2 - 150, WIN_HEIGHT / 2)
        keys = key.get_pressed()
        if keys[K_RETURN]:
            paused = False
        display.update()
        timer.tick(15)
    mixer.music.unpause()

def check_collision(sprite1, sprite2):
    col = sprite.collide_rect(sprite1, sprite2)
    if col == True:
        return True
    else:
        return False

def game_over():
    stopped = True
    while stopped:
        for e in pygame.event.get(): 
            if e.type == QUIT:
                pygame.quit()
                quit()
        print_text("Game over. Press enter to play again or esc to quit", 350, 50)
        keys = key.get_pressed()
        if keys[K_RETURN]:
            return True
        if keys[K_ESCAPE]:
            return False

        display.update()
        timer.tick(15)

def count_coins(coin, hero):
    global coins
    if check_collision(hero, coin) == True:
        coins += 300
        mixer.Sound.play(bucks_sound)

def HIT(hero, enemy):
    global lives
    if check_collision(hero, enemy) == True:
        lives = 0
    return lives

def start_game():
    global coins, lives
    while game():
        pass

def show_menu():
    menu_background = image.load("%s/sprites/fon.png" % dir)
    menu_background = transform.scale(menu_background, (1280, 720))
    startbutton = Button(185, 70)
    quitbutton = Button(80, 70)
    show = True
    while show: 
        for e in pygame.event.get(): 
            if e.type == QUIT:
                pygame.quit()
                quit()
        screen.blit(menu_background, (0, 0))
        startbutton.draw(540, 300, "Start game", startbutton_sound, start_game, 50)
        quitbutton.draw(590, 400, "Quit", quitbutton_sound, quit, 50)
        pygame.display.update()
        timer.tick(60)

show_menu()

pygame.quit()
quit()
