import pygame
import sys
import os
from fase1 import fase1
from fase2 import fase2
from fase3 import fase3
from personagem import *
pygame.init()

# Configurar a tela
largura, altura = 1920, 1080
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
caminho_assets = os.path.join(os.getcwd(), "assets", "images")
caminho_audios = os.path.join(os.getcwd(), "assets", "audios")

# Carregar sons
som_selecao = pygame.mixer.Sound(os.path.join(caminho_audios, "select.wav"))
som_selecao.set_volume(0.05)

som_fase = pygame.mixer.Sound(os.path.join(caminho_audios, "fase.wav"))
som_fase.set_volume(0.05)

# Função para carregar imagens e máscaras
def carregar_imagem(nome, tamanho):
    imagem = pygame.image.load(os.path.join(caminho_assets, nome)).convert_alpha()
    imagem = pygame.transform.scale(imagem, tamanho)
    return imagem, pygame.mask.from_surface(imagem)

# Carregar imagens de fundo e botões
background, _ = carregar_imagem("background.jpg", (largura, altura))
botao_play, mascara_play = carregar_imagem("botao_play.png", (300, 300))
botao_play_sel, mascara_play_sel = carregar_imagem("botao_play_selecionado.png", (300, 300))
botao_instrucao, mascara_instrucao = carregar_imagem("botao_instrucao.png", (300, 300))
botao_instrucao_sel, mascara_instrucao_sel = carregar_imagem("botao_instrucao_selecionado.png", (300, 300))
botao_sair, mascara_sair = carregar_imagem("botao_sair.png", (300, 300))
botao_sair_sel, mascara_sair_sel = carregar_imagem("botao_sair_selecionado.png", (300, 300))
botao_voltar, mascara_voltar = carregar_imagem("botao_voltar.png", (300, 300))
botao_voltar_sel, mascara_voltar_sel = carregar_imagem("botao_voltar_selecionado.png", (300, 300))

# Carregar asset de seleção
selecao_img, _ = carregar_imagem("select.png", (300, 300))

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

# Variável para armazenar o botão selecionado pelo mouse
botao_anterior = None
botao_selecionado = "jogar"

# Função para desenhar texto centralizado
def desenhar_texto_centralizado(texto, fonte, cor, superficie, x, y):
    textoobj = fonte.render(texto, True, cor)
    textorect = textoobj.get_rect(center=(x, y))
    superficie.blit(textoobj, textorect)

# Função para criar botões com som de seleção ao passar o mouse
def criar_botao(imagem, imagem_sel, mascara, mascara_sel, x_rel, y_rel, acao=None):
    global botao_anterior, botao_selecionado

    mouse = pygame.mouse.get_pos()
    clique = pygame.mouse.get_pressed()

    x_absoluto = monitor_x + (monitor_largura - 300) // 2 + x_rel - 10
    y_absoluto = monitor_y + (monitor_altura - 300) // 2 + y_rel

    mouse_sobre_botao = mascara.overlap(pygame.mask.Mask((1, 1), fill=True), (mouse[0] - x_absoluto, mouse[1] - y_absoluto))

    if mouse_sobre_botao:
        tela.blit(imagem_sel, (x_absoluto, y_absoluto))
        
        if botao_anterior != acao:
            som_selecao.play()
            botao_anterior = acao
        
        botao_selecionado = acao
        
        if clique[0] == 1 and acao is not None:
            return acao
    else:
        tela.blit(imagem, (x_absoluto, y_absoluto))

    return None

# Carregar imagem de instruções
instrucoes_bg, _ = carregar_imagem("main_menu_instrucoes.png", (largura, altura))

