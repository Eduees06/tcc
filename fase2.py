import pygame
import sys
from config import *
from utils import *
from personagem import *
from minigame1 import *
from fase1 import *
from minigame2 import *

# Inicialize o Pygame
pygame.init()


def animacao_figurantes_novos_fase2():
    animacao_figurante5 = [
        pygame.transform.scale(pygame.image.load(os.path.join(caminho_assets, f"figurante5esperando{i}.png")).convert_alpha(), (TAMANHO_PERSONAGEM, TAMANHO_PERSONAGEM))
        for i in range(1, 7) 
    ]
    animacao_figurante6 = [
        pygame.transform.scale(pygame.image.load(os.path.join(caminho_assets, f"figurante6esperando{i}.png")).convert_alpha(), (TAMANHO_PERSONAGEM, TAMANHO_PERSONAGEM))
        for i in range(1, 7) 
    ]    
    
    return animacao_figurante5, animacao_figurante6

#provisorio para testar a fase
personagem = Personagem(vidas=5, dinheiro= 200)

def fase2(personagem):
    
    tela, relogio = inicializar_jogo()
    (chao, parede, personagem_parado, animacao_andar, animacao_correr, ceu, janela, porta, maquina, maquina2, mesa, mesa_grande, computador1, 
     computador2, gato, cachorro, relogio_figura, rects, animacao_figurante1, animacao_figurante2, animacao_figurante3, animacao_figurante4, chefe, escrivaninha, caixa_dialogo, emails, som, som_mutado) = carregar_assets()
    
    animacao_figurante5, animacao_figurante6 = animacao_figurantes_novos_fase2()
    
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
        (rects['mesa19'].x + 30, rects['mesa19'].y - 60)
    ]
    
    tamanhos_figurantes = [(90, 70), (90, 70), (90, 70), (90, 70), (90, 70), (90, 70)]
    animacoes_figurantes = [animacao_figurante1, animacao_figurante2, animacao_figurante3, animacao_figurante4, animacao_figurante5, animacao_figurante6]
    
    figurantes, rects_figurantes = inicializar_figurantes(posicoes_figurantes, animacoes_figurantes, tamanhos_figurantes)

    dialogo_chefe = [
        "Chefe: Bom dia! Infelizmente, não temos boas notícias. Estamos enfrentando uma série de ataques de ransomware.",
        "Chefe: Alguns dados importantes da empresa já estão criptografados, e precisamos agir rapidamente.",
        "Chefe: Converse com seus colegas de trabalho para conseguir ajuda! É fundamental que todos estejam envolvidos nesse esforço.",
        "Chefe: Depois, dirija-se à sua mesa e tente buscar backups do sistema que possam ter sido salvos antes do ataque. Além disso, precisamos tentar desincriptografar alguns arquivos que foram sequestrados.",
        "Chefe: Lembre-se, o tempo é essencial! Quanto mais rápido agirmos, maiores serão nossas chances de recuperar os dados!"

    ]
    dialogo_chefe_completou_minigame_cheio = [
        "Chefe: Excelente trabalho em realizar todos os backups e recuperar os arquivos criptografados! Você ajudou a salvar a empresa de uma crise maior.", 
        "Chefe: Não esqueça das dicas que mencionei; elas serão fundamentais para manter nossa segurança no futuro!", 
        "Chefe: Graças aos seus esforços, estamos em uma posição muito melhor. Suas tarefas estão concluídas por hoje. Até amanhã!"
    ]

    dialogo_chefe_completou_minigame_baixo = [
        "Chefe: Vejo que você conseguiu realizar alguns backups, mas infelizmente perdemos acesso a alguns dados importantes. Isso é preocupante! É crucial ter cuidado com essas armadilhas.", 
        "Chefe: Lembre-se das dicas que mencionei; elas são essenciais para navegar neste ambiente e evitar problemas no futuro.", 
        "Chefe: Apesar disso, bom trabalho! Você fez o melhor que pôde, dadas as circunstâncias. Suas tarefas estão concluídas por hoje. Até amanhã! E não esqueça de descansar."
    ]
    
    dialogos_figurantes = {
        'figurante1': [
            "Arthur: Uau, você já ouviu sobre o ataque de ransomware que afetou a empresa? É alarmante! Precisamos estar atentos a cada e-mail que recebemos.",
            "Arthur: Antigamente, também enfrentamos um ataque DDoS na empresa. Eu sempre digo: um firewall melhor é como um guarda-chuva, nunca se sabe quando vai precisar! Manter backups offline e usar um firewall eficaz é essencial, ninguém quer perder dados importantes!"
        ],
        'figurante2': [
            "Ana: Esse ataque me deixou tão preocupada! Não se esqueça: se você receber um e-mail suspeito, não clique em nada. Confirme sempre a fonte!",
            "Ana: Uma vez, perdi muitos arquivos porque não tinha um backup recente. Aprendi da maneira mais difícil a importância de testar os backups regularmente."
        ],
        'figurante3': [
            "Soraia: Você sabia que a empresa mantém imagens de sistemas operacionais pré-configurados? Isso pode acelerar a recuperação em caso de ataque!",
            "Soraia: Lembre-se: um bom antivirus pode ser a nossa primeira linha de defesa contra malware."
        ],
        'figurante4': [
            "Matheus: O dia está pesado e a segurança vem em primeiro lugar! A internet é tão perigosa, que já não bastava o treinamento para phishing de ontem; agora temos ataques de ransomware. Amanhã, com certeza vou ser atropelado por uma tartaruga!",
            "Matheus: Um bom plano de resposta a incidentes pode ser a diferença entre perder tudo ou recuperar rapidamente. Vamos garantir que nossos dados estejam seguros! Porque, sinceramente, não sei o que mais pode acontecer hoje..."
        ],
        'figurante5': [
        "Karina: Ontem tive que lidar com uma auditoria de segurança. Agora que voltei, a situação é bem pior! Você sabia que os responsáveis por ataques podem ser desde hackers buscando diversão até terroristas patrocinados por governos estrangeiros? Precisamos estar preparados para tudo!",
        "Karina: Os atacantes estão utilizando um tipo de malware chamado Ransomware. Ele criptografa nossos dados e só libera o acesso de volta se pagarmos uma quantia em dinheiro. É uma situação bem delicada, e precisamos estar preparados para lidar com isso."
        ],
        'figurante6': [
            "Nicolas: Cheguei tarde porque estava isolando alguns sistemas comprometidos, e parece que a coisa aqui também está feia. Sabe o que pode indicar que estamos sob ataque? Servidores lentos, antivírus desabilitado, e aquele pico de tráfego de internet sem explicação.",
            "Nicolas: Já notei arquivos sendo modificados sozinhos e até logs com falhas de autenticação em massa. Se você vir algo assim, avise o time de TI imediatamente!"
        ]
    }
    
    som_dialogo = pygame.mixer.Sound(os.path.join(CAMINHO_AUDIO, "teclado.mp3"))
    # Adiciona os rects dos figurantes ao dicionário principal
    rects.update(rects_figurantes)
    
    frame_atual = 0
    direcao = "direita"
    tempo_espera_animacao = 200  # Intervalo entre frames (em milissegundos)
    minigame_completo = False
    flag_som = True
    fase2_rodando = True
    gabaritou = False
    while fase2_rodando:
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
            return False, personagem_atributos
        
        if dialogo_ativado == 'chefe':
            if not minigame_completo:
                exibir_dialogo(tela, caixa_dialogo, dialogo_chefe, som_dialogo, fonte_dialogo, PRETO)
            else:
                if gabaritou:
                    dialogo_a_exibir = dialogo_chefe_completou_minigame_cheio
                else:
                    dialogo_a_exibir = dialogo_chefe_completou_minigame_baixo
                exibir_dialogo(tela, caixa_dialogo, dialogo_a_exibir, som_dialogo, fonte_dialogo, PRETO)
                return True, personagem_atributos
                
        elif dialogo_ativado in dialogos_figurantes:
            exibir_dialogo(tela, caixa_dialogo, dialogos_figurantes[dialogo_ativado], som_dialogo, fonte_dialogo, PRETO)
        
        if iniciar_minigame:
            perdeu, ganhou, gabaritou = minigamefase2(tela, personagem_atributos, minigame_completo, gabaritou)
            if perdeu:
                fase2(personagem = Personagem(vidas=5, dinheiro= 0))  # Chama a fase2 novamente para reiniciar
                return False, personagem_atributos
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
    fase2(personagem)