HELP = {
    "c": "c → cria um novo dado no universo",
    
    "listar dados": "listar dados → lista todos os dados ativos",
    "listar dados mortos": "listar dados mortos → lista dados sem energia",
    "listar pulsos": "listar pulsos → mostra todos os pulsos existentes",

    "usar dado X": "usar dado <id> → consome 1 unidade de energia do dado",

    "duplicar dado X": "duplicar dado <id> → cria uma cópia do dado",

    "enviar pulso X Y": "enviar pulso <origem> <destino> → envia energia entre dados",

    "energia total": "energia total → mostra a energia total do universo",

    "status universo": "status universo → mostra o estado geral do universo",

    "tempo X": "tempo <valor> → ajusta a escala temporal do universo",

    "clear": "clear → limpa o terminal",
    "reset universo": "reset universo → apaga todos os dados e pulsos",
    "pause": "pause → pausa todo o universo. Se executar de novo, a evolucao do universo é retomada"
}


def processar_comando(comando, universo, estado):
    
    respostas = []
    partes = comando.split()

#    if comando.startswith("help"):
 #       if len(partes) == 1:
  #          respostas.append("comandos disponíveis:")

   #         for k in sorted(HELP.keys()):

    #            respostas.append(f"{k}")
     #       respostas.append("Use: help <comando>")
      #      return respostas
        
       # termo = " ".join(partes[1:])

        #encontrados = False

     #   for k, v in HELP.items():
      #      if k.startswith(termo):
       #         respostas.append(v)
        #        encontrados = True

       # if not encontrados:
        #    respostas.append(f"Nenhuma ajuda encontrada para: {termo}")

       # return respostas
    

   # elif comando == "pause":
    #    estado["pausado"] = not estado["pausado"]
     #   respostas.append("Universo pausado" if estado["pausado"] else "Universo retomado")
    
  #  elif comando == "c":
   #      dado = universo.criar_dado()
    #     respostas.append(f"Dado criado id={dado['id']}")

   # elif comando == "listar dados":
    ##    for d in universo.dados:
      #      respostas.append(str(d))

    #elif comando == "listar dados mortos":
     #   for d in universo.dados_mortos:
      #      respostas.append(f"id={d['id']} energia={d['energia']}")

   # elif comando == "clear":
    #    respostas.clear()
     #   return ["__CLEAR__"]
    

#    elif comando == "reset universo":
    #   universo.dados = []
       # universo.dados_mortos = []
        #universo.ultimo_id = 0
     #   universo.salvar()
      #  universo.salvar_mortos()
       # respostas.append("Universo reiniciado: todos os dados foram apagados, IDs resetados")

 ##   elif len(partes) == 3 and partes[0] == "duplicar" and partes[1] == "dado":
  #      id_dado = int(partes[2])
   #     dado_original = next((d for d in universo.dados if d["id"]==id_dado), None)
    #    if dado_original:
     #       novo_dado = universo.criar_dado()
      #      novo_dado["tipo"] = dado_original["tipo"]
       #     novo_dado["energia"] = dado_original["energia"]
        #    respostas.append(f"dado {id_dado} duplicado como id={novo_dado['id']}")
        #else:
         #   respostas.append(f"Dado {id_dado} não encontrado")

 #   elif len(partes) == 4 and partes[0] == "enviar" and partes[1] == "pulso":
  #      try:
   #         id1 = int(partes[2])
    #        id2 = int(partes[3])
     #       ok = universo.enviar_pulso(id1, id2)

      #      if ok:
       #         respostas.append(f"Pulso {id1} → {id2}")
        #    else:
         #       respostas.append(f"Falha ao enviar pulso")
        #except:
         #   respostas.append("Uso: enviar pulso <origem> <destino>")

  #  elif len(partes) == 2 and partes[0] == "energia" and partes[1] == "total":
   #     respostas.append(f"Energia total do universo: {universo.energia_total()}")

   # elif len(partes) == 2 and partes[0] == "status" and partes[1] == "universo":
    #    respostas.append(f"{universo.status_universo()}")

  #  elif partes[0] == "memoria" and partes[1] == "dado":
   #     try:
    #        id_dado = int(partes[2])
     #   except:
      #      respostas.append("id inválido")
       #     return respostas

        # Procura dado entre vivos e mortos
      #  dado = next((d for d in universo.dados + universo.dados_mortos if d["id"] == id_dado), None)
       # if dado is None:
        #    respostas.append(f"Dado {id_dado} não encontrado")
       # else:
        #    memoria = dado.get("memoria", [])
         #   if not memoria:
          #      respostas.append(f"Dado {id_dado} tem memória vazia")
           # else:
            #    respostas.append(f"Memória do dado {id_dado}:")
             #   for evento in memoria:
             #       if evento.get("acao") == "enviou pulso":
             #           respostas.append(f"Pulso {evento.get('pulso_id')} | Energia: {evento.get('energia')}")


    #elif comando == "listar pulsos":
   #     respostas = ["__CLEAR__"]
        
        #if not universo.pulsos:
       #     respostas.append(f"Nenhum dado ativo no universo")
      #  else:
     #       for i, pulso in enumerate(universo.pulsos, 1):
    #            respostas.append(f"Pulso {i} | "
   #                                 f"Origem: {pulso['origem']} → "
  #                                  f"Destino: {pulso['destino']} | "
 #                                   f"Energia: {pulso['energia']:.2f} | "
#                                    f"Progresso: {int(pulso['progresso'] * 100)}%")
                                     


    


  #  elif len(partes) >= 3:
   #     if partes[0] == "usar" and partes[1] == "dado":
    #        try:
     #           id_dado = int(partes[2])#usar dado 1
      #      except:
       #         respostas.append("id inválido")
        #        return respostas
#
 #           dado_encontrado = None
  #          for dado in universo.dados:
   #             if dado["id"] == id_dado:
    #                dado_encontrado = dado
     #               break      if dado_encontrado is None:
      #          respostas.append(f"dado {id_dado} não existe")
       #     else:
       #         dado_encontrado["energia"] -= 1
        #        respostas.append(f"dado {id_dado} usado|valor = {dado_encontrado['energia']}")
         #       if dado_encontrado["energia"] <= 0:
          #          universo.dados_mortos.append(dado_encontrado)
           #         universo.dados.remove(dado_encontrado)
            #        respostas.append(f"dado {id_dado} esgotado e removido")

      #  else:
       #     respostas.append(f"Comando inválido: {comando}")





    

                # -----------------------
                # ESCALA TEMPO
                # -----------------------
#    elif len(partes) == 2 and partes[0] == "tempo":
 #       try:
  #          estado["escala_tempo"] = float(partes[1])
   #         respostas.append(f"escala tempo ajustada para {estado["escala_tempo"]}")
    #    except:
     #       respostas.append("valor inválido")

    for app in universo.apps:
        respostas_app = app.handle(comando)
        if respostas_app is not None:
            return respostas_app

                # -----------------------
                # COMANDO INVÁLIDO
                # -----------------------
    else:
        respostas.append(f"Comando inválido: {comando}")

        
    return respostas


