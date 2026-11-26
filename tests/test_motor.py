
import unittest
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from motor import inferir
from base import carregar_regras, carregar_perguntas


class TestMotor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.regras = carregar_regras()

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

    def test_sem_diagnostico(self):
        perguntas = carregar_perguntas()

        fatos = {
            pergunta["fato"]: "nao_sei"
            for pergunta in perguntas
        }

        finais, disparadas = inferir(fatos, self.regras)

        self.assertNotIn("diagnostico", finais)
        self.assertEqual(disparadas, [])

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

    def test_quantidade_regras(self):
        self.assertGreaterEqual(len(self.regras), 22)

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

    def test_conflito_entre_suspeitas(self):
        fatos = {
            "sofreu_queda": "sim",
            "tela_danificada": "sim",
            "bateria_dura_pouco": "sim",
            "idade_aparelho": "mais_de_2_anos"
        }

        finais, disparadas = inferir(fatos, self.regras)

        self.assertEqual(finais.get("suspeita"), "tela")
        self.assertEqual(finais.get("diagnostico"), "Tela danificada")

        ids = [r["id"] for r in disparadas]
        self.assertIn("R14", ids)
        self.assertNotIn("R05", ids)
        self.assertNotIn("R16", ids)

    def test_tela_sem_queda_fora_garantia(self):
        fatos = {
            "touch_responde": "nao",
            "sofreu_queda": "nao",
            "idade_aparelho": "1_a_2_anos"
        }

        finais, disparadas = inferir(fatos, self.regras)

        self.assertEqual(finais.get("diagnostico"), "Defeito na tela (sem queda)")

        ids = [r["id"] for r in disparadas]
        self.assertIn("R04", ids)
        self.assertIn("R25", ids)
        self.assertIn("R27", ids)

    def test_camera_com_liquido(self):
        fatos = {
            "camera_funciona": "nao",
            "contato_liquido": "sim"
        }

        finais, _ = inferir(fatos, self.regras)

        self.assertEqual(finais.get("diagnostico"), "Oxidação na placa")

    def test_sem_defeito(self):
        fatos = {
            "liga": "sim",
            "contato_liquido": "nao",
            "sofreu_queda": "nao",
            "tela_danificada": "nao",
            "touch_responde": "sim",
            "bateria_dura_pouco": "nao",
            "carrega_normalmente": "sim",
            "esquenta_muito": "nao",
            "trava_ou_reinicia": "nao",
            "som_funciona": "sim",
            "camera_funciona": "sim",
            "idade_aparelho": "mais_de_2_anos"
        }

        finais, disparadas = inferir(fatos, self.regras)

        self.assertEqual(finais.get("diagnostico"), "Nenhum defeito identificado")
        self.assertIn("R33", [r["id"] for r in disparadas])

    def test_superaquecimento(self):
        fatos = {
            "esquenta_muito": "sim",
            "bateria_dura_pouco": "nao",
            "liga": "sim"
        }

        finais, _ = inferir(fatos, self.regras)

        self.assertEqual(
            finais.get("diagnostico"),
            "Superaquecimento (bateria ou placa)"
        )


if __name__ == "__main__":
    unittest.main()
