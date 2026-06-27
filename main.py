# main.py
import pygame
import sys
from code.config import WIN_WIDTH, WIN_HEIGHT, GAME_TITLE, COLOR_BLACK, COLOR_WHITE
from code.menu import Menu
from code.player import Player
from code.obstacle import Obstacle


def main():
    pygame.init()
    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption(GAME_TITLE)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 36, bold=True)


    menu = Menu(window)
    menu.run()

    player = Player()

    obstacles = []
    for _ in range(6):
        obstacles.append(Obstacle())

    score = 0
    running = True
    game_state = "PLAYING"


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if game_state == "PLAYING":
            player.move()


            for obs in obstacles:
                if obs.move():
                    score += 1

                if player.rect.colliderect(obs.rect):
                    game_state = "GAME_OVER"

            if score >= 20:
                game_state = "VICTORY"

            window.fill(COLOR_BLACK)
            player.draw(window)
            for obs in obstacles:
                obs.draw(window)

            score_text = font.render(f"Desvios: {score} / 20", True, COLOR_WHITE)
            window.blit(score_text, (20, 20))

        # Telas de Fim de Jogo
        elif game_state == "GAME_OVER":
            window.fill((40, 5, 5))  # Tela fica avermelhada
            text = font.render("GAME OVER! A nave foi destruída.", True, COLOR_WHITE)
            window.blit(text, text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2)))

        elif game_state == "VICTORY":
            window.fill((5, 40, 5))
            text = font.render("VITÓRIA! Você escapou!", True, COLOR_WHITE)
            window.blit(text, text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2)))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()