import pygame


class Explosion:
    def __init__(self, x, y):
        # Carrega a sequência de imagens para fazer a animacao
        self.images = [pygame.image.load(f'./assets/imagens/expl{i}.png').convert_alpha() for i in range(1, 3)]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(x, y))  # Centraliza a explosão onde houve o impacto
        self.timer = 0

    def update(self):
        """Atualiza os frames da animação. Retorna False quando a animação termina."""
        self.timer += 1
        # Controla a velocidade da animação
        if self.timer >= 5:
            self.index += 1
            self.timer = 0

            # Se ainda tiver frames, o desenho avança, caso contrário, ele é apagado
            if self.index < len(self.images):
                self.image = self.images[self.index]
            else:
                return False
        return True

    def draw(self, surface):
        """Desenha o frame atual da explosão na superfície de renderização."""
        surface.blit(self.image, self.rect)