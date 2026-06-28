import pygame
import sys
from code.config import WIN_WIDTH, WIN_HEIGHT, GAME_TITLE, COLOR_BLACK, COLOR_WHITE
from code.menu import Menu
from code.player import Player
from code.obstacle import Obstacle
from code.bullet import Bullet
from code.explosion import Explosion
from code.background import Background


def reset_game():
    return Player(), [Obstacle() for _ in range(4)], [], []


def main():
    pygame.init()
    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption(GAME_TITLE)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 28, bold=True)
    heart_img = pygame.transform.scale(pygame.image.load('./assets/imagens/heart.png').convert_alpha(), (30, 30))

    Menu(window).run()

    player, obstacles, bullets, explosions = reset_game()
    bg = Background()
    score = 0
    score_timer = 0
    running = True
    game_state = "PLAYING"

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if game_state == "GAME_OVER" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    player, obstacles, bullets, explosions = reset_game()
                    score = 0
                    game_state = "PLAYING"


        if game_state == "PLAYING":
            player.move()

            novo_tiro = player.shoot()
            if novo_tiro:
                bullets.append(novo_tiro)
            # -------------------------------------

            bg.move()
            score_timer += 1
            if score_timer >= 30:
                score += 1
                score_timer = 0
            difficulty_modifier = score // 100

            for b in bullets[:]:
                b.move()
                if b.rect.bottom < 0: bullets.remove(b)

            for obs in obstacles[:]:
                obs.move()
                obs.rect.y += difficulty_modifier
                if player.rect.colliderect(obs.rect):
                    player.take_damage()
                    obs.rect.y = -100
                    if player.health <= 0: game_state = "GAME_OVER"
                for b in bullets[:]:
                    if obs.is_destructible and b.rect.colliderect(obs.rect):
                        explosions.append(Explosion(obs.rect.centerx, obs.rect.centery))
                        score += 10
                        bullets.remove(b)
                        obs.rect.y = -100

            window.fill(COLOR_BLACK)
            bg.draw(window)
            player.draw(window)
            for obs in obstacles: obs.draw(window)
            for b in bullets: b.draw(window)
            for ex in explosions[:]:
                if not ex.update():
                    explosions.remove(ex)
                else:
                    ex.draw(window)

            score_text = font.render(f"SCORE: {score}", True, COLOR_WHITE)
            window.blit(score_text, (20, WIN_HEIGHT - 40))
            for i in range(player.health):
                window.blit(heart_img, (WIN_WIDTH - 40 - (i * 35), WIN_HEIGHT - 40))

        elif game_state == "GAME_OVER":
            window.fill(COLOR_BLACK)
            text = font.render("GAME OVER! Pressione [R] para reiniciar", True, COLOR_WHITE)
            window.blit(text, text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2)))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()