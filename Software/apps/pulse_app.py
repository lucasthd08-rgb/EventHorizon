class PulseApp:
    print("Carregado")
    def __init__(self, universo):
        self.universo = universo

    def handle(self, comando):
        respostas = []
        partes = comando.split()

        if comando == "listar pulsos":
       # respostas = ["__CLEAR__"]
        
            if not self.universo.pulsos:
                respostas.append(f"Nenhum pulso ativo no universo")
            else:
                for i, pulso in enumerate(self.universo.pulsos, 1):
                    respostas.append(f"Pulso {i} | "
                                    f"Origem: {pulso['origem']} → "
                                    f"Destino: {pulso['destino']} | "
                                    f"Energia: {pulso['energia']:.2f} | "
                                    f"Progresso: {int(pulso['progresso'] * 100)}%")
            return respostas
                    
        elif len(partes) == 4 and partes[0] == "enviar" and partes[1] == "pulso":
            try:
                id1 = int(partes[2])
                id2 = int(partes[3])
                ok = self.universo.enviar_pulso(id1, id2)

                if ok:
                    respostas.append(f"Pulso {id1} → {id2}")
                else:
                    respostas.append(f"Falha ao enviar pulso")
            except:
                respostas.append("Uso: enviar pulso <origem> <destino>")
        
        return None
                                      

    