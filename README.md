# TechFix – Sistema Especialista

**Empresa:** TechFix Assistência Técnica (fictícia)

Na TechFix, a triagem de smartphones no balcão é lenta e depende de um técnico experiente para identificar o provável defeito, decidir para onde o aparelho deve ser encaminhado e informar um preço ao cliente. Este sistema especialista faz a triagem inicial: pergunta ao atendente sobre os sintomas do aparelho e, com base em regras, sugere um diagnóstico, o encaminhamento adequado e um preço estimado, explicando o raciocínio usado.





1. Sobre o projeto

O TechFix é um sistema especialista desenvolvido em Python para auxiliar na identificação de possíveis problemas em smartphones.

O sistema faz perguntas sobre o aparelho, recebe as respostas do atendente e utiliza uma base de conhecimento composta por fatos e regras para chegar a uma conclusão.

Ao final da análise, apresenta:

Diagnóstico provável do problema.

Encaminhamento recomendado.

Preço estimado do serviço.

Explicação das regras utilizadas para chegar à conclusão.

O projeto utiliza encadeamento para frente (Forward Chaining).

2. Como executar o projeto

Requisitos

Python 3 instalado.

Visual Studio Code ou outro editor de código.

Terminal para executar os comandos.

Não é necessário instalar bibliotecas externas.

Executar o sistema

Abra o terminal na pasta principal do projeto e execute:

python main.py

Executar os testes automatizados

Para executar os testes utilizando a biblioteca nativa unittest:

python -m unittest

Para visualizar individualmente os testes:

python -m unittest discover -s tests -v

3. Estrutura de pastas

sistema_especialista_assistencia_tecnica/
│
├── dados/
│   ├── perguntas.json
│   └── regras.json
│
├── tests/
│   ├── __init__.py
│   └── test_motor.py
│
├── base.py
├── main.py
├── motor.py
└── README.md

Função de cada arquivo

Arquivo

Responsabilidade

main.py

Interface de interação com o usuário e execução da triagem.

motor.py

Motor de inferência e explicação das conclusões.

base.py

Carregamento e validação dos arquivos JSON.

dados/perguntas.json

Armazena as perguntas e opções de resposta.

dados/regras.json

Armazena as 24 regras do sistema especialista.

tests/__init__.py

Permite a descoberta dos testes na pasta.

tests/test_motor.py

Contém os testes automatizados do motor.

README.md

Documentação e instruções do projeto.

4. Tecnologias utilizadas

O projeto foi desenvolvido utilizando Python e JSON.

Python: escolhido por possuir uma sintaxe simples, facilitar a leitura do código e oferecer recursos suficientes para implementar um sistema especialista sem depender de bibliotecas externas.

JSON: utilizado para armazenar as perguntas e as regras de maneira organizada, permitindo atualizar a base de conhecimento sem precisar modificar o funcionamento do motor.

Unittest: biblioteca nativa do Python utilizada para realizar testes automatizados e verificar o funcionamento do sistema.

O motor de inferência foi desenvolvido pelo próprio grupo, sem utilizar bibliotecas prontas de sistemas especialistas. Essa escolha permite compreender e controlar diretamente o funcionamento da lógica de inferência.

5. Como funciona o encadeamento para frente

O sistema utiliza a técnica de encadeamento para frente (Forward Chaining), que começa com os fatos fornecidos pelo usuário e procura regras cujas condições sejam satisfeitas.

Primeiramente, o atendente responde às perguntas sobre o smartphone. Essas respostas são armazenadas como fatos iniciais.

Em seguida, o motor percorre as regras da base de conhecimento e verifica se as condições de cada regra correspondem aos fatos disponíveis. Quando todas as condições de uma regra são verdadeiras, sua conclusão é adicionada aos fatos.

Esse processo continua enquanto novas regras puderem ser ativadas. Assim, uma conclusão de uma regra pode servir como condição para outra regra, permitindo que o sistema avance do reconhecimento de sintomas até um diagnóstico, um encaminhamento e um preço estimado.

