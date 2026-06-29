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

    # --- CORREÇÃO DE ÁUDIO: Aumentando de 8 para 16 canais simultâneos ---
    pygame.mixer.set_num_channels(16)

    # 1. Carregando Som da Explosão (usando caminho relativo conforme exigência)
    try:
        snd_explosion = pygame.mixer.Sound('./assets/sons/som_explosao_meteoro.mp3')
        snd_explosion.set_volume(0.8)
    except Exception as e:
        print(f"ERRO: Não carregou som da explosão. {e}")
        snd_explosion = None

    # 2. Carregando Som de Impacto (Dano)
    try:
        snd_impact = pygame.mixer.Sound('./assets/sons/som_nave_batendo.mp3')
        snd_impact.set_volume(0.9)
    except Exception as e:
        print(f"ERRO: Não carregou som de impacto. {e}")
        snd_impact = None

    # 3. Carregando Som de Vida Ganha
    try:
        snd_heal = pygame.mixer.Sound('./assets/sons/som_vida_ganha.mp3')
        snd_heal.set_volume(1.0)
    except Exception as e:
        print(f"ERRO: Não carregou som de vida ganha. {e}")
        snd_heal = None

    # 4. Carregando Música de Fundo
    try:
        pygame.mixer.music.load('./assets/sons/musica_fundo.ogg')
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(loops=-1)
    except Exception as e:
        print(f"ERRO NA MÚSICA: {e}")

    # Janela real vs render_surface auxiliar (usada para aplicar efeitos como o screen shake)
    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    render_surface = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption(GAME_TITLE)
    clock = pygame.time.Clock()

    # Carregamento de fontes com plano de fundo (fallback) caso dê erro de caminho
    try:
        font_score = pygame.font.Font('./assets/fontes/PressStart2P-Regular.ttf', 16)
        font_level_up = pygame.font.Font('./assets/fontes/PressStart2P-Regular.ttf', 24)
        font_game_over = pygame.font.Font('./assets/fontes/PressStart2P-Regular.ttf', 20)
    except FileNotFoundError:
        font_score = pygame.font.SysFont("arial", 20, bold=True)
        font_level_up = pygame.font.SysFont("arial", 32, bold=True)
        font_game_over = pygame.font.SysFont("arial", 28, bold=True)

    heart_img = pygame.transform.scale(
        pygame.image.load('./assets/imagens/heart.png').convert_alpha(), (30, 30))

    # Chama o menu principal; a execução do jogo de fato só continua se ele retornar True
    Menu(window).run()

    # Inicialização das variáveis de estado e controle de progresso do jogo
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
        # --- POLÍTICA DE EVENTOS ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Mecânica para resetar e voltar a jogar (agora serve para derrota e vitória)
            if (game_state == "GAME_OVER" or game_state == "VICTORY") and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    if player:
                        player.stop_sounds()
                    player, obstacles, bullets, explosions = reset_game()
                    score = 0
                    current_level = 0
                    game_state = "PLAYING"

        # --- LÓGICA PRINCIPAL DA GAMEPLAY ---
        if game_state == "PLAYING":
            player.move()
            novo_tiro = player.shoot()
            if novo_tiro:
                bullets.append(novo_tiro)

            bg.move()

            # Incrementa a pontuação passiva por tempo de sobrevivência (15 pontos a cada 30 frames)
            score_timer += 1
            if score_timer >= 30:
                score += 15
                score_timer = 0

            # Sistema de Progressão: Sobe de nível a cada 3000 pontos alcançados
            new_level = score // 3000
            if new_level > current_level:
                current_level = new_level
                level_up_timer = 120  # Define o tempo de exibição do alerta na tela

            # --- CONDIÇÃO DE VITÓRIA (Requisito do Trabalho) ---
            if current_level >= 4:
                game_state = "VICTORY"
                player.stop_sounds()

            difficulty_modifier = current_level

            # Atualiza e limpa projéteis fora da tela (usando list slicing [:] para evitar bugs)
            for b in bullets[:]:
                b.move()
                if b.rect.bottom < 0: bullets.remove(b)

            for obs in obstacles[:]:
                obs.move()
                obs.rect.y += difficulty_modifier  # Deixa os meteoros mais rápidos conforme o nível sobe

                # --- COLISÃO: PLAYER E METEORO (DANO) ---
                if player.rect.colliderect(obs.rect):
                    player.take_damage()

                    if snd_impact:
                        snd_impact.stop()
                        snd_impact.play()

                    obs.respawn()
                    shake_timer = 15  # Ativa a tremedeira da tela por 15 frames

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

                        # --- GANHA 1 VIDA A CADA DESTRUIÇÃO (MÁXIMO DE 4 VIDAS) ---
                        if player.health < 4:
                            player.health += 1
                            if snd_heal:
                                snd_heal.stop()
                                snd_heal.play()

            # --- DESENHO DOS GRÁFICOS ---
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

            # Placar de pontuação formatado com zeros à esquerda
            score_text = font_score.render(f"SCORE:{score:07d}", True, COLOR_WHITE)
            render_surface.blit(score_text, (20, WIN_HEIGHT - 40))

            # Renderiza os corações de vida no canto inferior direito
            for i in range(player.health):
                render_surface.blit(heart_img, (WIN_WIDTH - 40 - (i * 35), WIN_HEIGHT - 40))

            # Exibe o alerta piscante de "VELOCIDADE ++" na subida de nível
            if level_up_timer > 0:
                if level_up_timer % 10 < 5:
                    lvl_text = font_level_up.render("VELOCIDADE ++", True, (255, 255, 0))
                    render_surface.blit(lvl_text, lvl_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 4)))
                level_up_timer -= 1

            # Lógica do Screen Shake
            render_x, render_y = 0, 0
            if shake_timer > 0:
                render_x = random.randint(-4, 4)
                render_y = random.randint(-4, 4)
                shake_timer -= 1

            # Passa o conteúdo da superfície auxiliar para a janela principal com o shake
            window.fill(COLOR_BLACK)
            window.blit(render_surface, (render_x, render_y))

        # --- TELA DE GAME OVER ---
        elif game_state == "GAME_OVER":
            window.fill(COLOR_BLACK)
            text1 = font_game_over.render("GAME OVER!", True, (255, 50, 50))
            text2 = font_score.render("Pressione [R] para reiniciar", True, COLOR_WHITE)
            text3 = font_score.render(f"SCORE FINAL: {score:07d}", True, (255, 255, 0))

            window.blit(text1, text1.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 50)))
            window.blit(text2, text2.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2)))
            window.blit(text3, text3.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 50)))

        # --- TELA DE VITÓRIA ---
        elif game_state == "VICTORY":
            window.fill(COLOR_BLACK)
            text1 = font_game_over.render("VOCE VENCEU!", True, (50, 255, 50))
            text2 = font_score.render("Pressione [R] para jogar de novo", True, COLOR_WHITE)
            text3 = font_score.render("Setor limpo! Bom trabalho.", True, (255, 255, 0))

            window.blit(text1, text1.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 50)))
            window.blit(text2, text2.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2)))
            window.blit(text3, text3.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 50)))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()