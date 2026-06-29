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
    """Reinicia o estado original do player e dos objetos do jogo."""
    return Player(), [Obstacle() for _ in range(4)], [], []


def main():
    pygame.init()
    pygame.mixer.init()

    # Aumentando o número de canais de audio
    pygame.mixer.set_num_channels(16)

    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Som da explosão
    explosao_path = os.path.join(base_dir, 'assets', 'sons', 'som_explosao_meteoro.mp3')
    try:
        snd_explosion = pygame.mixer.Sound(explosao_path)
        snd_explosion.set_volume(0.8)
    except Exception as e:
        print(f"ERRO: Não carregou som da explosão. {e}")
        snd_explosion = None

    # Som do impacto
    impacto_path = os.path.join(base_dir, 'assets', 'sons', 'som_nave_batendo.mp3')
    try:
        snd_impact = pygame.mixer.Sound(impacto_path)
        snd_impact.set_volume(0.9)
    except Exception as e:
        print(f"ERRO: Não carregou som de impacto. {e}")
        snd_impact = None

    # Efeito sonoro de quando o player ganhar 1 vida
    vida_path = os.path.join(base_dir, 'assets', 'sons', 'som_vida_ganha.mp3')
    try:
        snd_heal = pygame.mixer.Sound(vida_path)
        snd_heal.set_volume(1.0)
    except Exception as e:
        print(f"ERRO: Não carregou som de vida ganha. {e}")
        snd_heal = None

    # Música de fundo
    musica_path = os.path.join(base_dir, 'assets', 'sons', 'musica_fundo.ogg')
    try:
        pygame.mixer.music.load(musica_path)
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(loops=-1)
    except Exception as e:
        print(f"ERRO NA MÚSICA: {e}")

    # Efeito para a tela tremer
    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    render_surface = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption(GAME_TITLE)
    clock = pygame.time.Clock()

    # Carregando as fontes
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

    # Chama o menu principal
    Menu(window).run()

    # Inicialização das variáveis
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
        # EVENTOS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Mecânica para resetar e voltar a jogar apertando R quando der game over
            if game_state == "GAME_OVER" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    if player:
                        player.stop_sounds()
                    player, obstacles, bullets, explosions = reset_game()
                    score = 0
                    current_level = 0
                    game_state = "PLAYING"

        # Lógica da gameplay
        if game_state == "PLAYING":
            player.move()
            novo_tiro = player.shoot()
            if novo_tiro:
                bullets.append(novo_tiro)

            bg.move()

            # Pontuação
            score_timer += 1
            if score_timer >= 30:
                score += 15
                score_timer = 0

            # Dificuldade do jogo (aumenta a cada 3000  pontos)
            new_level = score // 3000
            if new_level > current_level:
                current_level = new_level
                level_up_timer = 120

            difficulty_modifier = current_level

            # Atualiza e limpa projéteis fora da tela
            for b in bullets[:]:
                b.move()
                if b.rect.bottom < 0: bullets.remove(b)

            for obs in obstacles[:]:
                obs.move()
                obs.rect.y += difficulty_modifier # Deixa os meteoros mais rápidos conforme o nível sobe

                # Colisão player e meteoro
                if player.rect.colliderect(obs.rect):
                    player.take_damage()

                    if snd_impact:
                        snd_impact.stop()
                        snd_impact.play()

                    obs.respawn()
                    shake_timer = 15 # efeito de tremor na tela

                    if player.health <= 0:
                        game_state = "GAME_OVER"
                        player.stop_sounds()

                # -Colisão bala e meteoro
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

                        # Sistema para ganhar vida por meteoro destruído (limite de 4 vidas)
                        if player.health < 4:
                            player.health += 1
                            if snd_heal:
                                snd_heal.stop()
                                snd_heal.play()

           #Desenho dos gráficos
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

            # Placar de pontuação
            score_text = font_score.render(f"SCORE:{score:07d}", True, COLOR_WHITE)
            render_surface.blit(score_text, (20, WIN_HEIGHT - 40))

            # Corações de vida
            for i in range(player.health):
                render_surface.blit(heart_img, (WIN_WIDTH - 40 - (i * 35), WIN_HEIGHT - 40))

            # Exibe o alerta piscante de "VELOCIDADE ++" quando subir de nível
            if level_up_timer > 0:
                if level_up_timer % 10 < 5:
                    lvl_text = font_level_up.render("VELOCIDADE ++", True, (255, 255, 0))
                    render_surface.blit(lvl_text, lvl_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 4)))
                level_up_timer -= 1

            # screen shake
            render_x, render_y = 0, 0
            if shake_timer > 0:
                render_x = random.randint(-4, 4)
                render_y = random.randint(-4, 4)
                shake_timer -= 1

            window.fill(COLOR_BLACK)
            window.blit(render_surface, (render_x, render_y))

        # tela game over
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