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

def inicializar_figurantes(posicoes, animações, tamanhos):
    figurantes = {}
    rects_figurantes = {}
    for i, posicao in enumerate(posicoes):
        figura_rect = pygame.Rect(posicao[0] + 90, posicao[1] + 70, 50, 100)
        figurantes[f"figurante{i+1}"] = {
            "rect": figura_rect,
            "animacao": animações[i],
            "frame_atual": 0,
            "ultimo_tempo_animacao": pygame.time.get_ticks()
        }
        rects_figurantes[f"figurante{i+1}"] = figura_rect
    return figurantes, rects_figurantes

def atualizar_figurantes(figurantes, tempo_espera_animacao):
    agora = pygame.time.get_ticks()
    for figurante in figurantes.values():
        if agora - figurante["ultimo_tempo_animacao"] > tempo_espera_animacao:
            figurante["frame_atual"] = (figurante["frame_atual"] + 1) % len(figurante["animacao"])
            figurante["ultimo_tempo_animacao"] = agora
    return figurantes

def desenhar_figurantes(tela, figurantes, posicoes_figurantes):
    for i, (nome, figurante) in enumerate(figurantes.items()):
        figura_atual = figurante["animacao"][figurante["frame_atual"]]
        posicao = posicoes_figurantes[i]
        tela.blit(figura_atual, posicao)

def fase1():
    tela, relogio = inicializar_jogo()
    (chao, parede, personagem_parado, animacao_andar, animacao_correr, ceu, janela, porta, maquina, maquina2, mesa, mesa_grande, computador1, computador2, gato, cachorro, relogio_figura, rects, animacao_figurante1, animacao_figurante2, animacao_figurante3, animacao_figurante4, vida, moeda) = carregar_assets()
    x_personagem, y_personagem = inicializar_posicoes()
    altura_chao, area_chao_horizontalmente_expandida = definir_areas_chao()
    posicoes, rects = definir_posicoes_objetos(altura_chao, rects)
    
    # Configurações dos figurantes
    posicoes_figurantes = [
        (rects['mesa0'].x - 150, rects['mesa0'].y - 80),
        (rects['mesa15'].x - 250, rects['mesa15'].y - 60),
        (rects['mesa9'].x - 510, rects['mesa9'].y - 70),
        (rects['mesa20'].x - 150, rects['mesa20'].y - 60)
    ]
    
    tamanhos_figurantes = [(90, 70), (90, 70), (90, 70), (90, 70)]
    animacoes_figurantes = [animacao_figurante1, animacao_figurante2, animacao_figurante3, animacao_figurante4]
    
    figurantes, rects_figurantes = inicializar_figurantes(posicoes_figurantes, animacoes_figurantes, tamanhos_figurantes)
    
    # Adiciona os rects dos figurantes ao dicionário principal
    rects.update(rects_figurantes)
    frame_atual = 0
    direcao = "direita"
    tempo_espera_animacao = 200  # Intervalo entre frames (em milissegundos)
    
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
        
        # Atualizar a animação dos figurantes
        figurantes = atualizar_figurantes(figurantes, tempo_espera_animacao)
        
        if direcao == "esquerda":
            personagem = pygame.transform.flip(personagem, True, False)
        
        desenhar_cenario(tela, chao, parede, ceu, janela, porta, pygame.transform.flip(porta, True, False), maquina, maquina2, mesa, mesa_grande, computador1, computador2, gato, cachorro, posicoes, altura_chao, relogio_figura, vida, moeda)
        tela.blit(personagem, (x_personagem, y_personagem))
        
        # Desenhar figurantes
        desenhar_figurantes(tela, figurantes, posicoes_figurantes)
        
        # Desenhar retângulos de colisão
        #for key, rect in rects.items():
            #pygame.draw.rect(tela, (255, 0, 0), rect, 2)  # Desenha retângulos vermelhos com borda de espessura 2
        
        pygame.display.flip()
        relogio.tick(30)
        
if __name__ == "__main__":
    fase1()