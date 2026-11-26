
import unittest
import sys
from pathlib import Path

# Garante que o Python encontre motor.py e base.py na raiz
RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from motor import inferir
from base import carregar_regras, carregar_perguntas


class TestMotor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.regras = carregar_regras()

    # TESTE 1: Aparelho não liga e teve contato com líquido
    def test_oxidacao(self):
        fatos = {
            "liga": "nao",
            "contato_liquido": "sim"
        }

        finais, disparadas = inferir(fatos, self.regras)

        self.assertEqual(finais.get("suspeita"), "oxidacao")
        self.assertEqual(
            finais.get("diagnostico"),
            "Oxidação na placa"
        )

        ids = [r["id"] for r in disparadas]
        self.assertIn("R01", ids)
        self.assertIn("R13", ids)

    # TESTE 2: Bateria dura pouco e aparelho tem mais de 2 anos
    def test_bateria_degradada(self):
        fatos = {
            "bateria_dura_pouco": "sim",
            "idade_aparelho": "mais_de_2_anos"
        }

        finais, disparadas = inferir(fatos, self.regras)

        self.assertEqual(finais.get("suspeita"), "bateria")
        self.assertEqual(
            finais.get("diagnostico"),
            "Bateria degradada"
        )

        ids = [r["id"] for r in disparadas]
        self.assertIn("R05", ids)
        self.assertIn("R16", ids)

    # TESTE 3: Aparelho com menos de um ano e defeito sem queda ou líquido
    def test_garantia(self):
        fatos = {
            "idade_aparelho": "menos_de_1_ano",
            "sofreu_queda": "nao",
            "contato_liquido": "nao",
            "tela_danificada": "sim"
        }

        finais, disparadas = inferir(fatos, self.regras)

        self.assertEqual(
            finais.get("diagnostico"),
            "Defeito coberto pela garantia"
        )

        self.assertEqual(
            finais.get("encaminhamento"),
            "Garantia do fabricante"
        )

        ids = [r["id"] for r in disparadas]
        self.assertIn("R03", ids)
        self.assertIn("R11", ids)
        self.assertIn("R15", ids)

    # TESTE 4: Todas as respostas são não sei
    def test_sem_diagnostico(self):
        perguntas = carregar_perguntas()

        fatos = {
            pergunta["fato"]: "nao_sei"
            for pergunta in perguntas
        }

        finais, disparadas = inferir(fatos, self.regras)

        self.assertNotIn("diagnostico", finais)
        self.assertEqual(disparadas, [])

    # TESTE 5: Integração entre nível 1 e nível 2
    def test_integracao_niveis(self):
        fatos = {
            "camera_funciona": "nao",
            "contato_liquido": "nao"
        }

        finais, disparadas = inferir(fatos, self.regras)

        self.assertEqual(
            finais.get("diagnostico"),
            "Câmera com defeito"
        )

        ids = [r["id"] for r in disparadas]

        nivel1 = any(
            int(id_regra[1:]) <= 12 for id_regra in ids
        )

        nivel2 = any(
            int(id_regra[1:]) >= 13 for id_regra in ids
        )

        self.assertTrue(nivel1)
        self.assertTrue(nivel2)

        self.assertIn("R10", ids)
        self.assertIn("R24", ids)

    # TESTE 6: A base possui pelo menos 22 regras
    def test_quantidade_regras(self):
        self.assertGreaterEqual(len(self.regras), 22)

    # TESTE 7: Conector com defeito sem contato com líquido
    def test_conector_danificado(self):
        fatos = {
            "carrega_normalmente": "nao",
            "contato_liquido": "nao"
        }

        finais, disparadas = inferir(fatos, self.regras)

        self.assertEqual(
            finais.get("diagnostico"),
            "Conector de carga danificado"
        )

        ids = [r["id"] for r in disparadas]

        self.assertIn("R06", ids)
        self.assertIn("R19", ids)

    # TESTE 8: Falha de software com aparelho ligado
    def test_falha_software(self):
        fatos = {
            "trava_ou_reinicia": "sim",
            "liga": "sim"
        }

        finais, disparadas = inferir(fatos, self.regras)

        self.assertEqual(
            finais.get("diagnostico"),
            "Falha de software"
        )

        ids = [r["id"] for r in disparadas]

        self.assertIn("R08", ids)
        self.assertIn("R21", ids)


if __name__ == "__main__":
    unittest.main()
