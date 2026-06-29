import pygame
import sys
import os
import random
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
    pygame.mixer.init()

    # --- CORREÇÃO DE ÁUDIO: Aumentando de 8 para 16 canais simultâneos ---
    pygame.mixer.set_num_channels(16)

    base_dir = os.path.dirname(os.path.abspath(__file__))

    # 1. Carregando Som da Explosão
    explosao_path = os.path.join(base_dir, 'assets', 'sons', 'som_explosao_meteoro.mp3')
    try:
        snd_explosion = pygame.mixer.Sound(explosao_path)
        snd_explosion.set_volume(0.8)
    except Exception as e:
        print(f"ERRO: Não carregou som da explosão. {e}")
        snd_explosion = None

    # 2. Carregando Som de Impacto (Dano)
    impacto_path = os.path.join(base_dir, 'assets', 'sons', 'som_nave_batendo.mp3')
    try:
        snd_impact = pygame.mixer.Sound(impacto_path)
        snd_impact.set_volume(0.9)
    except Exception as e:
        print(f"ERRO: Não carregou som de impacto. {e}")
        snd_impact = None

    # 3. Carregando Som de Vida Ganha
    vida_path = os.path.join(base_dir, 'assets', 'sons', 'som_vida_ganha.mp3')
    try:
        snd_heal = pygame.mixer.Sound(vida_path)
        snd_heal.set_volume(1.0)
    except Exception as e:
        print(f"ERRO: Não carregou som de vida ganha. {e}")
        snd_heal = None

    # 4. Carregando Música de Fundo
    musica_path = os.path.join(base_dir, 'assets', 'sons', 'musica_fundo.ogg')
    try:
        pygame.mixer.music.load(musica_path)
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(loops=-1)
    except Exception as e:
        print(f"ERRO NA MÚSICA: {e}")

    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    render_surface = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption(GAME_TITLE)
    clock = pygame.time.Clock()

    font_path = os.path.join(base_dir, 'assets', 'fontes', 'PressStart2P-Regular.ttf')
    try:
        font_score = pygame.font.Font(font_path, 16)
        font_level_up = pygame.font.Font(font_path, 24)
        font_game_over = pygame.font.Font(font_path, 20)
    except FileNotFoundError:
        font_score = pygame.font.SysFont("arial", 20, bold=True)
        font_level_up = pygame.font.SysFont("arial", 32, bold=True)
        font_game_over = pygame.font.SysFont("arial", 28, bold=True)

    heart_img = pygame.transform.scale(
        pygame.image.load(os.path.join(base_dir, 'assets', 'imagens', 'heart.png')).convert_alpha(), (30, 30))

    Menu(window).run()

    player, obstacles, bullets, explosions = reset_game()
    bg = Background()
    score = 0
    score_timer = 0
    current_level = 0
    level_up_timer = 0
    shake_timer = 0

    running = True
    game_state = "PLAYING"

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if game_state == "GAME_OVER" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    if player:
                        player.stop_sounds()
                    player, obstacles, bullets, explosions = reset_game()
                    score = 0
                    current_level = 0
                    game_state = "PLAYING"

        if game_state == "PLAYING":
            player.move()
            novo_tiro = player.shoot()
            if novo_tiro:
                bullets.append(novo_tiro)

            bg.move()

            score_timer += 1
            if score_timer >= 30:
                score += 15
                score_timer = 0

            new_level = score // 3000
            if new_level > current_level:
                current_level = new_level
                level_up_timer = 120

            difficulty_modifier = current_level

            for b in bullets[:]:
                b.move()
                if b.rect.bottom < 0: bullets.remove(b)

            for obs in obstacles[:]:
                obs.move()
                obs.rect.y += difficulty_modifier

                # --- COLISÃO: PLAYER E METEORO (DANO) ---
                if player.rect.colliderect(obs.rect):
                    player.take_damage()

                    if snd_impact:
                        snd_impact.stop()
                        snd_impact.play()

                    obs.respawn()
                    shake_timer = 15

                    if player.health <= 0:
                        game_state = "GAME_OVER"
                        player.stop_sounds()

                        # --- COLISÃO: BALA E METEORO (DESTRUIÇÃO) ---
                for b in bullets[:]:
                    if obs.is_destructible and b.rect.colliderect(obs.rect):
                        explosions.append(Explosion(obs.rect.centerx, obs.rect.centery))
                        score += 500
                        bullets.remove(b)
                        obs.respawn()
                        shake_timer = 5

                        if snd_explosion:
                            snd_explosion.stop()
                            snd_explosion.play()

                            # --- CHANCE DE GANHAR VIDA (20% DE CHANCE) ---
                        if random.random() < 0.20:
                            if player.health < player.max_health:
                                player.heal()
                                if snd_heal:
                                    snd_heal.stop()
                                    snd_heal.play()

            render_surface.fill(COLOR_BLACK)
            bg.draw(render_surface)
            player.draw(render_surface)
            for obs in obstacles: obs.draw(render_surface)
            for b in bullets: b.draw(render_surface)
            for ex in explosions[:]:
                if not ex.update():
                    explosions.remove(ex)
                else:
                    ex.draw(render_surface)

            score_text = font_score.render(f"SCORE:{score:07d}", True, COLOR_WHITE)
            render_surface.blit(score_text, (20, WIN_HEIGHT - 40))

            # Desenha os corações baseados na vida atual (agora pode ir até 4)
            for i in range(player.health):
                render_surface.blit(heart_img, (WIN_WIDTH - 40 - (i * 35), WIN_HEIGHT - 40))

            if level_up_timer > 0:
                if level_up_timer % 10 < 5:
                    lvl_text = font_level_up.render("VELOCIDADE ++", True, (255, 255, 0))
                    render_surface.blit(lvl_text, lvl_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 4)))
                level_up_timer -= 1

            render_x, render_y = 0, 0
            if shake_timer > 0:
                render_x = random.randint(-4, 4)
                render_y = random.randint(-4, 4)
                shake_timer -= 1

            window.fill(COLOR_BLACK)
            window.blit(render_surface, (render_x, render_y))

        elif game_state == "GAME_OVER":
            window.fill(COLOR_BLACK)
            text1 = font_game_over.render("GAME OVER!", True, (255, 50, 50))
            text2 = font_score.render("Pressione [R] para reiniciar", True, COLOR_WHITE)
            text3 = font_score.render(f"SCORE FINAL: {score:07d}", True, (255, 255, 0))

            window.blit(text1, text1.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 50)))
            window.blit(text2, text2.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2)))
            window.blit(text3, text3.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 50)))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()