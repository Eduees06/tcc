import pygame
import random
import os
from personagem import *
from config import LARGURA_TELA, ALTURA_TELA, TAMANHO_PERSONAGEM
from utils import *

# Função para verificar se uma posição é acessível a partir de outra
def posicao_acessivel(labirinto, pos_inicial, pos_alvo, pos_backup):
    largura = len(labirinto[0])
    altura = len(labirinto)

    visitados = set()  # Para rastrear células visitadas
    fila = [pos_inicial]  # Fila para BFS

    while fila:
        x, y = fila.pop(0)
        if (x, y) == pos_alvo:
            return True  # Encontrou o alvo
        visitados.add((x, y))

        # Verifica as direções possíveis (cima, baixo, esquerda, direita)
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < largura and 0 <= ny < altura and
                    labirinto[ny][nx] == 0 and
                    (nx, ny) not in visitados and
                    (nx, ny) != pos_backup):  # Não pode passar pelo backup
                fila.append((nx, ny))  # Adiciona à fila se for um caminho e não foi visitado

    return False  # Não encontrou um caminho para o alvo

# Função para gerar um labirinto mais complexo com arquivos corrompidos
def gerar_labirinto(largura, altura, pos_inicial, distancia_minima, arquivos_resolvidos):
    labirinto = [[1] * largura for _ in range(altura)]  # Inicializa com paredes (1)

    def carve_passages_from(x, y):
        direcoes = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        random.shuffle(direcoes)  # Embaralha direções para aleatoriedade

        for dx, dy in direcoes:
            nx, ny = x + dx, y + dy
            if 0 < nx < largura and 0 < ny < altura and labirinto[ny][nx] == 1:
                labirinto[y + dy // 2][x + dx // 2] = 0  # Abre um caminho
                labirinto[ny][nx] = 0  # Define a nova célula como caminho
                carve_passages_from(nx, ny)  # Recursão para novas células

    # Começa o carving a partir de uma posição inicial
    carve_passages_from(1, 1)

    # Definir a posição final como um caminho aleatório, respeitando a distância mínima
    while True:
        final_x = random.randint(1, largura - 2)
        final_y = random.randint(1, altura - 2)

        if labirinto[final_y][final_x] == 0:
            if (abs(final_x - pos_inicial[0]) >= distancia_minima or 
                abs(final_y - pos_inicial[1]) >= distancia_minima):  # Verifica a distância mínima
                labirinto[final_y][final_x] = 0
                break  # Define a posição final

    # Gerar 3 arquivos corrompidos em posições aleatórias do labirinto
    arquivos_corrompidos = []
    nomes_arquivos = list(arquivos.keys())  # Lista de nomes de arquivos
    anagramas_usados = set()  # Conjunto para armazenar anagramas usados

    while len(arquivos_corrompidos) < 3 and nomes_arquivos:
        arquivo_x = random.randint(1, largura - 2)
        arquivo_y = random.randint(1, altura - 2)

        if labirinto[arquivo_y][arquivo_x] == 0 and (arquivo_x, arquivo_y) != (final_x, final_y):
            nome_arquivo = random.choice(nomes_arquivos)  # Seleciona um arquivo aleatório
            
            # Verifica se o arquivo já foi resolvido
            if nome_arquivo not in arquivos_resolvidos:
                anagrama = arquivos[nome_arquivo]  # Obtém o anagrama correspondente
                
                # Verifica se o anagrama já foi usado
                if anagrama not in anagramas_usados:
                    # Verifica se a posição do arquivo é acessível a partir da posição inicial, sem passar pelo backup
                    if posicao_acessivel(labirinto, pos_inicial, (arquivo_x, arquivo_y), (final_x, final_y)):
                        arquivos_corrompidos.append((arquivo_x, arquivo_y, nome_arquivo, anagrama))  # Adiciona à lista
                        anagramas_usados.add(anagrama)  # Marca o anagrama como usado
                        nomes_arquivos.remove(nome_arquivo)  # Remove o arquivo da lista de nomes

    return labirinto, (final_x, final_y), arquivos_corrompidos  # Retorna os arquivos corrompidos também

# Dicionário com os arquivos e seus anagramas
arquivos = {
    "phishing.txt": "INGPHISH",         # Anagrama de phishing
    "ddos.txt": "SODD",                 # Anagrama de ddos
    "hacker.txt": "KEARCH",             # Anagrama de hacker
    "malware.txt": "WALMERA",           # Anagrama de malware
    "firewall.txt": "RAFWLILE",         # Anagrama de firewall
    "antivirus.txt": "VITRANUIS",       # Anagrama de antivirus
    "backup.txt": "KABUPC",             # Anagrama de backup
    "criptografia.txt": "TGRAIFCOPRIA", # Anagrama de criptografia
    "ransomware.txt": "RAMONSERAW",           # Anagrama de internet
}
# Função para exibir a tela de anagramas
def mostrar_tela_anagrama(tela, monitor_rect, anagrama, arquivo_nome, personagem):
    # Carregar a imagem de fundo
    imagem_fundo_original = pygame.image.load(f"{caminho_assets}/hackerbackground.png").convert()

    # Escalonar a imagem de fundo para o tamanho do monitor
    imagem_fundo = pygame.transform.scale(imagem_fundo_original, (monitor_rect.width, monitor_rect.height + 8))

    fonte = pygame.font.SysFont(None, 36)
    input_text = ""  # Para armazenar a entrada do jogador
    dica_exibida = False  # Para rastrear se a dica foi exibida
    tela_anagrama = True

    while tela_anagrama:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return False, False  # Sai da tela de anagrama
                elif evento.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]  # Apaga o último caractere
                elif evento.key == pygame.K_RETURN:
                    if input_text.lower() == arquivo_nome.split('.')[0]:  # Verifica se o anagrama está correto
                        return True, False  # Se estiver correto, retorna verdadeiro (passou no desafio)
                    else:
                        input_text = ""  # Reseta a entrada se estiver errado
                        personagem.perder_vida()
                        carregar_menu(tela, personagem, fonte_personalizada)
                        if personagem.vidas <= 0:
                            return False, True
                else:
                    input_text += evento.unicode  # Adiciona o caractere digitado

            # Detecta clique do mouse
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:  # Verifica se o botão esquerdo do mouse foi pressionado
                    mouse_x, mouse_y = evento.pos
                    if rect_dica.collidepoint(mouse_x, mouse_y):  # Verifica se clicou no botão Dica
                        # Solicita confirmação para comprar a dica
                        if personagem.dinheiro >= 20 and not dica_exibida:  # Verifica se o jogador tem dinheiro suficiente
                            confirmacao = mostrar_confirmacao(tela, "Deseja comprar uma dica por 20 moedas?", monitor_rect)  # Exibe a confirmação
                            if confirmacao:
                                personagem.remover_dinheiro(20)  # Remove 20 moedas
                                dica_exibida = True  # Marca que a dica foi exibida
                                
                        elif dica_exibida:
                            mostrar_mensagem(tela, "Você ja possui a dica para este anagrama", monitor_rect)  # Mensagem de alerta
                        else:
                            mostrar_mensagem(tela, "A dica custa 20 moedas, você não tem dinheiro suficiente!", monitor_rect)  # Mensagem de alerta

        # Desenhar a imagem de fundo escalonada dentro do monitor
        tela.blit(imagem_fundo, monitor_rect.topleft)

        # Exibir o anagrama
        anagrama_texto = fonte.render(f"Anagrama: {anagrama}", True, (255, 255, 255))
        anagrama_rect = anagrama_texto.get_rect(center=(monitor_rect.centerx, monitor_rect.centery - 50))

        # Criar retângulo preto atrás do anagrama
        pygame.draw.rect(tela, (0, 0, 0), anagrama_rect.inflate(20, 20))  # Inflar o retângulo para um pouco maior
        tela.blit(anagrama_texto, anagrama_rect)

        # Criar retângulo para a entrada do jogador
        rect_input = pygame.Rect(monitor_rect.centerx - 150, monitor_rect.centery + 30, 300, 50)  # Retângulo branco
        pygame.draw.rect(tela, (255, 255, 255), rect_input)  # Retângulo branco
        pygame.draw.rect(tela, (0, 0, 0), rect_input, 2)  # Borda preta

        # Exibir a mensagem "Insira a chave" ou a entrada do usuário
        if input_text == "":
            label_texto = fonte.render("Insira a chave", True, (0, 0, 0))  # Texto preto
            tela.blit(label_texto, label_texto.get_rect(center=rect_input.center))
        else:
            input_surface = fonte.render(input_text, True, (0, 0, 0))  # Texto preto
            tela.blit(input_surface, input_surface.get_rect(center=rect_input.center))

        # Mensagens de tentativas restantes e desistência
        tentativas_texto = fonte.render("Aperte Enter para inserir", True, (0, 0, 0))
        desistir_texto = fonte.render("Aperte ESC para desistir", True, (0, 0, 0))

        # Criar retângulo preto atrás das mensagens
        mensagens_rect = pygame.Rect(monitor_rect.x + 10, monitor_rect.y + 10, 300, 80)  # Retângulo para mensagens
        pygame.draw.rect(tela, (0, 255, 0), mensagens_rect)  # Retângulo VERDE
        pygame.draw.rect(tela, (0, 0, 0), mensagens_rect, 3)  # 3 é a espessura da borda

        # Blitar as mensagens
        tela.blit(tentativas_texto, (mensagens_rect.x + 5, mensagens_rect.y + 10))  # Tentativas
        tela.blit(desistir_texto, (mensagens_rect.x + 5, mensagens_rect.y + 40))  # Desistir

        # Botão Dica
        rect_dica = pygame.Rect(monitor_rect.right - 110, monitor_rect.bottom - 60, 100, 40)  # Botão Dica
        pygame.draw.rect(tela, (0, 255, 0), rect_dica)  # Botão verde
        pygame.draw.rect(tela, (0, 0, 0), rect_dica, 2)  # Bordas pretas
        dica_texto = fonte.render("Dica", True, (0, 0, 0))  # Texto preto
        tela.blit(dica_texto, dica_texto.get_rect(center=rect_dica.center))  # Exibir texto no botão

        # Exibir a dica se foi exibida
        if dica_exibida:
            dica = obter_dica(arquivo_nome)  # Função para obter a dica baseada no nome do arquivo
            dica_texto = fonte.render(f"Dica: {dica}", True, (255, 255, 255))  # Texto da dica
            dica_rect = dica_texto.get_rect(center=(monitor_rect.centerx, monitor_rect.centery + 100))  # Centraliza a dica abaixo do monitor

            # Cria um retângulo preto atrás da dica
            retangulo_dica_rect = dica_rect.inflate(20, 10)  # Inflar o retângulo para dar espaço extra ao redor do texto
            retangulo_dica_rect.center = dica_rect.center  # Centraliza o retângulo com o texto

            # Desenha o retângulo preto
            pygame.draw.rect(tela, (0, 100, 0), retangulo_dica_rect)  # Retângulo atrás da dica
            pygame.draw.rect(tela, (0, 0, 0), retangulo_dica_rect, 3)  # 3 é a espessura da borda
            # Exibe a dica na tela
            tela.blit(dica_texto, dica_rect)  # Exibe o texto da dica

        pygame.display.flip()
        
