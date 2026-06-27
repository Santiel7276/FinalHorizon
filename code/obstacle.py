# code/obstacle.py
import pygame
import random
from code.config import WIN_WIDTH, WIN_HEIGHT


class Obstacle:
    def __init__(self):
        self.width = 40
        self.height = 40
        self.color = (255, 50, 50)


        self.rect = pygame.Rect(
            random.randint(0, WIN_WIDTH - self.width),
            -50,
            self.width,
            self.height
        )


        self.speed = random.randint(5, 10)

    def move(self):
        self.rect.y += self.speed


        if self.rect.top > WIN_HEIGHT:
            self.rect.x = random.randint(0, WIN_WIDTH - self.width)
            self.rect.y = random.randint(-100, -40)
            self.speed = random.randint(5, 10)
            return True

        return False

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)