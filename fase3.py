import pygame
import sys
from config import *
from utils import *
from personagem import *
from minigame1 import *
from fase1 import *
from minigame3 import *

# Inicialize o Pygame
pygame.init()


def animacao_figurantes_novos_fase3():
    animacao_figurante5 = [
        pygame.transform.scale(pygame.image.load(os.path.join(caminho_assets, f"figurante5esperando{i}.png")).convert_alpha(), (TAMANHO_PERSONAGEM, TAMANHO_PERSONAGEM))
        for i in range(1, 7) 
    ]
    animacao_figurante6 = [
        pygame.transform.scale(pygame.image.load(os.path.join(caminho_assets, f"figurante6esperando{i}.png")).convert_alpha(), (TAMANHO_PERSONAGEM, TAMANHO_PERSONAGEM))
        for i in range(1, 7) 
        ] 
    animacao_figurante7 = [
    pygame.transform.scale(pygame.image.load(os.path.join(caminho_assets, f"figurante7esperando{i}.png")).convert_alpha(), (TAMANHO_PERSONAGEM, TAMANHO_PERSONAGEM))
    for i in range(1, 7) 
    ]    
    animacao_figurante8 = [
    pygame.transform.scale(pygame.image.load(os.path.join(caminho_assets, f"figurante8esperando{i}.png")).convert_alpha(), (TAMANHO_PERSONAGEM, TAMANHO_PERSONAGEM))
    for i in range(1, 7) 
    ]        
    return animacao_figurante5, animacao_figurante6, animacao_figurante7,  animacao_figurante8

#provisorio para testar a fase
personagem = Personagem(vidas=5, dinheiro= 200)

