import pygame
import os
from config import LARGURA_TELA, ALTURA_TELA, TAMANHO_PERSONAGEM
import sys

# Caminho dos assets
caminho_assets = "D:/jogo/assets/images"

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
    vida_original = pygame.image.load(os.path.join(caminho_assets, 'vida5-5.png')).convert_alpha()
    moeda_original = pygame.image.load(os.path.join(caminho_assets, 'moeda.png')).convert_alpha()
    
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
    vida = pygame.transform.scale(vida_original, (escala * 4.5, escala * 4.5))
    moeda = pygame.transform.scale(moeda_original, (escala * 2.3, escala * 2.3))
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
        "cachorro": cachorro.get_rect()
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
    
    return (chao, parede, personagem_parado, animacao_andar, animacao_correr, ceu, janela, porta, maquina, maquina2, mesa, mesa_grande, computador1, computador2, gato, cachorro, relogio_figura, rects, animacao_figurante1, animacao_figurante2, animacao_figurante3, animacao_figurante4, vida, moeda)

def desenhar_repetido(tela, imagem, largura, altura, x_inicial=0, y_inicial=0):
    for x in range(x_inicial, x_inicial + largura, imagem.get_width()):
        for y in range(y_inicial, y_inicial + altura, imagem.get_height()):
            tela.blit(imagem, (x, y))

def desenhar_borda_horizontal(tela, cor, largura_tela, largura, y_pos):
    pygame.draw.rect(tela, cor, (0, y_pos, largura_tela, largura))

