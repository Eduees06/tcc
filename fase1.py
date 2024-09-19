import pygame
import sys
from config import *
from utils import *

# Caminho dos assets
caminho_assets = "D:/jogo/assets/images"
def inicializar_jogo():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Fase 1 - Cyber Defender")
    relogio = pygame.time.Clock()
    return tela, relogio


def fase1():
    tela, relogio = inicializar_jogo()
    (chao, parede, personagem_parado, animacao_andar, animacao_correr, ceu, janela, porta, maquina, maquina2, mesa, mesa_grande, computador1, computador2, gato, cachorro, divisoria, rects) = carregar_assets()
    x_personagem, y_personagem = inicializar_posicoes()
    
    altura_chao, area_chao_horizontalmente_expandida = definir_areas_chao()
    posicoes, rects = definir_posicoes_objetos(altura_chao, rects)
    frame_atual = 0
    direcao = "direita"
    
    fase1_rodando = True
    while fase1_rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        teclas_pressionadas = pygame.key.get_pressed()
        x_personagem, y_personagem, direcao, voltar_para_tela_inicial = mover_personagem(teclas_pressionadas, x_personagem, y_personagem, VELOCIDADE_PERSONAGEM, direcao, TAMANHO_PERSONAGEM, area_chao_horizontalmente_expandida, VELOCIDADE_CORRER, posicoes, rects, tela)
        
        if voltar_para_tela_inicial:
            return
        
        personagem, frame_atual = atualizar_animacao(teclas_pressionadas, frame_atual, animacao_andar, animacao_correr, personagem_parado)
        
        if direcao == "esquerda":
            personagem = pygame.transform.flip(personagem, True, False)
        
        desenhar_cenario(tela, chao, parede, ceu, janela, porta, pygame.transform.flip(porta, True, False), maquina, maquina2, mesa, mesa_grande, computador1, computador2, gato, cachorro, posicoes, altura_chao)
        tela.blit(personagem, (x_personagem, y_personagem))
        
        pygame.display.flip()
        relogio.tick(30)
        
    
if __name__ == "__main__":
    fase1()