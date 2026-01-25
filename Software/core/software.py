from terminal import processar_comando
from config import CAMINHO_UNIVERSO, WIDTH, HEIGHT, cores_tipos
from engine import Universo
import pygame
import sys
import os
import random

# =========================================================
# CONFIGURAÇÃO INICIAL
# =========================================================

estado = {
    "escala_tempo": 1.0,
    "pausado": False
}

pygame.init()


screen = pygame.display.set_mode((WIDTH, HEIGHT))
tela_atual = "visual"
pygame.display.set_caption("SO Experimental - Simulação Computacional com Terminal")

clock = pygame.time.Clock()

font = pygame.font.SysFont("consolas", 20)
font_terminal = pygame.font.SysFont("consolas", 14)

# =========================================================
# LAYOUT
# =========================================================
#terminal_height = HEIGHT // 1.3
universe_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
#terminal_rect = pygam
terminal_linhas = []
historico_comandos = []
indice_historico = -1

# =========================================================
# DADOS E UNIVERSO
# =========================================================
universo = Universo(caminho=CAMINHO_UNIVERSO)

#tipos = ["Memória", "Processador", "Armazenamento", "Energia", "Rede"]

contador_salvamento = 0
current_text = ""

# =========================================================
# FUNÇÕES
# =========================================================
def desenhar_terminal(surface, linhas, font, largura_max):
    y = 40
    linhas_quebradas = []
    
    # Quebra cada linha se ultrapassar a largura máxima
    for linha in linhas:
        linha = str(linha)
        palavras = linha.split(" ")
        nova_linha = ""
        for palavra in palavras:
            teste = nova_linha + (" " if nova_linha else "") + palavra
            if font.size(teste)[0] > largura_max:
                linhas_quebradas.append(nova_linha)
                nova_linha = palavra
            else:
                nova_linha = teste
        linhas_quebradas.append(nova_linha)
    
    # Desenha todas as linhas quebradas
    for l in linhas_quebradas[-30:]:  # mostra só as últimas 15 linhas
        texto = font.render(l, True, (0, 255, 0))
        surface.blit(texto, (10, y))
        y += font.get_linesize()



def desenhar_pulsos(universo, screen):
    for pulso in universo.pulsos:

        x, y = pulso["pos"]
        energia = pulso["energia"]
        progresso = pulso["progresso"]

        raio = max(2, int(2 + energia * 0.1))

        energia_norm = min(energia / 1.0, 1.0)

        cor = (
            int(255 * energia_norm),
            50,
            int(255 * (1 - energia_norm))
        )

       
        pygame.draw.circle(
            screen,
            (cor),
            (int(x), int(y)),
            raio
        )



def evoluir_universo(universo, dados_mortos, estado, screen):
    if not hasattr(universo, "dados"):
        universo.dados = []

    escala = estado["escala_tempo"]
    if estado["pausado"]:
        escala = 0
       
    universo.evoluir_pulsos(escala)

    for dado in universo.dados:
        # Consumo por tipo
        if dado["tipo"] == "Processador":
            consumo = 0.02
        elif dado["tipo"] == "Memória":
            consumo = 0.01
        elif dado["tipo"] == "Armazenamento":
            consumo = 0.002
        elif dado["tipo"] == "Rede":
            consumo = 0.01
        elif dado["tipo"] == "Energia":
            consumo = 0.01
        else:
            consumo = 0.01

        for outro in universo.dados:
            if outro == dado:
                continue

            distancia = ((dado["pos"][0] - outro["pos"][0]) ** 2 +
                         (dado["pos"][1] - outro["pos"][1]) ** 2) ** 0.5

            if distancia < 100:
                # Checa se já existe pulso entre esses dois
                existe_pulso = any(
                    (p["origem"] == dado["id"] and p["destino"] == outro["id"]) or
                    (p["origem"] == outro["id"] and p["destino"] == dado["id"])
                    for p in getattr(universo, "pulsos", [])
                )
                if not existe_pulso:
                    # Cria pulso de energia
                    universo.enviar_pulso(dado["id"], outro["id"], energia=0.2)

        # -------------------------
        # Verifica se dado morreu
        # -------------------------
        if dado["energia"] <= 0:
            dados_mortos.append(dado)
            universo.dados.remove(dado)
            universo.salvar()  # salva universo sem o dado morto
            universo.salvar_mortos()  # salva na lista de mortos

        # -------------------------
        # Desenho
        # -------------------------
        radius = max(dado["energia"], 1)
        pygame.draw.circle(screen, cores_tipos[dado["tipo"]], dado["pos"], int(radius))
          
        
        # Atualiza fator tempo
        dado["fator_tempo"] = 1 / (1 + 0.1 * dado["energia"])

        # Atualiza energia
        dado["energia"] -= consumo * dado["fator_tempo"] * escala
        dado["energia"] = max(0, min(dado["energia"], 10))

        
        

    

        # Inicializa tempo próprio se não existir
        if "tempo_proprio" not in dado:
            dado["tempo_proprio"] = 0.0

        # Atualiza tempo próprio
        delta_t = escala
        delta_tau = delta_t * dado["fator_tempo"]
        dado["tempo_proprio"] += delta_tau

        # Remove dados mortos
        if dado["energia"] <= 0:
            universo.dados_mortos.append(dado)
            universo.dados.remove(dado)
            universo.salvar()
            universo.salvar_mortos()

        # Desenhar dado
        cor = cores_tipos[dado["tipo"]]
        energia_normalizada = dado["energia"] / 10

        r, g, b = cores_tipos[dado["tipo"]]
        cor = (int(r * energia_normalizada), int(g * energia_normalizada), int(b * energia_normalizada))
        radius = max(dado["energia"], 2)
        pygame.draw.circle(screen, cor, dado["pos"], int(radius))

