import pygame
import random
import os
from code.config import WIN_WIDTH, WIN_HEIGHT


class Background:
    def __init__(self):
        # Cria 100 estrelas com posições e velocidades aleatórias
        self.stars = [[random.randint(0, WIN_WIDTH), random.randint(0, WIN_HEIGHT), random.uniform(0.5, 2.0)] for _ in
                      range(100)]

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        planet_dir = os.path.join(base_dir, 'assets', 'imagens', 'Planets')

        # Carrega os 5 tipos de planetas da pasta de imagens
        self.planet_images = []
        for i in range(1, 6):
            img_path = os.path.join(planet_dir, f'planet{i}.png')
            try:
                img = pygame.image.load(img_path).convert_alpha()
                self.planet_images.append(img)
            except FileNotFoundError:
                print(f"ERRO: Não achou a imagem {img_path}")

        self.active_planets = []
        self.spawn_timer = 0

    def move(self):
        # Move as estrelas para baixo e faz elas voltarem para o topo se sumirem
        for star in self.stars:
            star[1] += star[2]
            if star[1] > WIN_HEIGHT:
                star[1] = 0
                star[0] = random.randint(0, WIN_WIDTH)

        can_spawn = True

        # Não deixa ter mais de 2 planetas ao mesmo tempo na tela
        if len(self.active_planets) >= 2:
            can_spawn = False
        else:
            # Não deixa nascer planeta novo se o anterior ainda estiver na parte de cima da tela
            for planet in self.active_planets:
                if planet[1] < WIN_HEIGHT // 2:
                    can_spawn = False

        # Se a tela estiver limpa, cria novos planetas
        if can_spawn:
            self.spawn_timer += 1
            if self.spawn_timer > 60 and random.random() < 0.02:
                if self.planet_images:
                    img = random.choice(self.planet_images)
                    x = random.randint(0, WIN_WIDTH - img.get_width())
                    y = -img.get_height()

                    speed = random.uniform(0.15, 0.3)

                    self.active_planets.append([x, y, img, speed])
                    self.spawn_timer = 0

        # Move os planetas ativos para baixo e remove os que já saíram da tela
        for planet in self.active_planets[:]:
            planet[1] += planet[3]
            if planet[1] > WIN_HEIGHT:
                self.active_planets.remove(planet)

    def draw(self, surface):
        for planet in self.active_planets:
            surface.blit(planet[2], (planet[0], planet[1]))

        # Desenha as estrelas por cima (estrelas rápidas ficam mais cinzas, as lentas ficam brancas)
        for star in self.stars:
            color = (200, 200, 200) if star[2] > 1.5 else (255, 255, 255)
            pygame.draw.circle(surface, color, (star[0], int(star[1])), int(star[2]))