def mostrar_mensagem(tela, mensagem, monitor_rect):
    """Função para exibir uma mensagem na tela dentro do retângulo do monitor."""
    fonte = pygame.font.SysFont(None, 36)

    # Cria um retângulo para a mensagem
    texto = fonte.render(mensagem, True, (255, 255, 255))
    texto_rect = texto.get_rect(center=(monitor_rect.centerx, monitor_rect.bottom - texto.get_height() // 2 - 20))

    # Cria um retângulo verde escuro atrás da mensagem
    retangulo_rect = texto_rect.inflate(20, 20)  # Inflar o retângulo para dar espaço extra ao redor do texto
    retangulo_rect.center = texto_rect.center  # Centraliza o retângulo com o texto

    # Desenha o retângulo verde escuro
    pygame.draw.rect(tela, (0, 100, 0), retangulo_rect)

    # Desenha a borda preta ao redor do retângulo
    pygame.draw.rect(tela, (0, 0, 0), retangulo_rect, 3)  # 3 é a espessura da borda

    # Exibir a mensagem
    tela.blit(texto, texto_rect)
    pygame.display.flip()

    # Esperar um tempo antes de voltar à tela anterior
    pygame.time.delay(1000)  # Exibe a mensagem por 1 segundo

def mostrar_confirmacao(tela, mensagem, monitor_rect):
    """Função para exibir uma tela de confirmação dentro do retângulo do monitor."""
    fonte = pygame.font.SysFont(None, 36)

    # Cria um retângulo para a mensagem dentro do monitor
    texto = fonte.render(mensagem, True, (255, 255, 255))
    texto_rect = texto.get_rect(center=(monitor_rect.centerx, monitor_rect.bottom - texto.get_height() // 2 - 40))

    # Cria um retângulo preto atrás da mensagem
    retangulo_texto_rect = texto_rect.inflate(20, 20)  # Inflar o retângulo para dar espaço extra ao redor do texto
    retangulo_texto_rect.center = texto_rect.center  # Centraliza o retângulo com o texto

    # Botões de confirmação
    rect_sim = pygame.Rect(texto_rect.centerx - 60, texto_rect.centery + 20, 50, 30)
    rect_nao = pygame.Rect(texto_rect.centerx + 10, texto_rect.centery + 20, 50, 30)

    # Desenha os retângulos pretos
    pygame.draw.rect(tela, (0, 100, 0), retangulo_texto_rect)  # Retângulo atrás da mensagem
    pygame.draw.rect(tela, (0, 0, 0), retangulo_texto_rect, 3)  # 3 é a espessura da borda
    
    # Desenha os botões
    pygame.draw.rect(tela, (0, 255, 0), rect_sim)  # Botão Sim
    pygame.draw.rect(tela, (255, 0, 0), rect_nao)  # Botão Não
    pygame.draw.rect(tela, (0, 0, 0), rect_sim, 2)  # Borda preta
    pygame.draw.rect(tela, (0, 0, 0), rect_nao, 2)  # Borda preta

    # Renderiza o texto dos botões
    texto_sim = fonte.render("Sim", True, (0, 0, 0))
    texto_nao = fonte.render("Não", True, (0, 0, 0))

    # Exibe o texto na tela
    tela.blit(texto, texto_rect)
    tela.blit(texto_sim, texto_sim.get_rect(center=rect_sim.center))
    tela.blit(texto_nao, texto_nao.get_rect(center=rect_nao.center))

    pygame.display.flip()

    # Loop de confirmação
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:  # Verifica se o botão esquerdo do mouse foi pressionado
                    mouse_x, mouse_y = evento.pos
                    if rect_sim.collidepoint(mouse_x, mouse_y):
                        return True  # Retorna verdadeiro se o jogador confirmou
                    if rect_nao.collidepoint(mouse_x, mouse_y):
                        return False  # Retorna falso se o jogador cancelou

def obter_dica(arquivo_nome):
    """Função para obter a dica baseada no nome do arquivo."""
    # Dicionário de dicas para cada arquivo
    dicas = {
        "phishing.txt": "Ataque com e-mails que parecem legítimos.",
        "ddos.txt": "Ataque que sobrecarrega um serviço.",
        "hacker.txt": "Perito em exploração de vulnerabilidades.",
        "malware.txt": "Software que causa danos ao sistema.",
        "firewall.txt": "Barreira de proteção em redes.",
        "antivirus.txt": "Defesa contra ameaças digitais.",
        "backup.txt": "Cópia de segurança de dados importantes.",
        "criptografia.txt": "Técnica para proteger informações.",
        "ransomware.txt": "Ataque que sequestra informações usando criptografia.",
    }
    
    # Retorna a dica correspondente ao arquivo, se existir
    return dicas.get(arquivo_nome, "Dica não disponível.")  # Dica padrão se o arquivo não estiver no dicionário
        
# Função principal do minigame
def minigamefase2(tela, personagem, concluido, completou_todos):
    som_game_over = pygame.mixer.Sound(os.path.join(CAMINHO_AUDIO, "game_over.wav"))
    largura_nova, altura_nova = 1000, 1000
    imagem_parede_original = pygame.image.load(os.path.join(caminho_assets, "caminho_labirinto.png")).convert_alpha()
    som_vitoria = pygame.mixer.Sound(os.path.join(CAMINHO_AUDIO, "victory.wav"))
    som_vitoria.set_volume(0.2)
    imagem_personagem_original = pygame.image.load(os.path.join(caminho_assets, "personagem.png")).convert_alpha()
    imagem_personagem = imagem_personagem_original
    largura_personagem, altura_personagem = imagem_personagem.get_size()
    regras = pygame.image.load(os.path.join(caminho_assets, "background_regras2.png")).convert_alpha()
    regras = pygame.transform.scale(regras, (largura_nova, altura_nova))
    background = pygame.image.load(os.path.join(caminho_assets, "background2.png")).convert_alpha()
    background = pygame.transform.scale(background, (largura_nova, altura_nova))
    
    pos_x = (tela.get_width() - largura_nova) // 2
    pos_y = (tela.get_height() - altura_nova) // 2    
    
    pos_jogador = [1, 1]  # Posição inicial do jogador
    monitor_rect = pygame.Rect(pos_x + 40, pos_y + 260, largura_nova // 1.085, altura_nova // 1.88)
    
    largura_labirinto, altura_labirinto = 20, 15  # Tamanho do labirinto
    labirinto = None
    final_pos = None
    pos_jogador = [1, 1]
    esperando = True
    mostrando_regras = False
    labirinto_gerado = False
    invertido = False
    cor_arquivo = (255, 0, 0)
    cor_caminho = (255, 228, 196)
    nivel = 1  # Começa no nível 1
    raio_visao = 5
    mostrando_labirintos = False
    arquivos_resolvidos = set()  # Para rastrear os arquivos já resolvidos
    completou_todos_arquivos = False
    if concluido:
        tela.blit(background, (pos_x, pos_y))
        fonte = pygame.font.SysFont(None, 36)
        mensagem_fim = fonte.render("Voce conseguiu! Vá falar com seu chefe", True, (0, 0, 0))
        mensagem_fim_rect = mensagem_fim.get_rect(center=monitor_rect.center)
        tela.blit(mensagem_fim, mensagem_fim_rect)

        pygame.display.flip()
        pygame.time.delay(1000)
        if completou_todos:
            return False, True, True
        else:
            return False, True, False
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return False, False, False
                if evento.key == pygame.K_e and not mostrando_labirintos:  # Iniciar o minigame e gerar o labirinto
                    mostrando_labirintos = True
                    if not labirinto_gerado:
                        labirinto_gerado = True
                        labirinto, final_pos, arquivos_corrompidos = gerar_labirinto(largura_labirinto, altura_labirinto,pos_jogador, 10, arquivos_resolvidos)
                if evento.key == pygame.K_i:  # Mostrar regras
                    mostrando_regras = not mostrando_regras

                if labirinto_gerado:  # Somente permitir movimentação após o labirinto ser gerado
                    if evento.type == pygame.KEYDOWN:  # Verifica se é um evento de tecla
                        nova_pos = pos_jogador.copy()  # Copia a posição atual
                        if evento.key == pygame.K_w:  # Mover para cima
                            nova_pos[1] -= 1
                        elif evento.key == pygame.K_s:  # Mover para baixo
                            nova_pos[1] += 1
                        elif evento.key == pygame.K_a:  # Mover para a esquerda
                            nova_pos[0] -= 1
                            if not invertido:  # Inverte a imagem se não estiver invertido
                                imagem_personagem = pygame.transform.flip(imagem_personagem_original, True, False)
                                invertido = True
                        elif evento.key == pygame.K_d:  # Mover para a direita
                            nova_pos[0] += 1
                            if invertido:  # Inverte a imagem de volta se estiver invertido
                                imagem_personagem = imagem_personagem_original
                                invertido = False
                        # Verificar se a nova posição está dentro dos limites do labirinto
                        if 0 <= nova_pos[0] < largura_labirinto and 0 <= nova_pos[1] < altura_labirinto:
                            # Verificar se a nova posição é um caminho
                            if labirinto[nova_pos[1]][nova_pos[0]] == 0:
                                pos_jogador = nova_pos  # Atualiza a posição do jogador
                        # Verificar se o jogador chegou ao final
                        for x, y, nome_arquivo, anagrama in arquivos_corrompidos:
                            if pos_jogador[0] == x and pos_jogador[1] == y:
                                # Se o jogador estiver em um arquivo corrompido, exibe o anagrama
                                if nome_arquivo not in arquivos_resolvidos:  # Verifica se já foi resolvido
                                    resolveu, perdeu = mostrar_tela_anagrama(tela, monitor_rect, anagrama, nome_arquivo, personagem)
                                    if resolveu:
                                        arquivos_resolvidos.add(nome_arquivo)  # Marca como resolvido
                                        personagem.adicionar_dinheiro(10)
                                        carregar_menu(tela, personagem, fonte_personalizada)  
                                    if perdeu:
                                        # Limpa a tela com a nova tela que já contém o background
                                        tela.blit(background, (pos_x, pos_y))
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
                                    break  # Sai do loop após encontrar o arquivo
                                
                        if pos_jogador == list(final_pos):
                            if nivel < 3:  # Se ainda não terminou todos os níveis
                                nivel += 1  # Próximo nível
                                pos_jogador = [1, 1]  # Reposicionar jogador no início
                                raio_visao -= 1
                                labirinto, final_pos, arquivos_corrompidos = gerar_labirinto(largura_labirinto, altura_labirinto,pos_jogador, 10, arquivos_resolvidos)  # Gerar novo labirinto
                            else:
                                # Jogador venceu
                                som_vitoria.play()
                                tela.blit(background, (pos_x, pos_y))
                                fonte = pygame.font.SysFont(None, 36)
                                mensagem_fim = fonte.render("Voce conseguiu! Vá falar com seu chefe", True, (0, 0, 0))
                                mensagem_fim_rect = mensagem_fim.get_rect(center=(monitor_rect.centerx, monitor_rect.centery + 150))
                                tela.blit(mensagem_fim, mensagem_fim_rect)
                                pygame.display.flip()
                                pygame.time.delay(1000)
                                completou_todos_arquivos = len(arquivos_resolvidos) == 9
                                return False, True, completou_todos_arquivos
                            
                            
        # Desenhar a tela
        if not mostrando_labirintos :
            tela.blit(background, (pos_x, pos_y))

        if labirinto_gerado:
            cell_width = monitor_rect.width // largura_labirinto
            cell_height = (monitor_rect.height // altura_labirinto) + 1

            # Redimensiona a imagem da parede uma vez
            imagem_parede = pygame.transform.scale(imagem_parede_original, (cell_width, cell_height))

            # Pré-calcular as posições do monitor
            monitor_x = monitor_rect.x
            monitor_y = monitor_rect.y
            
            # Posições do jogador
            pos_x_personagem = monitor_x + pos_jogador[0] * cell_width + (cell_width - largura_personagem) // 2
            pos_y_personagem = monitor_y + pos_jogador[1] * cell_height + (cell_height - altura_personagem) // 2

            # Desenhar o labirinto
            for y in range(altura_labirinto):
                for x in range(largura_labirinto):
                    if labirinto[y][x] == 0:  # Caminho
                        pygame.draw.rect(tela, cor_caminho, 
                                        (monitor_x + x * cell_width, 
                                        monitor_y + y * cell_height, 
                                        cell_width, 
                                        cell_height))
                    else:  # Parede
                        tela.blit(imagem_parede, (monitor_x + x * cell_width, 
                                                    monitor_y + y * cell_height))

            # Desenhar arquivos corrompidos
            fonte = pygame.font.SysFont(None, 20)
            for (arquivo_x, arquivo_y, nome_arquivo, anagrama) in arquivos_corrompidos:
                if nome_arquivo in arquivos_resolvidos:  # Verifica se o arquivo já foi resolvido
                    pygame.draw.rect(tela, cor_caminho, 
                                    (monitor_x + arquivo_x * cell_width, 
                                    monitor_y + arquivo_y * cell_height, 
                                    cell_width, 
                                    cell_height))  # Pintar na cor do caminho
                else:
                    rect = pygame.Rect(monitor_x + arquivo_x * cell_width, monitor_y + arquivo_y * cell_height, cell_width, cell_height)
                    pygame.draw.rect(tela, cor_arquivo, rect)  # Pinta de vermelho
                    texto_arquivo = fonte.render("Arquivo", True, (255, 255, 255))  # Renderiza o nome do arquivo
                    texto_rect = texto_arquivo.get_rect(center=rect.center)
                    tela.blit(texto_arquivo, texto_rect)  # Desenha o texto do arquivo

            # Desenhar o jogador
            tela.blit(imagem_personagem, (pos_x_personagem, pos_y_personagem))

            # Desenhar a posição final
            pygame.draw.rect(tela, (0, 0, 255), 
                            (monitor_x + final_pos[0] * cell_width,
                            monitor_y + final_pos[1] * cell_height,
                            cell_width,
                            cell_height))

            fonte_final = pygame.font.SysFont(None, 20)
            texto_final = fonte_final.render("Backup", True, (255, 255, 255))  # Texto em branco
            tela.blit(texto_final, (monitor_x + final_pos[0] * cell_width,
                                    monitor_y + final_pos[1] * cell_height + 5))

            # **Visibilidade Reduzida (Neblina)**
            overlay = pygame.Surface((monitor_rect.width, monitor_rect.height + 8), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 255))  # Preenche a superfície com preto total (255 alfa)

            # Posição do jogador
            visao_jogador_x = pos_jogador[0] * cell_width + cell_width // 2
            visao_jogador_y = pos_jogador[1] * cell_height + cell_height // 2

            # Círculo transparente na superfície preta que será a área visível
            pygame.draw.circle(overlay, (0, 0, 0, 0), (visao_jogador_x, visao_jogador_y), raio_visao * cell_width)  # Círculo transparente

            # Usar a superfície de overlay para cobrir o labirinto
            tela.blit(overlay, (monitor_x, monitor_y))  # Desenha a superfície escura dentro do monitor
        else:
            if nivel == 1:
                if mostrando_regras:
                    tela.blit(regras, (pos_x, pos_y))
                else:
                    fonte = pygame.font.SysFont(None, 25)
                    mensagem1 = fonte.render("{Aperte E para começar o minigame}", True, (0, 0, 0))
                    mensagem2 = fonte.render("{Aperte I para ver as regras}", True, (0, 0, 0))
                    mensagem3 = fonte.render("{Aperte ESC para sair}", True, (0, 0, 0))
                    
                    # Centralizando cada mensagem em relação ao monitor
                    tela.blit(mensagem1, mensagem1.get_rect(center=(monitor_rect.centerx - 300, monitor_rect.centery + 175)))
                    tela.blit(mensagem2, mensagem2.get_rect(center=(monitor_rect.centerx + 0, monitor_rect.centery + 175)))
                    tela.blit(mensagem3, mensagem3.get_rect(center=(monitor_rect.centerx + 300, monitor_rect.centery + 175)))
            
        pygame.display.flip()
    return False, False, False 