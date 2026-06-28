import pygame
import sys
import os
from code.config import WIN_WIDTH, WIN_HEIGHT, GAME_TITLE, COLOR_BLACK, COLOR_WHITE, COLOR_GRAY
from code.background import Background


class Menu:
    def __init__(self, window):
        self.window = window
        self.bg = Background()

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        font_path = os.path.join(base_dir, 'assets', 'fontes', 'PressStart2P-Regular.ttf')

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

        self.state = "MAIN"
        self.selected_index = 0

    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            self.bg.move()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if self.state == "MAIN":
                        if event.key == pygame.K_UP or event.key == pygame.K_w:
                            self.selected_index = 0
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            self.selected_index = 1

                        elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            if self.selected_index == 0:
                                return True
                            elif self.selected_index == 1:
                                self.state = "CONTROLS"

                    elif self.state == "CONTROLS":
                        if event.key == pygame.K_ESCAPE:
                            self.state = "MAIN"

            self.window.fill(COLOR_BLACK)
            self.bg.draw(self.window)

            if self.state == "MAIN":
                self.draw_main_menu()
            elif self.state == "CONTROLS":
                self.draw_controls()

            pygame.display.flip()
            clock.tick(60)

    def draw_main_menu(self):
        title_shadow = self.font_title.render(GAME_TITLE, True, (40, 40, 40))
        title = self.font_title.render(GAME_TITLE, True, COLOR_WHITE)

        title_rect = title.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 3))

        self.window.blit(title_shadow, (title_rect.x + 4, title_rect.y + 4))
        self.window.blit(title, title_rect)

        color_start = (255, 255, 0) if self.selected_index == 0 else COLOR_WHITE
        color_controls = (255, 255, 0) if self.selected_index == 1 else COLOR_WHITE

        inst1 = self.font_inst.render("Iniciar Jogo", True, color_start)
        inst2 = self.font_inst.render("Como Jogar", True, color_controls)

        self.window.blit(inst1, inst1.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 50)))
        self.window.blit(inst2, inst2.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 100)))

    def draw_controls(self):
        title = self.font_title.render("COMO JOGAR", True, COLOR_WHITE)
        self.window.blit(title, title.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 6)))

        # --- SEÇÃO 1: OBJETIVO E DICAS ---
        obj1 = self.font_small.render("OBJETIVO: Sobreviva o maximo de tempo que puder!", True, COLOR_WHITE)
        self.window.blit(obj1, obj1.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 80)))

        # Renderizando a linha da DICA em 3 partes separadas para aplicar cores diferentes
        dica_parte1 = self.font_small.render("DICA: ", True, (255, 255, 0))
        dica_parte2 = self.font_small.render("Apenas os meteoros que ", True, COLOR_WHITE)
        dica_parte3 = self.font_small.render("PISCAM", True, (255, 255, 0))

        # Calculando a largura total para centralizar a frase montada
        largura_total = dica_parte1.get_width() + dica_parte2.get_width() + dica_parte3.get_width()
        pos_x_inicial = (WIN_WIDTH // 2) - (largura_total // 2)
        pos_y_linha2 = (WIN_HEIGHT // 2) - 40 - (dica_parte1.get_height() // 2)

        # Desenhando as 3 partes uma colada na outra
        self.window.blit(dica_parte1, (pos_x_inicial, pos_y_linha2))
        self.window.blit(dica_parte2, (pos_x_inicial + dica_parte1.get_width(), pos_y_linha2))
        self.window.blit(dica_parte3, (pos_x_inicial + dica_parte1.get_width() + dica_parte2.get_width(), pos_y_linha2))

        # Terceira linha
        obj3 = self.font_small.render("podem ser destruidos com seus tiros.", True, COLOR_WHITE)
        self.window.blit(obj3, obj3.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 10)))

        # --- SEÇÃO 2: COMANDOS ---
        # Removido o COLOR_GRAY e adicionado COLOR_WHITE para ganhar destaque
        inst1 = self.font_small.render("WASD ou Setas - Mover a Nave", True, COLOR_WHITE)
        inst2 = self.font_small.render("Segurar Espaco - Atirar", True, COLOR_WHITE)

        # Mantive o botão ESC cinza para ele ficar sutil no rodapé e não competir com os comandos principais
        inst3 = self.font_small.render("ESC - Voltar ao Menu", True, COLOR_GRAY)

        self.window.blit(inst1, inst1.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 60)))
        self.window.blit(inst2, inst2.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 100)))

        self.window.blit(inst3, inst3.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT - 60)))