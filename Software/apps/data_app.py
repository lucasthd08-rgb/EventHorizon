class DataApp:
    def __init__(self, universo):
        self.universo = universo

    def handle(self, comando):
        partes = comando.split()
        respostas = []

        # criar dado
        if comando == "c":
            dado = self.universo.criar_dado()
            return [f"Dado criado id={dado['id']}"]
        
        

        # usar dado X
        if len(partes) == 3 and partes[0] == "usar" and partes[1] == "dado":
            try:
                id_dado = int(partes[2])
            except:
                return ["id inválido"]

            dado = next((d for d in self.universo.dados if d["id"] == id_dado), None)

            if dado is None:
                return [f"dado {id_dado} não existe"]

            dado["energia"] -= 1
            respostas.append(f"dado {id_dado} usado | energia = {dado['energia']}")

            if dado["energia"] <= 0:
                self.universo.dados.remove(dado)
                self.universo.dados_mortos.append(dado)
                respostas.append(f"dado {id_dado} esgotado e removido")

            return respostas

        # duplicar dado X
        if len(partes) == 3 and partes[0] == "duplicar" and partes[1] == "dado":
            try:
                id_dado = int(partes[2])
            except:
                return ["id inválido"]

            original = next((d for d in self.universo.dados if d["id"] == id_dado), None)
            if original is None:
                return [f"Dado {id_dado} não encontrado"]

            novo = self.universo.criar_dado()
            novo["tipo"] = original["tipo"]
            novo["energia"] = original["energia"]

            return [f"dado {id_dado} duplicado como id={novo['id']}"]

        # energia total
        if comando == "energia total":
            return [f"Energia total do universo: {self.universo.energia_total()}"]
        
        if comando == "listar dados":
            if not self.universo.dados:
                return ["Nenhum dado presente no universo"]
            
            for d in self.universo.dados:
                respostas.append(
                    f"Dado {d['id']} | "
                    f"Posição: {tuple(d['pos'])}"
                    f"Tipo: {d['tipo']} | "
                    f"Energia: {d['energia']} | "
                    f"Tempo próprio: {d['tempo_proprio']} | "
                    f"Fator tempo: {d['fator_tempo']} | "
                    f"Memória: {len(d['memoria'])} eventos"
                    

                )

            return respostas
                    
        if comando == "listar dados mortos":
            if not self.universo.dados_mortos:
                return ["Não há dados mortos"]
            
            respostas.append("Dados mortos:")
            for d in self.universo.dados:
                respostas.append(f"id: {d['id']} | "
                                 f"Tipo: {d['tipo']}")
            return respostas

        

        
        if len(partes) == 3 and partes[0] == "memoria" and partes[1] == "dado":
            try:
                id_dado = int(partes[2])
            except:
                return ["id inválido"]

            # Procura dado entre vivos e mortos
            dado = next(
                (d for d in self.universo.dados + self.universo.dados_mortos
                 if d["id"] == id_dado),
                None
            )

            if dado is None:
                return [f"Dado {id_dado} não encontrado"]

            memoria = dado.get("memoria", [])

            if not memoria:
                return [f"Dado {id_dado} tem memória vazia"]

            respostas.append(f"Memória do dado {id_dado}:")
            for evento in memoria:
                if evento.get("acao") == "enviou pulso":
                    respostas.append(
                        f"Pulso {evento.get('pulso_id')} | Energia: {evento.get('energia')}"
                    )


        return None  # não é deste app
