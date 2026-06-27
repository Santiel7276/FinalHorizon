# code/obstacle.py
import pygame
import random
from code.config import WIN_WIDTH, WIN_HEIGHT


class Obstacle:
    def __init__(self):
        self.is_destructible = random.random() < 0.3
        self.image = pygame.transform.scale(pygame.image.load('./assets/imagens/ast.png').convert_alpha(), (50, 50))
        self.rect = self.image.get_rect(x=random.randint(0, WIN_WIDTH - 50), y=-50)
        self.speed = random.randint(5, 10)

    def move(self):
        self.rect.y += self.speed
        if self.rect.top > WIN_HEIGHT:
            self.rect.x = random.randint(0, WIN_WIDTH - 50)
            self.rect.y = random.randint(-100, -40)
            return True
        return False

    def draw(self, surface):
        surface.blit(self.image, self.rect)