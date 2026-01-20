
from engine import Universo
import pygame
import sys
import json
import os
import random

escala_tempo = 1.0
CAMINHO_UNIVERSO = "data/universe.json"

def carregar_universo():
    if not os.path.exists(CAMINHO_UNIVERSO):
        return []

    with open(CAMINHO_UNIVERSO, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def salvar_universo(dados):
    os.makedirs("data", exist_ok=True)
    with open(CAMINHO_UNIVERSO, "w") as f:
        json.dump(dados, f, indent=4)


def evoluir_universo(universo, dados_mortos, escala_tempo, screen):

    
    if not hasattr(universo, "dados"):
        universo.dados = []

    for dado in universo.dados:

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

            distancia = (
                (dado["pos"][0] - outro["pos"][0]) ** 2 +
                (dado["pos"][1] - outro["pos"][1]) ** 2
            ) ** 0.5

            if distancia < 100:

                if outro["tipo"] == "Processador":
                    taxa_base = 0.5
                else:
                    taxa_base = 0.05

                transferencia = (100 - distancia) / 100 * taxa_base
                transferencia = min(transferencia, outro["energia"])

                dado["energia"] += transferencia * dado["fator_tempo"] * escala_tempo
                outro["energia"] -= transferencia * dado["fator_tempo"] * escala_tempo

                pygame.draw.line(
                    screen, (0, 255, 255),
                    dado["pos"], outro["pos"], 1
                )

        dado["fator_tempo"] = 1 / (1 + 0.1 * dado["energia"])

        dado["energia"] -= consumo * dado["fator_tempo"] * escala_tempo
        dado["energia"] = max(0, min(dado["energia"], 10))

        if "tempo_próprio" not in dado:
            dado["tempo_próprio"] = 0.0

        delta_t = escala_tempo
        delta_tau = delta_t * dado["fator_tempo"]
        dado["tempo_próprio"] += delta_tau

        if dado["energia"] <= 0:
            dados_mortos.append(dado)
            universo.dados.remove(dado)
            salvar_universo(universo.dados)

        radius = max(dado["energia"], 2)
        pygame.draw.circle(
            screen,
            cores_tipos[dado["tipo"]],
            dado["pos"],
            int(radius)
        )


pygame.init()

WIDTH, HEIGHT = 1360, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SO Experimental - Terminal")

clock = pygame.time.Clock()

font = pygame.font.SysFont("consolas", 20)
font_terminal = pygame.font.SysFont("consolas", 14)

# =========================================================
# LAYOUT 
# =========================================================
terminal_height = HEIGHT // 5
universe_rect = pygame.Rect(0, 0, WIDTH, HEIGHT - terminal_height)
terminal_rect = pygame.Rect(0, HEIGHT - terminal_height, WIDTH, terminal_height)

terminal_linhas = []

# =========================================================
# DADOS 
# =========================================================
dados = carregar_universo()
dados_mortos = []

universo = Universo()

# >>> SINCRONIZAÇÃO CRÍTICA <<<
universo.dados = dados

tipos = ["Memória", "Processador", "Armazenamento", "Energia", "Rede"]
cores_tipos = {
    "Memória": (255, 0, 0),
    "Processador": (0, 255, 0),
    "Armazenamento": (0, 0, 255),
    "Energia": (255, 255, 0),
    "Rede": (128, 0, 128)
}


contador_salvamento = 0
current_text = ""

# =========================================================
# TERMINAL (original)
# =========================================================
def desenhar_terminal(surface):
    y = 40
    for linha in terminal_linhas[-10:]:
        texto = font_terminal.render(str(linha), True, (0, 255, 0))
        surface.blit(texto, (10, y))
        y += 20

# =========================================================
# LOOP PRINCIPAL (original)
# =========================================================
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RETURN:
                comando = current_text.strip().lower()
                partes = comando.split()

                if comando == "":
                    current_text = ""
                    continue

                elif comando == "criar dado":
                    dado = {
                        "id": len(universo.dados) + 1,
                        "pos": [random.randint(200, 600), random.randint(50, 350)],
                        "tipo": random.choice(tipos),
                        "energia": 10,
                        "tempo_proprio": 0,
                        "fator_tempo": 1
                    }
                    universo.dados.append(dado)
                    salvar_universo(universo.dados)
                    terminal_linhas.append(f"Dado criado id={dado['id']}")

                elif comando == "listar dados":
                    for d in universo.dados:
                        terminal_linhas.append(str(d))

                elif comando == "listar dados mortos":
                    for elem in dados_mortos:
                        terminal_linhas.append(f"Dados mortos: {dado['id']}")

                elif comando == "clear":
                    terminal_linhas.clear()

                elif len(partes) >= 3:
                    if partes[0] == "usar" and partes[1] == "dado":
                        try:
                            id_dado = int(partes[2])#usar dado 1
                        except:
                            terminal_linhas.append("id inválido")
                            continue  

                        dado_encontrado = None
                        for dado in dados:
                            if dado["id"] == id_dado:
                                dado_encontrado = dado
                                break
                        if dado_encontrado is None:
                            terminal_linhas.append(f"dado {id_dado} não existe")
                        else:
                            dado_encontrado["energia"] -= 1
                            terminal_linhas.append(f"dado {id_dado} usado|valor = {dado_encontrado['energia']}")
                            if dado_encontrado["energia"] <= 0:
                                dados.remove(dado_encontrado)
                                terminal_linhas.append(f"dado {id_dado} esgotado e removido")

                    else:
                        terminal_linhas.append(f"Comando inválido: {comando}")

                elif partes[0] == "tempo":
                    try:
                        tempo = float(partes[1])
                        escala_tempo = tempo
                        terminal_linhas.append(f"escala tempo ajustada")
                    except:
                        terminal_linhas.append("")
                    
                    

                else:
                    terminal_linhas.append(f"Comando inválido: {comando}")

                current_text = ""

            elif event.key == pygame.K_BACKSPACE:
                current_text = current_text[:-1]
            else:
                current_text += event.unicode

    screen.fill((30, 30, 30))
    pygame.draw.rect(screen, (30, 30, 30), universe_rect)

    evoluir_universo(universo, dados_mortos, escala_tempo, screen)

    desenhar_terminal(screen)

    contador_salvamento += 1
    if contador_salvamento % 120 == 0:
        salvar_universo(universo.dados)

    text_surface = font.render(current_text, True, (0, 255, 0))
    screen.blit(text_surface, (10, 10))

    pygame.display.flip()
    clock.tick(60)