Quando nenhuma outra regra pode ser ativada, o processo termina e o sistema apresenta os resultados encontrados.

6. Base de conhecimento: todas as regras

A base de conhecimento possui 24 regras, divididas em dois níveis:

Nível 1 (R01 a R12): identifica suspeitas e situações intermediárias a partir das respostas do usuário.

Nível 2 (R13 a R24): utiliza as suspeitas identificadas para determinar o diagnóstico, o encaminhamento e o preço estimado.

A tabela abaixo documenta as regras cadastradas em dados/regras.json.

Regras de nível 1

ID

SE (condições)

ENTÃO (conclusão)

R01

liga = nao E contato_liquido = sim

suspeita = oxidacao

R02

sofreu_queda = sim E tela_danificada = sim

suspeita = tela

R03

tela_danificada = sim

suspeita = tela

R04

touch_responde = nao

suspeita = tela

R05

bateria_dura_pouco = sim

suspeita = bateria

R06

carrega_normalmente = nao

suspeita = conector

R07

esquenta_muito = sim E bateria_dura_pouco = sim

suspeita = bateria

R08

trava_ou_reinicia = sim

suspeita = software

R09

som_funciona = nao

suspeita = som

R10

camera_funciona = nao

suspeita = camera

R11

idade_aparelho = menos_de_1_ano

situacao_garantia = provavel

R12

liga = nao E contato_liquido = nao

suspeita = software

Regras de nível 2

ID

SE (condições)

ENTÃO (conclusão)

R13

suspeita = oxidacao

Diagnóstico: Oxidação na placa; encaminhamento: Técnico de placa; preço: R$ 250 a R$ 600.

R14

suspeita = tela E sofreu_queda = sim

Diagnóstico: Tela danificada; encaminhamento: Troca de peça; preço: R$ 300 a R$ 900.

R15

suspeita = tela E sofreu_queda = nao E situacao_garantia = provavel

Diagnóstico: Defeito coberto pela garantia; encaminhamento: Garantia do fabricante; preço: R$ 0.

R16

suspeita = bateria E idade_aparelho = mais_de_2_anos

Diagnóstico: Bateria degradada; encaminhamento: Troca de peça; preço: R$ 150 a R$ 350.

R17

suspeita = bateria E idade_aparelho = 1_a_2_anos

Diagnóstico: Bateria degradada; encaminhamento: Troca de peça; preço: R$ 150 a R$ 350.

R18

suspeita = bateria E contato_liquido = nao E situacao_garantia = provavel

Diagnóstico: Defeito coberto pela garantia; encaminhamento: Garantia do fabricante; preço: R$ 0.

R19

suspeita = conector E contato_liquido = nao

Diagnóstico: Conector de carga danificado; encaminhamento: Troca de peça; preço: R$ 100 a R$ 250.

R20

suspeita = conector E contato_liquido = sim

Diagnóstico: Oxidação na placa; encaminhamento: Técnico de placa; preço: R$ 250 a R$ 600.

R21

suspeita = software E liga = sim

Diagnóstico: Falha de software; encaminhamento: Resolver no balcão; preço: R$ 80 a R$ 150.

R22

suspeita = software E liga = nao E contato_liquido = nao

Diagnóstico: Falha de software; encaminhamento: Técnico de placa; preço: R$ 150 a R$ 300.

R23

suspeita = som E contato_liquido = nao

Diagnóstico: Alto-falante com defeito; encaminhamento: Troca de peça; preço: R$ 80 a R$ 200.

R24

suspeita = camera E contato_liquido = nao

Diagnóstico: Câmera com defeito; encaminhamento: Troca de peça; preço: R$ 150 a R$ 400.

7. Como adicionar uma nova regra

As regras ficam armazenadas no arquivo dados/regras.json.

Para adicionar uma nova regra, basta editar esse arquivo e inserir um novo objeto JSON seguindo o padrão utilizado pelas demais regras.

Exemplo:

{
  "id": "R25",
  "descricao": "Exemplo de nova regra",
  "se": {
    "camera_funciona": "nao",
    "contato_liquido": "nao"
  },
  "entao": {
    "suspeita": "camera"
  }
}

