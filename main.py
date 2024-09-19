import pygame
import sys
import os
from fase1 import fase1

pygame.init()

# Configurar a tela
largura, altura = 1920, 1080  # Tamanho da tela
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Cyber Defender")

relógio = pygame.time.Clock()

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

# Fontes
fonte = pygame.font.SysFont(None, 55)
fonte_pequena = pygame.font.SysFont(None, 35)

# Caminho dos assets
caminho_assets = "D:/jogo/assets/images"

# Função para carregar imagens e máscaras
def carregar_imagem(nome, tamanho):
    imagem = pygame.image.load(os.path.join(caminho_assets, nome)).convert_alpha()
    imagem = pygame.transform.scale(imagem, tamanho)
    return imagem, pygame.mask.from_surface(imagem)

# Carregar imagens de fundo e botões
background, _ = carregar_imagem("background.png", (largura, altura))
botao_play, mascara_play = carregar_imagem("botao_play.png", (300, 300))
botao_play_sel, mascara_play_sel = carregar_imagem("botao_play_selecionado.png", (300, 300))
botao_instrucao, mascara_instrucao = carregar_imagem("botao_instrucao.png", (300, 300))
botao_instrucao_sel, mascara_instrucao_sel = carregar_imagem("botao_instrucao_selecionado.png", (300, 300))
botao_sair, mascara_sair = carregar_imagem("botao_sair.png", (300, 300))
botao_sair_sel, mascara_sair_sel = carregar_imagem("botao_sair_selecionado.png", (300, 300))
botao_voltar, mascara_voltar = carregar_imagem("botao_voltar.png", (300, 300))
botao_voltar_sel, mascara_voltar_sel = carregar_imagem("botao_voltar_selecionado.png", (300, 300))

# Coordenadas e proporções do monitor
monitor_x_original = 5
monitor_y_original = 27
monitor_largura_original = 91
monitor_altura_original = 52

proporcao_x = largura / 100
proporcao_y = altura / 100

monitor_x = int(monitor_x_original * proporcao_x)
monitor_y = int(monitor_y_original * proporcao_y)
monitor_largura = int(monitor_largura_original * proporcao_x)
monitor_altura = int(monitor_altura_original * proporcao_y)

# Função para desenhar texto centralizado
def desenhar_texto_centralizado(texto, fonte, cor, superficie, x, y):
    textoobj = fonte.render(texto, True, cor)
    textorect = textoobj.get_rect(center=(x, y))
    superficie.blit(textoobj, textorect)

# Função para criar botões
def criar_botao(imagem, imagem_sel, mascara, mascara_sel, x_rel, y_rel, acao=None):
    mouse = pygame.mouse.get_pos()
    clique = pygame.mouse.get_pressed()

    x_absoluto = monitor_x + (monitor_largura - 300) // 2 + x_rel - 10
    y_absoluto = monitor_y + (monitor_altura - 300) // 2 + y_rel

    if mascara.overlap(pygame.mask.Mask((1, 1), fill=True), (mouse[0] - x_absoluto, mouse[1] - y_absoluto)):
        tela.blit(imagem_sel, (x_absoluto, y_absoluto))
        if clique[0] == 1 and acao is not None:
            return acao
    else:
        tela.blit(imagem, (x_absoluto, y_absoluto))

    return None

# Tela de Instruções
def instrucoes():
    instrucoes_rodando = True
    while instrucoes_rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        tela.fill(PRETO)
        tela.blit(background, (0, 0))

        desenhar_texto_centralizado("Instruções", fonte, BRANCO, tela, monitor_x + monitor_largura // 2, monitor_y + 50)
        
        texto_instrucoes = (
            "Bem-vindo ao 'Cyber defender', um jogo educativo onde você",
            "aprenderá sobre diversos tipos de ciberataques e suas",
            "prevenções/respostas. O objetivo principal é proteger seu",
            "computador contra invasões enquanto trabalha em uma empresa",
            "fictícia",
            "O jogo é baseado em escolhas, não deixe o seu computador ser",
            "infectado."
        )

        y_offset = monitor_y + 150
        for linha in texto_instrucoes:
            desenhar_texto_centralizado(linha, fonte_pequena, BRANCO, tela, largura // 2, y_offset)
            y_offset += 30

        if criar_botao(botao_voltar, botao_voltar_sel, mascara_voltar, mascara_voltar_sel, 0, 150, "voltar"):
            instrucoes_rodando = False

        pygame.display.flip()
        relógio.tick(15)

# Tela Inicial
def tela_inicial():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        tela.fill(PRETO)
        tela.blit(background, (0, 0))

        desenhar_texto_centralizado("Menu Iniciar", fonte, BRANCO, tela, largura // 2, monitor_y + 50)
        
        if criar_botao(botao_play, botao_play_sel, mascara_play, mascara_play_sel, 0, -100, "jogar"):
            fase1()
        
        if criar_botao(botao_instrucao, botao_instrucao_sel, mascara_instrucao, mascara_instrucao_sel, 0, 50, "instrucoes"):
            instrucoes()
        
        if criar_botao(botao_sair, botao_sair_sel, mascara_sair, mascara_sair_sel, 0, 200, "sair"):
            pygame.quit()
            sys.exit()

        pygame.display.flip()
        relógio.tick(30)

# Iniciar a tela inicial
tela_inicial()
