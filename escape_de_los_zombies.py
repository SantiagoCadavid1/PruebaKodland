import pygame
import sys
import os

# Inicialización de Pygame
pygame.init()

# Definir colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# Tamaño de la pantalla
ANCHO = 1080
ALTO = 720
pantalla = pygame.display.set_mode((ANCHO, ALTO))
clock = pygame.time.Clock()
pygame.display.set_caption("Escape de los zombies")

# Cargar fondos de pantalla
ruta_recursos = os.path.join("recursos", "bg")
fondo_menu = pygame.image.load(os.path.join(ruta_recursos, "bg_menu.png")).convert()
fondo_nivel1 = pygame.image.load(os.path.join(ruta_recursos, "bg_nivel1.png")).convert()
fondo_nivel2 = pygame.image.load(os.path.join(ruta_recursos, "bg_nivel2.png")).convert()
fondo_gameover = pygame.image.load(os.path.join(ruta_recursos, "bg_gameover.png")).convert()
fondo_victoria = pygame.image.load(os.path.join(ruta_recursos, "bg_menu.png")).convert()

# Crear botones
boton_jugar_rect = pygame.Rect((ANCHO/2)-100, (ALTO/2)-50, 200, 50)
boton_salir_rect = pygame.Rect((ANCHO/2)-100, (ALTO/2)+50, 200, 50)

# Fuente y texto de los botones
fuente = pygame.font.SysFont(None, 36)
texto_jugar = fuente.render("Jugar", True, NEGRO)
texto_salir = fuente.render("Salir", True, NEGRO)
texto_menu = fuente.render("Menu", True, NEGRO)

# Cargar bloques nivel 1
ruta_bloques_nivel1 = os.path.join("recursos", "bloques", "nivel1")
bloque1_nivel1 = pygame.image.load(os.path.join(ruta_bloques_nivel1, "1.png")).convert_alpha()
bloque2_nivel1 = pygame.image.load(os.path.join(ruta_bloques_nivel1, "2.png")).convert_alpha()
bloque3_nivel1 = pygame.image.load(os.path.join(ruta_bloques_nivel1, "3.png")).convert_alpha()
flecha_nivel1 = pygame.image.load(os.path.join(ruta_bloques_nivel1, "flecha.png")).convert_alpha()

# Cargar bloques nivel 2
ruta_bloques_nivel2 = os.path.join("recursos", "bloques", "nivel2")
bloque1_nivel2 = pygame.image.load(os.path.join(ruta_bloques_nivel2, "1.png")).convert_alpha()
bloque2_nivel2 = pygame.image.load(os.path.join(ruta_bloques_nivel2, "2.png")).convert_alpha()
bloque3_nivel2 = pygame.image.load(os.path.join(ruta_bloques_nivel2, "3.png")).convert_alpha()
flecha_nivel2 = pygame.image.load(os.path.join(ruta_bloques_nivel2, "flecha.png")).convert_alpha()

# Posición de los bloques nivel 1
x_bloque1_nivel1, y_bloque1_nivel1 = 0, ALTO - 60
x_bloques2_nivel1 = [i * 60 for i in range(1, 18)]
y_bloques2_nivel1 = [ALTO - 60] * 16
x_bloque3_nivel1, y_bloque3_nivel1 = 17 * 60, ALTO - 60

# Posición de los bloques nivel 2 (mismas que nivel 1)
x_bloque1_nivel2, y_bloque1_nivel2 = x_bloque1_nivel1, y_bloque1_nivel1
x_bloques2_nivel2, y_bloques2_nivel2 = x_bloques2_nivel1, y_bloques2_nivel1
x_bloque3_nivel2, y_bloque3_nivel2 = x_bloque3_nivel1, y_bloque3_nivel1
x_flecha, y_flecha = 1020, 600

# Cargar sprites del personaje
ruta_personaje = os.path.join("recursos", "jugador")
sprites_idle = [pygame.image.load(os.path.join(ruta_personaje, f"Idle ({i}).png")).convert_alpha() for i in range(1, 11)]
sprites_run = [pygame.image.load(os.path.join(ruta_personaje, f"Run ({i}).png")).convert_alpha() for i in range(1, 9)]
sprites_jump = [pygame.image.load(os.path.join(ruta_personaje, f"Jump ({i}).png")).convert_alpha() for i in range(1, 13)]