Para cadastrar corretamente uma nova regra:

Utilize um ID que ainda não exista.

Escreva uma descrição que explique a condição.

Utilize fatos e valores existentes nas perguntas ou conclusões das regras.

Coloque as condições dentro de se.

Coloque as conclusões dentro de entao.

Respeite a sintaxe JSON, incluindo aspas, vírgulas e chaves.

Não é necessário modificar o motor.py para adicionar regras que sigam o formato já utilizado pelo sistema.

8. Exemplo real de execução

A seguir, um exemplo de atendimento simulado no terminal.

Situação: smartphone não liga, teve contato com líquido e apresenta suspeita de oxidação.

Para reproduzir o exemplo, execute:

python main.py

Responda às perguntas utilizando os números indicados abaixo.

Sessão simulada

==================================================
TechFix Assistência Técnica
Triagem inicial de smartphones no balcão: diagnóstico,
encaminhamento e preço estimado sem depender de um técnico.
==================================================

1) Nova triagem
2) Sobre o sistema
3) Sair
> 1

O aparelho liga?
  1) sim
  2) nao
  3) nao_sei
> 2

O aparelho teve contato com líquido?
  1) sim
  2) nao
  3) nao_sei
> 1

O aparelho sofreu alguma queda?
  1) sim
  2) nao
  3) nao_sei
> 2

A tela está quebrada ou manchada?
  1) sim
  2) nao
  3) nao_sei
> 2

O touch responde normalmente?
  1) sim
  2) nao
  3) nao_sei
> 1

A bateria dura pouco?
  1) sim
  2) nao
  3) nao_sei
> 2

O aparelho carrega normalmente?
  1) sim
  2) nao
  3) nao_sei
> 1

O aparelho esquenta muito?
  1) sim
  2) nao
  3) nao_sei
> 2

O aparelho trava ou reinicia sozinho?
  1) sim
  2) nao
  3) nao_sei
> 2

O som/alto-falante funciona?
  1) sim
  2) nao
  3) nao_sei
> 1

A câmera funciona?
  1) sim
  2) nao
  3) nao_sei
> 1

Qual a idade do aparelho?
  1) menos_de_1_ano
  2) 1_a_2_anos
  3) mais_de_2_anos
  4) nao_sei
> 3

Diagnóstico: Oxidação na placa
Encaminhamento: Técnico de placa
Preço estimado: R$ 250 a R$ 600

[P] Por que chegou nessa conclusão?
[C] Como chegou no diagnóstico?
[V] Voltar ao menu
> p

R01: Se o aparelho não liga e teve contato com líquido,
há suspeita de oxidação
    você respondeu: liga = nao
    você respondeu: contato_liquido = sim
R13: Se há suspeita de oxidação, o diagnóstico é oxidação
na placa, encaminhada ao técnico de placa
    suspeita = oxidacao: concluído pela regra R01

[P] Por que chegou nessa conclusão?
[C] Como chegou no diagnóstico?
[V] Voltar ao menu
> v

1) Nova triagem
2) Sobre o sistema
3) Sair
> 3

Até logo!

Resultado esperado

O sistema identificou a suspeita de oxidação por meio da regra R01 e utilizou a regra R13 para concluir o diagnóstico.

O aparelho foi encaminhado ao técnico de placa, com preço estimado entre R$ 250 e R$ 600.

9. Considerações finais

O desenvolvimento do TechFix permitiu aplicar conceitos de programação em Python, estruturas de dados JSON, lógica de programação e sistemas especialistas.

A separação entre perguntas, regras, motor de inferência e interface facilita a manutenção e a expansão do projeto.

O sistema demonstra como o conhecimento pode ser organizado em regras lógicas para auxiliar na tomada de decisões, oferecendo uma triagem inicial mais organizada e explicável para a assistência técnica.

Observação: os diagnósticos e preços são estimativas fictícias utilizadas para fins acadêmicos, não substituindo uma avaliação técnica presencial.