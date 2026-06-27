import pygame
import random
from code.config import WIN_WIDTH, WIN_HEIGHT

class Background:
    def __init__(self):
        self.stars = [[random.randint(0, WIN_WIDTH), random.randint(0, WIN_HEIGHT), random.uniform(0.5, 2.0)] for _ in range(100)]

    def move(self):
        for star in self.stars:
            star[1] += star[2]
            if star[1] > WIN_HEIGHT:
                star[1] = 0
                star[0] = random.randint(0, WIN_WIDTH)

    def draw(self, surface):
        for star in self.stars:
            color = (200, 200, 200) if star[2] > 1.5 else (255, 255, 255)
            pygame.draw.circle(surface, color, (star[0], int(star[1])), int(star[2]))