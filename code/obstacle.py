import pygame
import random
from code.config import WIN_WIDTH, WIN_HEIGHT


class Obstacle:
    def __init__(self):
        # 1. Tamanho da imagem
        self.size = random.randint(130, 200)
        self.image_original = pygame.transform.scale(pygame.image.load('./assets/imagens/ast.png').convert_alpha(),
                                                     (self.size, self.size))
        self.image = self.image_original

        self.hitbox_size = int(self.size * 0.3)
        self.rect = pygame.Rect(0, 0, self.hitbox_size, self.hitbox_size)
        self.rect.center = (random.randint(0, WIN_WIDTH), random.randint(-600, -100))

        self.is_destructible = random.random() < 0.15
        self.speed = random.randint(3, 7)
        self.angle = 0
        self.rotation_speed = random.randint(-3, 3)
        self.blink_timer = 0
        self.visible = True

    def move(self):
        self.rect.y += self.speed

        # Rotação do asteroide
        self.angle += self.rotation_speed
        self.image = pygame.transform.rotate(self.image_original, self.angle)

        # Adicionando um efeito ao obstaculo destrutivel
        if self.is_destructible:
            self.blink_timer += 1
            if self.blink_timer >= 10:
                self.visible = not self.visible
                self.blink_timer = 0

        #
        if self.rect.top > WIN_HEIGHT:
            self.rect.x = random.randint(0, WIN_WIDTH - self.size)
            self.rect.y = random.randint(-600, -100)
            self.is_destructible = random.random() < 0.15
            return True
        return False

    def draw(self, surface):
        if self.visible:
            img_rect = self.image.get_rect(center=self.rect.center)
            surface.blit(self.image, img_rect)
