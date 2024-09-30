import pygame

import pygame

# Define o caminho para os áudios
CAMINHO_AUDIO = "D:\\jogo\\audios\\"

class Personagem:
    def __init__(self, vidas=5, dinheiro=0):
        # Inicializa o mixer do Pygame
        pygame.mixer.init()
        
        # Carrega os sons
        self.som_perder_vida = pygame.mixer.Sound(CAMINHO_AUDIO + "perder_vida.wav")
        self.som_gastar_dinheiro = pygame.mixer.Sound(CAMINHO_AUDIO + "gastar_dinheiro.mp3")
        self.som_ganhar_dinheiro = pygame.mixer.Sound(CAMINHO_AUDIO + "ganhar_dinheiro.wav")

        self.vidas = vidas
        self.dinheiro = dinheiro
        self.objetos = []  # Inicializa a lista de objetos

    def perder_vida(self):
        if self.vidas > 0:
            self.vidas -= 1
            self.som_perder_vida.play()  # Toca o som ao perder vida

    def ganhar_vida(self):
        if self.vidas < 5:
            self.vidas += 1

    def adicionar_dinheiro(self, valor):
        self.dinheiro += valor
        self.som_ganhar_dinheiro.play()  # Toca o som ao ganhar dinheiro

    def remover_dinheiro(self, valor):
        if self.dinheiro >= valor:
            self.dinheiro -= valor
            self.som_gastar_dinheiro.play()  # Toca o som ao gastar dinheiro

    def adicionar_objeto(self, objeto):
        self.objetos.append(objeto)  # Adiciona um objeto à lista

    def possui_objeto(self, objeto):
        return objeto in self.objetos  # Verifica se o objeto está na lista