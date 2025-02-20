import pygame
from random import randint

pygame.init()
ventana = pygame.display.set_mode((740,515))
pygame.display.set_caption("Ejemplo 4")

ball = pygame.image.load("pelotita.png")
ballrect = ball.get_rect()
speed = [randint(3,6),randint(3,6)]
ballrect.move_ip(0,0)  

barra = pygame.image.load("Manos_g.png")
barrarect = barra.get_rect()
barrarect.move_ip(240,450)

ladrillo = pygame.image.load("Pelota_Arkanoid.png")  # 🔹 Nuevo objeto ladrillo
fuente = pygame.font.Font(None, 36)

# 🔹 Lista para almacenar los ladrillos
ladrillos = []
filas, columnas = 5, 8

# 🔹 Crear ladrillos en la parte superior
for fila in range(filas):
    for columna in range(columnas):
        ladrillo_rect = ladrillo.get_rect()
        ladrillo_rect.topleft = (columna * (ladrillo_rect.width + 10) + 30, fila * (ladrillo_rect.height + 5) + 30)
        ladrillos.append(ladrillo_rect)

jugando = True
while jugando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jugando = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        barrarect = barrarect.move(-3,0)
    if keys[pygame.K_RIGHT]:
        barrarect = barrarect.move(3,0)

    # 🔹 Rebote al chocar con la barra
    if barrarect.colliderect(ballrect):
        speed[1] = -speed[1]

    # 🔹 Movimiento de la pelota
    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > ventana.get_width():
        speed[0] = -speed[0]
    if ballrect.top < 0: 
        speed[1] = -speed[1]

    # 🔹 Colisión con los ladrillos
    for ladrillo_rect in ladrillos[:]:  # Iterar sobre una copia de la lista
        if ballrect.colliderect(ladrillo_rect):
            ladrillos.remove(ladrillo_rect)  # Eliminar ladrillo
            speed[1] = -speed[1]  # Rebote de la pelota
            break  # Evitar múltiples colisiones en un solo frame

    # 🔹 Condición de victoria
    if not ladrillos:
        texto = fuente.render("¡Ganaste!", True, (0, 255, 0))
        texto_rect = texto.get_rect()
        texto_x = ventana.get_width() / 2 - texto_rect.width / 2
        texto_y = ventana.get_height() / 2 - texto_rect.height / 2
        ventana.blit(texto, [texto_x, texto_y])
        pygame.display.flip()
        pygame.time.delay(3000)
        jugando = False

    # 🔹 Game Over si la pelota cae
    if ballrect.bottom > ventana.get_height():
        texto = fuente.render("Perdiste Malo", True, (125,125,125))
        texto_rect = texto.get_rect()
        texto_x = ventana.get_width() / 2 - texto_rect.width / 2
        texto_y = ventana.get_height() / 2 - texto_rect.height / 2
        ventana.blit(texto, [texto_x, texto_y])
        pygame.display.flip()
        pygame.time.delay(3000)
        jugando = False

    # 🔹 Dibujar todos los elementos en pantalla
    ventana.fill((252, 243, 207))
    ventana.blit(ball, ballrect)
    ventana.blit(barra, barrarect)
    
    # 🔹 Dibujar los ladrillos
    for ladrillo_rect in ladrillos:
        ventana.blit(ladrillo, ladrillo_rect)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
