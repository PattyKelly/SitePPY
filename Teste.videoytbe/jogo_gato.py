import pygame
import random
import sys
import math
import tkinter as tk
from tkinter import simpledialog

# Inicialização do Pygame
pygame.init()

# Configuração da janela do Pygame
largura, altura = 600, 600
janela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo do Gatinho")

# Definição de cores
PRETO = (0, 0, 0)
CINZA_ESCURO = (105, 105, 105)  # Cor da bolinha
MARROM_CLARO = (210, 180, 140)  # Cor do fundo aproximada à madeira
BRANCO = (255, 255, 255)
ROSA = (255, 182, 193)  # Interior das orelhas
AMARELO = (255, 255, 102)  # Olhos do gato

# Tamanhos ajustados
tamanho_cabeca = 40  # Cabeça do gato
tamanho_segmento_cauda = 15  # Segmentos da cauda
tamanho_comida = 15  # Comida

# Configuração de velocidade
fps = 5  # Frames por segundo
fps_incremento = 1  # Incremento de FPS a cada 10 pontos

# Posição inicial e direção da cabeça
cabeca_pos = [300, 300]
cabeca_direcao = "STOP"

# Lista para armazenar a cauda e seus segmentos
cauda = []

# Posição inicial da comida
comida_pos = [random.randrange(1, largura // tamanho_comida) * tamanho_comida,
              random.randrange(1, altura // tamanho_comida) * tamanho_comida]

# Pontuação
pontuacao = 0

# Fonte para exibir a pontuação e o nome do jogador
fonte = pygame.font.Font(None, 36)

# Relógio do Pygame para controlar a velocidade do jogo
relogio = pygame.time.Clock()

# Função para capturar o nome do jogador com Tkinter
def obter_nome():
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal do Tkinter
    nome = simpledialog.askstring("Nome do Jogador", "Digite seu nome:")
    if not nome:
        nome = "Jogador"  # Nome padrão caso o usuário não digite nada
    return nome

# Captura o nome do jogador
nome_jogador = obter_nome()

# Função para mover a cabeça do gato
def mover():
    if cabeca_direcao == "UP":
        cabeca_pos[1] -= tamanho_cabeca
    elif cabeca_direcao == "DOWN":
        cabeca_pos[1] += tamanho_cabeca
    elif cabeca_direcao == "LEFT":
        cabeca_pos[0] -= tamanho_cabeca
    elif cabeca_direcao == "RIGHT":
        cabeca_pos[0] += tamanho_cabeca

# Função para mudar a direção
def mudar_direcao(nova_direcao):
    global cabeca_direcao
    if nova_direcao == "UP" and cabeca_direcao != "DOWN":
        cabeca_direcao = "UP"
    elif nova_direcao == "DOWN" and cabeca_direcao != "UP":
        cabeca_direcao = "DOWN"
    elif nova_direcao == "LEFT" and cabeca_direcao != "RIGHT":
        cabeca_direcao = "LEFT"
    elif nova_direcao == "RIGHT" and cabeca_direcao != "LEFT":
        cabeca_direcao = "RIGHT"

# Função para desenhar a cabeça do gato com orelhas triangulares
def desenhar_cabeca(pos):
    pygame.draw.circle(janela, PRETO, (pos[0] + tamanho_cabeca // 2, pos[1] + tamanho_cabeca // 2), tamanho_cabeca // 2)

    pygame.draw.polygon(janela, PRETO, [
        (pos[0] + 5, pos[1] - 10),  
        (pos[0] + 10, pos[1]),  
        (pos[0], pos[1])
    ])
    pygame.draw.polygon(janela, ROSA, [
        (pos[0] + 7, pos[1] - 8),  
        (pos[0] + 8, pos[1] - 2),  
        (pos[0] + 2, pos[1] - 2)
    ])

    pygame.draw.polygon(janela, PRETO, [
        (pos[0] + tamanho_cabeca - 5, pos[1] - 10),  
        (pos[0] + tamanho_cabeca, pos[1]),  
        (pos[0] + tamanho_cabeca - 10, pos[1])
    ])
    pygame.draw.polygon(janela, ROSA, [
        (pos[0] + tamanho_cabeca - 7, pos[1] - 8),  
        (pos[0] + tamanho_cabeca - 8, pos[1] - 2),  
        (pos[0] + tamanho_cabeca - 12, pos[1] - 2)
    ])

    pygame.draw.circle(janela, BRANCO, (pos[0] + 12, pos[1] + 20), 4)
    pygame.draw.circle(janela, BRANCO, (pos[0] + 28, pos[1] + 20), 4)

# Função para desenhar a cauda com segmentos próximos
def desenhar_cauda():
    for i, segmento in enumerate(cauda):
        x = segmento[0] + i  # Ajuste fino para união dos segmentos
        y = segmento[1]
        pygame.draw.circle(janela, PRETO, (x, y), tamanho_segmento_cauda // 2)

# Função para exibir a pontuação e o nome do jogador
def exibir_pontuacao():
    texto = fonte.render(f"{nome_jogador}: {pontuacao}", True, BRANCO)
    janela.blit(texto, (10, 10))

# Loop principal do jogo
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                mudar_direcao("UP")
            elif event.key == pygame.K_DOWN:
                mudar_direcao("DOWN")
            elif event.key == pygame.K_LEFT:
                mudar_direcao("LEFT")
            elif event.key == pygame.K_RIGHT:
                mudar_direcao("RIGHT")

    mover()

    if (cabeca_pos[0] < 0 or cabeca_pos[0] >= largura or
        cabeca_pos[1] < 0 or cabeca_pos[1] >= altura):
        print("Game Over!")
        pygame.quit()
        sys.exit()

    if (cabeca_pos[0] < comida_pos[0] + tamanho_comida and
        cabeca_pos[0] + tamanho_cabeca > comida_pos[0] and
        cabeca_pos[1] < comida_pos[1] + tamanho_comida and
        cabeca_pos[1] + tamanho_cabeca > comida_pos[1]):
        comida_pos = [random.randrange(1, largura // tamanho_comida) * tamanho_comida,
                      random.randrange(1, altura // tamanho_comida) * tamanho_comida]
        cauda.append(list(cabeca_pos))
        pontuacao += 1

        if pontuacao % 10 == 0:
            fps += fps_incremento

    if cauda:
        cauda.insert(0, list(cabeca_pos))
        cauda.pop()

    janela.fill(MARROM_CLARO)

    desenhar_cabeca(cabeca_pos)
    desenhar_cauda()
    exibir_pontuacao()

    pygame.draw.circle(janela, CINZA_ESCURO, (comida_pos[0] + tamanho_comida // 2, comida_pos[1] + tamanho_comida // 2), tamanho_comida // 2)

    pygame.display.flip()
    relogio.tick(fps)
