import pygame
import random
from personagem import *
import os
from config import LARGURA_TELA, ALTURA_TELA, TAMANHO_PERSONAGEM
from utils import *

def minigamefase1(tela, personagem, concluido):
    som_game_over = pygame.mixer.Sound(CAMINHO_AUDIO + "game_over.wav")
    som_vitoria = pygame.mixer.Sound(CAMINHO_AUDIO + "victory.wav")
    som_vitoria.set_volume(0.2)
    email_valido = pygame.image.load(os.path.join(caminho_assets, 'emails.png')).convert_alpha()
    largura_nova, altura_nova = 1000, 1000
    emails = []

    # Carregar emails
    for i in range(1, 6):
        emails.append((pygame.image.load(os.path.join("D:/jogo/assets/images", f"emailfalso{i}.png")).convert_alpha(), "falso"))
        emails.append((pygame.image.load(os.path.join("D:/jogo/assets/images", f"emailverdadeiro{i}.png")).convert_alpha(), "verdadeiro"))

    random.shuffle(emails)

    background = pygame.image.load(os.path.join(caminho_assets, "background2.png")).convert_alpha()
    regras =  pygame.image.load(os.path.join(caminho_assets, "background_regras.png")).convert_alpha()
    background = pygame.transform.scale(background, (largura_nova, altura_nova))
    regras = pygame.transform.scale(regras, (largura_nova, altura_nova))
    nova_tela = pygame.Surface((largura_nova, altura_nova))
    nova_tela.blit(background, (0, 0))

    pos_x = (tela.get_width() - largura_nova) // 2
    pos_y = (tela.get_height() - altura_nova) // 2
    monitor_rect = pygame.Rect(pos_x + 40, pos_y + 260, largura_nova // 1.085, altura_nova // 1.88)
    # Verificação se o jogo foi concluído
    if concluido:
        tela.blit(nova_tela, (pos_x, pos_y))
        fonte = pygame.font.SysFont(None, 36)
        mensagem_fim = fonte.render("Voce conseguiu! Vá falar com seu chefe", True, (0, 0, 0))
        mensagem_fim_rect = mensagem_fim.get_rect(center=monitor_rect.center)
        tela.blit(mensagem_fim, mensagem_fim_rect)

        pygame.display.flip()
        pygame.time.delay(1000)

        return False, True
    
    email_index = 0
    total_emails = len(emails)
    email_atual, email_tipo = emails[email_index]

    email_width, email_height = monitor_rect.width, monitor_rect.height
    email_atual = pygame.transform.scale(email_atual, (email_width, email_height))

    mostrando_emails = False
    mensagem_mostrada = True
    esperando = True
    mostrando_email_valido = False
    mostrando_regras = False
    # Tempo do minigame
    tempo_maximo = 90 # Tempo total em segundos
    tempo_inicial = 0  # Inicialmente 0
    jogo_iniciado = False  # Flag para verificar se o jogo foi iniciado

    botao_largura, botao_altura = 200, 50
    confirmar_rect = pygame.Rect(
        monitor_rect.centerx - botao_largura - 20,
        monitor_rect.bottom - botao_altura - 20,
        botao_largura,
        botao_altura
    )
    rejeitar_rect = pygame.Rect(
        monitor_rect.centerx + 20,
        monitor_rect.bottom - botao_altura - 20,
        botao_largura,
        botao_altura
    )

    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                # Permitir saída do minigame apenas com ESC quando a mensagem está visível
                if evento.key == pygame.K_ESCAPE and mensagem_mostrada:
                    return False, False
                if evento.key == pygame.K_e and not mostrando_emails:
                    mostrando_emails = True
                    mensagem_mostrada = False
                    tempo_inicial = pygame.time.get_ticks()  # Marca o tempo inicial quando o minigame começa
                    jogo_iniciado = True  # O jogo foi iniciado
                if evento.key == pygame.K_i and mensagem_mostrada:
                    mostrando_regras = not mostrando_regras  # Alterna entre mostrar e não mostrar regras
            
                # Não permitir sair com teclas de movimentação
                if evento.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    continue  # Ignora as teclas de movimentação

                if evento.key == pygame.K_f and personagem.possui_objeto("emails"):
                    mostrando_email_valido = not mostrando_email_valido

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1 and mostrando_emails:
                    if confirmar_rect.collidepoint(evento.pos):
                        if email_tipo == "verdadeiro":
                            personagem.adicionar_dinheiro(10)
                        else:
                            personagem.perder_vida()
                        
                        if personagem.vidas <= 0:
                            # Limpa a tela com a nova tela que já contém o background
                            tela.blit(nova_tela, (pos_x, pos_y))
                            
                            # Exibe a mensagem de derrota
                            fonte = pygame.font.SysFont(None, 36)
                            carregar_menu(tela, personagem, fonte_personalizada)
                            som_game_over.play() 
                            mensagem = fonte.render("Suas vidas acabaram! Aperte Enter para reiniciar", True, (0, 0, 0))
                            mensagem_rect = mensagem.get_rect(center=(monitor_rect.centerx, monitor_rect.centery + 150))
                            tela.blit(mensagem, mensagem_rect)
                            
                            pygame.display.flip()  # Atualiza a tela
                            
                            # Loop para esperar o usuário pressionar Enter
                            esperando_reinicio = True
                            while esperando_reinicio:
                                for evento in pygame.event.get():
                                    if evento.type == pygame.QUIT:
                                        pygame.quit()
                                        exit()
                                    if evento.type == pygame.KEYDOWN:
                                        if evento.key == pygame.K_RETURN:  # A tecla Enter
                                            esperando_reinicio = False

                            return True, False  # Retorna True para indicar que o jogo deve ser reiniciado
                        
                        email_index += 1
                    elif rejeitar_rect.collidepoint(evento.pos):
                        if email_tipo == "falso":
                            personagem.adicionar_dinheiro(10)
                        else:
                            personagem.perder_vida()
                        
                        if personagem.vidas <= 0:
                            # Limpa a tela com a nova tela que já contém o background
                            tela.blit(nova_tela, (pos_x, pos_y))
                            # Exibe a mensagem de derrota
                            fonte = pygame.font.SysFont(None, 36)
                            carregar_menu(tela, personagem, fonte_personalizada)
                            som_game_over.play() 
                            mensagem = fonte.render("Suas vidas acabaram! Aperte Enter para reiniciar", True, (0, 0, 0))
                            mensagem_rect = mensagem.get_rect(center=(monitor_rect.centerx, monitor_rect.centery + 150))
                            tela.blit(mensagem, mensagem_rect)
                            
                            pygame.display.flip()  # Atualiza a tela
                            
                            # Loop para esperar o usuário pressionar Enter
                            esperando_reinicio = True
                            while esperando_reinicio:
                                for evento in pygame.event.get():
                                    if evento.type == pygame.QUIT:
                                        pygame.quit()
                                        exit()
                                    if evento.type == pygame.KEYDOWN:
                                        if evento.key == pygame.K_RETURN:  # A tecla Enter
                                            esperando_reinicio = False

                            return True, False  # Retorna True para indicar que o jogo deve ser reiniciado
                        
                        email_index += 1

                    if email_index < total_emails:
                        email_atual, email_tipo = emails[email_index]
                        email_atual = pygame.transform.scale(email_atual, (email_width, email_height))
                    else:
                        mostrando_emails = False
                        
                    if email_index >= total_emails and not mostrando_emails:
                                    tela.blit(nova_tela, (pos_x, pos_y))
                                    fonte = pygame.font.SysFont(None, 36)
                                    som_vitoria.play() 
                                    mensagem_fim = fonte.render("Voce conseguiu! Vá falar com seu chefe", True, (0, 0, 0))
                                    mensagem_fim_rect = mensagem_fim.get_rect(center=(monitor_rect.centerx, monitor_rect.centery + 150))
                                    tela.blit(mensagem_fim, mensagem_fim_rect)

                                    pygame.display.flip()
                                    pygame.time.delay(1000)

                                    return False, True
                                
        # Cálculo do tempo restante se o jogo foi iniciado
        if jogo_iniciado:
            tempo_decorrido = (pygame.time.get_ticks() - tempo_inicial) / 1000  # Tempo em segundos
            tempo_restante = tempo_maximo - tempo_decorrido
            
            # Verifica se o tempo acabou
            if tempo_restante <= 0:
                personagem.perder_vida()
                personagem.perder_vida()
                personagem.perder_vida()
                personagem.perder_vida()
                personagem.perder_vida()
                # Limpa a tela com a nova tela que já contém o background
                tela.blit(nova_tela, (pos_x, pos_y))
                carregar_menu(tela, personagem, fonte_personalizada)
                
                # Exibe a mensagem de derrota
                fonte = pygame.font.SysFont(None, 36)
                som_game_over.play()
                mensagem = fonte.render("O tempo acabou! Aperte Enter para reiniciar", True, (0, 0, 0))
                mensagem_rect = mensagem.get_rect(center=(monitor_rect.centerx, monitor_rect.centery + 150))
                tela.blit(mensagem, mensagem_rect)
                
                pygame.display.flip()  # Atualiza a tela
                
                # Loop para esperar o usuário pressionar Enter
                esperando_reinicio = True
                while esperando_reinicio:
                    for evento in pygame.event.get():
                        if evento.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                        if evento.type == pygame.KEYDOWN:
                            if evento.key == pygame.K_RETURN:  # A tecla Enter
                                esperando_reinicio = False

                return True, False  # Retorna True para indicar que o jogo deve ser reiniciado
            # Desenhar o contador de tempo
            fonte_tempo = pygame.font.SysFont(None, 36)
            texto_tempo = fonte_tempo.render(f'Tempo Restante: {int(tempo_restante)}s', True, (0, 0, 0))  # Texto em preto
            carregar_menu(tela, personagem, fonte_personalizada)

        tela.blit(nova_tela, (pos_x, pos_y))

        if mostrando_emails and email_index < total_emails:
            tela.blit(email_atual, (monitor_rect.x, monitor_rect.y))

            pygame.draw.rect(tela, (0, 0, 0), confirmar_rect.inflate(4, 4))  # Aumenta o tamanho do rect para a borda
            pygame.draw.rect(tela, (0, 255, 0), confirmar_rect)  # Retângulo verde dentro

            pygame.draw.rect(tela, (0, 0, 0), rejeitar_rect.inflate(4, 4))  # Aumenta o tamanho do rect para a borda
            pygame.draw.rect(tela, (255, 0, 0), rejeitar_rect)  # Retângulo vermelho dentro

            fonte = pygame.font.SysFont(None, 36)
            texto_confirmar = fonte.render("Confirmar Email", True, (0, 0, 0))
            texto_rejeitar = fonte.render("Rejeitar Email", True, (0, 0, 0))
            tela.blit(texto_confirmar, (confirmar_rect.x + (confirmar_rect.width - texto_confirmar.get_width()) // 2, confirmar_rect.y + (confirmar_rect.height - texto_confirmar.get_height()) // 2))
            tela.blit(texto_rejeitar, (rejeitar_rect.x + (rejeitar_rect.width - texto_rejeitar.get_width()) // 2, rejeitar_rect.y + (rejeitar_rect.height - texto_rejeitar.get_height()) // 2))
        
        elif mensagem_mostrada:
            if mostrando_regras:
                tela.blit(regras, (pos_x, pos_y))  # Exibe a tela de regras
            else:
                fonte = pygame.font.SysFont(None, 25)
                mensagem1 = fonte.render("{Aperte E para começar o minigame}", True, (0, 0, 0))
                mensagem2 = fonte.render("{Aperte I para ver as regras}", True, (0, 0, 0))
                mensagem3 = fonte.render("{Aperte ESC para sair}", True, (0, 0, 0))

                # Centralizando cada mensagem em relação ao monitor
                tela.blit(mensagem1, mensagem1.get_rect(center=(monitor_rect.centerx - 300, monitor_rect.centery + 175)))
                tela.blit(mensagem2, mensagem2.get_rect(center=(monitor_rect.centerx + 0, monitor_rect.centery + 175)))
                tela.blit(mensagem3, mensagem3.get_rect(center=(monitor_rect.centerx + 300, monitor_rect.centery + 175)))
            
        if jogo_iniciado:
            tela.blit(texto_tempo, (monitor_rect.right - texto_tempo.get_width() - 10, monitor_rect.top + 10))  # Canto superior direito do retângulo
            
        if mostrando_email_valido:
            tela.blit(email_valido, (monitor_rect.x + 400, monitor_rect.y -20))

        pygame.display.flip()
        pygame.time.Clock().tick(60)  # 60 FPS

    return True, False  # Retorna para indicar que o jogo deve continuar