# Redimensionar sprites del personaje
TAMANO_PERSONAJE = (49, 51)

# Cargar sprites de los enemigos
ruta_enemigos_zombi1 = os.path.join("recursos", "enemigos", "zombi1")
sprites_zombi1 = [pygame.image.load(os.path.join(ruta_enemigos_zombi1, f"Walk ({i}).png")).convert_alpha() for i in range(1, 11)]
ruta_enemigos_zombi2 = os.path.join("recursos", "enemigos", "zombi2")
sprites_zombi2 = [pygame.image.load(os.path.join(ruta_enemigos_zombi2, f"Walk ({i}).png")).convert_alpha() for i in range(1, 11)]

# Redimensionar sprites de los enemigos
TAMANO_ZOMBI = (40, 40)

# Definir velocidad de los enemigos
velocidad_zombi1 = 1
velocidad_zombi2 = 5

# Posiciones de los enemigos
posiciones_zombi1_nivel1 = [(300, 600), (600, 600)]
posiciones_zombi2_nivel2 = [(300, 600), (600, 600)]

# Clase para los zombis
class Zombi:
    def __init__(self, sprites, velocidad, posiciones, nivel):
        self.sprites_derecha = sprites
        self.sprites_izquierda = [pygame.transform.flip(sprite, True, False) for sprite in sprites]
        self.velocidad = velocidad
        self.posiciones = posiciones
        self.nivel = nivel
        self.rects = [pygame.Rect(pos[0], pos[1], TAMANO_ZOMBI[0], TAMANO_ZOMBI[1]) for pos in posiciones]
        self.direcciones = [1] * len(posiciones)  # Inicialmente, los zombis se mueven hacia la derecha
        self.indices = [0] * len(posiciones)  # Índices para la animación de los sprites
        self.distancias_recorridas = [0] * len(posiciones)  # Distancias recorridas por los zombis
        self.estados = ["derecha"] * len(posiciones)  # Estado inicial: moviéndose hacia la derecha

    def update(self):
        for i, rect in enumerate(self.rects):
            # Mover el zombi en la dirección actual
            rect.x += self.velocidad * self.direcciones[i]
            self.distancias_recorridas[i] += abs(self.velocidad)
            
            if self.distancias_recorridas[i] >= 100 * self.nivel:  # Nivel 1
                # Cambiar dirección y estado
                self.velocidad *= -1
                self.direcciones[i] *= -1
                if self.estados[i] == "derecha":
                    self.estados[i] = "izquierda"
                else:
                    self.estados[i] = "derecha"
                self.distancias_recorridas[i] = 0  # Reiniciar la distancia recorrida

            # Actualizar índice de animación
            self.indices[i] = (self.indices[i] + 0.2) % len(self.sprites_derecha)
    
    def draw(self, pantalla):
        for i, rect in enumerate(self.rects):
            if self.estados[i] == "derecha":
                sprite = self.sprites_derecha[int(self.indices[i])]
            else:
                sprite = self.sprites_izquierda[int(self.indices[i])]
            pantalla.blit(sprite, rect)

# Crear zombis para cada nivel
zombis_nivel1 = Zombi(sprites_zombi1, velocidad_zombi1, posiciones_zombi1_nivel1, 1)
zombis_nivel2 = Zombi(sprites_zombi2, velocidad_zombi2, posiciones_zombi2_nivel2, 2)

# Definir velocidad del personaje y gravedad
velocidad_personaje = 5
gravedad = 0.5
salto = -13

# Posición inicial del personaje
x_personaje, y_personaje = 0, 600

# Velocidad inicial del personaje
vel_x_personaje = 0
vel_y_personaje = 0

# Índice de los sprites de animación
indice_animacion = 0
indice_salto = 0

# Dirección del personaje (1: derecha, -1: izquierda)
direccion_personaje = 1

# Estado del personaje
estado_personaje = "idle"

# Variable para rastrear si el personaje ha saltado
ha_saltado = False

