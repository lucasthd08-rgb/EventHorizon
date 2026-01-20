# engine.py
import json
import os
import random

class Universo:
    def __init__(self, caminho="data/universe.json"):
        self.caminho = caminho
        self.dados = []
        self.ultimo_id = 0  # guarda o último ID usado
        self.carregar()

    def criar_dado(self):
        self.ultimo_id += 1
        dado = {
            "id": self.ultimo_id,
            "pos": [random.randint(200, 600), random.randint(50, 350)],
            "tipo": random.choice(["Memória", "Processador", "Armazenamento", "Energia", "Rede"]),
            "energia": 10,
            "tempo_proprio": 0,
            "fator_tempo": 1
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