# Função para a tela de instruções
def instrucoes():
    global botao_selecionado

    # Criar fonte para o texto
    fonte_instrucoes = pygame.font.SysFont("Arial", 30)

    texto_instrucoes = (
        "Esse jogo é um projeto educacional voltado para o ensino de conceitos fundamentais "
        "de ciência da computação, com foco específico em ciberataques, suas prevenções e "
        "funcionamento. O projeto busca conscientizar os jogadores sobre as ameaças digitais "
        "crescentes, como phishing, ransomware e ataques DDoS, que podem comprometer "
        "a segurança de dispositivos e sistemas. Além de expor os principais tipos de ataques, "
        "o jogo ensina estratégias de prevenção, como o uso de firewalls, antivírus, criptografia "
        "e, principalmente, a conscientização do usuário."
    )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        tela.fill(PRETO)
        tela.blit(instrucoes_bg, (0, 0))

        largura_retangulo = 1200
        altura_retangulo = 300

        y_retangulo = (altura - altura_retangulo + 500) // 2

        linhas = []
        palavras = texto_instrucoes.split(' ')
        linha_atual = ""

        for palavra in palavras:
            linha_teste = linha_atual + palavra + ' '
            texto_renderizado = fonte_instrucoes.render(linha_teste, True,PRETO)
            if texto_renderizado.get_width() <= largura_retangulo - 20:
                linha_atual = linha_teste
            else:
                linhas.append(linha_atual)
                linha_atual = palavra + ' '

        if linha_atual:
            linhas.append(linha_atual)

        for i, linha in enumerate(linhas):
            texto_renderizado = fonte_instrucoes.render(linha, True, PRETO)
            textorect = texto_renderizado.get_rect(center=(largura // 2, y_retangulo + 50 + (i * 35)))  # Centralizar
            tela.blit(texto_renderizado, textorect)

        if criar_botao(botao_voltar, botao_voltar_sel, mascara_voltar, mascara_voltar_sel, 0, 430, acao="voltar"):
            tela_inicial()

        pygame.display.flip()
        relógio.tick(30)

def mostrar_transicao_com_fade(tela, texto, duracao=3000, fps=60):
    som_fase.play()
    clock = pygame.time.Clock()
    fonte = pygame.font.SysFont("arial", 50)
    mensagem = fonte.render(texto, True, (255, 255, 255))
    mensagem_rect = mensagem.get_rect(center=(tela.get_width() // 2, tela.get_height() // 2))

    fade_surface = pygame.Surface(tela.get_size())
    fade_surface.fill((0, 0, 0))

    for alpha in range(255, -1, -int(255 / (fps * (duracao / 2000)))):
        tela.fill((0, 0, 0))
        tela.blit(mensagem, mensagem_rect)
        fade_surface.set_alpha(alpha)
        tela.blit(fade_surface, (0, 0))
        pygame.display.flip()
        clock.tick(fps)
        
# Tela Inicial
def tela_inicial():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        tela.fill(PRETO)
        tela.blit(background, (0, 0))
        
        if criar_botao(botao_play, botao_play_sel, mascara_play, mascara_play_sel, 0, 0, acao="jogar"):
            try:
                mostrar_transicao_com_fade(tela, "Fase 1 - Phishing")
                fase1_concluida, personagem = fase1()
                if fase1_concluida:
                    mostrar_transicao_com_fade(tela, "Fase 2 - Ransomware")
                    fase2_concluida, personagem = fase2(personagem)
                if fase2_concluida:
                    mostrar_transicao_com_fade(tela, "Fase 3 - DDoS")
                    fase3(personagem)
                    
            except Exception as e:
                print(f"Ocorreu um erro: {e}")
                tela_inicial()
                
        if criar_botao(botao_instrucao, botao_instrucao_sel, mascara_instrucao, mascara_instrucao_sel, 0, 150, acao="instrucoes"):
            instrucoes()
        
        if criar_botao(botao_sair, botao_sair_sel, mascara_sair, mascara_sair_sel, 0, 300, acao="sair"):
            pygame.quit()
            sys.exit()

        if botao_selecionado == "jogar":
            tela.blit(selecao_img, (monitor_x + (monitor_largura - 300) // 2 - 150, monitor_y + (monitor_altura - 300) // 2 + 20))
        elif botao_selecionado == "instrucoes":
            tela.blit(selecao_img, (monitor_x + (monitor_largura - 300) // 2 - 150, monitor_y + (monitor_altura - 300) // 2 + 170))
        elif botao_selecionado == "sair":
            tela.blit(selecao_img, (monitor_x + (monitor_largura - 300) // 2 - 150, monitor_y + (monitor_altura - 300) // 2 + 320))

        pygame.display.flip()
        relógio.tick(30)

# Iniciar a tela inicial
tela_inicial()