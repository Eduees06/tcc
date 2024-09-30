import pygame
import sys
from config import *
from utils import *
import time
from personagem import *
from minigame1 import *


# Caminho dos assets
caminho_assets = "D:/jogo/assets/images"
CAMINHO_AUDIO = "D:\\jogo\\audios\\"

# Inicialize o Pygame
pygame.init()

PRETO = (0, 0, 0)

# Defina a fonte
fonte_dialogo = pygame.font.SysFont('Arial', 35)

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

def exibir_dialogo(tela, caixa_dialogo, falas, som_dialogo, fonte, cor):
    largura_tela, altura_tela = tela.get_size()
    
    # Calcula a posição da caixa de diálogo para ficar centralizada na parte inferior
    rect_caixa = caixa_dialogo.get_rect()
    rect_caixa.centerx = largura_tela // 2  # Centraliza horizontalmente
    rect_caixa.bottom = altura_tela + 150    # Posiciona 20px acima da parte inferior da tela

    for fala in falas:
        # Toca o som do diálogo
        som_dialogo.play()

        # Quebra o texto em linhas
        linhas = []
        palavras = fala.split(' ')
        linha_atual = ""
        largura_limite = rect_caixa.width - 100

        for palavra in palavras:
            if fonte.size(linha_atual + palavra)[0] < largura_limite:
                linha_atual += palavra + ' '
            else:
                linhas.append(linha_atual.strip())
                linha_atual = palavra + ' '

        if linha_atual:
            linhas.append(linha_atual.strip())

        # Limpa a tela e desenha a caixa de diálogo
        tela.blit(caixa_dialogo, rect_caixa)
        pygame.display.flip()

        # Define o espaço entre as linhas
        espaco_entre_linhas = 10

        avancar_fala = False

        for i, linha in enumerate(linhas):
            texto_atual = ""
            for letra in linha:
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_RETURN or evento.key == pygame.K_SPACE:
                            avancar_fala = True
                            break
                if avancar_fala:
                    break

                texto_atual += letra
                texto_renderizado = fonte.render(texto_atual, True, cor)

                # Ajusta a posição do texto renderizado
                rect_texto = texto_renderizado.get_rect(topleft=(rect_caixa.x + 50, rect_caixa.y + 550 + i * (30 + espaco_entre_linhas)))
                tela.blit(texto_renderizado, rect_texto)
                pygame.display.update()

                time.sleep(0.02)

            if avancar_fala:
                break

            time.sleep(0.1)

        som_dialogo.stop()

        texto_instrucao = "(aperte Enter/espaço para avançar)"
        texto_renderizado_instrucao = fonte.render(texto_instrucao, True, cor)

        rect_instrucao = texto_renderizado_instrucao.get_rect(center=(rect_caixa.centerx, rect_caixa.bottom - 220))
        tela.blit(texto_renderizado_instrucao, rect_instrucao)
        pygame.display.flip()

        while not avancar_fala:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN or evento.key == pygame.K_SPACE:
                        avancar_fala = True
                        tela.blit(caixa_dialogo, rect_caixa)
                        pygame.display.flip()

    
