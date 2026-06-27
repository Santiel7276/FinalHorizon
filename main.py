# main.py
import pygame
import sys
from code.config import WIN_WIDTH, WIN_HEIGHT, GAME_TITLE, COLOR_BLACK
from code.menu import Menu
from code.player import Player
from code.obstacle import Obstacle
from code.bullet import Bullet
from code.explosion import Explosion


def main():
    pygame.init()
    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption(GAME_TITLE)
    clock = pygame.time.Clock()

    menu = Menu(window)
    menu.run()

    player = Player()
    obstacles = [Obstacle() for _ in range(6)]
    bullets = []
    explosions = []

    running = True
    game_state = "PLAYING"

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bullets.append(Bullet(player.rect.centerx, player.rect.top))

        if game_state == "PLAYING":
            player.move()

            # Movimentação das balas e explosões
            for b in bullets[:]:
                b.move()
                if b.rect.bottom < 0: bullets.remove(b)

            # Lógica de colisões
            for obs in obstacles[:]:
                obs.move()
                if player.rect.colliderect(obs.rect):
                    player.take_damage()
                    obs.rect.y = -100
                    if player.health <= 0: game_state = "GAME_OVER"

                for b in bullets[:]:
                    if obs.is_destructible and b.rect.colliderect(obs.rect):
                        explosions.append(Explosion(obs.rect.centerx, obs.rect.centery))
                        bullets.remove(b)
                        obs.rect.y = -100

            # Desenho
            window.fill(COLOR_BLACK)
            player.draw(window)
            for obs in obstacles: obs.draw(window)
            for b in bullets: b.draw(window)
            for ex in explosions[:]:
                if not ex.update():
                    explosions.remove(ex)
                else:
                    ex.draw(window)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()