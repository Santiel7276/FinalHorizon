# code/player.py
import pygame
from code.config import WIN_WIDTH, WIN_HEIGHT


class Player:
    def __init__(self):
        self.image = pygame.image.load('./assets/imagens/nave.png').convert_alpha()

        # Redimensionando a nave
        self.image = pygame.transform.scale(self.image, (100, 100))

        #
        self.rect = self.image.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT - 60))

        # Velocidade de movimento
        self.speed = 7

    def move(self):
        # Captura as teclas pressionadas
        keys = pygame.key.get_pressed()

        # Move para a esquerda, mas não deixa sair do limite da tela
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed

        # Move para a direita, mas não deixa passar da largura da tela
        if keys[pygame.K_RIGHT] and self.rect.right < WIN_WIDTH:
            self.rect.x += self.speed

    def draw(self, surface):
        # Desenha a nave na tela na posição atual
        surface.blit(self.image, self.rect)