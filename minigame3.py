import pygame
import random
import os
from config import LARGURA_TELA, ALTURA_TELA
from utils import *

CAMINHO_ASSETS = caminho_assets

BRANCO = (255, 255, 255)

# Classe para inimigos
class Inimigo(pygame.Rect):
    def __init__(self, x, y, largura, altura, cor, imagem, velocidade):
        super().__init__(x, y, largura, altura)
        self.cor = cor
        self.direcao = 1  # Direção inicial de movimento
        self.imagem = imagem  # Adiciona a imagem do inimigo
        self.velocidade = velocidade  # Define a velocidade de movimento
        self.posicao_inicial = (x, y)
        
# Classe para os projéteis do jogador
class Projetil(pygame.Rect):
    def __init__(self, x, y, largura, altura, cor):
        super().__init__(x, y, largura, altura)
        self.cor = cor
        self.velocidade = -5  # Projétil vai para cima
        
class PowerUp:
    def __init__(self, x, y, tipo, imagem, velocidade):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.tipo = tipo
        self.imagem = imagem
        self.velocidade = velocidade

    def mover(self):
        self.rect.y += self.velocidade

    def desenhar(self, tela):
        tela.blit(self.imagem, self.rect.topleft)

class Requisicao(pygame.Rect):
    def __init__(self, x, y, largura, altura, cor, imagem, velocidade):
        super().__init__(x, y, largura, altura)
        self.rect = pygame.Rect(x, y, 40, 40)
        self.cor = cor
        self.imagem = imagem  # Adiciona a imagem do inimigo
        self.velocidade = velocidade  # Define a velocidade de movimento
        self.posicao_inicial = (x, y)
    def mover(self):
        self.rect.y += self.velocidade
    def desenhar(self, tela):
        deslocamento_x = -17 
        deslocamento_y = -5  

        # Atualiza a posição com o deslocamento
        tela.blit(self.imagem, (self.rect.x + deslocamento_x, self.rect.y + deslocamento_y))
              
# Adicionar lista de controle para power-ups usados
powerups_usados = set()

def ativar_cdn(inimigos):
    for inimigo in inimigos:
        inimigo.x, inimigo.y = inimigo.posicao_inicial

def ativar_ratelimiter(inimigos, velocidade_original, tempo):
    for inimigo in inimigos:
        inimigo.velocidade *= 0.5  # Reduz a velocidade pela metade
    pygame.time.set_timer(pygame.USEREVENT + 1, tempo)  # Evento para restaurar velocidade

def restaurar_velocidade(inimigos, velocidade_original):
    for inimigo in inimigos:
        inimigo.velocidade = velocidade_original
    
