# імпортуємо бібліотеки
from pygame import *
from random import randint
import time as t
init()

W = 500
H = 700

# створюємот вікно
window = display.set_mode((W, H))
# даємо назву
display.set_caption("Shooter")
# задаємо картинку
display.set_icon(image.load("rocket.png"))

back = transform.scale(image.load('galaxy.jpg'), (W, H))
clock = time.Clock()
# змінні для підрахування життів, пропущених ворогів, вбитих
lost = 0
killed = 0
life = 5
# """ЗВУКИ"""
# mixer.init()
# mixer.music.load("space.ogg")
# mixer.music.set_volume(0.3)
# fire = mixer.Sound('fire.ogg')
# mixer.music.play()
# створюємо шрифти
"""ШРИФТ"""
font.init()
font1 = font.SysFont("Arial", 30, bold=True)


"""КЛАСИ"""
class GameSprite(sprite.Sprite):
    # конструктор класу
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # викликаємо конструктор класу (Sprite):
        super().__init__()
        # кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

# кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    # метод, що малює героя у вікні
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] or keys_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_d] or keys_pressed[K_RIGHT] and self.rect.x < W - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 25 )
        bullets.add(bullet)

# функції для оновлення спрайтів
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > H:
            self.rect.y = 0
            self.rect.x = randint(0, W - 80)
            lost += 1

class Asteroid(Enemy):
     def update(self):
        self.rect.y += self.speed
        if self.rect.y > H:
            self.rect.y = 0
            self.rect.x = randint(0, W - 80)




class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

    
# створюємо гравців
player = Player("rocket.png", W/2, H-100, 80, 100, 15)
monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()
# створюємо цикл для того щоб було багато ворогів
for i in range(5):
    monster = Enemy("ufo.png", randint(0, W-80), randint(-50, 0), 80, 50, randint(3, 4))
    monsters.add(monster)

for i in range(3):
    asteroid = Asteroid("asteroid.png", randint(0, W-80), randint(-50, 0), 80, 50, randint(3, 4))
    asteroids.add(asteroid)
finish = False
# ігровий цикл
game = True
num_fire = 0
rel_time = False
color_life = (0, 255, 0)
while game:
    time.delay(10)
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire <= 10 and rel_time is False:
                    num_fire += 1
                    player.fire()     
                    # fire.play()
                if num_fire > 10 and rel_time is False:
                    rel_time = True
                    last_time = t.time()
                    
    if not finish:
        window.blit(back, (0, 0)) # малювання фону
        player.reset() # малюємо гравця
        player.update() # метод для руху вліво вправо
        
        monsters.draw(window)
        monsters.update()
        
        asteroids.draw(window)
        asteroids.update()

        bullets.draw(window)
        bullets.update() 
# перезарядка
        if rel_time:
            new_time = t.time()
            if new_time - last_time < 2:
                reload_txt = font1.render('Перезарядка...', True, (255, 0, 0))
                window.blit(reload_txt, (W/2-100, H/2))
            else:
                rel_time = False
                num_fire = 0 

# текст пропущено
        lost_txt = font1.render("Пропущено: " + str(lost), 1, (255, 255, 255)) 
        window.blit(lost_txt, (10, 10))
        # текст вбито
        killed_txt = font1.render("Вбито: " + str(killed), 1, (255, 255, 255))
        window.blit(killed_txt, (10, 40))
        life_txt = font1.render(" " + str(life), 1, color_life)
        window.blit(life_txt, (450, 5))
         # відображення тексту
# перевірка життів, зміна кольору
        if life == 2:
            color_life = (212, 174, 38)
        
        if life == 1:
            color_life = (255, 0, 0)

        if sprite.spritecollide(player, monsters, True):
            life -= 1
            monster = Enemy("ufo.png", randint(0, W-80), -50, 80, 50, randint(3, 4))
            monsters.add(monster)
       
        collides = sprite.groupcollide(monsters, bullets, True, True)
# перевірка вбивтсв
        for col in collides:
            monster = Enemy("ufo.png", randint(0, W-80), -50, 80, 50, randint(3, 4))
            monsters.add(monster)
            killed += 1
# перевірка виграшу
        if killed > 50:
            win = font1.render("Ти виграв!", True, (0, 255, 0))
            window.blit(win, (W/2-100, H/2))
            finish = True
# перевірка програшу
        if life <= 0 or lost >= 5:
            lose = font1.render("Ти програв!", True, (255, 0, 0))
            window.blit(lose, (W/2-100, H/2))
            finish = True
    
        if sprite.spritecollide(player, asteroids, True):
            life -= 1
            asteroid = Asteroid("asteroid.png", randint(0, W-80), randint(-50, 0), 80, 50, randint(3, 4))
            asteroids.add(asteroid)
    
    # перезагрузка
    else:
        keys_pressed = key.get_pressed()
        if keys_pressed[K_r]:
            life = 5
            killed = 0
            lost = 0
            for m in monsters:
                m.kill()
            for b in bullets:
                b.kill()
            for i in range(5):
                monster = Enemy("ufo.png", randint(0, W-80), randint(-50, 0), 80, 50, randint(3, 4))
                monsters.add(monster)
            finish = False





    display.update()

    