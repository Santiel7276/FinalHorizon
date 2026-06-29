import pygame
import random
from code.config import WIN_WIDTH, WIN_HEIGHT


class Obstacle:
    def __init__(self):
        # Define um tamanho aleatório para o meteoro e carrega a imagem dele
        self.size = random.randint(130, 200)
        self.image_original = pygame.transform.scale(pygame.image.load('./assets/imagens/ast.png').convert_alpha(),
                                                     (self.size, self.size))
        self.image = self.image_original

        # Hibbox do meteoro
        self.hitbox_size = int(self.size * 0.3)
        self.rect = pygame.Rect(0, 0, self.hitbox_size, self.hitbox_size)

        # respawn do meteoro
        self.respawn()

        # Velocidade e efeiteo de rotação do meteoro
        self.speed = random.randint(3, 7)
        self.angle = 0
        self.rotation_speed = random.randint(-3, 3)
        self.blink_timer = 0
        self.visible = True

    def respawn(self):
        """Joga o meteoro de volta para o topo da tela em uma posição X aleatória."""
        self.rect.x = random.randint(0, WIN_WIDTH - self.hitbox_size)
        self.rect.y = random.randint(-600, -100) # Spawna lá em cima, fora da visão do jogador
        self.is_destructible = random.random() < 0.15 # Tem 15% de chance de nascer como um meteoro destrutível
        self.speed = random.randint(3, 7)
        self.visible = True

    def move(self):
        self.rect.y += self.speed
        self.angle += self.rotation_speed
        self.image = pygame.transform.rotate(self.image_original, self.angle)

        # Se for um meteoro destrutível, faz ele piscar a cada 10 frames
        if self.is_destructible:
            self.blink_timer += 1
            if self.blink_timer >= 10:
                self.visible = not self.visible
                self.blink_timer = 0

        # Se o meteoro passou direto pelo fundo da tela, reseta ele no topo
        if self.rect.top > WIN_HEIGHT:
            self.respawn()
            return True
        return False

    def draw(self, surface):
        # Só desenha o meteoro se ele estiver visível
        if self.visible:
            img_rect = self.image.get_rect(center=self.rect.center)
            surface.blit(self.image, img_rect)

