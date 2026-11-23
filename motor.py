def inferir(fatos, regras):
    fatos_finais = dict(fatos)
    regras_disparadas = []
    disparou = True
    while disparou:
        disparou = False
        for regra in regras:
            if regra in regras_disparadas:
                continue
            condicoes_batem = all(
                valor != "nao_sei" and fatos_finais.get(fato) == valor
                for fato, valor in regra["se"].items()
            )
            if condicoes_batem:
                fatos_finais.update(regra["entao"])
                regras_disparadas.append(regra)
                disparou = True
    return fatos_finais, regras_disparadas
