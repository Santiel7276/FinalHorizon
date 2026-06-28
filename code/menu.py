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

        self.state = "MAIN"

        # Variável para rastrear a opção selecionada no menu principal
        # 0 = Iniciar Jogo, 1 = Comandos
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
                        # Navegação com as setas
                        if event.key == pygame.K_UP:
                            self.selected_index = 0
                        elif event.key == pygame.K_DOWN:
                            self.selected_index = 1

                            # Confirmação com Enter ou Espaço
                        elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            if self.selected_index == 0:
                                return True  # Inicia o jogo
                            elif self.selected_index == 1:
                                self.state = "CONTROLS"  # Abre a tela de comandos

                    elif self.state == "CONTROLS":
                        # O ESC serve para voltar
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
        # Título
        title_shadow = self.font_title.render(GAME_TITLE, True, (40, 40, 40))
        title = self.font_title.render(GAME_TITLE, True, COLOR_WHITE)

        title_rect = title.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 3))

        self.window.blit(title_shadow, (title_rect.x + 4, title_rect.y + 4))
        self.window.blit(title, title_rect)

        # Define as cores com base na opção selecionada
        color_start = (255, 255, 0) if self.selected_index == 0 else COLOR_WHITE
        color_controls = (255, 255, 0) if self.selected_index == 1 else COLOR_WHITE

        # Renderiza os textos com as novas cores
        inst1 = self.font_inst.render("Iniciar Jogo", True, color_start)
        inst2 = self.font_inst.render("Comandos", True, color_controls)

        self.window.blit(inst1, inst1.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 50)))
        self.window.blit(inst2, inst2.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 100)))

    def draw_controls(self):
        title = self.font_title.render("COMANDOS", True, COLOR_WHITE)
        self.window.blit(title, title.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 4)))

        # Lista de botões padronizada
        inst1 = self.font_inst.render("Setas Esq/Dir - Mover Nave", True, COLOR_GRAY)
        inst2 = self.font_inst.render("Seta Cima - Ativar Propulsor", True, COLOR_GRAY)
        inst3 = self.font_inst.render("Espaco - Atirar", True, COLOR_GRAY)
        inst4 = self.font_inst.render("ESC - Voltar ao Menu", True, COLOR_GRAY)  # Adicionado na lista

        # Ajustei o espaçamento Y para caber os 4 itens direitinho
        self.window.blit(inst1, inst1.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 40)))
        self.window.blit(inst2, inst2.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 10)))
        self.window.blit(inst3, inst3.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 60)))
        self.window.blit(inst4, inst4.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 110)))