import pygame

pygame.init()
ANCHO, ALTO = 740, 515
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Prueba Pygame")

# Intentar cargar imágenes y manejar errores
try:
    ball = pygame.image.load("pelotita.png")
    barra = pygame.image.load("Manos_g.png")
except pygame.error as e:
    print(f"Error al cargar imágenes: {e}")
    exit()

ballrect = ball.get_rect()
barrarect = barra.get_rect()
barrarect.move_ip(240, 450)

jugando = True
while jugando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jugando = False

    # Dibujar elementos en pantalla
    ventana.fill((252, 243, 207))  # Fondo
    ventana.blit(ball, ballrect)  # Pelota
    ventana.blit(barra, barrarect)  # Barra
    pygame.display.flip()  # Actualizar pantalla

pygame.quit()
