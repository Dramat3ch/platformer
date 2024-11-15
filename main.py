import pygame
from pygame.locals import *
import sys
import random # Добавляем библиотеку случайной генерации
import time

pygame.init() # Инициализируем модуль pygame
vec = pygame.math.Vector2  # 2 for two dimensional

HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 60

FramePerSec = pygame.time.Clock() # наш объект таймера

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT)) #Поле
pygame.display.set_caption("PLATFORMER") # Заголовок


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # self.image = pygame.image.load("character.png")
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((255, 255, 0))
        self.rect = self.surf.get_rect()

        self.pos = vec((10, 360))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.jumping = False
        self.score = 0

    def move(self):
        self.acc = vec(0, 0.5)

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos

    def jump(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -15

    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def update(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if self.vel.y > 0:
            if hits:
                if self.pos.y < hits[0].rect.bottom:
                    if hits[0].point == True:  ##
                        hits[0].point = False  ##
                        self.score += 1  ##
                    self.pos.y = hits[0].rect.top + 1
                    self.vel.y = 0
                    self.jumping = False


class Platform(pygame.sprite.Sprite): # определим класс, который описывает, что такое платформа (их будет много). pygame.sprite.Sprite это называется наследование. С его помощью, мы можем использовать готовые классы и дополнять их.
    def __init__(self): # Волшебный метод __init__, который говорит интерпретатору, как создать платформу. Метод супер - специальный метод, который берет все, что есть в наследуемом классе и сохраняет в нашем новом классе.
        super().__init__()

        self.surf = pygame.Surface((random.randint(50, 100), 12))
# Задаем форму и размер платформы
        self.surf.fill((0, 255, 0))
# Задаем цвет платформы
        self.rect = self.surf.get_rect(center=(random.randint(0, WIDTH - 10),
                                               random.randint(0, HEIGHT - 30)))
# Задаем местоположение платформы
        self.point = True

    def move(self):
        pass


def check(platform, groupies):
    if pygame.sprite.spritecollideany(platform, groupies):
        return True
    else:
        for entity in groupies:
            if entity == platform:
                continue
            if (abs(platform.rect.top - entity.rect.bottom) < 40) and (
                    abs(platform.rect.bottom - entity.rect.top) < 40):
                return True
        c = False


def plat_gen():
    while len(platforms) < 6:
        width = random.randrange(50, 100)
        p = Platform()
        c = True

        while c:
            p = Platform()
            p.rect.center = (random.randrange(0, WIDTH - width),
                             random.randrange(-50, 0))
            c = check(p, platforms)
        platforms.add(p)
        all_sprites.add(p)


PT1 = Platform() # Объявляем создание экземпляра класса
P1 = Player() # Объявляем создание экземпляра класса игрок

PT1.surf = pygame.Surface((WIDTH, 20)) # Задаем свойство размера
PT1.surf.fill((255, 0, 0)) # Задаем цвет
PT1.rect = PT1.surf.get_rect(center=(WIDTH / 2, HEIGHT - 10)) # Позиционируем наш пол

PT1.point = False # Это свойство потребуется при подсчете очков

all_sprites = pygame.sprite.Group()
all_sprites.add(PT1) # Добавляем наш спрайт-платформу в группу
all_sprites.add(P1) # Добавляем наш спрайт-игрока в группу

platforms = pygame.sprite.Group()
platforms.add(PT1) # Создаем группу, в которой будут только наши платформы

for x in range(random.randint(4, 5)):
    c = True
    pl = Platform()
    while c:
        pl = Platform()
        c = check(pl, platforms)
    platforms.add(pl)
    all_sprites.add(pl)
# Генерируем плафтормы при первом запуске, чтобы потом работал генератор

while True:
    P1.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                P1.jump()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                P1.cancel_jump()
    if P1.rect.top > HEIGHT:
        for entity in all_sprites:
            entity.kill()
            time.sleep(1)
            displaysurface.fill((255, 0, 0))
            pygame.display.update()
            time.sleep(1)
            pygame.quit()
            sys.exit() # Выход из игры

    if P1.rect.top <= HEIGHT / 3:
        P1.pos.y += abs(P1.vel.y)
        for plat in platforms:
            plat.rect.y += abs(P1.vel.y)
            if plat.rect.top >= HEIGHT:
                plat.kill()


    plat_gen() # теперь постоянно нужно создавать новые платформы
    displaysurface.fill((0, 0, 0)) # Эта строка заливает (fill) наш фон в окне указанным цветом

    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
        f = pygame.font.SysFont("Verdana", 20)  #Функция .blit отрисовывает спрайты
        g = f.render(str(P1.score), True, (123, 255, 0))  ##
        displaysurface.blit(g, (WIDTH / 2, 10))  ##
        entity.move()

    pygame.display.update() # Метод внутри PyGame, который обновляет наш экран.
    FramePerSec.tick(FPS)   # Метод, который обновляет значение таймера FPS раз в секунду