def ativar_scrubbing_tool(inimigos):
    quantidade_removida = max(1, len(inimigos) // 3)  # Remove 1/3 dos inimigos ou pelo menos 1
    for _ in range(quantidade_removida):
        inimigos.pop(random.randint(0, len(inimigos) - 1))
    
# Função para o minigame estilo Space Invaders
def minigamefase3(tela, personagem, concluido, gabaritou):
    
    # Sons do jogo
    som_explosao = pygame.mixer.Sound(os.path.join(CAMINHO_AUDIO, "explosao.wav"))
    som_disparo = pygame.mixer.Sound(os.path.join(CAMINHO_AUDIO, "laser.wav"))
    som_vitoria = pygame.mixer.Sound(os.path.join(CAMINHO_AUDIO, "victory.wav"))
    som_powerup = pygame.mixer.Sound(os.path.join(CAMINHO_AUDIO, "powerup.wav"))
    som_explosao.set_volume(0.3)
    som_disparo.set_volume(0.1)
    som_vitoria.set_volume(0.2)
    som_powerup.set_volume(0.5)
    som_game_over = pygame.mixer.Sound(os.path.join(CAMINHO_AUDIO, "game_over.wav"))
    # Configuração do monitor e fundo do jogo
    largura_monitor, altura_monitor = 1000, 1000
    pos_x_monitor = (tela.get_width() - largura_monitor) // 2
    pos_y_monitor = (tela.get_height() - altura_monitor) // 2
    monitor_rect = pygame.Rect(pos_x_monitor + 40, pos_y_monitor + 260, largura_monitor // 1.085, altura_monitor // 1.88)
    
    regras = pygame.image.load(os.path.join(caminho_assets, "background_regras3.png")).convert_alpha()
    regras = pygame.transform.scale(regras, (largura_monitor, altura_monitor))
    lista_powerups =  pygame.image.load(os.path.join(caminho_assets, "lista_powerups.png")).convert_alpha()
    lista_powerups = pygame.transform.scale(lista_powerups, (largura_monitor, altura_monitor))
    fundo_jogo = pygame.image.load(os.path.join(CAMINHO_ASSETS, "backgroundminigame3.jpg")).convert_alpha()
    fundo_jogo = pygame.transform.scale(fundo_jogo, (monitor_rect.width, monitor_rect.height))  # Fundo ajustado ao tamanho do monitor
    fundo = pygame.image.load(os.path.join(CAMINHO_ASSETS, "background2.png")).convert_alpha()
    fundo = pygame.transform.scale(fundo, (largura_monitor, altura_monitor))

    imagem_requisicao = pygame.image.load(os.path.join(CAMINHO_ASSETS, "requisicao.png")).convert_alpha()
    imagem_requisicao = pygame.transform.scale(imagem_requisicao, (80, 80))  # Ajuste do tamanho da requisicao
    
    # Carregar imagens dos inimigos e personagem
    imagem_inimigo = pygame.image.load(os.path.join(CAMINHO_ASSETS, "virus.png")).convert_alpha()
    imagem_inimigo = pygame.transform.scale(imagem_inimigo, (80, 80))  # Ajuste do tamanho do inimigo

    imagem_personagem = pygame.image.load(os.path.join(CAMINHO_ASSETS, "personagem.png")).convert_alpha()
    imagem_personagem_original = pygame.transform.scale(imagem_personagem, (80, 80))  # Ajuste do tamanho do personagem
    
    powerup_imgs = {
        "scrubbingTool": pygame.transform.scale(
            pygame.image.load(os.path.join(CAMINHO_ASSETS, "scrubbingTool.png")).convert_alpha(), (100, 100)
        ),
        "ratelimiter": pygame.transform.scale(
            pygame.image.load(os.path.join(CAMINHO_ASSETS, "ratelimiter.png")).convert_alpha(), (100, 100)
        ),
        "firewall": pygame.transform.scale(
            pygame.image.load(os.path.join(CAMINHO_ASSETS, "firewall.png")).convert_alpha(), (100, 50)
        ),
        "cdn": pygame.transform.scale(
            pygame.image.load(os.path.join(CAMINHO_ASSETS, "cdn.png")).convert_alpha(), (100, 100)
        ),
    }
    # Lista de power-ups disponíveis
    tipos_powerups = list(powerup_imgs.keys())

    # Inicializa o power-up atual
    powerup_atual = None
    inventario = []
    requisicao = None
    # Função para gerar um power-up único por fase
    def gerar_powerup():
        tipos_disponiveis = [tipo for tipo in tipos_powerups if tipo not in powerups_usados]
        if not tipos_disponiveis:
            return None  # Nenhum power-up disponível
        tipo_escolhido = random.choice(tipos_disponiveis)
        powerups_usados.add(tipo_escolhido)
        x = random.randint(monitor_rect.left + 100, monitor_rect.right - 100)
        y = monitor_rect.top # Começa fora da tela
        velocidade = 2
        return PowerUp(x, y, tipo_escolhido, powerup_imgs[tipo_escolhido], velocidade)

    # Gerar power-up no início da fase
    powerup_atual = gerar_powerup()
    # Função para exibir a mensagem do power-up
    def exibir_mensagem(mensagem, tempo_inicio, duracao):
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - tempo_inicio <= duracao:  # Exibe apenas enquanto dentro do intervalo
            texto = fonte.render(mensagem, True, BRANCO)
            # Desenha no canto inferior direito relativo ao monitor
            tela.blit(texto, 
                    (monitor_rect.width - texto.get_width() + 450, 
                    monitor_rect.height - texto.get_height() + 200))
            return True
        return False
        
    # Tela de instruções
    esperando = True
    mostrando_regras = False
    mostrando_poweups = False
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return False, False, False
                elif evento.key == pygame.K_i:
                    mostrando_regras = not mostrando_regras
                elif evento.key == pygame.K_p:
                    mostrando_poweups = not mostrando_poweups
                elif evento.key == pygame.K_e:
                    esperando = False  # Inicia o minigame

        # Renderizar o monitor e o fundo com instruções
        tela.blit(fundo, (pos_x_monitor, pos_y_monitor))  # Fundo dentro do monitor

        fonte = pygame.font.SysFont(None, 25)
        if mostrando_regras:
                pos_x = (tela.get_width() - largura_monitor) // 2
                pos_y = (tela.get_height() - altura_monitor) // 2   
                tela.blit(regras, (pos_x, pos_y))
                
        elif mostrando_poweups:
                pos_x = (tela.get_width() - largura_monitor) // 2
                pos_y = (tela.get_height() - altura_monitor) // 2   
                tela.blit(lista_powerups, (pos_x, pos_y))
        else:
            mensagem1 = fonte.render("{Aperte E para começar o minigame}", True, (0, 0, 0))
            mensagem2 = fonte.render("{Aperte I para ver as regras}", True, (0, 0, 0))
            mensagem3 = fonte.render("{Aperte ESC para sair}", True, (0, 0, 0))
            mensagem4 = fonte.render("{Aperte P para ver a lista de powerups}", True, (0, 0, 0))
            # Centralizando cada mensagem em relação ao monitor
            tela.blit(mensagem1, mensagem1.get_rect(center=(monitor_rect.centerx - 300, monitor_rect.centery + 175)))
            tela.blit(mensagem2, mensagem2.get_rect(center=(monitor_rect.centerx + 0, monitor_rect.centery + 175)))
            tela.blit(mensagem3, mensagem3.get_rect(center=(monitor_rect.centerx + 300, monitor_rect.centery + 175)))
            tela.blit(mensagem4, mensagem4.get_rect(center=(monitor_rect.centerx + 0, monitor_rect.centery + 125)))
            
        pygame.display.flip()
        pygame.time.Clock().tick(60)

    # Função para configurar os inimigos para cada fase
    def gerar_inimigos(fase):
        linhas_inimigos = 3 + fase  # Aumenta o número de linhas com o nível
        colunas_inimigos = 6 + fase  # Aumenta o número de colunas com o nível
        espacamento = 50
        inimigos = []
        velocidade_inimigo = 3 + fase  # Aumenta a velocidade do inimigo com a fase
        for linha in range(linhas_inimigos):
            for coluna in range(colunas_inimigos):
                x = monitor_rect.left + coluna * espacamento + 20
                y = monitor_rect.top + linha * espacamento + 20
                inimigos.append(Inimigo(x, y, 40, 40, (255, 0, 0), imagem_inimigo, velocidade_inimigo))
        return inimigos

    def gerar_requisicao(fase):
        espacamento = 50
        velocidade_requisicoes = 3
        x = random.randint(monitor_rect.left + espacamento, monitor_rect.right - 40 - espacamento)
        y = monitor_rect.top + espacamento + 20
        requisicao = Requisicao(x, y, 40, 40, (255, 0, 0), imagem_requisicao, velocidade_requisicoes)
        return requisicao
    
    # Inicializa os inimigos para a primeira fase
    fase_atual = 1
    inimigos = gerar_inimigos(fase_atual)

    # Configuração do jogador e projéteis
    jogador = pygame.Rect(
        monitor_rect.centerx - 25,  # Centraliza horizontalmente no monitor
        monitor_rect.bottom - 80,  # Posiciona na parte inferior do monitor
        50, 50
    )
    projeteis = []
    tempo_recarregar = 1000  # 1 segundo de recarga
    ultimo_disparo = 0  # Armazena o tempo do último disparo
    invertido = False
    tempo_inicio = 0
    exibindo_mensagem = False
    # Loop do jogo
    rodando = True
    while rodando:
        tela.blit(fundo_jogo, monitor_rect.topleft)
        if not requisicao:
            requisicao = gerar_requisicao(fase_atual)
        # Eventos do jogo
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    tempo_atual = pygame.time.get_ticks()

                    # Verifica se o tempo de recarga passou
                    if tempo_atual - ultimo_disparo >= tempo_recarregar:
                        som_disparo.play()
                        projeteis.append(Projetil(jogador.centerx - 5, jogador.top, 10, 20, (255, 255, 0)))
                        ultimo_disparo = tempo_atual  # Atualiza o tempo do último disparo

                # Ativações de habilidades do inventário
                elif evento.key == pygame.K_r and "ratelimiter" in inventario:
                    ativar_ratelimiter(inimigos, velocidade_original=2, tempo=5000)
                    inventario.remove("ratelimiter")
                    som_powerup.play()
                elif evento.key == pygame.K_f and "firewall" in inventario:
                    tempo_recarregar = 500
                    inventario.remove("firewall")
                    som_powerup.play()
                elif evento.key == pygame.K_s and "scrubbingTool" in inventario:
                    ativar_scrubbing_tool(inimigos)
                    inventario.remove("scrubbingTool")
                    som_explosao.set_volume(1.5)
                    som_explosao.play()
                    som_explosao.set_volume(0.3)
                elif evento.key == pygame.K_c and "cdn" in inventario:
                    ativar_cdn(inimigos)
                    inventario.remove("cdn")
                    som_powerup.play()
            
            # Evento de restauração de velocidade
            elif evento.type == pygame.USEREVENT + 1:
                restaurar_velocidade(inimigos, velocidade_original=2)
                
        # Movimento do jogador
        teclas = pygame.key.get_pressed()

        # Movimentação para a esquerda (seta ou tecla A)
        if (teclas[pygame.K_LEFT] or teclas[pygame.K_a]) and jogador.left > monitor_rect.left + 5:
            jogador.move_ip(-5, 0)
            if not invertido:  # Inverte a imagem se não estiver invertido
                imagem_personagem = pygame.transform.flip(imagem_personagem_original, True, False)
                invertido = True

        # Movimentação para a direita (seta ou tecla D)
        if (teclas[pygame.K_RIGHT] or teclas[pygame.K_d]) and jogador.right < monitor_rect.right - 5:
            jogador.move_ip(5, 0)
            if invertido:  # Inverte a imagem de volta se estiver invertido
                imagem_personagem = imagem_personagem_original
                invertido = False
            
        # Movimento dos inimigos
        move_lado = False
        for inimigo in inimigos:
            inimigo.move_ip(inimigo.velocidade * inimigo.direcao, 0)
            if inimigo.right >= monitor_rect.right - 15 or inimigo.left - 15 <= monitor_rect.left:
                move_lado = True
                
        if requisicao:
            requisicao.mover()
            if requisicao.rect.bottom >= monitor_rect.bottom:
                requisicao = None
                personagem.adicionar_dinheiro(5)
                carregar_menu(tela, personagem, fonte_personalizada) 
                
        # Alterar direção e descer uma linha
        if move_lado:
            for inimigo in inimigos:
                inimigo.direcao *= -1
                inimigo.move_ip(0, 20)

        # Movimento dos projéteis
        for projetil in projeteis[:]:
            projetil.move_ip(0, projetil.velocidade)
            if projetil.top < monitor_rect.top + 10:
                projetil.width = 0  # Define a largura do projetil como 0
                projetil.height = 0  # Define a altura do projetil como 0
            
        # Movimento do power-up
        if powerup_atual:
            powerup_atual.mover()
            if powerup_atual.rect.bottom > monitor_rect.bottom - 20:
                powerup_atual = None  # Remove o power-up se sair da tela

        # Colisão do jogador com o power-up
        if powerup_atual and jogador.colliderect(powerup_atual.rect):
            tempo_inicio = pygame.time.get_ticks()
            exibindo_mensagem = True
            nome = powerup_atual.tipo
            primeira_letra = nome[0]
            primeira_letra = primeira_letra.upper()
            inventario.append(nome)
            powerup_atual = None  # Remove o power-up da tela
        
        if exibindo_mensagem:
            exibindo_mensagem = exibir_mensagem(f"Power-up coletado: {nome} Aperte '{primeira_letra}' para utilizar", tempo_inicio, 2000)
            
        # Colisões entre projéteis e inimigos
        for projetil in projeteis[:]:
            for inimigo in inimigos[:]:
                if projetil.colliderect(inimigo):
                    som_explosao.play()
                    projeteis.remove(projetil)
                    inimigos.remove(inimigo)
                    break
                
        # Colisões entre projéteis e requisicoes
        for projetil in projeteis[:]:
            if requisicao:
                if projetil.colliderect(requisicao.rect):
                    som_explosao.play()
                    projeteis.remove(projetil)
                    requisicao = None
                    personagem.perder_vida()
                    carregar_menu(tela, personagem, fonte_personalizada)
                    if personagem.vidas <= 0:
                        # Limpa a tela com a nova tela que já contém o background
                        tela.blit(fundo, (pos_x_monitor, pos_y_monitor))
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
                        return True, False, False   
        # Verifica colisões entre o jogador e os inimigos
        for inimigo in inimigos[:]:
            if jogador.colliderect(inimigo) or inimigo.bottom > monitor_rect.bottom:
                    personagem.perder_vida()
                    carregar_menu(tela, personagem, fonte_personalizada) 
                    inimigos.remove(inimigo)  # Remove o inimigo que colidiu
                    if personagem.vidas <= 0:
                        # Limpa a tela com a nova tela que já contém o background
                        tela.blit(fundo, (pos_x_monitor, pos_y_monitor))
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
                        return True, False, False   
        # Verifica vitória
        if not inimigos:
            fase_atual += 1
            powerup_atual = gerar_powerup()
            if fase_atual > 3:
                som_vitoria.play()
                tela.blit(fundo, (pos_x_monitor, pos_y_monitor))
                fonte = pygame.font.SysFont(None, 36)
                mensagem_fim = fonte.render("Voce conseguiu! Vá falar com seu chefe", True, (0, 0, 0))
                mensagem_fim_rect = mensagem_fim.get_rect(center=monitor_rect.center)
                tela.blit(mensagem_fim, mensagem_fim_rect)

                pygame.display.flip()
                pygame.time.delay(1000)
                return False, True, True
            
            inimigos = gerar_inimigos(fase_atual)

        # Renderiza os objetos no jogo
        tela.blit(imagem_personagem, jogador)
        for inimigo in inimigos:
            tela.blit(inimigo.imagem, inimigo)
        for projetil in projeteis:
            pygame.draw.rect(tela, projetil.cor, projetil)
        if powerup_atual:
            powerup_atual.desenhar(tela)
            
        if requisicao:
            requisicao.desenhar(tela)
        pygame.display.flip()
        
        pygame.time.Clock().tick(60)

    return False, False, False