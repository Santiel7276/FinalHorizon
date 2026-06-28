import pygame
import sys
import os  # Importado para garantir que o caminho da fonte seja encontrado sempre
from code.config import WIN_WIDTH, WIN_HEIGHT, GAME_TITLE, COLOR_BLACK, COLOR_WHITE, COLOR_GRAY
from code.background import Background


class Menu:
    def __init__(self, window):
        self.window = window
        self.bg = Background()  # Instancia as estrelas para o fundo do menu

        # Descobre o caminho absoluto da pasta raiz do projeto
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # AQUI ESTAVA O ERRO: O nome do arquivo precisa ser exatamente o da imagem
        font_path = os.path.join(base_dir, 'assets', 'fontes', 'PressStart2P-Regular.ttf')

        # Sistema seguro de fontes: tenta carregar a fonte customizada.
        try:
            # Reduzi o tamanho para 48 porque essa fonte é grande
            self.font_title = pygame.font.Font(font_path, 48)
        except FileNotFoundError:
            print(f"ERRO: Não achou a fonte em {font_path}")
            self.font_title = pygame.font.SysFont("courier", 64, bold=True)

        try:
            # Reduzi o tamanho para 16
            self.font_inst = pygame.font.Font(font_path, 16)
        except FileNotFoundError:
            self.font_inst = pygame.font.SysFont("courier", 24)

        # Controle de estado do menu
        self.state = "MAIN"

    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            self.bg.move()  # Anima o fundo no menu

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    # Lógica de navegação do menu
                    if self.state == "MAIN":
                        if event.key == pygame.K_SPACE:
                            return True  # Inicia o jogo
                        elif event.key == pygame.K_c:
                            self.state = "CONTROLS"  # Muda para a tela de comandos
                    elif self.state == "CONTROLS":
                        if event.key == pygame.K_v:
                            self.state = "MAIN"  # Volta para a tela principal


            self.window.fill(COLOR_BLACK)
            self.bg.draw(self.window)

            if self.state == "MAIN":
                self.draw_main_menu()
            elif self.state == "CONTROLS":
                self.draw_controls()

            pygame.display.flip()
            clock.tick(60)

    def draw_main_menu(self):
        # Efeito de sombra no título
        title_shadow = self.font_title.render(GAME_TITLE, True, (40, 40, 40))
        title = self.font_title.render(GAME_TITLE, True, COLOR_WHITE)

        title_rect = title.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 3))

        self.window.blit(title_shadow, (title_rect.x + 4, title_rect.y + 4))
        self.window.blit(title, title_rect)

        # Opções do menu
        inst1 = self.font_inst.render("Pressione [ ESPACO ] para Iniciar", True, COLOR_WHITE)
        inst2 = self.font_inst.render("Pressione [ C ] para Comandos", True, COLOR_GRAY)

        self.window.blit(inst1, inst1.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 50)))
        self.window.blit(inst2, inst2.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 100)))

    def draw_controls(self):
        # Cabeçalho da tela de comandos
        title = self.font_title.render("COMANDOS", True, COLOR_WHITE)
        self.window.blit(title, title.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 4)))

        # Lista de botões alinhada
        inst1 = self.font_inst.render("Setas Esq/Dir - Mover Nave", True, COLOR_GRAY)
        inst2 = self.font_inst.render("Seta Cima - Ativar Propulsor", True, COLOR_GRAY)
        inst3 = self.font_inst.render("Espaco - Atirar", True, COLOR_GRAY)

        # Opção de voltar em destaque
        back = self.font_inst.render("Pressione [ V ] para Voltar", True, COLOR_WHITE)

        self.window.blit(inst1, inst1.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 20)))
        self.window.blit(inst2, inst2.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 20)))
        self.window.blit(inst3, inst3.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 60)))

        self.window.blit(back, back.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT - 100)))