import pygame

class Bullet:
    def __init__(self, x, y):
        # Define o tamanho do tiro e a posição inicial
        self.rect = pygame.Rect(x, y, 5, 15)
        self.speed = 10

    def move(self):
        # Move o tiro para cima na tela
        self.rect.y -= self.speed

    def draw(self, surface):
        # Desenha o tiro na tela com a cor desejada
        pygame.draw.rect(surface, (0, 255, 255), self.rect)