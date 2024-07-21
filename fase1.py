import pygame
import sys
from config import *
from utils import carregar_imagens, desenhar_repetido, desenhar_borda_horizontal, mover_personagem

def inicializar_jogo():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Fase 1 - Cyber Defender")
    relogio = pygame.time.Clock()
    return tela, relogio

def carregar_assets():
    return carregar_imagens(CAMINHO_ASSETS)

def inicializar_posicoes():
    x_personagem = LARGURA_TELA // 2 - TAMANHO_PERSONAGEM // 2
    y_personagem = ALTURA_TELA // 2 - TAMANHO_PERSONAGEM // 2
    return x_personagem, y_personagem

def definir_areas_chao():
    altura_chao = int(ALTURA_TELA * 0.7)
    area_chao = pygame.Rect(0, ALTURA_TELA - altura_chao, LARGURA_TELA, altura_chao)
    area_chao_horizontalmente_expandida = area_chao.inflate(int(LARGURA_TELA * 0.1), int(LARGURA_TELA * 0.08))
    return altura_chao, area_chao_horizontalmente_expandida

def definir_posicoes_objetos(altura_chao):
    escala = LARGURA_TELA // 10

    x_janela1 = LARGURA_TELA // 2 - escala * 4
    y_janela1 = int(ALTURA_TELA * 0.2)
    x_janela2 = LARGURA_TELA // 2 + escala * 3
    y_janela2 = int(ALTURA_TELA * 0.2)

    x_porta1 = LARGURA_TELA // 2
    y_porta1 = int(ALTURA_TELA * 0.26)
    x_porta2 = x_porta1 - 100
    y_porta2 = y_porta1

    x_maquina = LARGURA_TELA // 2 - 500
    y_maquina = int(ALTURA_TELA * 0.26) + 20
    x_maquina2 = x_maquina + 800
    y_maquina2 = y_maquina

    x_mesa_grande = LARGURA_TELA // 2 - 700
    y_mesa_grande = int(ALTURA_TELA * 0.26) + 100

    espaco_horizontal = 200
    espaco_vertical = 500

    mesas = [(LARGURA_TELA // 2 - espaco_horizontal - 75, ALTURA_TELA - altura_chao + espaco_vertical),
             (LARGURA_TELA // 2 - espaco_horizontal - 75, ALTURA_TELA - altura_chao + espaco_vertical + 100),
             (LARGURA_TELA // 2 - espaco_horizontal - 75 + 100, ALTURA_TELA - altura_chao + espaco_vertical + 100),
             (LARGURA_TELA // 2 - espaco_horizontal - 75 + 100, ALTURA_TELA - altura_chao + espaco_vertical),
             (LARGURA_TELA // 2 + espaco_horizontal - 75, ALTURA_TELA - altura_chao + espaco_vertical),
             (LARGURA_TELA // 2 + espaco_horizontal - 75, ALTURA_TELA - altura_chao + espaco_vertical + 100),
             (LARGURA_TELA // 2 + espaco_horizontal - 75 + 100, ALTURA_TELA - altura_chao + espaco_vertical + 100),
             (LARGURA_TELA // 2 + espaco_horizontal - 75 + 100, ALTURA_TELA - altura_chao + espaco_vertical),
             (LARGURA_TELA // 2 - espaco_horizontal - 75, ALTURA_TELA - espaco_vertical),
             (LARGURA_TELA // 2 - espaco_horizontal - 75, ALTURA_TELA - espaco_vertical + 100),
             (LARGURA_TELA // 2 - espaco_horizontal - 75 + 100, ALTURA_TELA - espaco_vertical + 100),
             (LARGURA_TELA // 2 - espaco_horizontal - 75 + 100, ALTURA_TELA - espaco_vertical),
             (LARGURA_TELA // 2 + espaco_horizontal - 75, ALTURA_TELA - espaco_vertical),
             (LARGURA_TELA // 2 + espaco_horizontal - 75, ALTURA_TELA - espaco_vertical + 100),
             (LARGURA_TELA // 2 + espaco_horizontal - 75 + 100, ALTURA_TELA - espaco_vertical + 100),
             (LARGURA_TELA // 2 + espaco_horizontal - 75 + 100, ALTURA_TELA - espaco_vertical)]

    computadores = [(mesa[0] + 5, mesa[1] + 10) for mesa in mesas]

    x_gato = x_mesa_grande + 50
    y_gato = y_mesa_grande - 10

    x_cachorro = x_maquina2 + 150
    y_cachorro = y_maquina2 + 90

    return (x_janela1, y_janela1, x_janela2, y_janela2, x_porta1, y_porta1, x_porta2, y_porta2,
            x_maquina, y_maquina, x_maquina2, y_maquina2, x_mesa_grande, y_mesa_grande, mesas, computadores, x_gato, y_gato, x_cachorro, y_cachorro)

def desenhar_cenario(tela, chao, parede, ceu, janela, porta, porta2, maquina, maquina2, mesa, mesa_grande, computador1, computador2, gato, cachorro, posicoes, altura_chao):
    (x_janela1, y_janela1, x_janela2, y_janela2, x_porta1, y_porta1, x_porta2, y_porta2,
     x_maquina, y_maquina, x_maquina2, y_maquina2, x_mesa_grande, y_mesa_grande, mesas, computadores, x_gato, y_gato, x_cachorro, y_cachorro) = posicoes

    tela.fill((0, 0, 0))

    desenhar_repetido(tela, chao, LARGURA_TELA, altura_chao, 0, ALTURA_TELA - altura_chao)
    desenhar_repetido(tela, parede, LARGURA_TELA, int(ALTURA_TELA * 0.2), 0, ALTURA_TELA - altura_chao - int(ALTURA_TELA * 0.2))
    tela.blit(ceu, (0, 0))

    tela.blit(janela, (x_janela1, y_janela1))
    tela.blit(janela, (x_janela2, y_janela2))

    tela.blit(porta, (x_porta1, y_porta1))
    tela.blit(porta2, (x_porta2, y_porta2))

    tela.blit(maquina, (x_maquina, y_maquina))
    tela.blit(maquina2, (x_maquina2, y_maquina2))

    for i, (x_mesa, y_mesa) in enumerate(mesas):
        tela.blit(mesa, (x_mesa, y_mesa))
        tela.blit(computador1 if i % 2 == 0 else computador2, computadores[i])

    tela.blit(mesa_grande, (x_mesa_grande, y_mesa_grande))
    tela.blit(gato, (x_gato, y_gato))
    tela.blit(cachorro, (x_cachorro, y_cachorro))
    
    desenhar_borda_horizontal(tela, (100, 100, 100), LARGURA_TELA, 5, ALTURA_TELA - altura_chao - int(ALTURA_TELA * 0.2))

def atualizar_animacao(teclas_pressionadas, frame_atual, animacao_andar, animacao_correr, personagem_parado):
    if any([teclas_pressionadas[pygame.K_UP], teclas_pressionadas[pygame.K_DOWN], teclas_pressionadas[pygame.K_LEFT], teclas_pressionadas[pygame.K_RIGHT], teclas_pressionadas[pygame.K_w], teclas_pressionadas[pygame.K_s], teclas_pressionadas[pygame.K_a], teclas_pressionadas[pygame.K_d]]):
        if teclas_pressionadas[pygame.K_LSHIFT] or teclas_pressionadas[pygame.K_RSHIFT]:
            personagem = animacao_correr[frame_atual // 5]
            frame_atual = (frame_atual + 1) % (len(animacao_correr) * 5)
        else:
            personagem = animacao_andar[frame_atual // 5]
            frame_atual = (frame_atual + 1) % (len(animacao_andar) * 5)
    else:
        personagem = personagem_parado
        frame_atual = 0
    return personagem, frame_atual

def fase1():
    tela, relogio = inicializar_jogo()
    (chao, parede, personagem_parado, animacao_andar, animacao_correr, ceu, janela, porta, maquina, maquina2, mesa, mesa_grande, computador1, computador2, gato, cachorro, divisoria) = carregar_assets()
    x_personagem, y_personagem = inicializar_posicoes()
    altura_chao, area_chao_horizontalmente_expandida = definir_areas_chao()
    posicoes = definir_posicoes_objetos(altura_chao)

    frame_atual = 0
    direcao = "direita"

    fase1_rodando = True
    while fase1_rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        teclas_pressionadas = pygame.key.get_pressed()
        x_personagem, y_personagem, direcao = mover_personagem(teclas_pressionadas, x_personagem, y_personagem, VELOCIDADE_PERSONAGEM, direcao, LARGURA_TELA, ALTURA_TELA, TAMANHO_PERSONAGEM, area_chao_horizontalmente_expandida, VELOCIDADE_CORRER)
        
        personagem, frame_atual = atualizar_animacao(teclas_pressionadas, frame_atual, animacao_andar, animacao_correr, personagem_parado)
        
        if direcao == "esquerda":
            personagem = pygame.transform.flip(personagem, True, False)
        
        desenhar_cenario(tela, chao, parede, ceu, janela, porta, pygame.transform.flip(porta, True, False), maquina, maquina2, mesa, mesa_grande, computador1, computador2, gato, cachorro, posicoes, altura_chao)
        tela.blit(personagem, (x_personagem, y_personagem))

        pygame.display.flip()
        relogio.tick(30)

if __name__ == "__main__":
    fase1()