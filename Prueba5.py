import pygame
from random import randint

pygame.init()
ANCHO, ALTO = 740, 515
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Arkanoid Mejorado")

# Cargar imágenes
ball = pygame.image.load("pelotita.png")
barra = pygame.image.load("Manos_g.png")
ladrillo = pygame.image.load("NUEVO FREEZER.png")
ladrillo_irrompible = pygame.image.load("Freezer chiquito.png")  # Nuevo ladrillo
ladrillo_endurecido_1 = pygame.image.load("Zarbon.png")  # Nivel 1
ladrillo_endurecido_2 = pygame.image.load("dodoria.png")  # Nivel 2

# Rectángulos de los objetos
ballrect = ball.get_rect()
ballrect.move_ip(370, 207)
barrarect = barra.get_rect()
barrarect.move_ip(240, 450)

# Velocidad de la pelota
speed = [randint(3, 6), randint(3, 6)]
barra_speed = 6  # Velocidad inicial de la barra
aceleracion_barra = 0.3  # Cuánto aumenta la velocidad al mantener presionada la tecla

# Fuente para los mensajes
fuente = pygame.font.Font(None, 36)

# Clases de ladrillos
class Ladrillo:
    def __init__(self, x, y, imagen):
        self.image = imagen
        self.rect = imagen.get_rect()
        self.rect.topleft = (x, y)

class LadrilloIrrompible(Ladrillo):
    """Ladrillo que la pelota solo rebota y no se destruye"""
    pass  # No se elimina al colisionar

class LadrilloEndurecido(Ladrillo):
    """Ladrillo que necesita varios golpes para romperse"""
    def __init__(self, x, y):
        super().__init__(x, y, ladrillo_endurecido_1)
        self.nivel = 2  # Golpes necesarios para romperlo
    
    def debilitar(self):
        self.nivel -= 1
        if self.nivel == 1:
            self.image = ladrillo_endurecido_2  # Cambiar color al nivel 1

# Listas para almacenar los ladrillos
ladrillos = []
filas, columnas = 4, 7
espacio_horizontal = 12
espacio_vertical = 15

# Posicionar los ladrillos en la parte superior
ladrillo_width = ladrillo.get_width()
ladrillo_height = ladrillo.get_height()
total_width = (columnas * ladrillo_width) + ((columnas - 1) * espacio_horizontal)
inicio_x = (ANCHO - total_width) // 2

# Evitar solapamiento
def posicion_valida(x, y, ladrillos):
    for ladrillo_obj in ladrillos:
        if abs(x - ladrillo_obj.rect.x) < ladrillo_width and abs(y - ladrillo_obj.rect.y) < ladrillo_height:
            return False  # Se superpone con otro ladrillo
    return True

# Generar ladrillos aleatorios sin solaparse
contador_irrompibles = 0  # Solo los 3 primeros serán irrompibles
for _ in range(filas * columnas):
    while True:
        x = randint(50, ANCHO - ladrillo_width - 50)
        y = randint(30, 200)
        
        if posicion_valida(x, y, ladrillos):  # Asegurar que no se superpongan
            if contador_irrompibles < 3:
                ladrillos.append(LadrilloIrrompible(x, y, ladrillo_irrompible))
                contador_irrompibles += 1
            elif randint(0, 2) == 0:
                ladrillos.append(LadrilloEndurecido(x, y))
            else:
                ladrillos.append(Ladrillo(x, y, ladrillo))
            break  # Salir del while si la posición es válida

# Bucle principal del juego
jugando = True
while jugando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jugando = False

    keys = pygame.key.get_pressed()
    
    # Movimiento de la barra con aceleración
    if keys[pygame.K_LEFT] and barrarect.left > 0:
        barra_speed += aceleracion_barra  # Aumenta la velocidad al mantener pulsado
        barrarect = barrarect.move(-barra_speed, 0)
    elif keys[pygame.K_RIGHT] and barrarect.right < ANCHO:
        barra_speed += aceleracion_barra
        barrarect = barrarect.move(barra_speed, 0)
    else:
        barra_speed = 6  # Resetear velocidad si no se presiona ninguna tecla

    # Rebote en la barra
    if barrarect.colliderect(ballrect):
        speed[1] = -speed[1]

    # Movimiento de la pelota
    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > ventana.get_width():
        speed[0] = -speed[0]
    if ballrect.top < 0:
        speed[1] = -speed[1]

    # Colisión con los ladrillos
    for ladrillo_obj in ladrillos[:]:
        if ballrect.colliderect(ladrillo_obj.rect):
            if isinstance(ladrillo_obj, LadrilloIrrompible):
                speed[1] = -speed[1]  # Rebota pero no se destruye
            elif isinstance(ladrillo_obj, LadrilloEndurecido):
                ladrillo_obj.debilitar()
                if ladrillo_obj.nivel == 0:  # Se rompe si llega a nivel 0
                    ladrillos.remove(ladrillo_obj)
                speed[1] = -speed[1]
            else:
                ladrillos.remove(ladrillo_obj)
                speed[1] = -speed[1]
            break  # Evitar múltiples colisiones en un solo frame
   
    ladrillos_rompibles = [ladrillo for ladrillo in ladrillos if not isinstance(ladrillo, LadrilloIrrompible)]

    # Condición de victoria
    if not ladrillos_rompibles:  # Si no quedan ladrillos normales o endurecidos, ganas
        texto = fuente.render("¡Ganaste!", True, (0, 255, 0))
        ventana.blit(texto, [ANCHO / 2 - texto.get_width() / 2, ALTO / 2])
        pygame.display.flip()
        pygame.time.delay(3000)
        jugando = False

    # Game Over si la pelota cae
    if ballrect.bottom > ventana.get_height():
        texto = fuente.render("Game Over", True, (125, 125, 125))
        ventana.blit(texto, [ANCHO / 2 - texto.get_width() / 2, ALTO / 2])
        pygame.display.flip()
        pygame.time.delay(3000)
        jugando = False

    # Dibujar elementos
    ventana.fill((252, 243, 207))
    ventana.blit(ball, ballrect)
    ventana.blit(barra, barrarect)

    # Dibujar ladrillos
    for ladrillo_obj in ladrillos:
        ventana.blit(ladrillo_obj.image, ladrillo_obj.rect)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
