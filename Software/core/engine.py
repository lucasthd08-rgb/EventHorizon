# engine.py
from config import WIDTH, HEIGHT
import json #persistência
import os
import random

class Universo:
    def __init__(self, caminho="data/universe.json"):
        self.caminho = caminho
        self.caminho_mortos = "data/dados_mortos.json"
        self.dados = []
        self.dados_mortos = []
        self.ultimo_id = 0  # guarda o último ID usado
        self.pulsos = []
        self.carregar()
        self.carregar_mortos()

    def criar_dado(self):
        self.ultimo_id += 1
        dado = {
            "id": self.ultimo_id,
            "pos": [random.randint(10, WIDTH - 10), random.randint(10, HEIGHT - 10)],
            "tipo": random.choice(["Memória", "Processador", "Armazenamento", "Energia", "Rede"]),
            "energia": 10,
            "tempo_proprio": 0,
            "fator_tempo": 1,
        
        }
        self.dados.append(dado)
        self.salvar()
        return dado

    def salvar(self):
        os.makedirs("data", exist_ok=True)
        with open(self.caminho, "w") as f:
            json.dump({"ultimo_id": self.ultimo_id, "dados": self.dados}, f, indent=4)

    def carregar(self):
        if os.path.exists(self.caminho):
            with open(self.caminho, "r") as f:
                universo_salvo = json.load(f)
                if "dados" in universo_salvo:
                    self.dados = universo_salvo["dados"]
                else:
                    self.dados = []
                if "ultimo_id" in universo_salvo:
                    self.ultimo_id = universo_salvo["ultimo_id"]
                else:
                    self.ultimo_id = 0

    def salvar_mortos(self):
        os.makedirs("data", exist_ok=True)
        with open(self.caminho_mortos, "w") as f:
            json.dump(self.dados_mortos, f, indent=4)

    def carregar_mortos(self):
        if os.path.exists(self.caminho_mortos):
            with open(self.caminho_mortos, "r") as f:
                self.dados_mortos = json.load(f)

    def enviar_pulso(self, id_origem, id_destino, energia=0.2):
        origem = next((d for d in self.dados if d["id"] == id_origem), None)
        destino = next((d for d in self.dados if d["id"] == id_destino), None)

        if origem is None or destino is None:
            return False

        if origem["energia"] < energia:
            return False

        origem["energia"] -= energia

        

        pulso = {
           "origem": id_origem,
           "destino": id_destino,
           "energia": energia,
           "progresso": 0.0,
           "pos_origem": origem["pos"][:],
           "pos_destino": destino["pos"][:],
           "pos": origem["pos"][:],
           "distancia": 0.0,
           "velocidade": 10
        }

        pulso["energia"] = origem["energia"] * 0.1


        self.pulsos.append(pulso)
        return True

    def evoluir_pulsos(self, escala):
       for pulso in self.pulsos[:]:
    
           # avança no tempo
           if pulso["distancia"] > 0:
               delta = (pulso["velocidade"] * escala) / pulso["distancia"]
               pulso["progresso"] += delta
    
           # chegou ao destino
           if pulso["progresso"] >= 1.0:
               destino = next(
                   (d for d in self.dados if d["id"] == pulso["destino"]),
                   None
               )
    
               if destino:
                   destino["energia"] += pulso["energia"]
    
               self.pulsos.remove(pulso)
               continue  # pula para o próximo pulso
    
           # movimento espacial (só se ainda estiver viajando)


           ox, oy = pulso["pos_origem"]
           dx, dy = pulso["pos_destino"]

           pulso["distancia"] = ((dx - ox)**2 + (dy - oy)**2)**0.5  
           pulso["velocidade"] = 1
           pulso["energia"] *= 0.995


           t = pulso["progresso"]
           pulso["pos"][0] = ox + (dx - ox) * t
           pulso["pos"][1] = oy + (dy - oy) * t

    def energia_total(self):
        energia_total = sum(d["energia"] for d in self.dados)     
        energia_total_pulsos = sum(p["energia"] for p in self.pulsos)
        return energia_total + energia_total_pulsos
    
    def status_universo(self):
        return {
            "dados": len(self.dados),
            "pulsos": len(self.pulsos),
            "energia_total": self.energia_total()
        }
    
    def listar_pulsos(self):
        return [
           {
            "origem": p["origem"],
            "destino": p["destino"],
            "energia": p["energia"]
           }
           for p in self.pulsos
        ]
    

