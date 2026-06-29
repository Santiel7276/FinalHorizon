import pygame
import sys
import os
from code.config import WIN_WIDTH, WIN_HEIGHT, GAME_TITLE, COLOR_BLACK, COLOR_WHITE, COLOR_GRAY
from code.background import Background


class Menu:
    def __init__(self, window):
        self.window = window
        self.bg = Background()

        # Garante o caminho correto para os assets, independente de onde o script principal foi chamado
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        font_path = os.path.join(base_dir, 'assets', 'fontes', 'PressStart2P-Regular.ttf')

        # Carrega a fonte principal do jogo ou usa uma padrão do sistema
        try:
            self.font_title = pygame.font.Font(font_path, 52)
        except FileNotFoundError:
            print(f"ERRO: Não achou a fonte em {font_path}")
            self.font_title = pygame.font.SysFont("courier", 52, bold=True)

        try:
            self.font_inst = pygame.font.Font(font_path, 24)
        except FileNotFoundError:
            self.font_inst = pygame.font.SysFont("courier", 24)

        try:
            self.font_small = pygame.font.Font(font_path, 14)
        except FileNotFoundError:
            self.font_small = pygame.font.SysFont("courier", 14)

        # Controla as telas do menu e qual opção está selecionada
        self.state = "MAIN"
        self.selected_index = 0

    def run(self):
        running = True
        clock = pygame.time.Clock()

        # Game loop exclusivo da tela de menu
        while running:
            self.bg.move() # Mantém o fundo se movendo

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    # Lógica de navegação no menu principal
                    if self.state == "MAIN":
                        if event.key == pygame.K_UP or event.key == pygame.K_w:
                            self.selected_index = 0
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            self.selected_index = 1

                        elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            if self.selected_index == 0:
                                return True # Sai do menu e inicia a gameplay no main.py
                            elif self.selected_index == 1:
                                self.state = "CONTROLS" # Muda para a tela de instruções

                    # Voltar para o menu principal
                    elif self.state == "CONTROLS":
                        if event.key == pygame.K_ESCAPE:
                            self.state = "MAIN"

            # Renderização de acordo com o estado da tela
            self.window.fill(COLOR_BLACK)
            self.bg.draw(self.window)

            if self.state == "MAIN":
                self.draw_main_menu()
            elif self.state == "CONTROLS":
                self.draw_controls()

            pygame.display.flip()
            clock.tick(60)

    def draw_main_menu(self):
        # Efeito no título
        title_shadow = self.font_title.render(GAME_TITLE, True, (40, 40, 40))
        title = self.font_title.render(GAME_TITLE, True, COLOR_WHITE)

        title_rect = title.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 3))

        self.window.blit(title_shadow, (title_rect.x + 4, title_rect.y + 4))
        self.window.blit(title, title_rect)

        # Destaca em amarelo a opção que o player estiver
        color_start = (255, 255, 0) if self.selected_index == 0 else COLOR_WHITE
        color_controls = (255, 255, 0) if self.selected_index == 1 else COLOR_WHITE

        inst1 = self.font_inst.render("Iniciar Jogo", True, color_start)
        inst2 = self.font_inst.render("Como Jogar", True, color_controls)

        self.window.blit(inst1, inst1.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 50)))
        self.window.blit(inst2, inst2.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 100)))

    def draw_controls(self):
        title = self.font_title.render("COMO JOGAR", True, COLOR_WHITE)
        self.window.blit(title, title.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 6)))

        # objetivo e dicas
        obj1 = self.font_small.render("OBJETIVO: Alcance 12.000 Pontos para VENCER!", True, (50, 255, 255))
        self.window.blit(obj1, obj1.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 80)))

        dica_parte1 = self.font_small.render("DICA: ", True, (255, 255, 0))
        dica_parte2 = self.font_small.render("Apenas os meteoros que ", True, COLOR_WHITE)
        dica_parte3 = self.font_small.render("PISCAM", True, (255, 255, 0))

        largura_total = dica_parte1.get_width() + dica_parte2.get_width() + dica_parte3.get_width()
        pos_x_inicial = (WIN_WIDTH // 2) - (largura_total // 2)
        pos_y_linha2 = (WIN_HEIGHT // 2) - 40 - (dica_parte1.get_height() // 2)

        self.window.blit(dica_parte1, (pos_x_inicial, pos_y_linha2))
        self.window.blit(dica_parte2, (pos_x_inicial + dica_parte1.get_width(), pos_y_linha2))
        self.window.blit(dica_parte3, (pos_x_inicial + dica_parte1.get_width() + dica_parte2.get_width(), pos_y_linha2))
        obj3 = self.font_small.render("podem ser destruidos com seus tiros.", True, COLOR_WHITE)
        self.window.blit(obj3, obj3.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 10)))
        obj4 = self.font_small.render("Destruir um deles te da 1 VIDA!", True, (50, 255, 50))
        self.window.blit(obj4, obj4.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 20)))
        inst1 = self.font_small.render("WASD ou Setas - Mover a Nave", True, COLOR_WHITE)
        inst2 = self.font_small.render("Segurar Espaco - Atirar", True, COLOR_WHITE)
        inst3 = self.font_small.render("ESC - Voltar ao Menu", True, COLOR_GRAY)
        self.window.blit(inst1, inst1.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 80)))
        self.window.blit(inst2, inst2.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 120)))
        self.window.blit(inst3, inst3.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT - 60)))