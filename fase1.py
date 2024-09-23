import pygame
import sys
from config import *
from utils import *
import time
from personagem import *

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

def exibir_dialogo(tela, caixa_dialogo, falas, posicao, som_dialogo, fonte, cor):
    # Define a cor do contorno como vermelho
    cor_contorno = (255, 0, 0)  # Vermelho

    for fala in falas:
        # Toca o som do diálogo
        pygame.mixer.music.load(som_dialogo)
        pygame.mixer.music.play(0)  # Toca uma vez

        # Armazena o rect da caixa de diálogo
        rect_caixa = caixa_dialogo.get_rect(topleft=posicao)
        rect_caixa.topleft = (rect_caixa.x + 150, rect_caixa.y + 770)
        rect_caixa.width = rect_caixa.width // 1.7
        rect_caixa.height = rect_caixa.height // 4
        
        # Quebra o texto em linhas
        linhas = []
        palavras = fala.split(' ')
        linha_atual = ""
        largura_limite = rect_caixa.width

        for palavra in palavras:
            if fonte.size(linha_atual + palavra)[0] < largura_limite:
                linha_atual += palavra + ' '
            else:
                linhas.append(linha_atual.strip())
                linha_atual = palavra + ' '

        if linha_atual:
            linhas.append(linha_atual.strip())

        # Limpa a tela e desenha a caixa de diálogo
        tela.blit(caixa_dialogo, posicao)
        pygame.display.flip()

        # Define o espaço entre as linhas
        espaco_entre_linhas = 10  # Ajuste esse valor conforme necessário

        # Renderiza cada linha dentro da caixa de diálogo
        for i, linha in enumerate(linhas):
            texto_atual = ""
            for letra in linha:
                texto_atual += letra
                texto_renderizado = fonte.render(texto_atual, True, cor)

                # Ajusta a posição do texto renderizado
                rect_texto = texto_renderizado.get_rect(topleft=(rect_caixa.x + 10, rect_caixa.y + 10 + i * (30 + espaco_entre_linhas)))
                tela.blit(texto_renderizado, rect_texto)
                pygame.display.update()  # Use update para melhor performance

                # Espera um pouco antes de adicionar a próxima letra
                time.sleep(0.02)

            # Atraso após a linha completa
            time.sleep(0.1)

        # Texto de instrução abaixo da caixa de diálogo
        texto_instrucao = "(aperte Enter/espaço para avançar)"
        texto_renderizado_instrucao = fonte.render(texto_instrucao, True, cor)

        # Centraliza o texto embaixo da caixa de diálogo, mantendo o mesmo rect
        rect_instrucao = texto_renderizado_instrucao.get_rect(center=(rect_caixa.centerx, rect_caixa.bottom - 20))
        tela.blit(texto_renderizado_instrucao, rect_instrucao)
        pygame.display.flip()

        # Para o som após a fala
        pygame.mixer.music.stop()

        # Espera até que o usuário pressione "Enter" ou "Space"
        esperando = True
        while esperando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN or evento.key == pygame.K_SPACE:
                        esperando = False
                        # Limpa a área da caixa de diálogo ao pressionar a tecla
                        tela.blit(caixa_dialogo, posicao)
                        pygame.display.flip()

    # Para o som após o diálogo
    pygame.mixer.music.stop()

