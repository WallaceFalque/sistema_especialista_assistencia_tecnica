import json
import os
import sys

PASTA = os.path.dirname(os.path.abspath(__file__))


def carregar_json(nome):
    caminho = os.path.join(PASTA, "dados", nome)
    try:
        with open(caminho, encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        print(f"Erro: o arquivo {nome} não foi encontrado em {caminho}.")
        sys.exit(1)
    except json.JSONDecodeError as erro:
        print(f"Erro: o arquivo {nome} está malformado (linha {erro.lineno}, coluna {erro.colno}: {erro.msg}).")
        sys.exit(1)


def carregar_regras():
    regras = carregar_json("regras.json")
    for posicao, regra in enumerate(regras, start=1):
        for campo in ("id", "descricao", "se", "entao"):
            if campo not in regra:
                identificacao = regra.get("id", f"na posição {posicao}")
                print(f"Erro: a regra {identificacao} não tem o campo '{campo}'.")
                sys.exit(1)
    return regras


def carregar_perguntas():
    return carregar_json("perguntas.json")