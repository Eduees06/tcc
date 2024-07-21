import pygame
import sys
import os
from fase1 import fase1

pygame.init()

# Configurar a tela
largura, altura = 1024, 1024  # Tamanho da tela
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Cyber Defender")

relógio = pygame.time.Clock()

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

fonte = pygame.font.SysFont(None, 55)
fonte_pequena = pygame.font.SysFont(None, 35)

# Carregar a imagem de fundo do monitor
caminho_assets = "D:/jogo/assets/images"
background = pygame.image.load(os.path.join(caminho_assets, "background.png")).convert()
background = pygame.transform.scale(background, (largura, altura))

# Carregar imagens dos botões
botao_play = pygame.image.load(os.path.join(caminho_assets, "botao_play.png")).convert_alpha()
botao_play = pygame.transform.scale(botao_play, (300, 300))
botao_play_sel = pygame.image.load(os.path.join(caminho_assets, "botao_play_selecionado.png")).convert_alpha()
botao_play_sel = pygame.transform.scale(botao_play_sel, (300, 300))

botao_instrucao = pygame.image.load(os.path.join(caminho_assets, "botao_instrucao.png")).convert_alpha()
botao_instrucao = pygame.transform.scale(botao_instrucao, (300, 300))
botao_instrucao_sel = pygame.image.load(os.path.join(caminho_assets, "botao_instrucao_selecionado.png")).convert_alpha()
botao_instrucao_sel = pygame.transform.scale(botao_instrucao_sel, (300, 300))

botao_sair = pygame.image.load(os.path.join(caminho_assets, "botao_sair.png")).convert_alpha()
botao_sair = pygame.transform.scale(botao_sair, (300, 300))
botao_sair_sel = pygame.image.load(os.path.join(caminho_assets, "botao_sair_selecionado.png")).convert_alpha()
botao_sair_sel = pygame.transform.scale(botao_sair_sel, (300, 300))

# Carregar imagens do botão voltar e redimensionar
botao_voltar = pygame.image.load(os.path.join(caminho_assets, "botao_voltar.png")).convert_alpha()
botao_voltar = pygame.transform.scale(botao_voltar, (300, 300))
botao_voltar_sel = pygame.image.load(os.path.join(caminho_assets, "botao_voltar_selecionado.png")).convert_alpha()
botao_voltar_sel = pygame.transform.scale(botao_voltar_sel, (300, 300))

# Criar máscaras para os botões
mascara_play = pygame.mask.from_surface(botao_play)
mascara_play_sel = pygame.mask.from_surface(botao_play_sel)
mascara_instrucao = pygame.mask.from_surface(botao_instrucao)
mascara_instrucao_sel = pygame.mask.from_surface(botao_instrucao_sel)
mascara_sair = pygame.mask.from_surface(botao_sair)
mascara_sair_sel = pygame.mask.from_surface(botao_sair_sel)
mascara_voltar = pygame.mask.from_surface(botao_voltar)
mascara_voltar_sel = pygame.mask.from_surface(botao_voltar_sel)

# Coordenadas do monitor na imagem original (100x100 pixels)
monitor_x_original = 5
monitor_y_original = 27
monitor_largura_original = 91
monitor_altura_original = 52

# Proporções para o monitor na tela de 1024x1024
proporcao_x = largura / 100  # Proporção de redimensionamento em x
proporcao_y = altura / 100  # Proporção de redimensionamento em y

# Coordenadas do monitor na tela de 1024x1024
monitor_x = int(monitor_x_original * proporcao_x)
monitor_y = int(monitor_y_original * proporcao_y)
monitor_largura = int(monitor_largura_original * proporcao_x)
monitor_altura = int(monitor_altura_original * proporcao_y)

# Função para desenhar texto na tela centralizado
def desenhar_texto_centralizado(texto, fonte, cor, superficie, x, y):
    textoobj = fonte.render(texto, True, cor)
    textorect = textoobj.get_rect(center=(x, y))
    superficie.blit(textoobj, textorect)

# Função para criar botões dentro da área do monitor
def criar_botao(imagem, imagem_sel, mascara, mascara_sel, x_rel, y_rel, acao=None):
    mouse = pygame.mouse.get_pos()
    clique = pygame.mouse.get_pressed()
    
    # Ajustar coordenadas para a área do monitor na tela
    x_absoluto = monitor_x + (monitor_largura - 300) // 2 + x_rel - 10  # Ajuste de 1 pixel para a esquerda
    y_absoluto = monitor_y + (monitor_altura - 300) // 2 + y_rel 
    
    # Desenhar o botão na tela
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
                sys.exit()

        tela.fill(PRETO)
        tela.blit(background, (0, 0))  # Desenha o monitor como plano de fundo

        desenhar_texto_centralizado("Instruções", fonte, BRANCO, tela, monitor_x + monitor_largura // 2, monitor_y + 50)  # Centraliza o título
        
        texto_instrucoes = (
            "Bem-vindo ao 'Cyber defender', um jogo educativo onde você",
            "aprenderá sobre diversos tipos de ciberataques e suas",
            "prevenções/respostas. O objetivo principal é proteger seu",
            "computador contra invasões enquanto trabalha em uma empresa",
            "fictícia",
            "O jogo é baseado em escolhas, não deixe o seu computador ser",
            "infectado."
        )

        y_offset = monitor_y + 150  # Offset inicial
        for linha in texto_instrucoes:
            desenhar_texto_centralizado(linha, fonte_pequena, BRANCO, tela, largura // 2, y_offset)
            y_offset += 30

        if criar_botao(botao_voltar, botao_voltar_sel, mascara_voltar, mascara_voltar_sel, 0, 150, "voltar"):  # Usar o botão voltar
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
        tela.blit(background, (0, 0))  # Desenha o monitor como plano de fundo

        desenhar_texto_centralizado("Menu Iniciar", fonte, BRANCO, tela, largura // 2, monitor_y + 50)  # Centraliza o título
        
        if criar_botao(botao_play, botao_play_sel, mascara_play, mascara_play_sel, 0, -100, "jogar"):  # Ajuste na posição do botão "Jogar"
            fase1()  # Chamar a fase 1 quando clicar em jogar
        
        if criar_botao(botao_instrucao, botao_instrucao_sel, mascara_instrucao, mascara_instrucao_sel, 0, 50, "instrucoes"):  # Ajuste na posição do botão "Instruções"
            instrucoes()
        
        if criar_botao(botao_sair, botao_sair_sel, mascara_sair, mascara_sair_sel, 0, 200, "sair"):  # Ajuste na posição do botão "Sair"
            pygame.quit()
            sys.exit()

        pygame.display.flip()
        relógio.tick(15)

# Iniciar a tela inicial
tela_inicial()