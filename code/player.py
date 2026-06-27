# code/player.py
import pygame
from code.config import WIN_WIDTH, WIN_HEIGHT


class Player:
    def __init__(self):
        # Carregando e redimensionando as 3 imagens de estado da nave
        self.image_full = pygame.transform.scale(pygame.image.load('./assets/imagens/nave_full.png').convert_alpha(),
                                                 (100, 100))
        self.image_dmg1 = pygame.transform.scale(pygame.image.load('./assets/imagens/nave_dmg1.png').convert_alpha(),
                                                 (100, 100))
        self.image_dmg2 = pygame.transform.scale(pygame.image.load('./assets/imagens/nave_dmg2.png').convert_alpha(),
                                                 (100, 100))

        # Atributos iniciais do jogador
        self.health = 3
        self.image = self.image_full

        # Posição e velocidade da nave
        self.rect = self.image.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT - 60))
        self.speed = 7

    def move(self):
        keys = pygame.key.get_pressed()

        # Movimentação Horizontal
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIN_WIDTH:
            self.rect.x += self.speed

        # Movimentação vertical
        if keys[pygame.K_UP] and self.rect.top > (WIN_HEIGHT // 2):
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < WIN_HEIGHT:
            self.rect.y += self.speed

    def take_damage(self):
        """Reduz a vida da nave e troca a imagem automaticamente."""
        self.health -= 1

        if self.health == 2:
            self.image = self.image_dmg1
        elif self.health == 1:
            self.image = self.image_dmg2

    def draw(self, surface):
        surface.blit(self.image, self.rect)