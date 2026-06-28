import pygame
from code.config import WIN_WIDTH, WIN_HEIGHT


class Player:
    def __init__(self):
        # Carregando as imagens da nave
        self.image_full = pygame.transform.scale(pygame.image.load('./assets/imagens/nave_full.png').convert_alpha(),
                                                 (100, 100))
        self.image_dmg1 = pygame.transform.scale(pygame.image.load('./assets/imagens/nave_dmg1.png').convert_alpha(),
                                                 (100, 100))
        self.image_dmg2 = pygame.transform.scale(pygame.image.load('./assets/imagens/nave_dmg2.png').convert_alpha(),
                                                 (100, 100))

        # Definindo o tamanho da chama de acordo com a velocidade da nave
        fire_size = (30, 40)
        self.fire_frames = [
            pygame.transform.scale(pygame.image.load('./assets/imagens/fire.png').convert_alpha(), fire_size),
            pygame.transform.scale(pygame.image.load('./assets/imagens/fire2.png').convert_alpha(), fire_size),
            pygame.transform.scale(pygame.image.load('./assets/imagens/fire3.png').convert_alpha(), fire_size),
            pygame.transform.scale(pygame.image.load('./assets/imagens/fire4.png').convert_alpha(), fire_size)
        ]

        self.health = 3
        self.image = self.image_full
        self.speed = 7
        self.fire_index = 0.0
        self.rect = pygame.Rect(0, 0, 60, 60)
        self.rect.center = (WIN_WIDTH // 2, WIN_HEIGHT - 60)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0: self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIN_WIDTH: self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > (WIN_HEIGHT // 2): self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < WIN_HEIGHT: self.rect.y += self.speed

    def take_damage(self):
        self.health -= 1
        if self.health == 2:
            self.image = self.image_dmg1
        elif self.health == 1:
            self.image = self.image_dmg2

    def draw(self, surface):
        keys = pygame.key.get_pressed()
        img_rect = self.image.get_rect(center=self.rect.center)

        if keys[pygame.K_UP]:
            self.fire_index = (self.fire_index + 0.3) % 4
            fire_img = self.fire_frames[int(self.fire_index)]

            # Centralizando a animação do fogo com a nave
            surface.blit(fire_img, (img_rect.centerx - 30, img_rect.centery + 10))
            surface.blit(fire_img, (img_rect.centerx - 2, img_rect.centery + 11))

        surface.blit(self.image, img_rect)