def desenhar_tela_visual():
    screen.fill((30, 30, 30))
    pygame.draw.rect(screen, (30, 30, 30), universe_rect)

    evoluir_universo(universo, universo.dados_mortos, estado, screen)
   # universo.evoluir_pulsos(escala)
    desenhar_pulsos(universo, screen)
    

def desenhar_tela_terminal():
    screen.fill((10, 10, 10))
    desenhar_terminal(screen, terminal_linhas, font_terminal, WIDTH - 20)
    



# =========================================================
# LOOP PRINCIPAL
# =========================================================
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_TAB):
                tela_atual = "visual" if tela_atual == "terminal" else "terminal"
                current_text = ""


            elif event.key == pygame.K_RETURN and tela_atual == "terminal":
                comando = current_text.strip().lower()
                if comando == "":
                    current_text = ""
                    continue
                
                respostas = processar_comando(comando, universo, estado)

                if comando != "":
                   historico_comandos.append(comando)
                   indice_historico = len(historico_comandos)

                for r in respostas:
                    if r == "__CLEAR__":
                        terminal_linhas.clear()
                    else:
                        terminal_linhas.append(r)
                current_text = ""

            elif event.key == pygame.K_BACKSPACE and tela_atual == "terminal":
                current_text = current_text[:-1]

            
            elif event.key == pygame.K_UP and tela_atual == "terminal":
                if historico_comandos:
                    indice_historico = max(0, indice_historico - 1)
                    current_text = historico_comandos[indice_historico]

            # SETA PARA BAIXO
            elif event.key == pygame.K_DOWN and tela_atual == "terminal":
                if historico_comandos:
                    indice_historico = min(len(historico_comandos), indice_historico + 1)
                    if indice_historico == len(historico_comandos):
                        current_text = ""
                    else:
                      
                        current_text = historico_comandos[indice_historico]


            

            elif tela_atual == "terminal":
                
                current_text += event.unicode

                   

    # -----------------------
    # DESENHO
    # -----------------------
    screen.fill((30, 30, 30))
    #pygame.draw.rect(screen, (30, 30, 30), universe_rect)

   # evoluir_universo(universo, universo.dados_mortos, escala_tempo, screen)
   # desenhar_terminal(screen)

   # universo.evoluir_pulsos(escala_tempo)
    #desenhar_pulsos(universo, screen)
    if tela_atual == "visual":
        desenhar_tela_visual()
    elif tela_atual == "terminal":
        desenhar_tela_terminal()

    

    contador_salvamento += 1
    if contador_salvamento % 120 == 0:
        universo.salvar()

    text_surface = font.render(current_text, True, (0, 255, 0))
    screen.blit(text_surface, (10, 10))

    pygame.display.flip()
    clock.tick(60)
