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


def origem(fato, valor, fatos_iniciais, regras_disparadas):
    if fatos_iniciais.get(fato) == valor:
        return None
    for regra in regras_disparadas:
        if regra["entao"].get(fato) == valor:
            return regra
    return None


def explicar_porque(fatos_iniciais, regras_disparadas):
    if not regras_disparadas:
        return "Nenhuma regra foi disparada."
    linhas = []
    for regra in regras_disparadas:
        linhas.append(f"{regra['id']}: {regra['descricao']}")
        for fato, valor in regra["se"].items():
            regra_origem = origem(fato, valor, fatos_iniciais, regras_disparadas)
            if regra_origem is None:
                linhas.append(f"    você respondeu: {fato} = {valor}")
            else:
                linhas.append(f"    {fato} = {valor}: concluído pela regra {regra_origem['id']}")
    return "\n".join(linhas)


def cadeia(fato, valor, fatos_iniciais, regras_disparadas, nivel):
    recuo = "    " * nivel
    regra = origem(fato, valor, fatos_iniciais, regras_disparadas)
    if regra is None:
        return [f"{recuo}você respondeu: {fato} = {valor}"]
    linhas = [f"{recuo}{fato} = {valor}  <- {regra['id']}"]
    for fato_se, valor_se in regra["se"].items():
        linhas += cadeia(fato_se, valor_se, fatos_iniciais, regras_disparadas, nivel + 1)
    return linhas


def explicar_como(fato, fatos_iniciais, regras_disparadas):
    for regra in reversed(regras_disparadas):
        if fato in regra["entao"]:
            valor = regra["entao"][fato]
            return "\n".join(cadeia(fato, valor, fatos_iniciais, regras_disparadas, 0))
    return f"O fato '{fato}' não foi concluído por nenhuma regra."
