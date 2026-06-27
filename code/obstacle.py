import pygame
import random
from code.config import WIN_WIDTH, WIN_HEIGHT


class Obstacle:
    def __init__(self):
        self.size = random.randint(60, 90)
        self.image = pygame.transform.scale(pygame.image.load('./assets/imagens/ast.png').convert_alpha(),
                                            (self.size, self.size))
        self.rect = self.image.get_rect(x=random.randint(0, WIN_WIDTH - self.size), y=-100).inflate(-20, -20)

        self.is_destructible = random.random() < 0.25
        self.speed = random.randint(3, 6)
        self.blink_timer = 0
        self.visible = True

    def move(self):
        self.rect.y += self.speed

        if self.is_destructible:
            self.blink_timer += 1
            if self.blink_timer >= 10:
                self.visible = not self.visible
                self.blink_timer = 0

        if self.rect.top > WIN_HEIGHT:
            self.rect.x = random.randint(0, WIN_WIDTH - self.size)
            self.rect.y = random.randint(-150, -50)
            return True
        return False

    def draw(self, surface):
        if self.visible:
            surface.blit(self.image, self.rect)