def fase3(personagem):
    
    tela, relogio = inicializar_jogo()
    (chao, parede, personagem_parado, animacao_andar, animacao_correr, ceu, janela, porta, maquina, maquina2, mesa, mesa_grande, computador1, 
    computador2, gato, cachorro, relogio_figura, rects, animacao_figurante1, animacao_figurante2, animacao_figurante3, animacao_figurante4, chefe, escrivaninha, caixa_dialogo, emails, som, som_mutado) = carregar_assets()
    
    animacao_figurante5, animacao_figurante6, animacao_figurante7, animacao_figurante8 = animacao_figurantes_novos_fase3()
    
    # Inicializar vidas
    personagem_atributos = personagem
    
    x_personagem, y_personagem = inicializar_posicoes()
    altura_chao, area_chao_horizontalmente_expandida = definir_areas_chao()
    posicoes, rects = definir_posicoes_objetos(altura_chao, rects)
    # Configurações da música de fundo
    pygame.mixer.music.load(os.path.join(CAMINHO_AUDIO, "background.mp3"))
    pygame.mixer.music.set_volume(0.05)
    pygame.mixer.music.play(-1)  # -1 para repetir indefinidamente
    # Configurações dos figurantes
    posicoes_figurantes = [
        (rects['mesa0'].x - 150, rects['mesa0'].y - 80),
        (rects['mesa15'].x - 250, rects['mesa15'].y - 60),
        (rects['mesa9'].x - 510, rects['mesa9'].y - 70),
        (rects['mesa20'].x - 150, rects['mesa20'].y - 60),
        (rects['mesa16'].x - 510, rects['mesa16'].y + 30),
        (rects['mesa19'].x + 30, rects['mesa19'].y - 60),
        (rects['mesa2'].x + 385, rects['mesa2'].y - 170),
        (rects['mesa10'].x + 385, rects['mesa10'].y - 170)
    ]
    
    tamanhos_figurantes = [(90, 70), (90, 70), (90, 70), (90, 70), (90, 70), (90, 70)]
    animacoes_figurantes = [animacao_figurante1, animacao_figurante2, animacao_figurante3, animacao_figurante4, animacao_figurante5, animacao_figurante6, animacao_figurante7,animacao_figurante8]
    
    figurantes, rects_figurantes = inicializar_figurantes(posicoes_figurantes, animacoes_figurantes, tamanhos_figurantes)

    dialogo_chefe = [
        "Chefe: Bom dia! Pois é, terceiro dia seguido enfrentando problemas... Se continuar assim, acho que vou virar especialista em apagar incêndios!",
        "Chefe: Mas agora, falando sério, temos uma situação urgente. Nosso servidor está sob ataque DDoS, e o tráfego malicioso está crescendo rapidamente.",
        "Chefe: O servidor está recebendo uma quantidade absurda de requisições, a maioria delas suspeitas. Precisamos agir rápido para evitar que tudo saia do ar.",
        "Chefe: Antes de ir para sua mesa, sugiro que converse com os outros funcionários. Trabalhar em equipe pode ajudar a identificar padrões de ataque e melhorar nossa defesa.",
        "Chefe: Quando estiver pronto, vá para sua estação e comece a filtrar as requisições. Lembre-se de bloquear as suspeitas e permitir as legítimas, vamos tentar manter o servidor estável!",
        "Chefe: Quanto mais protegermos o sistema agora, menos chance de ele cair e afetar o trabalho de todos. Estamos contando com você!"
    ]
    
    dialogo_chefe_completou_minigame_cheio = [
        "Chefe: Excelente trabalho! Você conseguiu proteger o servidor e manteve o sistema estável mesmo com o ataque DDoS intenso!",
        "Chefe: Graças ao seu empenho em bloquear o tráfego malicioso, conseguimos manter as operações da empresa funcionando sem interrupções.",
        "Chefe: As estratégias que você utilizou foram fundamentais. Com seu conhecimento e dedicação, nossa segurança está mais forte do que nunca.",
        "Chefe: Parabéns! Você cumpriu seu dever com excelência e ajudou a proteger nossa empresa. Missão cumprida!"
    ]

    dialogo_chefe_completou_minigame_baixo = [
        "Chefe: Vejo que você conseguiu bloquear algumas requisições maliciosas, mas o servidor ainda enfrentou certa instabilidade. Precisamos ficar atentos a esses ataques!",
        "Chefe: Lembre-se das estratégias que discutimos; elas podem fazer toda a diferença em momentos críticos como esse.",
        "Chefe: Apesar das dificuldades, você fez o possível para manter o sistema no ar. Continue aprimorando suas habilidades de defesa. Por hoje, suas tarefas estão concluídas. Até breve, e obrigado pelo esforço!"
    ]
        
    dialogos_figurantes = {
        'figurante1': [
            "Arthur: Já viu o caos que o DDoS está causando? Parece que os servidores estão em um daqueles shows com milhões de fãs gritando ao mesmo tempo!",
            "Arthur: Lembre-se, um bom firewall e sistema de detecção de intrusos podem ajudar muito. E, claro, é sempre bom ter planos de mitigação preparados. Vai por mim, não queremos isso de novo!"
        ],
        'figurante2': [
            "Ana: Já viu aqueles sistemas que espalham o tráfego para vários servidores? Como um CDN, sabe? Acho genial. Se um lugar fica sobrecarregado, é só redirecionar.",
            "Ana: Só que não dá para confiar só nisso. Se o ataque for muito grande, todos os servidores podem acabar sofrendo. Nada é infalível!"
        ],
        'figurante3': [
            "Soraia: Eu adoro a ideia de firewalls, é como ter um portão de ferro na porta de casa, o único problema é quando alguém descobre um buraco no muro, sabe?",
            "Soraia: Mas se estiver bem configurado, é uma das melhores defesas. Bloquear quem não deveria estar ali faz uma diferença enorme."
        ],
        'figurante4': [
            "Matheus: DDoS, ransomware, phishing... daqui a pouco, só falta o servidor fugir sozinho pela porta! Esse ano tá uma loucura!",
            "Matheus: Mas falando sério, um bom plano de contingência pode nos salvar. Se as coisas apertarem, desligue os serviços não essenciais para manter o essencial em pé. E nunca subestime o poder de um simples bloqueio de IP!"
        ],
        'figurante5': [
            "Karina: Sabia que algumas ferramentas conseguem até identificar tráfego malicioso em tempo real? Não é magia, é análise de padrões.",
            "Karina: Mas o desafio é sempre a velocidade. Se o ataque for rápido demais, até o sistema mais esperto pode acabar ficando para trás."
        ],
        'figurante6': [
            "Nicolas: Ah, DDoS... nada como um monte de bots para tornar nosso dia mais 'emocionante', né? Aposto que os hackers estão se divertindo às nossas custas.",
            "Nicolas: Fique de olho em picos de tráfego e lentidão inexplicável nos sistemas. E se os logs mostrarem conexões vindo de locais aleatórios pelo mundo, bom... hora de acionar as defesas!"
        ],
        'figurante7': [
            "Beatriz: É meu primeiro dia aqui e já estamos enfrentando um ataque DDoS... Sério, parece que eu cheguei na empresa e tudo já tá pegando fogo!",
            "Beatriz: Já ouviu falar de Scrubbing? É como um filtro gigante que separa tráfego bom do ruim. Claro, não é perfeito... mas ajuda muito quando estamos no meio do caos.",
            "Beatriz: O problema é que às vezes o sistema filtra coisas demais ou não é rápido o suficiente. Mas ei, é melhor do que deixar tudo passar!"
        ],
        'figurante8': [
            "Antonio: Acabei de voltar das férias e já caí no meio de um ataque DDoS... Isso é que é sorte, né?",
            "Antonio: Uma vez usamos algo que limitava a taxa de requisições para o servidor. Parece simples, né? Mas foi incrível como aquilo estabilizou o sistema.",
            "Antonio: Só tem que tomar cuidado para não limitar tráfego legítimo junto. Ninguém gosta de ficar na fila, mesmo que seja digital!"
        ]
    }
    
    som_dialogo = pygame.mixer.Sound(os.path.join(CAMINHO_AUDIO, "teclado.mp3"))
    som_zerou = pygame.mixer.Sound(os.path.join(CAMINHO_AUDIO, "zerou.wav"))
    
    # Adiciona os rects dos figurantes ao dicionário principal
    rects.update(rects_figurantes)
    
    frame_atual = 0
    direcao = "direita"
    tempo_espera_animacao = 200  # Intervalo entre frames (em milissegundos)
    minigame_completo = False
    flag_som = True
    fase3_rodando = True
    gabaritou = False
    while fase3_rodando:
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
        x_personagem, y_personagem, direcao, voltar_para_tela_inicial, dialogo_ativado, iniciar_minigame = mover_personagem(teclas_pressionadas, x_personagem, y_personagem, VELOCIDADE_PERSONAGEM, direcao, TAMANHO_PERSONAGEM, area_chao_horizontalmente_expandida, VELOCIDADE_CORRER, posicoes, rects, tela, personagem_atributos, 2)
        
        if voltar_para_tela_inicial:
            pygame.mixer.music.stop()
            return False
        
        if dialogo_ativado == 'chefe':
            if not minigame_completo:
                exibir_dialogo(tela, caixa_dialogo, dialogo_chefe, som_dialogo, fonte_dialogo, PRETO)
            else:
                if gabaritou:
                    dialogo_a_exibir = dialogo_chefe_completou_minigame_cheio
                else:
                    dialogo_a_exibir = dialogo_chefe_completou_minigame_baixo
                som_zerou.play()
                exibir_dialogo(tela, caixa_dialogo, dialogo_a_exibir, som_dialogo, fonte_dialogo, PRETO)
                fase3_rodando = False  # Finaliza a fase após o diálogo do chefe
                
        elif dialogo_ativado in dialogos_figurantes:
            exibir_dialogo(tela, caixa_dialogo, dialogos_figurantes[dialogo_ativado], som_dialogo, fonte_dialogo, PRETO)
        
        if iniciar_minigame:
            perdeu, ganhou, gabaritou = minigamefase3(tela, personagem_atributos, minigame_completo, gabaritou)
            if perdeu:
                fase3(personagem = Personagem(vidas=5, dinheiro= 0))  # Chama a fase3 novamente para reiniciar
                return True
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
        
        pygame.display.flip()
        relogio.tick(30)
        
if __name__ == "__main__":
    fase3(personagem)