import pygame
import os
from config import LARGURA_TELA, ALTURA_TELA, TAMANHO_PERSONAGEM
import sys
from personagem import *

pygame.init()

# Caminho dos assets
caminho_assets = "D:/jogo/assets/images"
CAMINHO_AUDIO = "D:\\jogo\\audios\\"

fonte_personalizada = pygame.font.Font('D:/jogo/fontes/Early GameBoy.ttf', 35)

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
    relogio_original = pygame.image.load(os.path.join(caminho_assets, 'relogio.png')).convert_alpha()
    chefe_original = pygame.image.load(os.path.join(caminho_assets, 'chefe.png')).convert_alpha()
    escrivaninha_original = pygame.image.load(os.path.join(caminho_assets, 'escrivaninha.png')).convert_alpha()
    caixa_dialogo_original = pygame.image.load(os.path.join(caminho_assets, 'caixadialogo2.png')).convert_alpha()
    emails = pygame.image.load(os.path.join(caminho_assets, 'emails.png')).convert_alpha()
    som_original = pygame.image.load(os.path.join(caminho_assets, 'som.png')).convert_alpha()
    som_mutado_original = pygame.image.load(os.path.join(caminho_assets, 'som_mutado.png')).convert_alpha()
    # Calcular escala com base na largura da tela
    escala = calcular_escala(LARGURA_TELA)
    
    # Escalar as imagens para o tamanho desejado
    chao = pygame.transform.scale(chao_original, (escala * 2.5, escala * 1.2))
    parede = pygame.transform.scale(parede_original, (escala * 1.0, escala * 1.0))
    personagem_parado = pygame.transform.scale(personagem_parado, (TAMANHO_PERSONAGEM - 20, TAMANHO_PERSONAGEM - 20))
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
    gato = pygame.transform.flip(gato, True, False)
    cachorro = pygame.transform.scale(cachorro_original, (escala * 0.7, escala * 0.5))
    relogio_figura = pygame.transform.scale(relogio_original, (escala * 0.5, escala * 0.3))
    chefe = pygame.transform.scale(chefe_original, (escala * 1.7, escala * 1.7))
    escrivaninha = pygame.transform.scale(escrivaninha_original, (escala * 1.7, escala * 1.7))
    caixa_dialogo = pygame.transform.scale(caixa_dialogo_original, (escala * 15.0, escala * 10.0))
    som = pygame.transform.scale(som_original, (som_original.get_width() // 5, som_original.get_height() // 5))
    som_mutado = pygame.transform.scale(som_mutado_original, (som_mutado_original.get_width() // 5, som_mutado_original.get_height() // 5))
    
    # Definir os rects
    rects = {
        "chao": chao.get_rect(),
        "parede": parede.get_rect(),
        "janela": janela.get_rect(),
        "janela2": janela.get_rect(),
        "porta": porta.get_rect(),
        "porta2": porta.get_rect(),
        "maquina": maquina.get_rect(),
        "maquina2": maquina2.get_rect(),
        "mesa": mesa.get_rect(),
        "mesa_grande": mesa_grande.get_rect(),
        "computador1": computador1.get_rect(),
        "computador2": computador2.get_rect(),
        "gato": gato.get_rect(),
        "cachorro": cachorro.get_rect(),
        "chefe" : chefe.get_rect(),
        'escrivaninha' : escrivaninha.get_rect(),
        'som' : som.get_rect()
    }
    
    # Carregar animações de andar e correr
    animacao_andar = [
        pygame.transform.scale(pygame.image.load(os.path.join(caminho_assets, f"personagem_andando{i}.png")).convert_alpha(), (TAMANHO_PERSONAGEM, TAMANHO_PERSONAGEM))
        for i in range(1, 9)
    ]

    animacao_correr = [
        pygame.transform.scale(pygame.image.load(os.path.join(caminho_assets, f"personagem_correndo{i}.png")).convert_alpha(), (TAMANHO_PERSONAGEM, TAMANHO_PERSONAGEM))
        for i in range(1, 9)
    ]
    
    animacao_figurante1 = [
        pygame.transform.scale(pygame.image.load(os.path.join(caminho_assets, f"figurante1esperando{i}.png")).convert_alpha(), (TAMANHO_PERSONAGEM, TAMANHO_PERSONAGEM))
        for i in range(1, 7) 
    ]
    
    animacao_figurante2 = [
        pygame.transform.scale(pygame.image.load(os.path.join(caminho_assets, f"figurante2esperando{i}.png")).convert_alpha(), (TAMANHO_PERSONAGEM, TAMANHO_PERSONAGEM))
        for i in range(1, 7) 
    ]
    
    animacao_figurante3 = [
        pygame.transform.scale(pygame.image.load(os.path.join(caminho_assets, f"figurante3esperando{i}.png")).convert_alpha(), (TAMANHO_PERSONAGEM, TAMANHO_PERSONAGEM))
        for i in range(1, 7) 
    ]
        
    animacao_figurante4 = [
        pygame.transform.scale(pygame.image.load(os.path.join(caminho_assets, f"figurante4esperando{i}.png")).convert_alpha(), (TAMANHO_PERSONAGEM, TAMANHO_PERSONAGEM))
        for i in range(1, 7) 
    ]

    # Carregar imagem do céu
    ceu_original = pygame.image.load(os.path.join(caminho_assets, "ceu.png")).convert()
    ceu = pygame.transform.scale(ceu_original, (LARGURA_TELA, int(ALTURA_TELA * 0.1)))
    
    return (chao, parede, personagem_parado, animacao_andar, animacao_correr, ceu, janela, porta, maquina, maquina2, mesa, mesa_grande, computador1, computador2, gato, cachorro,
            relogio_figura, rects, animacao_figurante1, animacao_figurante2, animacao_figurante3, animacao_figurante4, chefe, escrivaninha, caixa_dialogo, emails, som, som_mutado)
   
def carregar_assets_menu():
    escala = calcular_escala(LARGURA_TELA)
    menu = pygame.image.load(os.path.join(caminho_assets, 'menu.png')).convert_alpha()
    largura_menu, altura_menu = 502, 128
    menu = pygame.transform.scale(menu, (largura_menu, altura_menu))
    # Carregar as imagens de vida
    vida_imgs = [
        pygame.image.load(os.path.join(caminho_assets, f'vida{i}-5.png')).convert_alpha() for i in range(5, -1, -1)
    ]
    moeda_original = pygame.image.load(os.path.join(caminho_assets, 'moeda.png')).convert_alpha()
    # Carregar as imagens de vida, se necessário, escalando de acordo com a tela
    vida_imgs = [pygame.transform.scale(img, (escala * 4.5, escala * 4.5)) for img in vida_imgs]
    
    # Escalar a imagem da moeda
    moeda_img = pygame.transform.scale(moeda_original, (escala * 2.3, escala * 2.3))
    
    return(menu, vida_imgs, moeda_img)

def carregar_menu(tela, personagem_atributos, fonte):
    menu, vida_imgs, moeda_img = carregar_assets_menu()
    
    # Posições do menu
    x_menu = -10  # Ajuste conforme necessário
    y_menu = -10  # Ajuste conforme necessário
    
    # Desenhar o menu na tela
    tela.blit(menu, (x_menu, y_menu))
    
    # Desenhar a vida atual sobre o menu
    x_vida = x_menu + 60
    y_vida = y_menu - 90
    vida_index = max(0, min(5, 5 - personagem_atributos.vidas))  # Índice da vida atual
    tela.blit(vida_imgs[vida_index], (x_vida, y_vida))

    # Desenhar a quantidade de moedas sobre o menu
    x_moeda = x_menu + 240  # Ajustar conforme necessário
    y_moeda = y_vida + 40
    tela.blit(moeda_img, (x_moeda, y_moeda))

    # Calcular a posição do texto das moedas
    pos_texto_moedas = (x_moeda + moeda_img.get_width() - 85, y_moeda + 95)
    largura_texto_moedas = fonte.size(str(personagem_atributos.dinheiro))[0]
    altura_texto_moedas = fonte.get_height()  # Altura do texto

    tela.fill((65, 166, 246), (pos_texto_moedas[0], pos_texto_moedas[1], largura_texto_moedas, altura_texto_moedas))  # Preenche com a cor especificada

    # Desenhar o novo texto das moedas
    texto_moedas = fonte.render(str(personagem_atributos.dinheiro), True, (0, 0, 0))  # Texto em preto
    tela.blit(texto_moedas, pos_texto_moedas)
    
def desenhar_repetido(tela, imagem, largura, altura, x_inicial=0, y_inicial=0):
    for x in range(x_inicial, x_inicial + largura, imagem.get_width()):
        for y in range(y_inicial, y_inicial + altura, imagem.get_height()):
            tela.blit(imagem, (x, y))

def desenhar_borda_horizontal(tela, cor, largura_tela, largura, y_pos):
    pygame.draw.rect(tela, cor, (0, y_pos, largura_tela, largura))

def pausar_jogo_mensagem(tela, mensagem):
    fonte = pygame.font.SysFont('Arial', 25)
    texto = fonte.render(mensagem, True, (0, 0, 0))  # Texto em vermelho
    texto_rect = texto.get_rect(center=(LARGURA_TELA // 2, (ALTURA_TELA // 2) - 400))  # Centraliza o texto na tela

    # Loop para pausar o jogo
    pausado = True
    while pausado:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

            if evento.type == pygame.KEYDOWN:  # Verifica se alguma tecla foi pressionada
                pausado = False  # Sai do loop

        # Desenha a mensagem na tela
        tela.blit(texto, texto_rect)  # Desenha o texto
        pygame.display.flip()  # Atualiza a tela
        
def pausar_jogo_imagem(tela, img):
    pausado = True
    while pausado:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

            if evento.type == pygame.KEYDOWN:  # Verifica se alguma tecla foi pressionada
                pausado = False  # Sai do loop ao pressionar qualquer tecla

        # Desenha a imagem dos emails no canto superior esquerdo sem limpar a tela
        tela.blit(img, (1375, 10))  # Desenha a imagem na posição desejada
        pygame.display.flip()  # Atualiza a tela
        
def mover_personagem(teclas, x, y, velocidade, direcao, tamanho_personagem, area_chao_horizontalmente_expandida, velocidade_correr, posicoes, rects, tela, personagem):
    novo_x, novo_y = x, y
    teclas_pressionadas = pygame.key.get_pressed()
    mesas = posicoes[14]
    iniciar_minigame = False
    if teclas[pygame.K_LSHIFT] or teclas[pygame.K_RSHIFT]:
        velocidade = velocidade_correr

    if teclas[pygame.K_UP] or teclas[pygame.K_w]:
        novo_y -= velocidade
    if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
        novo_y += velocidade
    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        novo_x -= velocidade
        direcao = "esquerda"
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        novo_x += velocidade
        direcao = "direita"

    rect_personagem = pygame.Rect(novo_x, novo_y, tamanho_personagem, tamanho_personagem)
    ponto = (novo_x + tamanho_personagem // 2, novo_y + tamanho_personagem // 2)
    
    if area_chao_horizontalmente_expandida.contains(rect_personagem):
        objetos = ['janela', 'janela2', 'porta', 'porta2', 
                   'maquina', 'maquina2', 'mesa_grande', 
                   'gato', 'cachorro', 'escrivaninha', 
                   'chefe', 'figurante1', 'figurante2', 
                   'figurante3', 'figurante4']
        
        colisao = False
        dialogos = {
            'figurante1': 'figurante1',
            'figurante2': 'figurante2',
            'figurante3': 'figurante3',
            'figurante4': 'figurante4',
            'chefe': 'chefe'
        }

        for obj in objetos:
            if obj in rects:
                obj_rect = rects[obj]
                retangulo_objeto = pygame.Rect(obj_rect.x, obj_rect.y, obj_rect.width, obj_rect.height)
                retangulo_expandido = retangulo_objeto.inflate(retangulo_objeto.width * 0.2, retangulo_objeto.height * 0.2)
                if retangulo_objeto.collidepoint(ponto):
                    colisao = True
                    if obj.startswith('porta') and teclas_pressionadas[pygame.K_e]:
                        resposta = mostrar_caixa_dialogo(tela)
                        if resposta == 'sim':
                            return None, None, None, True, False, iniciar_minigame
                    if obj in dialogos and teclas_pressionadas[pygame.K_e]:
                        return x, y, direcao, False, dialogos[obj],  iniciar_minigame

                    if obj == 'escrivaninha' and teclas_pressionadas[pygame.K_e]:
                        if "emails" in personagem.objetos:
                            pausar_jogo_mensagem(tela, 'Você já possui a lista de e-mails! Pressione "F" para visualizá-la quando estiver em seu computador.')
                        else:
                            personagem.adicionar_objeto("emails")
                            pausar_jogo_mensagem(tela, 'Você adquiriu a lista de e-mails válidos! Pressione "F" para visualizá-la quando estiver em seu computador.')
                    
                    if obj in ['maquina', 'maquina2'] and personagem.dinheiro >= 30 and teclas_pressionadas[pygame.K_e]:
                        if obj == 'maquina':
                            personagem.adicionar_objeto("petisco cachorro")
                            pausar_jogo_mensagem(tela, 'Você adquiriu o petisco para cachorro!')
                        else:
                            personagem.adicionar_objeto("petisco gato")
                            pausar_jogo_mensagem(tela, 'Você adquiriu o petisco para gato!')
                        personagem.remover_dinheiro(30)

                    if obj == 'cachorro' and teclas_pressionadas[pygame.K_e]:
                        if "petisco cachorro" in personagem.objetos and personagem.vidas < 5:
                            personagem.ganhar_vida()
                            personagem.objetos.remove("petisco cachorro")
                            pygame.mixer.Sound(CAMINHO_AUDIO + "cachorro.wav").play()
                            pausar_jogo_mensagem(tela, 'Você ganhou 1 ponto de vida!')

                    if obj == 'mesa_grande' and teclas_pressionadas[pygame.K_e]:
                        if "petisco gato" in personagem.objetos and personagem.vidas < 5:
                            personagem.ganhar_vida()
                            personagem.objetos.remove("petisco gato")
                            pygame.mixer.Sound(CAMINHO_AUDIO + "gato.mp3").play()
                            pausar_jogo_mensagem(tela, 'Você ganhou 1 ponto de vida!')      
                    break
                
                # Verifique se o personagem está próximo do objeto
                elif retangulo_expandido.collidepoint(ponto):
                    if obj.startswith('porta') and teclas_pressionadas[pygame.K_e]:
                        resposta = mostrar_caixa_dialogo(tela)
                        if resposta == 'sim':
                            return None, None, None, True, False, iniciar_minigame
                    if obj in dialogos and teclas_pressionadas[pygame.K_e]:
                        return x, y, direcao, False, dialogos[obj],  iniciar_minigame

                    if obj == 'escrivaninha' and teclas_pressionadas[pygame.K_e]:
                        if "emails" in personagem.objetos:
                            pausar_jogo_mensagem(tela, 'Você já possui a lista de e-mails! Pressione "F" para visualizá-la quando estiver em seu computador.')
                        else:
                            personagem.adicionar_objeto("emails")
                            pausar_jogo_mensagem(tela, 'Você adquiriu a lista de e-mails válidos! Pressione "F" para visualizá-la quando estiver em seu computador.')
                    
                    if obj in ['maquina', 'maquina2'] and personagem.dinheiro >= 30 and teclas_pressionadas[pygame.K_e]:
                        if obj == 'maquina':
                            personagem.adicionar_objeto("petisco cachorro")
                            pausar_jogo_mensagem(tela, 'Você adquiriu o petisco para cachorro!')
                        else:
                            personagem.adicionar_objeto("petisco gato")
                            pausar_jogo_mensagem(tela, 'Você adquiriu o petisco para gato!')
                        personagem.remover_dinheiro(30)

                    if obj == 'cachorro' and teclas_pressionadas[pygame.K_e]:
                        if "petisco cachorro" in personagem.objetos and personagem.vidas < 5:
                            personagem.ganhar_vida()
                            personagem.objetos.remove("petisco cachorro")
                            pygame.mixer.Sound(CAMINHO_AUDIO + "cachorro.wav").play()
                            pausar_jogo_mensagem(tela, 'Você ganhou 1 ponto de vida!')

                    if obj == 'mesa_grande' and teclas_pressionadas[pygame.K_e]:
                        if "petisco gato" in personagem.objetos and personagem.vidas < 5:
                            personagem.ganhar_vida()
                            personagem.objetos.remove("petisco gato")
                            pygame.mixer.Sound(CAMINHO_AUDIO + "gato.mp3").play()
                            pausar_jogo_mensagem(tela, 'Você ganhou 1 ponto de vida!')                
    
        # Verificar colisão com mesas
        retangulos_mesas = [pygame.Rect(mesa_x, mesa_y, rects['mesa'].width, rects['mesa'].height) for mesa_x, mesa_y in mesas]
        retangulo_expandido_mesa5 = retangulos_mesas[5].inflate(retangulos_mesas[5].width * 0.5, retangulos_mesas[5].height * 0.5)
        for i, rect_mesa in enumerate(retangulos_mesas):
            # Verificar colisão com o retângulo normal
            if rect_mesa.collidepoint(ponto):
                if i == 5 and teclas_pressionadas[pygame.K_e]: 
                    iniciar_minigame = True
                    return x, y, direcao, False, None, iniciar_minigame
                colisao = True
                break

        # Verificar colisão expandida apenas para a mesa de índice 5
        if retangulo_expandido_mesa5.collidepoint(ponto):
            if teclas_pressionadas[pygame.K_e]: 
                iniciar_minigame = True
                return x, y, direcao, False, None, iniciar_minigame
            
        if not colisao:
            x, y = novo_x, novo_y
            
    return x, y, direcao, False, None, iniciar_minigame

def mostrar_caixa_dialogo(screen):
    largura_tela, altura_tela = screen.get_size()
    
    # Definir o tamanho e a posição da caixa de diálogo
    largura_caixa = 400
    altura_caixa = 200
    x_caixa = (largura_tela - largura_caixa) // 2
    y_caixa = ((altura_tela - altura_caixa) // 2) - 100
    
    # Fonte para o texto
    fonte = pygame.font.Font(None, 36)
    texto = fonte.render("Deseja voltar para a tela inicial?", True, (0, 0, 0))  # Texto preto
    
    # Desenhar caixa de diálogo
    caixa_dialogo = pygame.Rect(x_caixa, y_caixa, largura_caixa, altura_caixa)
    pygame.draw.rect(screen, (247, 236, 182), caixa_dialogo)  # Caixa com cor 247, 236, 182
    pygame.draw.rect(screen, (84, 47, 28), caixa_dialogo, 5)  # Borda com cor 84, 47, 28
    
    # Desenhar o texto da mensagem
    screen.blit(texto, (x_caixa + (largura_caixa - texto.get_width()) // 2, y_caixa + 30))
    
    fonte_opcao = pygame.font.Font(None, 28)
    texto_sim = fonte_opcao.render('Sim', True, (255, 255, 255))
    texto_nao = fonte_opcao.render('Não', True, (255, 255, 255))
    
    # Definir a posição dos botões
    largura_botao = 100
    altura_botao = 50
    x_botao_sim = x_caixa + (largura_caixa - 2 * largura_botao - 20) // 2
    x_botao_nao = x_botao_sim + largura_botao + 20
    y_botao = y_caixa + altura_caixa - 80
    
    botao_sim = pygame.Rect(x_botao_sim, y_botao, largura_botao, altura_botao)
    botao_nao = pygame.Rect(x_botao_nao, y_botao, largura_botao, altura_botao)
    
    # Desenhar os botões
    pygame.draw.rect(screen, (0, 255, 0), botao_sim)  # Botão verde para "Sim"
    pygame.draw.rect(screen, (255, 0, 0), botao_nao)  # Botão vermelho para "Não"
    
    # Desenhar as bordas dos botões
    pygame.draw.rect(screen, (0, 0, 0), botao_sim, 2)  # Borda preta para o botão "Sim"
    pygame.draw.rect(screen, (0, 0, 0), botao_nao, 2)  # Borda preta para o botão "Não"
    
    # Desenhar o texto dos botões
    screen.blit(texto_sim, (x_botao_sim + (largura_botao - texto_sim.get_width()) // 2, y_botao + (altura_botao - texto_sim.get_height()) // 2))
    screen.blit(texto_nao, (x_botao_nao + (largura_botao - texto_nao.get_width()) // 2, y_botao + (altura_botao - texto_nao.get_height()) // 2))
    
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if botao_sim.collidepoint(pos):
                    return 'sim'
                elif botao_nao.collidepoint(pos):
                    return 'não'


def carregar_assets():
    return carregar_imagens(caminho_assets)

def inicializar_posicoes():
    x_personagem = LARGURA_TELA // 3 - TAMANHO_PERSONAGEM // 3
    y_personagem = ALTURA_TELA // 3 - TAMANHO_PERSONAGEM // 3
    return x_personagem, y_personagem

def definir_areas_chao():
    altura_chao = int(ALTURA_TELA * 0.7)
    area_chao = pygame.Rect(0, ALTURA_TELA - altura_chao, LARGURA_TELA, altura_chao)
    area_chao_horizontalmente_expandida = area_chao.inflate(int(LARGURA_TELA * 0.1), int(LARGURA_TELA * 0.08))
    return altura_chao, area_chao_horizontalmente_expandida

def definir_posicoes_objetos(altura_chao, rects):
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

    ajuste_horizontal =  - 175
    espaco_horizontal = 200
    espaco_vertical = 200

    x_relogio = x_porta1 - 25
    y_relogio = y_porta1 - 40
    
    x_som = 1800
    y_som = 20
    
    mesas = [
        # Bloco 1 (Canto Esquerdo)
        (LARGURA_TELA // 6 - espaco_horizontal - 75 - ajuste_horizontal, ALTURA_TELA - altura_chao + espaco_vertical),
        (LARGURA_TELA // 6 - espaco_horizontal - 75 - ajuste_horizontal, ALTURA_TELA - altura_chao + espaco_vertical + 100),
        (LARGURA_TELA // 6 - espaco_horizontal - 75 + 100 - ajuste_horizontal, ALTURA_TELA - altura_chao + espaco_vertical + 100),
        (LARGURA_TELA // 6 - espaco_horizontal - 75 + 100 - ajuste_horizontal, ALTURA_TELA - altura_chao + espaco_vertical),
        
        (LARGURA_TELA // 6 - espaco_horizontal - 75 - ajuste_horizontal, ALTURA_TELA - altura_chao + 2 * espaco_vertical),
        (LARGURA_TELA // 6 - espaco_horizontal - 75 - ajuste_horizontal, ALTURA_TELA - altura_chao + 2 * espaco_vertical + 100),
        (LARGURA_TELA // 6 - espaco_horizontal - 75 + 100 - ajuste_horizontal, ALTURA_TELA - altura_chao + 2 * espaco_vertical + 100),
        (LARGURA_TELA // 6 - espaco_horizontal - 75 + 100 - ajuste_horizontal, ALTURA_TELA - altura_chao + 2 * espaco_vertical),

        # Bloco 2 (Central)
        (LARGURA_TELA // 2 - espaco_horizontal - 75 - ajuste_horizontal, ALTURA_TELA - altura_chao + espaco_vertical),
        (LARGURA_TELA // 2 - espaco_horizontal - 75 - ajuste_horizontal, ALTURA_TELA - altura_chao + espaco_vertical + 100),
        (LARGURA_TELA // 2 - espaco_horizontal - 75 + 100 - ajuste_horizontal, ALTURA_TELA - altura_chao + espaco_vertical + 100),
        (LARGURA_TELA // 2 - espaco_horizontal - 75 + 100 - ajuste_horizontal, ALTURA_TELA - altura_chao + espaco_vertical),
        
        (LARGURA_TELA // 2 - espaco_horizontal - 75 - ajuste_horizontal, ALTURA_TELA - altura_chao + 2 * espaco_vertical),
        (LARGURA_TELA // 2 - espaco_horizontal - 75 - ajuste_horizontal, ALTURA_TELA - altura_chao + 2 * espaco_vertical + 100),
        (LARGURA_TELA // 2 - espaco_horizontal - 75 + 100 - ajuste_horizontal, ALTURA_TELA - altura_chao + 2 * espaco_vertical + 100),
        (LARGURA_TELA // 2 - espaco_horizontal - 75 + 100 - ajuste_horizontal, ALTURA_TELA - altura_chao + 2 * espaco_vertical),

        # Bloco 3 (Canto Direito)
        (LARGURA_TELA * 5 // 6 - espaco_horizontal - 75 - ajuste_horizontal, ALTURA_TELA - altura_chao + espaco_vertical),
        (LARGURA_TELA * 5 // 6 - espaco_horizontal - 75 - ajuste_horizontal, ALTURA_TELA - altura_chao + espaco_vertical + 100),
        (LARGURA_TELA * 5 // 6 - espaco_horizontal - 75 + 100 - ajuste_horizontal, ALTURA_TELA - altura_chao + espaco_vertical + 100),
        (LARGURA_TELA * 5 // 6 - espaco_horizontal - 75 + 100 - ajuste_horizontal, ALTURA_TELA - altura_chao + espaco_vertical),
        
        (LARGURA_TELA * 5 // 6 - espaco_horizontal - 75 - ajuste_horizontal, ALTURA_TELA - altura_chao + 2 * espaco_vertical),
        (LARGURA_TELA * 5 // 6 - espaco_horizontal - 75 - ajuste_horizontal, ALTURA_TELA - altura_chao + 2 * espaco_vertical + 100),
        (LARGURA_TELA * 5 // 6 - espaco_horizontal - 75 + 100 - ajuste_horizontal, ALTURA_TELA - altura_chao + 2 * espaco_vertical + 100),
        (LARGURA_TELA * 5 // 6 - espaco_horizontal - 75 + 100 - ajuste_horizontal, ALTURA_TELA - altura_chao + 2 * espaco_vertical),
    ]
    computadores = [(mesa[0] + 5, mesa[1] + 10) for mesa in mesas]
    
    x_gato = x_mesa_grande + 50
    y_gato = y_mesa_grande - 10

    x_cachorro = x_maquina2 + 150
    y_cachorro = y_maquina2 + 90
    
    x_chefe = x_cachorro + 310
    y_chefe = y_cachorro - 80

    x_escrivaninha = x_mesa_grande - 200
    y_escrivaninha = y_chefe
    
        # Atualizar os rects com as posições fornecidas
    rects['janela'].topleft = (x_janela1, y_janela1)
    rects['janela2'].topleft = (x_janela2, y_janela2)
    rects['porta'].topleft = (x_porta1, y_porta1)
    rects['porta2'].topleft = (x_porta2, y_porta2)
    rects['maquina'].topleft = (x_maquina, y_maquina)
    rects['maquina2'].topleft = (x_maquina2, y_maquina2)
    rects['mesa_grande'].topleft = (x_mesa_grande, y_mesa_grande)
    rects['cachorro'].topleft = (x_cachorro, y_cachorro)
    rects['chefe'].topleft = (x_chefe + 30 , y_chefe)
    rects['chefe'].height = rects['chefe'].height // 1.3
    rects['chefe'].width = rects['chefe'].width // 1.3
    rects['porta2'].height = rects['porta2'].height // 1.3
    rects['porta'].height = rects['porta'].height // 1.3
    rects['escrivaninha'].topleft = (x_escrivaninha + 30, y_escrivaninha)
    rects['escrivaninha'].height = rects['escrivaninha'].height // 1.3
    rects['escrivaninha'].width = rects['escrivaninha'].width // 1.5
    rects['som'].topleft = (x_som, y_som)
    # Criar e atualizar os retângulos das mesas e computadores
    retangulos_mesas = [pygame.Rect(mesa_x, mesa_y, rects['mesa'].width, rects['mesa'].height) for mesa_x, mesa_y in mesas]

    # Atualizar retângulos na lista de rects
    for i, rect_mesa in enumerate(retangulos_mesas):
        rects[f'mesa{i}'] = rect_mesa

    return (x_janela1, y_janela1, x_janela2, y_janela2, x_porta1, y_porta1, x_porta2, y_porta2,
            x_maquina, y_maquina, x_maquina2, y_maquina2, x_mesa_grande, y_mesa_grande, mesas, computadores, x_gato, y_gato, 
            x_cachorro, y_cachorro, x_relogio, y_relogio, x_chefe, y_chefe, x_escrivaninha, y_escrivaninha, x_som, y_som), rects

def desenhar_cenario(tela, chao, parede, ceu, janela, porta, porta2, maquina, maquina2, mesa, mesa_grande, computador1,
                     computador2, gato, cachorro, posicoes, altura_chao, relogio_figura, chefe, escrivaninha, som, som_mutado, flag_som):
    
    (x_janela1, y_janela1, x_janela2, y_janela2, x_porta1, y_porta1, x_porta2, y_porta2,
     x_maquina, y_maquina, x_maquina2, y_maquina2, x_mesa_grande, y_mesa_grande, mesas, computadores, x_gato, y_gato, 
     x_cachorro, y_cachorro, x_relogio, y_relogio, x_chefe, y_chefe, x_escrivaninha, y_escrivaninha, x_som, y_som) = posicoes

    # Limpar a tela com uma cor de fundo (preto)
    tela.fill((0, 0, 0))

    # Desenhar o chão e as paredes repetidamente
    desenhar_repetido(tela, chao, LARGURA_TELA, altura_chao, 0, ALTURA_TELA - altura_chao)
    desenhar_repetido(tela, parede, LARGURA_TELA, int(ALTURA_TELA * 0.2), 0, ALTURA_TELA - altura_chao - int(ALTURA_TELA * 0.2))
    tela.blit(ceu, (0, 0))

    # Desenhar os objetos do cenário
    tela.blit(relogio_figura, (x_relogio, y_relogio))
    tela.blit(janela, (x_janela1, y_janela1))
    tela.blit(janela, (x_janela2, y_janela2))
    tela.blit(porta, (x_porta1, y_porta1))
    tela.blit(porta2, (x_porta2, y_porta2))
    tela.blit(maquina, (x_maquina, y_maquina))
    tela.blit(maquina2, (x_maquina2, y_maquina2))

    if flag_som:
        tela.blit(som, (x_som, y_som))
    else:
        tela.blit(som_mutado, (x_som, y_som))
        
    # Desenhar as mesas e os computadores
    for i, (x_mesa, y_mesa) in enumerate(mesas):
        tela.blit(mesa, (x_mesa, y_mesa))
        # Alterna entre computador1 e computador2 para cada par de mesas
        computador = computador1 if (i // 2) % 2 == 0 else computador2
        tela.blit(computador, (x_mesa + 5, y_mesa + 10))

    # Desenhar outros objetos do cenário
    tela.blit(mesa_grande, (x_mesa_grande, y_mesa_grande))
    tela.blit(gato, (x_gato, y_gato))
    tela.blit(cachorro, (x_cachorro, y_cachorro))
    tela.blit(chefe, (x_chefe, y_chefe))
    tela.blit(escrivaninha, (x_escrivaninha, y_escrivaninha))

    # Desenhar uma borda horizontal
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