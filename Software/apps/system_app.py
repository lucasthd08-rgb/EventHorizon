class SystemApp:
    def __init__(self, universo, estado):
        self.universo = universo
        self.estado = estado

    def handle(self, comando):
        respostas = []
        partes = comando.split()

        if comando == "help":
            respostas.append("comandos do sistema:")
            respostas.append("help")
            respostas.append("clear")
            respostas.append("pause")
            respostas.append("status")
            respostas.append("enviar pulso X Y")
            respostas.append("c")
            respostas.append("listar dados")
            respostas.append("listar dados mortos")
            respostas.append("energia total")
            respostas.append("duplicar dado X")
            respostas.append("tempo X")
            respostas.append("reset universo")
            return respostas

        if comando == "pause":
            self.estado["pausado"] = not self.estado["pausado"]
            return ["Universo pausado" if self.estado["pausado"] else "Universo retomado"]

        if comando == "status":                
            return [self.universo.status_universo()]

        if comando == "clear":
            return ["__CLEAR__"]
        
        elif comando == "reset universo":
            self.universo.dados = []
            self.universo.dados_mortos = []
            self.universo.ultimo_id = 0
            self.universo.salvar()
            self.universo.salvar_mortos()
            respostas.append("Universo reiniciado: todos os dados foram apagados, IDs resetados")
            return respostas

        return None  # comando não é desse app
