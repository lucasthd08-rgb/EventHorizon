import pygame
import sys
import random

# ------------------------
# Inicialização
# ------------------------
pygame.init()

WIDTH, HEIGHT = 1360, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SO Experimental - Terminal")

clock = pygame.time.Clock()

# Fonte
font = pygame.font.SysFont("consolas", 20)
font_terminal = pygame.font.SysFont("consolas", 14)

# ------------------------
# Layout
# ------------------------
terminal_height = HEIGHT // 5
universe_rect = pygame.Rect(0, 0, WIDTH, HEIGHT - terminal_height)
terminal_rect = pygame.Rect(0, HEIGHT - terminal_height, WIDTH, terminal_height)
terminal_linhas = []
#dadopos = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
id = 0
dados = []
dados_mortos = []
tipos = ["Memória", "Processador", "Armazenamento", "Energia", "Rede"]
cores_tipos = {
    "Memória": (255, 0, 0),
    "Processador": (0, 255, 0),
    "Armazenamento": (0, 0, 255),
    "Energia": (255, 255, 0),
    "Rede": (128, 0, 128)
}

k=1
# ------------------------
# Terminal
# ------------------------
current_text = ""  # texto que o usuário está digitando

def desenhar_terminal(surface):
    y = 40
    for linha in terminal_linhas[-10:]:
        texto = font_terminal.render(str(linha), True, (0, 255, 0))
        surface.blit(texto, (10, y))
        y += 20


        



# ------------------------
# Loop principal
# ------------------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            # ENTER → executa comando
            if event.key == pygame.K_RETURN:
                comando = current_text.strip().lower()
                partes = comando.split()


                if comando == "criar dado":
                    terminal_linhas.append("Dado criado")
                   # id = id + 1
                   # dados.append(id)
                    #desenhar_dados()
                    id += 1
                    energia_inicial = 10
                    dado = {
                        "id": id,
                        "pos": (random.randint(220, 550), random.randint(50, 350)),
                        "tipo": (random.choice(tipos)),
                        "energia": energia_inicial,
                        "tempo_proprio": 0,
                        "fator_tempo": 0
                    }
                    
                    dados.append(dado)
                    terminal_linhas.append(f"o id do dado criado é: {id}")
                    

                elif comando == "listar dados":
                    terminal_linhas.append(f"total de dados listados: {len(dados)}")
                    for elem in dados:
                        terminal_linhas.append(f"{elem}")

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


                elif comando != "":
                    terminal_linhas.append(f"comando inválido: {comando}")
                current_text = ""  # limpa linha após Enter


            # BACKSPACE → apaga caractere
            elif event.key == pygame.K_BACKSPACE:
                current_text = current_text[:-1]

            # TEXTO NORMAL
            else:
                current_text += event.unicode

    # ------------------------
    # Desenho
    # ------------------------
   # desenhar_dados()
    
    screen.fill((30, 30, 30))

    # Universo (parte de cima)
    pygame.draw.rect(screen, (30, 30, 30), universe_rect)

    # Terminal (parte de baixo)
   # pygame.draw.rect(screen, (0, 0, 0), terminal_rect)


    


    for dado in dados:
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

        for outro in dados:
            if outro == dado:
                continue
            else:
                x1, y1 = dado["pos"]
                x2, y2 = outro["pos"]
                dx = x2 - x1
                dy = y2 - y1
                distancia = (dx**2 + dy**2) ** 0.5
                if distancia < 100:
                    transferencia = (100 - distancia) / 100 * 0.005
                    dado["energia"] += transferencia
                    outro["energia"] -= transferencia
                    print(transferencia)
                    
  

        dado["fator_tempo"] = 1 / (1 + 0.1 * dado["energia"])



        dado["energia"] -= consumo * dado["fator_tempo"]

        dado["energia"] = max(dado["energia"], 0)
        

        dado["tempo_proprio"] = 1 - dado["energia"] / 10
        dado["tempo_proprio"] = min(max(dado["tempo_proprio"], 0), 1)

        if dado["energia"] <= 0:
            dados_mortos.append(dado)
            dados.remove(dado)
        
        radius = max(dado["energia"], 2)
        color = cores_tipos[dado["tipo"]]
      #  print(dado["fator_tempo"])
        pygame.draw.circle(screen, color, dado["pos"], int(radius))


        


    # Texto do terminal
    desenhar_terminal(screen)
    
    text_surface = font.render(current_text, True, (0, 255, 0))
    screen.blit(
        text_surface,
        (10, 10)
    )

    pygame.display.flip()
    clock.tick(60)
