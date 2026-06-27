import pygame
import random
from code.config import WIN_WIDTH, WIN_HEIGHT


class Obstacle:
    def __init__(self):
        self.size = random.randint(60, 120)
        self.image = pygame.transform.scale(pygame.image.load('./assets/imagens/ast.png').convert_alpha(),
                                            (self.size, self.size))

        self.rect = self.image.get_rect(x=random.randint(0, WIN_WIDTH - self.size),
                                        y=random.randint(-500, -50)).inflate(-30, -30)

        self.is_destructible = random.random() < 0.15
        self.speed = random.randint(3, 7)
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
            self.rect.y = random.randint(-600, -100)
            self.is_destructible = random.random() < 0.15
            return True
        return False

    def draw(self, surface):
        if self.visible:
            surface.blit(self.image, self.rect)