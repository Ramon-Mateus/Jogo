import pygame
from random import randint
from pygame import font
from pygame import display
from pygame.image import load
from pygame.transform import scale
from pygame.sprite import Sprite, Group, GroupSingle, groupcollide
from pygame import event
from pygame.locals import QUIT, KEYUP, K_SPACE
from pygame.time import Clock

pygame.init()

tela = 800, 600
municao = 5
som_bala = pygame.mixer.Sound('sons/laser.wav')
som_bala.set_volume(0.1)

fonte = font.SysFont('comicsans', 50)
fonte_perdeu = font.SysFont('comicsans', 100)
fonte_vida = font.SysFont('comicsans', 50)

superficie = display.set_mode(tela)
display.set_caption('O Foguete E Os Cometas Assassinos')

fundo = scale(
    load('imagens/universo.jpg'),
    tela
)

class Foguete(Sprite):
    def __init__(self, balas):
        super().__init__()

        self.image = load('imagens/Foguete_ofc.png')
        self.rect = self.image.get_rect()
        self.balas = balas
        self.speed = 2
            
    def lancar_balas(self):
        if len(self.balas) < 5:
            som_bala.play()
            self.balas.add(
                Bala(*self.rect.center)
        )
    
    def update(self):
        keys = pygame.key.get_pressed()

        balas_fonte = fonte.render(
            f'Munição: {municao - len(self.balas)}',
            True, 
            (129, 101, 239)
        )
        superficie.blit(balas_fonte, (20, 20))

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

class Bala(Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = load('imagens/Bala.png')
        self.rect = self.image.get_rect(
            center=(x, y)
        )

    def update(self):
        self.rect.x += 3

        if self.rect.x > tela[0]:
            self.kill()

class Cometa(Sprite):
    def __init__(self):
        super().__init__()

        self.image = load('imagens/Cometa_ofc.png')
        self.rect = self.image.get_rect(
            center=(800, randint(20, 580))
        )

    def update(self):
        global perdeu
        self.rect.x -= 0.1

        if self.rect.x == 0:
            self.kill()

grupo_cometas = Group()
grupo_balas = Group()
foguete = Foguete(grupo_balas)
grupo_foguete = GroupSingle(foguete)
grupo_cometas.add(Cometa())

clock = Clock()
abates = 0
round = 0
perdeu = False
vida_foguete = 3

pygame.mixer.music.load("sons/musica_fundo.ogg")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

while True:

    clock.tick(120)
    if round % 120 == 0:
        if abates < 10:
            grupo_cometas.add(Cometa())
        for _ in range(int(abates / 10)):
            grupo_cometas.add(Cometa())

    for evento in event.get():
        if evento.type == QUIT:
            pygame.quit()
        if evento.type == KEYUP:
            if evento.key == K_SPACE:
                foguete.lancar_balas()
    
    if groupcollide(grupo_balas, grupo_cometas, True, True):
        abates += 1
    
    if groupcollide(grupo_foguete, grupo_cometas, False, True): ####
        vida_foguete += -1
        if vida_foguete == 0:
            perdeu = True

    superficie.blit(fundo, (0, 0))

    fonte_abates = fonte.render(
        f'Abates: {abates}',
        True, 
        (129, 101, 239)
        )
    superficie.blit(fonte_abates, (20, 70))

    fonte_vida = fonte.render(
        f'Vidas: {vida_foguete}',
        True, 
        (129, 101, 239)
        )
    superficie.blit(fonte_vida, (20, 550))

    grupo_foguete.draw(superficie)
    grupo_cometas.draw(superficie)
    grupo_balas.draw(superficie)

    grupo_foguete.update()
    grupo_cometas.update()
    grupo_balas.update()

    if perdeu:
        game_over = fonte_perdeu.render(
            'Game Over',
            True,
            (129, 101, 239)
        )
        superficie.blit(game_over, (200, 200))
        display.update()
        pygame.mixer.music.stop()
        som_bala.stop()
        pygame.time.delay(1000)


    display.update()
    round += 1
