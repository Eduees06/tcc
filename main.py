import pygame
import sys
import os
from fase1 import fase1
from fase2 import fase2
from personagem import *
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
caminho_audios = "D:/jogo/audios"

# Carregar sons
som_selecao = pygame.mixer.Sound(os.path.join(caminho_audios, "select.wav"))
som_selecao.set_volume(0.05)  # Ajustar o volume do som para 5%

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
botao_selecionado = "jogar"  # Iniciar com o botão "play" selecionado

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

    # Verificar se o mouse está sobre o botão
    mouse_sobre_botao = mascara.overlap(pygame.mask.Mask((1, 1), fill=True), (mouse[0] - x_absoluto, mouse[1] - y_absoluto))

    # Se o mouse estiver sobre o botão, tocar o som e mudar o selecionado
    if mouse_sobre_botao:
        tela.blit(imagem_sel, (x_absoluto, y_absoluto))
        
        # Tocar som de seleção apenas uma vez ao passar sobre o botão
        if botao_anterior != acao:
            som_selecao.play()
            botao_anterior = acao
        
        # Atualizar o botão selecionado
        botao_selecionado = acao
        
        
        # Se o botão for clicado, retornar a ação correspondente
        if clique[0] == 1 and acao is not None:
            return acao
    else:
        tela.blit(imagem, (x_absoluto, y_absoluto))

    return None

# Carregar imagem de instruções
instrucoes_bg, _ = carregar_imagem("main_menu_instrucoes.png", (largura, altura))

# Função para a tela de instruções
def instrucoes():
    global botao_selecionado  # Para manter o botão selecionado ao voltar

    # Criar fonte para o texto
    fonte_instrucoes = pygame.font.SysFont("Arial", 30)  # Tamanho da fonte

    # Texto a ser exibido
    texto_instrucoes = (
        "Esse jogo é um projeto educacional voltado para o ensino de conceitos fundamentais "
        "de ciência da computação, com foco específico em ciberataques, suas prevenções e "
        "funcionamento. O projeto busca conscientizar os jogadores sobre as ameaças digitais "
        "crescentes, como malware, phishing, ransomware e ataques DDoS, que podem comprometer "
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
        tela.blit(instrucoes_bg, (0, 0))  # Substitui o fundo pela imagem de instruções

        # Definir as dimensões do retângulo
        largura_retangulo = 1200
        altura_retangulo = 300

        y_retangulo = (altura - altura_retangulo + 500) // 2  # Centralizar na altura

        # Quebrar o texto em linhas que cabem no retângulo
        linhas = []
        palavras = texto_instrucoes.split(' ')
        linha_atual = ""

        for palavra in palavras:
            # Adiciona a palavra atual à linha
            linha_teste = linha_atual + palavra + ' '
            texto_renderizado = fonte_instrucoes.render(linha_teste, True,PRETO)
            if texto_renderizado.get_width() <= largura_retangulo - 20:  # Considera 20px de margem
                linha_atual = linha_teste
            else:
                # Se ultrapassar a largura, armazena a linha atual e inicia uma nova
                linhas.append(linha_atual)
                linha_atual = palavra + ' '

        # Adiciona a última linha se não estiver vazia
        if linha_atual:
            linhas.append(linha_atual)

        # Desenhar cada linha do texto dentro do retângulo
        for i, linha in enumerate(linhas):
            texto_renderizado = fonte_instrucoes.render(linha, True, PRETO)
            textorect = texto_renderizado.get_rect(center=(largura // 2, y_retangulo + 50 + (i * 35)))  # Centralizar
            tela.blit(texto_renderizado, textorect)

        # Botão voltar centralizado na parte inferior do retângulo
        if criar_botao(botao_voltar, botao_voltar_sel, mascara_voltar, mascara_voltar_sel, 0, 430, acao="voltar"):
            tela_inicial()

        # Atualizar a tela
        pygame.display.flip()
        relógio.tick(30)
        
# Tela Inicial
def tela_inicial():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        tela.fill(PRETO)
        tela.blit(background, (0, 0))
        
        # Criar os botões e verificar seleção
        if criar_botao(botao_play, botao_play_sel, mascara_play, mascara_play_sel, 0, 0, acao="jogar"):
            try:
                # Chama a fase 1 e armazena o resultado
                fase1_concluida, personagem = fase1()
                if fase1_concluida:  # Se fase 1 for concluída com sucesso
                    fase2(personagem)  # Inicia a fase 2
            except Exception as e:
                print(f"Ocorreu um erro: {e}")
                tela_inicial()
                
        if criar_botao(botao_instrucao, botao_instrucao_sel, mascara_instrucao, mascara_instrucao_sel, 0, 150, acao="instrucoes"):
            instrucoes()
        
        if criar_botao(botao_sair, botao_sair_sel, mascara_sair, mascara_sair_sel, 0, 300, acao="sair"):
            pygame.quit()
            sys.exit()

        # Desenhar "select.png" no botão atualmente selecionado, se o mouse não estiver sobre nenhum
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