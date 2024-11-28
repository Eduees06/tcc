
# Configurações da tela
RESOLUCAO = "FULL_HD"  # Pode ser "HD" ou "FULL_HD"

# Configurações de resolução
if RESOLUCAO == "HD":
    LARGURA_TELA = 1280
    ALTURA_TELA = 720
elif RESOLUCAO == "FULL_HD":
    LARGURA_TELA = 1920
    ALTURA_TELA = 1080
else:
    raise ValueError("Resolução não suportada. Use 'HD' ou 'FULL_HD'.")

# Configurações do personagem
VELOCIDADE_PERSONAGEM = int(4 * LARGURA_TELA / 1280)
VELOCIDADE_CORRER = int(8 * LARGURA_TELA / 1280)
TAMANHO_PERSONAGEM = int(150 * LARGURA_TELA / 1280)