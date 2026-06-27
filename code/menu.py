# code/menu.py
import pygame
from code.config import WIN_WIDTH, WIN_HEIGHT, GAME_TITLE, COLOR_BLACK, COLOR_WHITE, COLOR_GRAY


class Menu:
    def __init__(self, window):
        self.window = window
        #
        self.font_title = pygame.font.SysFont("arial", 48, bold=True)
        self.font_inst = pygame.font.SysFont("arial", 24)

    def run(self):
        #
        running = True
        while running:
            #
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()  #

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return  #

            #
            self.window.fill(COLOR_BLACK)

            #
            title = self.font_title.render(GAME_TITLE, True, COLOR_WHITE)
            title_rect = title.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 3))
            self.window.blit(title, title_rect)

            #
            inst1 = self.font_inst.render("COMANDOS DE CONTROLE:", True, COLOR_GRAY)
            inst2 = self.font_inst.render("Setas Esquerda / Direita  -  Mover a Nave", True, COLOR_GRAY)
            inst3 = self.font_inst.render("Pressione [ ESPAÇO ] para Iniciar", True, COLOR_WHITE)

            self.window.blit(inst1, inst1.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2)))
            self.window.blit(inst2, inst2.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 40)))
            self.window.blit(inst3, inst3.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 120)))

            #
            pygame.display.flip()