# Variables de estado del juego
estado = "menu"  # Estado inicial: menú de inicio

# Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif estado == "menu" and event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Botón izquierdo del ratón
                if boton_jugar_rect.collidepoint(event.pos):
                    estado = "nivel1"  # Cambiar al estado de nivel 1
                elif boton_salir_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        elif estado in ["victoria", "game_over"] and event.type == pygame.MOUSEBUTTONDOWN:
            if boton_jugar_rect.collidepoint(event.pos):
                estado = "menu"
            elif boton_salir_rect.collidepoint(event.pos):
                pygame.quit()
                sys.exit()
    
    # Obtener teclas presionadas
    teclas = pygame.key.get_pressed()

    # Lógica del movimiento del personaje
    if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
        vel_x_personaje = -velocidad_personaje
        direccion_personaje = -1
        estado_personaje = "run"
    elif teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
        vel_x_personaje = velocidad_personaje
        direccion_personaje = 1
        estado_personaje = "run"
    else:
        vel_x_personaje = 0
        estado_personaje = "idle"
        
    # Limitar movimiento del personaje dentro de la pantalla
    if y_personaje > ALTO - TAMANO_PERSONAJE[1]:
        y_personaje = ALTO - TAMANO_PERSONAJE[1]
        vel_y_personaje = 0

    if teclas[pygame.K_SPACE] and not ha_saltado and estado_personaje != "jump":
        estado_personaje = "jump"
        vel_y_personaje = salto
        ha_saltado = True

    # Animar al personaje
    if estado_personaje == "run":
        indice_animacion += 0.2
        if indice_animacion >= len(sprites_run):
            indice_animacion = 0
        sprite_personaje = sprites_run[int(indice_animacion)]
    elif estado_personaje == "jump":
        indice_salto += 0.3
        if indice_salto >= len(sprites_jump):
            indice_salto = 0
            estado_personaje = "idle"
        sprite_personaje = sprites_jump[int(indice_salto)]
    else:
        indice_animacion += 0.1
        if indice_animacion >= len(sprites_idle):
            indice_animacion = 0
        sprite_personaje = sprites_idle[int(indice_animacion)]

    # Invertir sprite si el personaje se mueve hacia la izquierda
    if direccion_personaje == -1:
        sprite_personaje = pygame.transform.flip(sprite_personaje, True, False)

    # Lógica del juego basada en el estado
    if estado == "menu":
        # Dibujar fondo del menú de inicio
        pantalla.blit(fondo_menu, (0, 0))

        # Dibujar botones
        pygame.draw.rect(pantalla, BLANCO, boton_jugar_rect)
        pygame.draw.rect(pantalla, BLANCO, boton_salir_rect)

        # Dibujar texto de los botones
        pantalla.blit(texto_jugar, (boton_jugar_rect.centerx - texto_jugar.get_width() // 2,
                                    boton_jugar_rect.centery - texto_jugar.get_height() // 2))
        pantalla.blit(texto_salir, (boton_salir_rect.centerx - texto_salir.get_width() // 2,
                                    boton_salir_rect.centery - texto_salir.get_height() // 2))
        
        # Dibujar título del menú
        titulo_texto = fuente.render("Escape de los zombies", True, NEGRO)
        pantalla.blit(titulo_texto, ((ANCHO - titulo_texto.get_width()) // 2, 150))

    elif estado == "nivel1":
        # Actualizar posición de los zombis
        zombis_nivel1.update()
        
        # Aplicar gravedad al personaje
        vel_y_personaje += gravedad

        # Actualizar posición del personaje
        x_personaje += vel_x_personaje
        y_personaje += vel_y_personaje
        
        # Limitar movimiento del personaje dentro de la pantalla
        x_personaje = max(0, min(ANCHO - TAMANO_PERSONAJE[0], x_personaje))
        y_personaje = max(0, min(ALTO - TAMANO_PERSONAJE[1], y_personaje))
        
        # Detección de colisiones con bloques nivel 1
        rect_personaje = pygame.Rect(x_personaje, y_personaje, TAMANO_PERSONAJE[0], TAMANO_PERSONAJE[1])
        rect_bloque1_nivel1 = pygame.Rect(x_bloque1_nivel1, y_bloque1_nivel1, 60, 60)
        rect_bloque3_nivel1 = pygame.Rect(x_bloque3_nivel1, y_bloque3_nivel1, 60, 60)
        
        # Detección de colisiones entre el personaje y los enemigos
        for zombi in zombis_nivel1.rects:  # Suponiendo que zombis_nivel1 y zombis_nivel2 son instancias de la clase Zombi
            if rect_personaje.colliderect(zombi):
                estado = "game_over"  # Cambiar al estado de game over
                x_personaje, y_personaje = 0, 600

        if rect_personaje.colliderect(rect_bloque1_nivel1) or rect_personaje.colliderect(rect_bloque3_nivel1):
            if vel_y_personaje > 0:
                y_personaje = min(rect_bloque1_nivel1.top, rect_bloque3_nivel1.top) - TAMANO_PERSONAJE[1]
                vel_y_personaje = 0
                ha_saltado = False

        for i in range(16):
            rect_bloque2_nivel1 = pygame.Rect(x_bloques2_nivel1[i], y_bloques2_nivel1[i], 60, 60)
            if rect_personaje.colliderect(rect_bloque2_nivel1):
                if vel_y_personaje > 0:
                    y_personaje = rect_bloque2_nivel1.top - TAMANO_PERSONAJE[1]
                    vel_y_personaje = 0
                    ha_saltado = False

        # Detección de colisión con la flecha y cambio de estado a nivel 2 o victoria
        rect_flecha = pygame.Rect(1020, 600, 60, 60)
        if rect_personaje.colliderect(rect_flecha):
            if estado == "nivel1":
                estado = "nivel2"
                # Posición inicial del personaje
                x_personaje, y_personaje = 0, 600
            elif estado == "nivel2":
                estado = "victoria"
        
        # Dibujar fondo del nivel 1
        pantalla.blit(fondo_nivel1, (0, 0))

        # Dibujar bloques nivel 1
        pantalla.blit(bloque1_nivel1, (x_bloque1_nivel1, y_bloque1_nivel1))
        for x, y in zip(x_bloques2_nivel1, y_bloques2_nivel1):
            pantalla.blit(bloque2_nivel1, (x, y))
        pantalla.blit(bloque3_nivel1, (x_bloque3_nivel1, y_bloque3_nivel1))

        
        # Dibujar flecha
        pantalla.blit(flecha_nivel1, (x_flecha, y_flecha))
        
        # Dibujar zombis
        zombis_nivel1.draw(pantalla)
        
        # Dibujar personaje
        pantalla.blit(sprite_personaje, (x_personaje, y_personaje))

    elif estado == "nivel2":
        # Actualizar posición de los zombis
        zombis_nivel2.update()
        
        # Fondo del segundo nivel
        pantalla.blit(fondo_nivel2, (0, 0))
        
        # Aplicar gravedad al personaje
        vel_y_personaje += gravedad

        # Actualizar posición del personaje
        x_personaje += vel_x_personaje
        y_personaje += vel_y_personaje
        
        # Limitar movimiento del personaje dentro de la pantalla
        x_personaje = max(0, min(ANCHO - TAMANO_PERSONAJE[0], x_personaje))
        y_personaje = max(0, min(ALTO - TAMANO_PERSONAJE[1], y_personaje))
        
        # Detección de colisiones con bloques nivel 1
        rect_personaje = pygame.Rect(x_personaje, y_personaje, TAMANO_PERSONAJE[0], TAMANO_PERSONAJE[1])
        rect_bloque1_nivel2 = pygame.Rect(x_bloque1_nivel2, y_bloque1_nivel2, 60, 60)
        rect_bloque3_nivel2 = pygame.Rect(x_bloque3_nivel2, y_bloque3_nivel2, 60, 60)
        
        # Detección de colisiones entre el personaje y los enemigos
        for zombi in zombis_nivel2.rects:  # Suponiendo que zombis_nivel1 y zombis_nivel2 son instancias de la clase Zombi
            if rect_personaje.colliderect(zombi):
                estado = "game_over"  # Cambiar al estado de game over
                x_personaje, y_personaje = 0, 600

        if rect_personaje.colliderect(rect_bloque1_nivel2) or rect_personaje.colliderect(rect_bloque3_nivel2):
            if vel_y_personaje > 0:
                y_personaje = min(rect_bloque1_nivel2.top, rect_bloque3_nivel2.top) - TAMANO_PERSONAJE[1]
                vel_y_personaje = 0
                ha_saltado = False

        for i in range(16):
            rect_bloque2_nivel2 = pygame.Rect(x_bloques2_nivel2[i], y_bloques2_nivel2[i], 60, 60)
            if rect_personaje.colliderect(rect_bloque2_nivel2):
                if vel_y_personaje > 0:
                    y_personaje = rect_bloque2_nivel2.top - TAMANO_PERSONAJE[1]
                    vel_y_personaje = 0
                    ha_saltado = False

        # Detección de colisión con la flecha y cambio de estado a nivel 2 o victoria
        rect_flecha = pygame.Rect(1020, 600, 60, 60)
        if rect_personaje.colliderect(rect_flecha):
            if estado == "nivel1":
                estado = "nivel2"
                # Posición inicial del personaje
                x_personaje, y_personaje = 0, 600
            elif estado == "nivel2":
                estado = "victoria"
                x_personaje, y_personaje = 0, 600
        
        # Dibujar fondo del nivel 2
        pantalla.blit(fondo_nivel2, (0, 0))

        # Dibujar bloques nivel 2
        pantalla.blit(bloque1_nivel2, (x_bloque1_nivel2, y_bloque1_nivel2))
        for x, y in zip(x_bloques2_nivel2, y_bloques2_nivel2):
            pantalla.blit(bloque2_nivel2, (x, y))
        pantalla.blit(bloque3_nivel2, (x_bloque3_nivel2, y_bloque3_nivel2))
        
        # Dibujar flecha
        pantalla.blit(flecha_nivel2, (x_flecha, y_flecha))
        
        # Dibujar zombis
        zombis_nivel2.draw(pantalla)
        
        # Dibujar personaje
        pantalla.blit(sprite_personaje, (x_personaje, y_personaje))
    
    elif estado == "game_over":
        # Dibujar fondo de game over
        pantalla.blit(fondo_gameover, (0, 0))
        
        # Dibujar botones
        pygame.draw.rect(pantalla, BLANCO, boton_jugar_rect)
        pygame.draw.rect(pantalla, BLANCO, boton_salir_rect)

        # Dibujar texto de los botones
        pantalla.blit(texto_menu, (boton_jugar_rect.centerx - texto_menu.get_width() // 2,
                                   boton_jugar_rect.centery - texto_menu.get_height() // 2))
        pantalla.blit(texto_salir, (boton_salir_rect.centerx - texto_salir.get_width() // 2,
                                    boton_salir_rect.centery - texto_salir.get_height() // 2))
        # Dibujar título del menú
        titulo_texto = fuente.render("Perdiste", True, NEGRO)
        pantalla.blit(titulo_texto, ((ANCHO - titulo_texto.get_width()) // 2, 150))
    
    elif estado == "victoria":
        # Dibujar fondo de victoria
        pantalla.blit(fondo_victoria, (0, 0))
        
        # Dibujar botones
        pygame.draw.rect(pantalla, BLANCO, boton_jugar_rect)
        pygame.draw.rect(pantalla, BLANCO, boton_salir_rect)

        # Dibujar texto de los botones
        pantalla.blit(texto_menu, (boton_jugar_rect.centerx - texto_menu.get_width() // 2,
                                   boton_jugar_rect.centery - texto_menu.get_height() // 2))
        pantalla.blit(texto_salir, (boton_salir_rect.centerx - texto_salir.get_width() // 2,
                                    boton_salir_rect.centery - texto_salir.get_height() // 2))
        # Dibujar título del menú
        titulo_texto = fuente.render("Has escapado", True, NEGRO)
        pantalla.blit(titulo_texto, ((ANCHO - titulo_texto.get_width()) // 2, 150))
    
    pygame.display.flip()
    clock.tick(60)
