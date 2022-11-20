from pygame import *
from random import randint
from time import time as timer


win_width = 700
win_height = 500

#фоновая музыка
# mixer.init()
# mixer.music.load('undertale_036. Dummy!.mp3')
# mixer.music.play()
# fire_sound = mixer.Sound('snd_hurt1.wav')

font.init()
font2 = font.Font(None,36)

font1= font.Font(None,36)
win = font1.render('Ты ПОБЕДУН',True,(255,255,255))
lose = font1.render('Ты ПРОМГРАЛ',True,(180, 0, 0))


score = 0
lost = 0
goal = 10
max_lost = 3
life = 3

class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_height - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y < 0:
            self.kill()
            

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 615:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < 375:
            self.rect.y += self.speed
    def fire(self):
        bullet = Bullet("./uno.jpg",self.rect.centerx, self.rect.top, 10, 20, -15)
        bullets.add(bullet)

display.set_caption("Шутер 3")
window = display.set_mode((win_width,win_height))
background = transform.scale(image.load("./galaxy.jpg"),(win_width,win_height))

monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy("./ufo.png", randint(80, win_height - 80), -40, 80, 50, randint(1,5))
    monsters.add(monster)
bullets = sprite.Group()
asteroids = sprite.Group()
for i in range(1,3):
    asteroid = Enemy("./asteroid.png", randint(30, win_height - 30), -40, 80, 50, randint(1,7))
    asteroids.add(asteroid)




ship = Player("./rocket.png",5,400,80,100,30)

run = True

finish = False

num_fire = 0

rel_time = False


while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                # fire_sound.play()
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    ship.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
                
    
    if not finish:
        window.blit(background,(0,0))
        text = font2.render('Счёт'+str(score),1,(225,225,225))
        window.blit(text,(10,20))
        text_lose = font2.render('Пропущено'+str(lost),1,(225,225,225))
        window.blit(text_lose,(10,50))


        bullets.update()

        asteroid.update()

        ship.update()

        monsters.update()

        ship.reset()

        bullets.draw(window)
        monsters.draw(window)
        asteroids.draw(window)

        if rel_time == True:
            now_time = timer()
            if now_time - rel_time < 3:
                reload = font2.render('ПЕРЕЗАРЯДКА', 1 ,(150,0,0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time= False    
            

        collides = sprite.groupcollide(monsters,bullets,True,True)
        for c in collides:
            score += 1
            monster = Enemy("./ufo.png", randint(80, win_height - 80), -40, 80, 50, randint(1,5))
            monsters.add(monster)
        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)  
            life -= 1
        if life == 0 and lost>=max_lost:
            finish = True
            window.blit(win, (200,200)) 
        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose,(200,200))
        if score >= goal:
            finish = True
            window.blit(win,(200,200))

        text_life = font1.render(str(life),1,(255,0,0))
        window.blit(text_life,(650,10))

        monsters.draw(window)
        display.update()

    else:
        finish = False
        score = 0
        lost = 0
        num_fire = 0
        life = 3
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill() 
        for a in asteroids:
            a.kill()   
        time.delay(3000)
        for i in range(1,6):
            monster = Enemy("./ufo.png", randint(80, win_height - 80), -40, 80, 50, randint(1,5))
            monsters.add(monster)
        for i in range(1,3):
            asteroid = Enemy("./asteroid.png", randint(30, win_height - 30), -40, 80, 50, randint(1,7))
            asteroids.add(asteroid)    


    time.delay(60)