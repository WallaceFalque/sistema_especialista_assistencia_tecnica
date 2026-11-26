import base
import motor


def cabecalho():
    print("=" * 50)
    print("TechFix Assistência Técnica")
    print("Triagem inicial de smartphones no balcão: diagnóstico,")
    print("encaminhamento e preço estimado sem depender de um técnico.")
    print("=" * 50)


def sobre():
    print()
    print("Este é um sistema especialista: ele faz perguntas sobre o aparelho")
    print("e aplica regras de uma base de conhecimento para sugerir um diagnóstico.")
    print(f"Regras carregadas: {len(base.carregar_regras())}")
    print("O motor de inferência usa encadeamento para frente.")


def normalizar(texto):
    texto = "_".join(texto.lower().replace("ã", "a").split())
    if texto == "s":
        return "sim"
    if texto == "n":
        return "nao"
    return texto


def perguntar(pergunta):
    opcoes = pergunta["opcoes"]
    while True:
        print()
        print(pergunta["texto"])
        for numero, opcao in enumerate(opcoes, start=1):
            print(f"  {numero}) {opcao}")
        resposta = normalizar(input("> "))
        if resposta.isdigit() and 1 <= int(resposta) <= len(opcoes):
            return opcoes[int(resposta) - 1]
        if resposta in opcoes:
            return resposta
        print("Resposta inválida. Digite o número ou o texto de uma das opções.")


def mostrar_explicacoes(fatos, regras_disparadas):
    while True:
        print()
        print("[P] Por que chegou nessa conclusão?")
        print("[C] Como chegou no diagnóstico?")
        print("[V] Voltar ao menu")
        opcao = input("> ").strip().lower()
        if opcao == "p":
            print()
            print(motor.explicar_porque(fatos, regras_disparadas))
        elif opcao == "c":
            print()
            print(motor.explicar_como("diagnostico", fatos, regras_disparadas))
        elif opcao == "v":
            return
        else:
            print("Opção inválida. Escolha P, C ou V.")


def triagem():
    perguntas = base.carregar_perguntas()
    regras = base.carregar_regras()
    fatos = {}
    for pergunta in perguntas:
        fatos[pergunta["fato"]] = perguntar(pergunta)
    fatos_finais, regras_disparadas = motor.inferir(fatos, regras)
    print()
    if "diagnostico" in fatos_finais:
        print(f"Diagnóstico: {fatos_finais['diagnostico']}")
        print(f"Encaminhamento: {fatos_finais['encaminhamento']}")
        print(f"Preço estimado: {fatos_finais['preco']}")
        mostrar_explicacoes(fatos, regras_disparadas)
    else:
        print("Não foi possível concluir um diagnóstico com as informações fornecidas.")
        nao_sei = [p["texto"] for p in perguntas if fatos[p["fato"]] == "nao_sei"]
        if nao_sei:
            print("Perguntas respondidas com \"nao_sei\":")
            for texto in nao_sei:
                print(f"  - {texto}")
        print("Recomendamos uma avaliação presencial com um técnico.")


def principal():
    cabecalho()
    try:
        while True:
            print()
            print("1) Nova triagem")
            print("2) Sobre o sistema")
            print("3) Sair")
            opcao = input("> ").strip()
            if opcao == "1":
                triagem()
            elif opcao == "2":
                sobre()
            elif opcao == "3":
                print("Até logo!")
                return
            else:
                print("Opção inválida. Escolha 1, 2 ou 3.")
    except (KeyboardInterrupt, EOFError):
        print()
        print("Atendimento encerrado. Até logo!")


if __name__ == "__main__":
    principal()
