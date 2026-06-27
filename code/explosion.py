import pygame

class Explosion:
    def __init__(self, x, y):
        # Buscando as imagens para o efeito de explosão
        self.images = [pygame.image.load(f'./assets/imagens/expl{i}.png').convert_alpha() for i in range(1, 3)]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.timer = 0

    def update(self):
        self.timer += 1
        if self.timer >= 6:
            self.index += 1
            self.timer = 0
            if self.index < len(self.images):
                self.image = self.images[self.index]
            else:
                return False
        return True

    def draw(self, surface):
        surface.blit(self.image, self.rect)