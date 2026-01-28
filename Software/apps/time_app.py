class TimeApp: 
    def __init__ (self, estado):
        self.estado = estado
    
    def handle(self, comando):
        partes = comando.split()
        

        if len(partes) == 2 and partes[0] == "tempo:":
            try:
                self.estado["escala_tempo"] = float(partes[1])
                return [f"Escala de tempo ajustada para {self.estado['escala_tempo']}"]
            except:
                return ["Valor inválido para tempo"]
        
        return None
            