from engine import Universo
import pygame
import sys
import os
import random

# =========================================================
# CONFIGURAÇÃO INICIAL
# =========================================================
escala_tempo = 1.0
CAMINHO_UNIVERSO = "data/universe.json"

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
terminal_height = HEIGHT // 1.3
universe_rect = pygame.Rect(0, 0, WIDTH, HEIGHT - terminal_height)
terminal_rect = pygame.Rect(0, HEIGHT - terminal_height , WIDTH, terminal_height)
terminal_linhas = []

# =========================================================
# DADOS E UNIVERSO
# =========================================================
universo = Universo(caminho=CAMINHO_UNIVERSO)
#dados_mortos = []

tipos = ["Memória", "Processador", "Armazenamento", "Energia", "Rede"]
cores_tipos = {
    "Memória": (255, 0, 0),
    "Processador": (0, 255, 0),
    "Armazenamento": (0, 0, 255),
    "Energia": (255, 255, 0),
    "Rede": (128, 0, 128)
}

contador_salvamento = 0
fx, fy = 0.0, 0.0
current_text = ""

# =========================================================
# FUNÇÕES
# =========================================================
def desenhar_terminal(surface):
    y = 40
    for linha in terminal_linhas[-10:]:
        texto = font_terminal.render(str(linha), True, (0, 255, 0))
        surface.blit(texto, (10, y))
        y += 20

def desenhar_pulsos(universo, screen):
    for pulso in universo.pulsos:
        x, y = pulso["pos"]
        pygame.draw.circle(
            screen,
            (0, 255, 255),
            (int(x), int(y)),
            3
        )



def evoluir_universo(universo, dados_mortos, escala_tempo, screen):
    if not hasattr(universo, "dados"):
        universo.dados = []

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
        radius = max(dado["energia"], 2)
        pygame.draw.circle(screen, cores_tipos[dado["tipo"]], dado["pos"], int(radius))
          
        
        # Atualiza fator tempo
        dado["fator_tempo"] = 1 / (1 + 0.1 * dado["energia"])

        # Atualiza energia
        dado["energia"] -= consumo * dado["fator_tempo"] * escala_tempo
        dado["energia"] = max(0, min(dado["energia"], 10))

        
        

    

        # Inicializa tempo próprio se não existir
        if "tempo_proprio" not in dado:
            dado["tempo_proprio"] = 0.0

        # Atualiza tempo próprio
        delta_t = escala_tempo
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