def mover_personagem(teclas, x, y, velocidade, direcao, tamanho_personagem, area_chao_horizontalmente_expandida, velocidade_correr, posicoes, rects, tela):
    novo_x, novo_y = x, y
    teclas_pressionadas = pygame.key.get_pressed()
    mesas = posicoes[14]
    
    if teclas[pygame.K_LSHIFT] or teclas[pygame.K_RSHIFT]:
        velocidade = velocidade_correr  # Aumentar a velocidade se Shift estiver pressionado

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

    # Criar o retângulo do personagem na nova posição
    rect_personagem = pygame.Rect(novo_x, novo_y, tamanho_personagem, tamanho_personagem)
    ponto = (novo_x + tamanho_personagem // 2, novo_y + tamanho_personagem // 2)
    
    if area_chao_horizontalmente_expandida.contains(rect_personagem):
        
        # Criar retângulos dos objetos para verificar colisão
        objetos = [
            'janela', 'janela2', 'porta', 'porta2', 
            'maquina', 'maquina2', 'mesa_grande', 'gato', 'cachorro', 'figurante1', 'figurante2', 'figurante3', 'figurante4'
        ]
        
        # Verificar colisão com objetos fixos
        colisao = False
        for obj in objetos:
            if obj in rects:  # Verificar se o objeto está na lista de retângulos
                obj_rect = rects[obj]
                # Ajustar retângulo do objeto fixo para a sua dimensão real
                retangulo_objeto = pygame.Rect(obj_rect.x, obj_rect.y, obj_rect.width, obj_rect.height)
                if retangulo_objeto.collidepoint(ponto):
                    if obj.startswith('porta') and teclas_pressionadas[pygame.K_e]:
                        resposta = mostrar_caixa_dialogo(tela)
                        if resposta == 'sim':
                            return None, None, None, True  # Indica que deve voltar à tela inicial
                    colisao = True
                    break
        
        # Verificar colisão com mesas
        retangulos_mesas = [pygame.Rect(mesa_x, mesa_y, rects['mesa'].width, rects['mesa'].height) for mesa_x, mesa_y in mesas]
        for rect_mesa in retangulos_mesas:
            if rect_mesa.collidepoint(ponto):
                colisao = True
                break
        
        # Se não houver colisão com qualquer objeto, atualizar a posição
        if not colisao:
            x, y = novo_x, novo_y
            
    return x, y, direcao, False

def mostrar_caixa_dialogo(screen):
    largura_tela, altura_tela = screen.get_size()
    
    # Definir o tamanho e a posição da caixa de diálogo
    largura_caixa = 400
    altura_caixa = 200
    x_caixa = (largura_tela - largura_caixa) // 2
    y_caixa = (altura_tela - altura_caixa) // 2
    
    fonte = pygame.font.Font(None, 36)
    texto = fonte.render("Deseja voltar para a tela inicial?", True, (255, 255, 255))
    
    # Desenhar caixa de diálogo
    caixa_dialogo = pygame.Rect(x_caixa, y_caixa, largura_caixa, altura_caixa)
    pygame.draw.rect(screen, (0, 0, 0), caixa_dialogo)  # Caixa preta
    pygame.draw.rect(screen, (255, 255, 255), caixa_dialogo, 2)  # Borda branca
    
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
    
    x_vida = - 10
    y_vida = - 100
    
    x_moeda = - 65
    y_moeda = - 10
    
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

        # Atualizar os rects com as posições fornecidas
    rects['janela'].topleft = (x_janela1, y_janela1)
    rects['janela2'].topleft = (x_janela2, y_janela2)
    rects['porta'].topleft = (x_porta1, y_porta1)
    rects['porta2'].topleft = (x_porta2, y_porta2)
    rects['maquina'].topleft = (x_maquina, y_maquina)
    rects['maquina2'].topleft = (x_maquina2, y_maquina2)
    rects['mesa_grande'].topleft = (x_mesa_grande, y_mesa_grande)
    rects['cachorro'].topleft = (x_cachorro, y_cachorro)
    rects['porta'].height = rects['porta'].height // 1.3
    rects['porta2'].height = rects['porta2'].height // 1.3
    # Criar e atualizar os retângulos das mesas e computadores
    retangulos_mesas = [pygame.Rect(mesa_x, mesa_y, rects['mesa'].width, rects['mesa'].height) for mesa_x, mesa_y in mesas]

    # Atualizar retângulos na lista de rects
    for i, rect_mesa in enumerate(retangulos_mesas):
        rects[f'mesa{i}'] = rect_mesa

    return (x_janela1, y_janela1, x_janela2, y_janela2, x_porta1, y_porta1, x_porta2, y_porta2,
            x_maquina, y_maquina, x_maquina2, y_maquina2, x_mesa_grande, y_mesa_grande, mesas, computadores, x_gato, y_gato, x_cachorro, y_cachorro, x_relogio, y_relogio, x_vida, y_vida, x_moeda, y_moeda), rects


def desenhar_cenario(tela, chao, parede, ceu, janela, porta, porta2, maquina, maquina2, mesa, mesa_grande, computador1, computador2, gato, cachorro, posicoes, altura_chao, relogio_figura, vida, moeda):
    
    
    (x_janela1, y_janela1, x_janela2, y_janela2, x_porta1, y_porta1, x_porta2, y_porta2,
     x_maquina, y_maquina, x_maquina2, y_maquina2, x_mesa_grande, y_mesa_grande, mesas, computadores, x_gato, y_gato, x_cachorro, y_cachorro, x_relogio, y_relogio, x_vida, y_vida, x_moeda, y_moeda) = posicoes

    tela.fill((0, 0, 0))

    desenhar_repetido(tela, chao, LARGURA_TELA, altura_chao, 0, ALTURA_TELA - altura_chao)
    desenhar_repetido(tela, parede, LARGURA_TELA, int(ALTURA_TELA * 0.2), 0, ALTURA_TELA - altura_chao - int(ALTURA_TELA * 0.2))
    tela.blit(ceu, (0, 0))

    tela.blit(relogio_figura, (x_relogio, y_relogio))
    
    tela.blit(janela, (x_janela1, y_janela1))
    tela.blit(janela, (x_janela2, y_janela2))

    tela.blit(porta, (x_porta1, y_porta1))
    tela.blit(porta2, (x_porta2, y_porta2))

    tela.blit(maquina, (x_maquina, y_maquina))
    tela.blit(maquina2, (x_maquina2, y_maquina2))

    for i, (x_mesa, y_mesa) in enumerate(mesas):
        tela.blit(mesa, (x_mesa, y_mesa))
        computador = computador1 if (i // 2) % 2 == 0 else computador2
        tela.blit(computador, (x_mesa + 5, y_mesa + 10))

    tela.blit(mesa_grande, (x_mesa_grande, y_mesa_grande))
    tela.blit(gato, (x_gato, y_gato))
    tela.blit(cachorro, (x_cachorro, y_cachorro))
    
    desenhar_borda_horizontal(tela, (100, 100, 100), LARGURA_TELA, 5, ALTURA_TELA - altura_chao - int(ALTURA_TELA * 0.2))
    
    tela.blit(vida, (x_vida, y_vida))
    tela.blit(moeda, (x_moeda, y_moeda))
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