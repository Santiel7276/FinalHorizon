import pygame
from code.config import WIN_WIDTH, WIN_HEIGHT
from code.bullet import Bullet


class Player:
    def __init__(self):
        self.image_full = pygame.transform.scale(pygame.image.load('./assets/imagens/nave_full.png').convert_alpha(),
                                                 (100, 100))
        self.image_dmg1 = pygame.transform.scale(pygame.image.load('./assets/imagens/nave_dmg1.png').convert_alpha(),
                                                 (100, 100))
        self.image_dmg2 = pygame.transform.scale(pygame.image.load('./assets/imagens/nave_dmg2.png').convert_alpha(),
                                                 (100, 100))

        fire_size = (30, 40)
        self.fire_frames = [
            pygame.transform.scale(pygame.image.load('./assets/imagens/fire.png').convert_alpha(), fire_size),
            pygame.transform.scale(pygame.image.load('./assets/imagens/fire2.png').convert_alpha(), fire_size),
            pygame.transform.scale(pygame.image.load('./assets/imagens/fire3.png').convert_alpha(), fire_size),
            pygame.transform.scale(pygame.image.load('./assets/imagens/fire4.png').convert_alpha(), fire_size)
        ]

        self.health = 3
        self.max_health = 4
        self.image = self.image_full
        self.speed = 7
        self.fire_index = 0.0
        self.rect = pygame.Rect(0, 0, 35, 45)
        self.rect.center = (WIN_WIDTH // 2, WIN_HEIGHT - 60)
        self.shoot_delay = 30
        self.shoot_cooldown = 0

        self.snd_shoot = pygame.mixer.Sound('./assets/sons/som_disparo.mp3')
        self.snd_shoot.set_volume(0.2)
        self.snd_thrust = pygame.mixer.Sound('./assets/sons/som_nave_acelerando.mp3')
        self.snd_thrust.set_volume(0.15)
        self.snd_idle = pygame.mixer.Sound('./assets/sons/som_nave.mp3')
        self.snd_idle.set_volume(0.05)
        self.thrust_channel = pygame.mixer.Channel(1)
        self.idle_channel = pygame.mixer.Channel(2)
        self.idle_channel.play(self.snd_idle, loops=-1)

    def move(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > 0: self.rect.x -= self.speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < WIN_WIDTH: self.rect.x += self.speed
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.top > 0: self.rect.y -= self.speed
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.bottom < WIN_HEIGHT: self.rect.y += self.speed

        if (keys[pygame.K_UP] or keys[pygame.K_w]):
            if not self.thrust_channel.get_busy(): self.thrust_channel.play(self.snd_thrust, loops=-1)
        else:
            self.thrust_channel.stop()
        if self.shoot_cooldown > 0: self.shoot_cooldown -= 1

    def shoot(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.shoot_cooldown == 0:
            self.shoot_cooldown = self.shoot_delay
            self.snd_shoot.stop()
            self.snd_shoot.play()
            return Bullet(self.rect.centerx - 2, self.rect.top)
        return None

    def update_visuals(self):
        if self.health >= 3:
            self.image = self.image_full
        elif self.health == 2:
            self.image = self.image_dmg1
        elif self.health <= 1:
            self.image = self.image_dmg2

    def take_damage(self):
        if self.health > 0:
            self.health -= 1
            self.update_visuals()

    def heal(self):
        if self.health < self.max_health:
            self.health += 1
            self.update_visuals()

    def draw(self, surface):
        keys = pygame.key.get_pressed()
        img_rect = self.image.get_rect(center=self.rect.center)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.fire_index = (self.fire_index + 0.3) % 4
            fire_img = self.fire_frames[int(self.fire_index)]
            surface.blit(fire_img, (img_rect.centerx - 30, img_rect.centery + 10))
            surface.blit(fire_img, (img_rect.centerx - 2, img_rect.centery + 11))
        surface.blit(self.image, img_rect)

    def stop_sounds(self):
        self.idle_channel.stop()
        self.thrust_channel.stop()