# =========================================================
# LOOP PRINCIPAL
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

                # -----------------------
                # CRIAR DADO
                # -----------------------
                elif comando == "c":
                    dado = universo.criar_dado()
                    terminal_linhas.append(f"Dado criado id={dado['id']}")

                # -----------------------
                # LISTAR DADOS
                # -----------------------
                elif comando == "listar dados":
                    for d in universo.dados:
                        terminal_linhas.append(str(d))

                elif comando == "listar dados mortos":
                    for d in universo.dados_mortos:
                        terminal_linhas.append(f"id={d['id']} energia={d['energia']}")

                elif comando == "reset universo":
                    universo.dados = []
                    universo.dados_mortos = []
                    universo.ultimo_id = 0
                    universo.salvar()
                    universo.salvar_mortos()
                    terminal_linhas.append("Universo reiniciado: todos os dados foram apagados, IDs resetados")

                elif partes[0] == "duplicar" and partes[1] == "dado" and len(partes) == 3:
                    id_dado = int(partes[2])
                    dado_original = next((d for d in universo.dados if d["id"]==id_dado), None)
                    if dado_original:
                        novo_dado = universo.criar_dado()
                        novo_dado["tipo"] = dado_original["tipo"]
                        novo_dado["energia"] = dado_original["energia"]
                        terminal_linhas.append(f"dado {id_dado} duplicado como id={novo_dado["id"]}")
                    else:
                        terminal_linhas.append(f"Dado {id_dado} não encontrado")

                elif partes[0] == "enviar" and partes[1] == "pulso":
                    try:
                        id1 = int(partes[2])
                        id2 = int(partes[3])
                        ok = universo.enviar_pulso(id1, id2)

                        if ok:
                            terminal_linhas.append(f"Pulso {id1} → {id2}")
                        else:
                            terminal_linhas.append(f"Falha ao enviar pulso")
                    except:
                        terminal_linhas.append("Uso: enviar pulso <origem> <destino>")

                elif partes[0] == "energia" and partes[1] == "total":
                    terminal_linhas.append(f"Energia total do universo: {universo.energia_total()}")

                elif partes[0] == "status" and partes[1] == "universo":
                    terminal_linhas.append(f"{universo.status_universo()}")

                elif comando == "listar dados":
                    terminal_linhas.append(universo.listar_pulsos())


                elif len(partes) >= 3:
                    if partes[0] == "usar" and partes[1] == "dado":
                        try:
                            id_dado = int(partes[2])#usar dado 1
                        except:
                            terminal_linhas.append("id inválido")
                            continue  

                        dado_encontrado = None
                        for dado in universo.dados:
                            if dado["id"] == id_dado:
                                dado_encontrado = dado
                                break
                        if dado_encontrado is None:
                            terminal_linhas.append(f"dado {id_dado} não existe")
                        else:
                            dado_encontrado["energia"] -= 1
                            terminal_linhas.append(f"dado {id_dado} usado|valor = {dado_encontrado['energia']}")
                            if dado_encontrado["energia"] <= 0:
                                universo.dados_mortos.append(dado_encontrado)
                                universo.dados.remove(dado_encontrado)
                                terminal_linhas.append(f"dado {id_dado} esgotado e removido")

                    else:
                        terminal_linhas.append(f"Comando inválido: {comando}")





                elif comando == "clear":
                    terminal_linhas.clear()

                # -----------------------
                # USAR DADO
                # -----------------------
                elif len(partes) >= 3 and partes[0] == "usar" and partes[1] == "dado":
                    try:
                        id_dado = int(partes[2])
                    except:
                        terminal_linhas.append("id inválido")
                        current_text = ""
                        continue

                    dado_encontrado = None
                    for d in universo.dados:
                        if d["id"] == id_dado:
                            dado_encontrado = d
                            break
                    if dado_encontrado is None:
                        terminal_linhas.append(f"dado {id_dado} não existe")
                    else:
                        dado_encontrado["energia"] -= 1
                        terminal_linhas.append(f"dado {id_dado} usado|valor={dado_encontrado['energia']}")
                        if dado_encontrado["energia"] <= 0:
                            universo.dados.remove(dado_encontrado)
                            terminal_linhas.append(f"dado {id_dado} esgotado e removido")
                            universo.salvar()

                # -----------------------
                # ESCALA TEMPO
                # -----------------------
                elif partes[0] == "tempo":
                    try:
                        tempo = float(partes[1])
                        escala_tempo = tempo
                        terminal_linhas.append(f"escala tempo ajustada para {escala_tempo}")
                    except:
                        terminal_linhas.append("valor inválido")

                # -----------------------
                # COMANDO INVÁLIDO
                # -----------------------
                else:
                    terminal_linhas.append(f"Comando inválido: {comando}")

                current_text = ""

            elif event.key == pygame.K_BACKSPACE:
                current_text = current_text[:-1]
            else:
                current_text += event.unicode

    # -----------------------
    # DESENHO
    # -----------------------
    screen.fill((30, 30, 30))
    pygame.draw.rect(screen, (30, 30, 30), universe_rect)

    evoluir_universo(universo, universo.dados_mortos, escala_tempo, screen)
    desenhar_terminal(screen)

    universo.evoluir_pulsos(escala_tempo)
    desenhar_pulsos(universo, screen)

    

    contador_salvamento += 1
    if contador_salvamento % 120 == 0:
        universo.salvar()

    text_surface = font.render(current_text, True, (0, 255, 0))
    screen.blit(text_surface, (10, 10))

    pygame.display.flip()
    clock.tick(60)
