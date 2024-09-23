import pygame

class Dialogo:
    def __init__(self, npc, jogador_ponto, falas, caixa_dialogo, fonte, cor, som_fala=None):
        self.npc = npc  # Retângulo do NPC para colisão
        self.jogador_ponto = jogador_ponto  # Ponto do jogador (centro do personagem)
        self.falas = falas  # Lista de falas
        self.caixa_dialogo = caixa_dialogo  # Asset da caixa de diálogo
        self.fonte = fonte  # Fonte usada para exibir o texto
        self.cor = cor  # Cor do texto
        self.som_fala = som_fala  # Som reproduzido ao exibir letras (opcional)
        self.step = 0  # Fase do diálogo (qual fala está sendo exibida)
        self.texto_atual = ""  # Texto sendo exibido no momento
        self.contador_letras = 0  # Controla o efeito de "máquina de escrever"
        self.exibindo_dialogo = False  # Flag para ativar o diálogo
        self.tempo_por_letra = 50  # Intervalo de tempo entre letras (em milissegundos)
        self.ultimo_tempo = pygame.time.get_ticks()  # Tempo da última letra exibida
        self.som_tocando = False  # Controle para saber se o som está tocando

    def iniciar_dialogo(self, ponto_personagem):
        """Ativa o diálogo quando o ponto do personagem estiver dentro do rect do NPC."""
        print("to tentando inicializar")
        if self.npc.collidepoint(ponto_personagem):
            self.step = 0
            self.texto_atual = ""
            self.contador_letras = 0
            self.exibindo_dialogo = True
            if self.som_fala:
                pygame.mixer.Sound.play(self.som_fala)

    def avancar_dialogo(self):
        """Avança o diálogo para a próxima fala."""
        print("to tentando avancar")
        if self.exibindo_dialogo:
            if self.step < len(self.falas) - 1:
                self.step += 1
                self.texto_atual = ""
                self.contador_letras = 0
            else:
                self.exibindo_dialogo = False  # Termina o diálogo

    def atualizar(self):
        """Atualiza o efeito de máquina de escrever e controla o som."""
        print("to tentando atualizar")
        if self.exibindo_dialogo:
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - self.ultimo_tempo > self.tempo_por_letra and self.contador_letras < len(self.falas[self.step]):
                self.texto_atual += self.falas[self.step][self.contador_letras]
                self.contador_letras += 1
                self.ultimo_tempo = tempo_atual
                
                # Toca o som de fala se definido
                if self.som_fala and not self.som_tocando:
                    pygame.mixer.Sound.play(self.som_fala)
                    self.som_tocando = True

            # Parar o som quando terminar de escrever a fala atual
            if self.contador_letras == len(self.falas[self.step]):
                self.som_tocando = False

    def desenhar(self, tela):
        """Desenha a caixa de diálogo e o texto atual."""
        if self.exibindo_dialogo:
            print("to tentando desenhar")
            tela.blit(self.caixa_dialogo, (200, 200))  # Ajuste a posição conforme necessário
            
            # Desenha o texto dentro da caixa de diálogo
            linhas = self.quebrar_texto(self.texto_atual, self.fonte, self.caixa_dialogo.get_width() - 20)
            for i, linha in enumerate(linhas):
                texto_renderizado = self.fonte.render(linha, True, self.cor)
                tela.blit(texto_renderizado, (60, 420 + i * 30))  # Ajuste conforme o espaçamento desejado

    def quebrar_texto(self, texto, fonte, largura_max):
        """Quebra o texto em múltiplas linhas para caber na caixa de diálogo."""
        print("to tentando quebrar o texto")
        palavras = texto.split(' ')
        linhas = []
        linha_atual = ""
        for palavra in palavras:
            if fonte.size(linha_atual + palavra)[0] < largura_max:
                linha_atual += palavra + " "
            else:
                linhas.append(linha_atual)
                linha_atual = palavra + " "
        if linha_atual:
            linhas.append(linha_atual)
        return linhas