def mostrar_instrucoes(tela):
    # Carregar a imagem de instruções
    instrucoes_img = pygame.image.load(caminho_assets + '/instrucoes.png')
    
    # Obtém o retângulo da tela para centralizar a imagem
    rect_instrucoes = instrucoes_img.get_rect(center=(tela.get_width() // 2, tela.get_height() // 2))
    
    # Exibe a imagem de instruções sobre a tela atual
    tela.blit(instrucoes_img, rect_instrucoes)
    pygame.display.flip()

    # Espera até que o jogador aperte Enter
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:  # Verifica se a tecla Enter foi pressionada
                    esperando = False  # Sai do loop ao pressionar Enter
                
def fase1():
    
    tela, relogio = inicializar_jogo()
    (chao, parede, personagem_parado, animacao_andar, animacao_correr, ceu, janela, porta, maquina, maquina2, mesa, mesa_grande, computador1, 
     computador2, gato, cachorro, relogio_figura, rects, animacao_figurante1, animacao_figurante2, animacao_figurante3, animacao_figurante4, chefe, escrivaninha, caixa_dialogo, emails, som, som_mutado) = carregar_assets()
    # Inicializar vidas
    personagem_atributos = Personagem(vidas=5, dinheiro= 0)
    x_personagem, y_personagem = inicializar_posicoes()
    altura_chao, area_chao_horizontalmente_expandida = definir_areas_chao()
    posicoes, rects = definir_posicoes_objetos(altura_chao, rects)
    # Configurações da música de fundo
    pygame.mixer.music.load(CAMINHO_AUDIO + "background.mp3")
    pygame.mixer.music.set_volume(0.05)
    pygame.mixer.music.play(-1)  # -1 para repetir indefinidamente
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

    dialogo_chefe = [
        "Chefe: Bem-vindo ao seu primeiro dia na Plunder Drifflin Co! Estamos animados em tê-lo aqui.",
        "Chefe: Nossa empresa é especializada na compra e venda de itens, e seu papel é fundamental para nosso sucesso.",
        "Chefe: Sua primeira missão é responder a alguns e-mails que deixei na sua mesa. Eles contêm informações importantes para você começar.",
        "Chefe: Mas antes de tudo, converse com seus colegas de trabalho! Eles poderão te mostrar onde fica seu computador e dar algumas dicas úteis sobre como funcionamos aqui.",
        "Chefe: Ah, e uma dica importante sobre e-mails: fique sempre alerta para tentativas de golpe, especialmente o que chamamos de phishing.",
        "Chefe: Phishing é quando alguém tenta se passar por uma empresa legítima para roubar suas informações. Então, sempre verifique quem está enviando o e-mail antes de clicar em qualquer link.",
        "Chefe: Se um e-mail parecer muito bom para ser verdade ou vier com um senso de urgência, é melhor desconfiar! E-mails com anexos também podem ser perigosos.",
        "Chefe: Para te ajudar, deixei uma lista de e-mails confiáveis na escrivaninha. Isso vai facilitar na hora de identificar o que é seguro. Depois de responder os e-mails, volte aqui e me avise!"
    ]
    dialogo_chefe_completou_minigame_cheio = [
        "Chefe: Ótimo trabalho em responder os e-mails! Agora você está pronto para enfrentar os desafios do dia a dia.",
        "Chefe: Não esqueça das dicas que mencionei. Elas serão úteis em sua jornada aqui na Plunder Drifflin Co!",
        "Chefe: Acabaram suas tarefas por hoje, até amanhã!"
    ]

    dialogo_chefe_completou_minigame_baixo = [
    "Chefe: Vejo que você caiu em alguns e-mails falsos. É importante ter cuidado com essas armadilhas!",
    "Chefe: Lembre-se das dicas que mencionei. Elas são cruciais para navegar neste ambiente.",
    "Chefe: Mesmo assim, bom trabalho! Acabaram suas tarefas por hoje, até amanhã! E não esqueça de descansar."
    ]
    
    dialogos_figurantes = {
        'figurante1': [
            "Arthur: Bem-vindo! Eu sou o Arthur, sou alérgico a gatos, mas aqui estou eu, trabalhando ao lado de um—quem precisa de ar fresco, não é mesmo?",
            "Arthur: O seu computador? é a última máquina desta fileira! Espero que ela não tenha uma 'crise de identidade', como a maioria dos nossos computadores!"
        ],
        'figurante2': [
            "Ana: Não me deixe começar a falar sobre e-mails suspeitos! Já caí em algumas armadilhas por causa deles. Uma vez, recebi um e-mail que parecia legítimo, mas o endereço tinha um erro de digitação que eu não percebi.",
            "Ana: Acredite, os golpistas são espertos! Às vezes, é só uma letra que muda, como 'com' no lugar de 'con'.",
            "Ana: Fique esperto! Sempre cheque o endereço antes de clicar. Pode fazer toda a diferença!"
        ],
        'figurante3': [
            "Lorena: Oi, você viu nossos amigos de quatro patas por aqui? O cachorro ali adora os petiscos que ficam naquela máquina perto do gato, e o gato, bem, ele não consegue resistir aos petiscos da outra máquina",
            "Lorena: Sabe, é curioso... Eu realmente não entendo por que eles ficam tão distantes das máquinas que vendem as comidas que eles gostam! Você acha que eles estão tentando nos pregar uma peça?",
            "Lorena: Ah, e se você tiver 30 moedas, pode comprar uns petiscos para eles. Garanto que vão ficar super felizes! Pode ser uma boa forma de conquistar a confiança deles, quem sabe?"

        ],
        'figurante4': [
            "Matheus: Hmph, mais um dia nessa selva de pedra... Se eu soubesse que ia passar tanto tempo aqui, teria trazido um travesseiro. Quem precisa de mais café?!",
            "Matheus: Sério, hoje é um daqueles dias em que até o café parece estar de mal com a vida. Alguém me diga que isso vai acabar logo!"
        ]
    }
    
    som_dialogo = pygame.mixer.Sound(CAMINHO_AUDIO + "teclado.mp3")
    # Adiciona os rects dos figurantes ao dicionário principal
    rects.update(rects_figurantes)
    
    frame_atual = 0
    direcao = "direita"
    tempo_espera_animacao = 200  # Intervalo entre frames (em milissegundos)
    minigame_completo = False
    primeira_execucao = True
    flag_som = True
    fase1_rodando = True
    while fase1_rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos_mouse = pygame.mouse.get_pos()

                # Verifica se o clique foi no ícone de som
                if rects['som'].collidepoint(pos_mouse):
                    flag_som = not flag_som
                    if flag_som:
                        pygame.mixer.music.unpause()  # Desmuta o som
                    else:
                        pygame.mixer.music.pause()  # Muta o som

        teclas_pressionadas = pygame.key.get_pressed()
        x_personagem, y_personagem, direcao, voltar_para_tela_inicial, dialogo_ativado, iniciar_minigame = mover_personagem(teclas_pressionadas, x_personagem, y_personagem, VELOCIDADE_PERSONAGEM, direcao, TAMANHO_PERSONAGEM, area_chao_horizontalmente_expandida, VELOCIDADE_CORRER, posicoes, rects, tela, personagem_atributos, 1)
        
        if voltar_para_tela_inicial:
            pygame.mixer.music.stop()
            return False, None
        
        if dialogo_ativado == 'chefe':
            if not minigame_completo:
                exibir_dialogo(tela, caixa_dialogo, dialogo_chefe, som_dialogo, fonte_dialogo, PRETO)
            else:
                if personagem_atributos.vidas < 5:
                    dialogo_a_exibir = dialogo_chefe_completou_minigame_baixo
                else:
                    dialogo_a_exibir = dialogo_chefe_completou_minigame_cheio
                exibir_dialogo(tela, caixa_dialogo, dialogo_a_exibir, som_dialogo, fonte_dialogo, PRETO)
                return True, personagem_atributos  # Finaliza a fase após o diálogo do chefe
                
        elif dialogo_ativado in dialogos_figurantes:
            exibir_dialogo(tela, caixa_dialogo, dialogos_figurantes[dialogo_ativado], som_dialogo, fonte_dialogo, PRETO)
        
        if iniciar_minigame:
            perdeu, ganhou = minigamefase1(tela, personagem_atributos, minigame_completo)
            if perdeu:
                fase1()  # Chama a fase1 novamente para reiniciar
                return False, None
            if ganhou:
                minigame_completo = True
        personagem, frame_atual = atualizar_animacao(teclas_pressionadas, frame_atual, animacao_andar, animacao_correr, personagem_parado)
        # Atualizar a animação dos figurantes
        figurantes = atualizar_figurantes(figurantes, tempo_espera_animacao)
        
        if direcao == "esquerda":
            personagem = pygame.transform.flip(personagem, True, False)
        
        desenhar_cenario(tela, chao, parede, ceu, janela, porta, pygame.transform.flip(porta, True, False), maquina, maquina2, mesa,
                         mesa_grande, computador1, computador2, gato, cachorro, posicoes, altura_chao, relogio_figura, chefe, escrivaninha, som, som_mutado, flag_som)
        
        tela.blit(personagem, (x_personagem, y_personagem))
        
        # Desenhar figurantes
        desenhar_figurantes(tela, figurantes, posicoes_figurantes)
        carregar_menu(tela, personagem_atributos, fonte_personalizada)
        
        if primeira_execucao:
            mostrar_instrucoes(tela)
            primeira_execucao = False
            
        pygame.display.flip()
        relogio.tick(30)
        
if __name__ == "__main__":
    fase1()