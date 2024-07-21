import pygame
import os
from config import LARGURA_TELA, ALTURA_TELA, TAMANHO_PERSONAGEM

def calcular_escala(largura_tela):
    if largura_tela == 1280:
        return largura_tela // 13
    elif largura_tela == 1920:
        return largura_tela // 19
    else:
        raise ValueError("Resolução não suportada.")

def carregar_imagens(caminho_assets):
    # Carregar todas as imagens necessárias
    chao_original = pygame.image.load(os.path.join(caminho_assets, "chao.png")).convert()
    parede_original = pygame.image.load(os.path.join(caminho_assets, "parede.png")).convert_alpha()
    personagem_parado = pygame.image.load(os.path.join(caminho_assets, "personagem.png")).convert_alpha()
    janela_original = pygame.image.load(os.path.join(caminho_assets, "janela.png")).convert_alpha()
    porta_original = pygame.image.load(os.path.join(caminho_assets, "porta.png")).convert_alpha()
    maquina_original = pygame.image.load(os.path.join(caminho_assets, "maquina.png")).convert_alpha()
    maquina2_original = pygame.image.load(os.path.join(caminho_assets, "maquina2.png")).convert_alpha()
    mesa_original = pygame.image.load(os.path.join(caminho_assets, "mesa.png")).convert_alpha()
    mesa_grande_original = pygame.image.load(os.path.join(caminho_assets, "mesagrande.png")).convert_alpha()
    computador1_original = pygame.image.load(os.path.join(caminho_assets, "computador1.png")).convert_alpha()
    computador2_original = pygame.image.load(os.path.join(caminho_assets, "computador2.png")).convert_alpha()
    gato_original = pygame.image.load(os.path.join(caminho_assets, "gato.png")).convert_alpha()
    cachorro_original = pygame.image.load(os.path.join(caminho_assets, "cachorro.png")).convert_alpha()
    divisoria = pygame.image.load(os.path.join(caminho_assets, 'divisoria.png')).convert_alpha()
    
    # Calcular escala com base na largura da tela
    escala = calcular_escala(LARGURA_TELA)
    
    # Escalar as imagens para o tamanho desejado
    chao = pygame.transform.scale(chao_original, (escala * 2.5, escala * 1.2))
    parede = pygame.transform.scale(parede_original, (escala * 1.0, escala * 1.0))
    personagem_parado = pygame.transform.scale(personagem_parado, (TAMANHO_PERSONAGEM, TAMANHO_PERSONAGEM))
    janela = pygame.transform.scale(janela_original, (escala * 0.9, escala * 0.9))
    porta = pygame.transform.scale(porta_original, (escala * 1.0, escala * 2.0))
    maquina = pygame.transform.scale(maquina_original, (escala * 1.0, escala * 1.5))
    maquina2 = pygame.transform.scale(maquina2_original, (escala * 1.0, escala * 1.5))
    mesa = pygame.transform.scale(mesa_original, (escala * 1.0, escala * 1.0))
    mesa_grande = pygame.transform.scale(mesa_grande_original, (escala * 1.5, escala * 0.6))
    computador1 = pygame.transform.scale(computador1_original, (escala * 0.7, escala * 0.7))
    computador2 = pygame.transform.scale(computador2_original, (escala * 0.8, escala * 0.8))
    computador2 = pygame.transform.flip(computador2, True, False)
    gato = pygame.transform.scale(gato_original, (escala * 0.5, escala * 0.5))
    gato= pygame.transform.flip(gato, True, False)
    cachorro = pygame.transform.scale(cachorro_original, (escala * 0.7, escala * 0.5))
    
    # Carregar animações de andar e correr
    animacao_andar = [
        pygame.transform.scale(pygame.image.load(os.path.join(caminho_assets, f"personagem_andando{i}.png")).convert_alpha(), (TAMANHO_PERSONAGEM, TAMANHO_PERSONAGEM))
        for i in range(1, 9)
    ]

    animacao_correr = [
        pygame.transform.scale(pygame.image.load(os.path.join(caminho_assets, f"personagem_correndo{i}.png")).convert_alpha(), (TAMANHO_PERSONAGEM, TAMANHO_PERSONAGEM))
        for i in range(1, 9)
    ]

    # Carregar imagem do céu
    ceu_original = pygame.image.load(os.path.join(caminho_assets, "ceu.png")).convert()
    ceu = pygame.transform.scale(ceu_original, (LARGURA_TELA, int(ALTURA_TELA * 0.1)))

    return chao, parede, personagem_parado, animacao_andar, animacao_correr, ceu, janela, porta, maquina,maquina2, mesa, mesa_grande,computador1, computador2, gato, cachorro, divisoria

def desenhar_repetido(tela, imagem, largura, altura, x_inicial=0, y_inicial=0):
    for x in range(x_inicial, x_inicial + largura, imagem.get_width()):
        for y in range(y_inicial, y_inicial + altura, imagem.get_height()):
            tela.blit(imagem, (x, y))

def desenhar_borda_horizontal(tela, cor, largura_tela, largura, y_pos):
    pygame.draw.rect(tela, cor, (0, y_pos, largura_tela, largura))

def mover_personagem(teclas, x, y, velocidade, direcao, largura, altura, tamanho_personagem, area_chao_horizontalmente_expandida, velocidade_correr):
    novo_x, novo_y = x, y

    if teclas[pygame.K_LSHIFT] or teclas[pygame.K_RSHIFT]:
        velocidade = velocidade_correr  # Aumentar a velocidade se Shift estiver pressionado

    if teclas[pygame.K_UP] or teclas[pygame.K_w]:
        novo_y = y - velocidade
    if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
        novo_y = y + velocidade
    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        novo_x = x - velocidade
        direcao = "esquerda"
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        novo_x = x + velocidade
        direcao = "direita"

    # Verificar colisão com a área do chão
    rect_personagem = pygame.Rect(novo_x, novo_y, tamanho_personagem, tamanho_personagem)
    if area_chao_horizontalmente_expandida.contains(rect_personagem):
        x, y = novo_x, novo_y

    return x, y, direcao

