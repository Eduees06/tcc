class Personagem:
    def __init__(self, vidas=5, dinheiro=0):
        self.vidas = vidas
        self.dinheiro = dinheiro
        self.objetos = []  # Inicializa a lista de objetos

    def perder_vida(self):
        if self.vidas > 0:
            self.vidas -= 1

    def ganhar_vida(self):
        self.vidas += 1

    def adicionar_dinheiro(self, valor):
        self.dinheiro += valor

    def remover_dinheiro(self, valor):
        if self.dinheiro >= valor:
            self.dinheiro -= valor

    def adicionar_objeto(self, objeto):
        self.objetos.append(objeto)  # Adiciona um objeto à lista

    def possui_objeto(self, objeto):
        return objeto in self.objetos  # Verifica se o objeto está na lista