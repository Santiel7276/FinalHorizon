import pygame
import random
from code.config import WIN_WIDTH, WIN_HEIGHT


class Obstacle:
    def __init__(self):
        self.size = random.randint(130, 200)
        self.image_original = pygame.transform.scale(pygame.image.load('./assets/imagens/ast.png').convert_alpha(),
                                                     (self.size, self.size))
        self.image = self.image_original

        self.hitbox_size = int(self.size * 0.3)
        self.rect = pygame.Rect(0, 0, self.hitbox_size, self.hitbox_size)

        # Inicia o meteoro já usando a lógica correta de spawn
        self.respawn()

        self.speed = random.randint(3, 7)
        self.angle = 0
        self.rotation_speed = random.randint(-3, 3)
        self.blink_timer = 0
        self.visible = True

    def respawn(self):
        # Função dedicada para resetar o meteoro totalmente (Novo X e Novo Y)
        self.rect.x = random.randint(0, WIN_WIDTH - self.hitbox_size)
        self.rect.y = random.randint(-600, -100)
        self.is_destructible = random.random() < 0.15
        self.speed = random.randint(3, 7)
        self.visible = True

    def move(self):
        self.rect.y += self.speed
        self.angle += self.rotation_speed
        self.image = pygame.transform.rotate(self.image_original, self.angle)

        if self.is_destructible:
            self.blink_timer += 1
            if self.blink_timer >= 10:
                self.visible = not self.visible
                self.blink_timer = 0

        if self.rect.top > WIN_HEIGHT:
            self.respawn()
            return True
        return False

    def draw(self, surface):
        if self.visible:
            img_rect = self.image.get_rect(center=self.rect.center)
            surface.blit(self.image, img_rect)

            # TRUQUE DE DESENVOLVEDOR: Tire o '#' da linha abaixo para enxergar as hitboxes vermelhas na tela
            # pygame.draw.rect(surface, (255, 0, 0), self.rect, 2)