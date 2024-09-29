
import pygame
import random
import sys

largura = 1000
altura = 1000

def minigame_reflexo():
    global malwares_capturados

    # Posicionamento inicial do malware
    malware_rect = malware_imagem.get_rect()
    malware_rect.x = random.randint(0, largura - 50)
    malware_rect.y = random.randint(0, altura - 50)

    tempo_inicio = pygame.time.get_ticks()
    jogo_em_andamento = True

    while jogo_em_andamento:
        # Verificar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if malware_rect.collidepoint(evento.pos):
                    malwares_capturados += 1
                    # Reposicionar malware
                    malware_rect.x = random.randint(0, LARGURA_TELA - 50)
                    malware_rect.y = random.randint(0, ALTURA_TELA - 50)

                    # Se o jogador capturar 5 malwares, terminar o minigame
                    if malwares_capturados >= 5:
                        jogo_em_andamento = False
                        return True  # Retorna que o jogador capturou 5 malwares

        # Atualizar o tempo
        tempo_atual = pygame.time.get_ticks()
        tempo_gasto = (tempo_atual - tempo_inicio) // 1000

        # Se o tempo gasto atingir o limite definido, terminar o minigame
        if tempo_gasto >= tempo_maximo:
            jogo_em_andamento = False
            return False  # Retorna que o tempo máximo foi atingido

        # Desenhar a tela
        tela.fill(BRANCO)
        exibir_texto(tela, f"Malwares Capturados: {malwares_capturados}", PRETO, (10, 10))
        exibir_texto(tela, f"Tempo Gasto: {tempo_gasto}s", PRETO, (10, 50))

        # Desenhar o malware
        tela.blit(malware_imagem, malware_rect)

        # Atualizar a tela
        pygame.display.flip()

        # Controlar FPS
        clock.tick(60)