def fase1():
    
    tela, relogio = inicializar_jogo()
    (chao, parede, personagem_parado, animacao_andar, animacao_correr, ceu, janela, porta, maquina, maquina2, mesa, mesa_grande, computador1, 
     computador2, gato, cachorro, relogio_figura, rects, animacao_figurante1, animacao_figurante2, animacao_figurante3, animacao_figurante4, vida, moeda, chefe, escrivaninha, caixa_dialogo, emails) = carregar_assets()
    # Inicializar vidas
    personagem_atributos = Personagem(vidas=2, dinheiro=60)
    email_aberto = False
    
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

    dialogo_chefe = [
        "Chefe: Bem-vindo ao seu primeiro dia na Plunder Drifflin Co! Estamos animados em tê-lo aqui.",
        "Chefe: Nossa empresa é especializada na compra e venda de itens. Seu papel é fundamental para nosso sucesso.",
        "Chefe: Sua primeira tarefa é analisar alguns e-mails. Fique atento, pois estão surgindo muitas tentativas de golpe, especialmente phishing.",
        "Chefe: Phishing é quando alguém finge ser uma empresa legítima para roubar suas informações. Fique atento!",
        "Chefe: Isso pode levar ao roubo de identidade e perdas financeiras. Sempre verifique antes de clicar em links.",
        "Chefe: Se algo parecer bom demais para ser verdade, desconfie! E-mails com senso de urgência também são suspeitos. Não abra anexos inesperados e sempre verifique o remetente. Um endereço estranho pode ser um sinal de alerta.",
        "Chefe: Deixei uma lista de e-mails confiáveis na escrivaninha, isso vai te ajudar a identificar o que é seguro. Após responder todos os e-mails, volte aqui e fale comigo."
    ]

    dialogos_figurantes = {
        'figurante1': [
            "Arthur: Bem-vindo! Eu sou o Arthur, sou alérgico a gatos, mas aqui estou eu, trabalhando ao lado de um—quem precisa de ar fresco, não é mesmo?",
            "Arthur: A última máquina desta fileira é a sua. Espero que ela não tenha uma 'crise de identidade', como a maioria dos nossos computadores!"
        ],
        'figurante2': [
            "Ana: Ah, e não me deixe começar a falar sobre e-mails suspeitos! Já caí em algumas armadilhas por causa deles. Uma vez, recebi um e-mail que parecia legítimo, mas o endereço tinha um erro de digitação que eu não percebi.",
            "Ana: Acredite, os golpistas são espertos! Às vezes, é só uma letra que muda, como 'com' no lugar de 'con'.",
            "Ana: Fique esperto! Sempre cheque o endereço antes de clicar. Pode fazer toda a diferença!"
        ],
        'figurante3': [
            "Lorena: Oi, você viu nossos amigos de quatro patas por aqui? O cachorro ali adora os petiscos que ficam naquela máquina perto do gato, e o gato, bem, ele só consegue resistir aos petiscos da outra máquina",
            "Lorena: Sabe, é curioso... Eu realmente não entendo por que eles ficam tão distantes das máquinas que vendem as comidas que eles gostam! Você acha que eles estão tentando nos pregar uma peça?",
            "Lorena: Ah, e se você tiver 30 moedas, pode comprar uns petiscos para eles. Garanto que vão ficar super felizes! Pode ser uma boa forma de conquistar a confiança deles, quem sabe?"


        ],
        'figurante4': [
            "Matheus: Hmph, mais um dia nessa selva de pedra... Se eu soubesse que ia passar tanto tempo aqui, teria trazido um travesseiro. Quem precisa de mais café?!",
            "Matheus: Sério, hoje é um daqueles dias em que até o café parece estar de mal com a vida. Alguém me diga que isso vai acabar logo!"
        ]
    }
    
    som_dialogo = CAMINHO_AUDIO + "teclado.mp3"
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
        x_personagem, y_personagem, direcao, voltar_para_tela_inicial, dialogo_ativado = mover_personagem(teclas_pressionadas, x_personagem, y_personagem, VELOCIDADE_PERSONAGEM, direcao, TAMANHO_PERSONAGEM, area_chao_horizontalmente_expandida, VELOCIDADE_CORRER, posicoes, rects, tela, personagem_atributos)
        
        if voltar_para_tela_inicial:
            return
        
        if dialogo_ativado == 'chefe':
            exibir_dialogo(tela, caixa_dialogo, dialogo_chefe, (300, -200), som_dialogo, fonte_dialogo, PRETO)

        elif dialogo_ativado in dialogos_figurantes:
            exibir_dialogo(tela, caixa_dialogo, dialogos_figurantes[dialogo_ativado], (300, -200), som_dialogo, fonte_dialogo, PRETO)
            
        if not email_aberto and teclas_pressionadas[pygame.K_f]:
            if "emails" in personagem_atributos.objetos:  # Verifica se o personagem possui os emails
                email_aberto = True  # Abre o email

        if email_aberto:
            pausar_jogo_imagem(tela, emails)  # Mostra a imagem dos emails
            email_aberto = False

        personagem, frame_atual = atualizar_animacao(teclas_pressionadas, frame_atual, animacao_andar, animacao_correr, personagem_parado)
        # Atualizar a animação dos figurantes
        figurantes = atualizar_figurantes(figurantes, tempo_espera_animacao)
        
        if direcao == "esquerda":
            personagem = pygame.transform.flip(personagem, True, False)
        
        desenhar_cenario(tela, chao, parede, ceu, janela, porta, pygame.transform.flip(porta, True, False), maquina, maquina2, mesa,
                         mesa_grande, computador1, computador2, gato, cachorro, posicoes, altura_chao, relogio_figura, vida, personagem_atributos.vidas, moeda, personagem_atributos.dinheiro, chefe, escrivaninha)
        
        tela.blit(personagem, (x_personagem, y_personagem))
        
        # Desenhar figurantes
        desenhar_figurantes(tela, figurantes, posicoes_figurantes)
        pygame.display.flip()
        relogio.tick(30)
        
if __name__ == "__main__":
    fase1()