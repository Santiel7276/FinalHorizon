import pygame
from code.config import WIN_WIDTH, WIN_HEIGHT
from code.bullet import Bullet  # Certifique-se de importar a classe Bullet aqui


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

        # SISTEMA DE TIRO CONTÍNUO
        self.shoot_delay = 30  # Intervalo de frames entre cada tiro
        self.shoot_cooldown = 0

    def move(self):
        keys = pygame.key.get_pressed()

        # Movimento aceitando Setas OU (or) WASD
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > 0:
            self.rect.x -= self.speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < WIN_WIDTH:
            self.rect.x += self.speed
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.top > (WIN_HEIGHT // 2):
            self.rect.y -= self.speed
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.bottom < WIN_HEIGHT:
            self.rect.y += self.speed

        # Reduz o cooldown do tiro a cada frame (se for maior que 0)
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def shoot(self):
        keys = pygame.key.get_pressed()
        # Se a barra de espaço estiver pressionada E o cooldown estiver zerado
        if keys[pygame.K_SPACE] and self.shoot_cooldown == 0:
            self.shoot_cooldown = self.shoot_delay  # Reseta o cronômetro

            # Centralizando o tiro com a nave (subtraí 2 do x porque o tiro tem 5px de largura)
            return Bullet(self.rect.centerx - 2, self.rect.top)

        return None  # Retorna nada se não for a hora de atirar

    def take_damage(self):
        self.health -= 1
        if self.health == 2:
            self.image = self.image_dmg1
        elif self.health == 1:
            self.image = self.image_dmg2

    def draw(self, surface):
        keys = pygame.key.get_pressed()
        img_rect = self.image.get_rect(center=self.rect.center)

        # Adicionado K_w para a animação do fogo também funcionar no WASD
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.fire_index = (self.fire_index + 0.3) % 4
            fire_img = self.fire_frames[int(self.fire_index)]

            # Centralizando a animação do fogo com a nave
            surface.blit(fire_img, (img_rect.centerx - 30, img_rect.centery + 10))
            surface.blit(fire_img, (img_rect.centerx - 2, img_rect.centery + 11))

        surface.blit(self.image, img_rect)