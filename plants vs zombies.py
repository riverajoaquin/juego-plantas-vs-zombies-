# Mini-invaders, version 0.10
# (Puntuac.)
# Parte de la intro a Pygame, por Nacho Cabanes
 
import pygame
from pygame.locals import *
import random
 
pygame.init()
 
ancho = 900
alto = 620
cantidadMarcianos = 5
 
pantalla = pygame.display.set_mode( (ancho, alto) )
pygame.key.set_repeat(1,25)
reloj = pygame.time.Clock()
 
imagenNave = pygame.image.load("nave.png")
rectanguloNave = imagenNave.get_rect()
imagenUfo = pygame.image.load("ufo.png")
rectanguloUfo = imagenUfo.get_rect()
imagenMarciano = pygame.image.load("spaceinvader.png")
rectangulosMarcianos = { }
marcianosVisibles = { }
velocidadesX = { }
velocidadesY = { }
imagenDisparo = pygame.image.load("disparo.png")
rectanguloDisparo = imagenDisparo.get_rect()
 #intro
imagenPresent = pygame.image.load("invadersIntro.png")
rectanguloPresent = imagenPresent.get_rect()
rectanguloPresent.top = 60
rectanguloPresent.left = 100
#sonido
pygame.mixer.music.load('sonido.mp3')
pygame.mixer.music.play(1)
 #intro letras
letra30 = pygame.font.SysFont("Arial", 30)
imagenTextoPresent = letra30.render('Pulsa Espacio para jugar',
    True, (200,200,200), (0,0,0) )
rectanguloTextoPresent = imagenTextoPresent.get_rect()
rectanguloTextoPresent.centerx = pantalla.get_rect().centerx
rectanguloTextoPresent.centery = 520
 
letra18 = pygame.font.SysFont("Arial", 18)
 
partidaEnMarcha = True
 
while partidaEnMarcha:
 
    # ---- Presentacion ----
    pantalla.fill( (0,0,0) )
    pantalla.blit(imagenPresent, rectanguloPresent)
    pantalla.blit(imagenTextoPresent, rectanguloTextoPresent)
    pygame.display.flip()
 
    entrarAlJuego = False
    while not entrarAlJuego:
        pygame.time.wait(100)
        for event in pygame.event.get(KEYUP):
            if event.key == K_SPACE:
                entrarAlJuego = True
 
    # ---- Comienzo de una sesion de juego ----
    puntos = 0                            # Nuevo 0.10
    rectanguloNave.left = ancho/2
    rectanguloNave.top = alto-50
    rectanguloUfo.top = 20
 
    for i in range(0,cantidadMarcianos+1):
        rectangulosMarcianos[i] = imagenMarciano.get_rect()
        rectangulosMarcianos[i].left = random.randrange(50,751)
        rectangulosMarcianos[i].top = random.randrange(10,301)
        marcianosVisibles[i] = True
        velocidadesX[i] = 3
        velocidadesY[i] = 3
 
    disparoActivo = False
    ufoVisible = True
    terminado = False
 #----------------------------
    while not terminado:
        # ---- Comprobar acciones del usuario ----
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                terminado = True
                partidaEnMarcha = False
 
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            rectanguloNave.left -= 8
        if keys[K_RIGHT]:
            rectanguloNave.left += 8
        if keys[K_SPACE] and not disparoActivo:
            disparoActivo = True
            rectanguloDisparo.left = rectanguloNave.left + 18
            rectanguloDisparo.top = rectanguloNave.top - 25
 
        # ---- Actualizar estado ----
        for i in range(0,cantidadMarcianos+1):
            rectangulosMarcianos[i].left += velocidadesX[i]
            rectangulosMarcianos[i].top += velocidadesY[i]
            if rectangulosMarcianos[i].left < 0 or rectangulosMarcianos[i].right > ancho:
                velocidadesX[i] = -velocidadesX[i]
            if rectangulosMarcianos[i].top < 0 or rectangulosMarcianos[i].bottom > alto:
                velocidadesY[i] = -velocidadesY[i]
 
        rectanguloUfo.left += 2
        if rectanguloUfo.right > ancho:
            rectanguloUfo.left = 0
 
        if disparoActivo:
            rectanguloDisparo.top -= 6
            if rectanguloDisparo.top <= 0:
                disparoActivo = False
 
        # ---- Comprobar colisiones ----
        for i in range(0,cantidadMarcianos+1):
            if marcianosVisibles[i]:
                if rectanguloNave.colliderect( rectangulosMarcianos[i] ):
                    terminado = True
 
                if disparoActivo:
                    if rectanguloDisparo.colliderect( rectangulosMarcianos[i]) :
                        marcianosVisibles[i] = False
                        disparoActivo = False
                        puntos += 10        # Nuevo 0.10
 
        if disparoActivo:
            if rectanguloDisparo.colliderect( rectanguloUfo) :
                ufoVisible = False
                disparoActivo = False
                puntos += 50                # Nuevo 0.10
 
        cantidadMarcianosVisibles = 0
        for i in range(0,cantidadMarcianos+1):
            if marcianosVisibles[i]:
                cantidadMarcianosVisibles = cantidadMarcianosVisibles + 1
 
        if not ufoVisible and cantidadMarcianosVisibles == 0:
            terminado = True    
 
        # ---- Dibujar elementos en pantalla ----
        pantalla.fill( (0,0,0) )
        for i in range(0,cantidadMarcianos+1):
            if marcianosVisibles[i]:
                pantalla.blit(imagenMarciano, rectangulosMarcianos[i])
        if ufoVisible:
            pantalla.blit(imagenUfo, rectanguloUfo)
        if disparoActivo:
            pantalla.blit(imagenDisparo, rectanguloDisparo)
        pantalla.blit(imagenNave, rectanguloNave)
 
        imagenPuntos = letra18.render('Puntos '+str(puntos), # Nuevo 0.10
            True, (200,200,200), (0,0,0) )                   # Nuevo 0.10
        rectanguloPuntos = imagenPuntos.get_rect()           # Nuevo 0.10
        rectanguloPuntos.left = 10                           # Nuevo 0.10
        rectanguloPuntos.top = 10                            # Nuevo 0.10
        pantalla.blit(imagenPuntos, rectanguloPuntos)        # Nuevo 0.10
 
        pygame.display.flip()
 
        # ---- Ralentizar hasta 40 fotogramas por segundo  ----
        reloj.tick(50)  # 50 fps
 
# ---- Final de partida ----
pygame.quit()
 
