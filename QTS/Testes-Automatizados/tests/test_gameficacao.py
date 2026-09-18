"""
Suíte de testes unitários — Motor de Gamificação
=================================================
Cobre as funções `calcular_xp`, `calcular_nivel` e `subiu_de_nivel`
de `app/business.py`.

Pirâmide de testes: camada UNITÁRIA (marcador @pytest.mark.unit).
Nenhuma dependência de banco de dados ou HTTP — somente lógica pura.
"""

import pytest

from app.business import calcular_nivel, calcular_xp, subiu_de_nivel


# ---------------------------------------------------------------------------
# calcular_xp — regras de pontuação por tempo de resposta
# ---------------------------------------------------------------------------

class TestCalcularXP:
    """Testa todos os intervalos de tempo e as fronteiras exatas (boundary values)."""

    # --- Faixa rápida: tempo <= 5 s → 100 XP ---

    @pytest.mark.unit
    def test_xp_maximo_resposta_instantanea(self):
        """Tempo zero (resposta instantânea) retorna XP máximo."""
        assert calcular_xp(0.0) == 100

    @pytest.mark.unit
    def test_xp_maximo_dentro_faixa_rapida(self):
        """Tempo dentro da faixa rápida (3 s) retorna 100 XP."""
        assert calcular_xp(3.0) == 100

    @pytest.mark.unit
    def test_xp_limite_exato_5_segundos(self):
        """Exatamente 5 s é o limite da faixa rápida — deve retornar 100 XP."""
        assert calcular_xp(5.0) == 100

    @pytest.mark.unit
    def test_xp_logo_apos_limite_rapido(self):
        """5,001 s já ultrapassa a faixa rápida — deve retornar 50 XP."""
        assert calcular_xp(5.001) == 50

    # --- Faixa média: 5 s < tempo <= 15 s → 50 XP ---

    @pytest.mark.unit
    def test_xp_medio_inicio_da_faixa(self):
        """Início da faixa média (6 s) retorna 50 XP."""
        assert calcular_xp(6.0) == 50

    @pytest.mark.unit
    def test_xp_medio_meio_da_faixa(self):
        """Meio da faixa média (10 s) retorna 50 XP."""
        assert calcular_xp(10.0) == 50

    @pytest.mark.unit
    def test_xp_limite_exato_15_segundos(self):
        """Exatamente 15 s é o limite da faixa média — deve retornar 50 XP."""
        assert calcular_xp(15.0) == 50

    @pytest.mark.unit
    def test_xp_logo_apos_limite_medio(self):
        """15,001 s ultrapassa a faixa média — deve retornar 25 XP."""
        assert calcular_xp(15.001) == 25

    # --- Faixa lenta: tempo > 15 s → 25 XP ---

    @pytest.mark.unit
    def test_xp_minimo_inicio_da_faixa_lenta(self):
        """Início da faixa lenta (16 s) retorna 25 XP."""
        assert calcular_xp(16.0) == 25

    @pytest.mark.unit
    def test_xp_minimo_tempo_muito_alto(self):
        """Tempo muito alto (300 s) ainda retorna o XP mínimo de 25."""
        assert calcular_xp(300.0) == 25

    # --- Valores de retorno — só três valores possíveis ---

    @pytest.mark.unit
    @pytest.mark.parametrize("tempo,esperado", [
        (0.0,   100),
        (1.0,   100),
        (5.0,   100),
        (5.1,    50),
        (10.0,   50),
        (15.0,   50),
        (15.1,   25),
        (60.0,   25),
    ])
    def test_xp_valores_parametrizados(self, tempo, esperado):
        """Tabela de decisão completa dos três intervalos de XP."""
        assert calcular_xp(tempo) == esperado

    @pytest.mark.unit
    def test_xp_retorna_inteiro(self):
        """O tipo de retorno deve ser sempre int."""
        assert isinstance(calcular_xp(7.5), int)


# ---------------------------------------------------------------------------
# calcular_nivel — fórmula: xp // 1000 + 1
# ---------------------------------------------------------------------------

class TestCalcularNivel:
    """Testa o cálculo de nível com base no XP acumulado."""

    @pytest.mark.unit
    def test_nivel_1_com_xp_zero(self):
        """Sem XP algum o jogador deve estar no nível 1."""
        assert calcular_nivel(0) == 1

    @pytest.mark.unit
    def test_nivel_1_com_xp_maximo_da_faixa(self):
        """Com 999 XP o jogador ainda está no nível 1."""
        assert calcular_nivel(999) == 1

    @pytest.mark.unit
    def test_nivel_2_no_limite_exato(self):
        """Exatamente 1000 XP deve promover ao nível 2."""
        assert calcular_nivel(1000) == 2

    @pytest.mark.unit
    def test_nivel_2_dentro_da_faixa(self):
        """1500 XP está dentro da faixa do nível 2."""
        assert calcular_nivel(1500) == 2

    @pytest.mark.unit
    def test_nivel_2_no_teto_da_faixa(self):
        """1999 XP é o teto do nível 2 (antes de subir para 3)."""
        assert calcular_nivel(1999) == 2

    @pytest.mark.unit
    def test_nivel_3_no_limite_exato(self):
        """Exatamente 2000 XP deve promover ao nível 3."""
        assert calcular_nivel(2000) == 3

    @pytest.mark.unit
    def test_nivel_3_com_xp_fracionado(self):
        """2500 XP está dentro da faixa do nível 3."""
        assert calcular_nivel(2500) == 3

    @pytest.mark.unit
    def test_nivel_10_no_limite_exato(self):
        """9000 XP deve corresponder ao nível 10."""
        assert calcular_nivel(9000) == 10

    @pytest.mark.unit
    def test_nivel_cresce_linearmente(self):
        """Cada 1000 XP extra deve incrementar o nível em 1."""
        for nivel_esperado in range(1, 6):
            xp = (nivel_esperado - 1) * 1000
            assert calcular_nivel(xp) == nivel_esperado, (
                f"calcular_nivel({xp}) deveria retornar {nivel_esperado}"
            )

    @pytest.mark.unit
    def test_nivel_retorna_inteiro(self):
        """O tipo de retorno deve ser sempre int."""
        assert isinstance(calcular_nivel(500), int)

    @pytest.mark.unit
    @pytest.mark.parametrize("xp,nivel_esperado", [
        (0,    1),
        (999,  1),
        (1000, 2),
        (1999, 2),
        (2000, 3),
        (4999, 5),
        (5000, 6),
    ])
    def test_nivel_parametrizado(self, xp, nivel_esperado):
        """Tabela de equivalência completa dos limites de nível."""
        assert calcular_nivel(xp) == nivel_esperado


# ---------------------------------------------------------------------------
# subiu_de_nivel — detecta transição entre níveis
# ---------------------------------------------------------------------------

class TestSubiuDeNivel:
    """Testa a detecção de subida de nível ao comparar XP antes e depois."""

    @pytest.mark.unit
    def test_sobe_nivel_cruzando_limite_de_1000(self):
        """Cruzar a barreira de 1000 XP deve indicar subida de nível."""
        assert subiu_de_nivel(950, 1050) is True

    @pytest.mark.unit
    def test_sobe_nivel_com_xp_exato_no_limite(self):
        """XP antes = 999 e depois = 1000 é a transição mínima para nível 2."""
        assert subiu_de_nivel(999, 1000) is True

    @pytest.mark.unit
    def test_sobe_nivel_cruzando_2000(self):
        """Cruzar 2000 XP deve indicar subida do nível 2 para o 3."""
        assert subiu_de_nivel(1900, 2100) is True

    @pytest.mark.unit
    def test_sobe_nivel_pulando_dois_niveis(self):
        """
        Ganhar XP suficiente para pular dois níveis de uma vez deve
        indicar subida (o resultado é True independente de quantos
        níveis foram pulados).
        """
        assert subiu_de_nivel(900, 2100) is True

    @pytest.mark.unit
    def test_nao_sobe_nivel_no_mesmo_nivel(self):
        """Permanecer na mesma faixa de nível deve retornar False."""
        assert subiu_de_nivel(100, 500) is False

    @pytest.mark.unit
    def test_nao_sobe_nivel_ganho_zero(self):
        """Nenhum ganho de XP não deve indicar subida de nível."""
        assert subiu_de_nivel(500, 500) is False

    @pytest.mark.unit
    def test_nao_sobe_nivel_proximo_ao_limite(self):
        """999 → 999 permanece no nível 1, sem subida."""
        assert subiu_de_nivel(0, 999) is False

    @pytest.mark.unit
    def test_nao_sobe_nivel_ainda_no_nivel_2(self):
        """1000 → 1999 permanece no nível 2, sem subida."""
        assert subiu_de_nivel(1000, 1999) is False

    @pytest.mark.unit
    def test_subida_exatamente_no_limite_do_nivel_3(self):
        """1999 → 2000 deve indicar a transição do nível 2 para o 3."""
        assert subiu_de_nivel(1999, 2000) is True

    @pytest.mark.unit
    def test_retorna_bool(self):
        """O retorno deve ser do tipo bool."""
        assert isinstance(subiu_de_nivel(0, 100), bool)

    @pytest.mark.unit
    @pytest.mark.parametrize("xp_antes,xp_depois,esperado", [
        (0,    999,  False),  # nível 1 → nível 1
        (0,    1000, True),   # nível 1 → nível 2
        (1000, 1999, False),  # nível 2 → nível 2
        (1000, 2000, True),   # nível 2 → nível 3
        (950,  1050, True),   # cruza barreira de 1000
        (500,  600,  False),  # dentro do nível 1
        (900,  2100, True),   # pula dois níveis
    ])
    def test_subiu_de_nivel_parametrizado(self, xp_antes, xp_depois, esperado):
        """Tabela de decisão cobrindo todos os cenários relevantes."""
        assert subiu_de_nivel(xp_antes, xp_depois) is esperado


# ---------------------------------------------------------------------------
# Cenários de integração entre calcular_xp e subiu_de_nivel
# (ainda unitários — sem banco de dados)
# ---------------------------------------------------------------------------

class TestFluxoXPParaNivel:
    """
    Verifica que o XP gerado por calcular_xp é suficiente para
    eventualmente disparar uma subida de nível, simulando o fluxo
    real da aplicação sem depender de banco de dados.
    """

    @pytest.mark.unit
    def test_dez_respostas_rapidas_sobem_nivel(self):
        """
        10 respostas rápidas (10 × 100 XP = 1000 XP) devem
        elevar o jogador do nível 1 ao nível 2.
        """
        xp = 0
        for _ in range(10):
            xp += calcular_xp(3.0)  # 100 XP cada

        assert calcular_nivel(xp) == 2

    @pytest.mark.unit
    def test_vinte_respostas_medias_sobem_nivel(self):
        """
        20 respostas médias (20 × 50 XP = 1000 XP) devem
        elevar o jogador do nível 1 ao nível 2.
        """
        xp = 0
        for _ in range(20):
            xp += calcular_xp(10.0)  # 50 XP cada

        assert calcular_nivel(xp) == 2

    @pytest.mark.unit
    def test_nona_resposta_rapida_nao_sobe_nivel(self):
        """
        9 respostas rápidas (900 XP) não são suficientes para
        a subida de nível — a 10.ª será determinante.
        """
        xp_antes = calcular_xp(3.0) * 9  # 900 XP
        xp_depois = xp_antes + calcular_xp(3.0)  # 1000 XP

        assert subiu_de_nivel(xp_antes, xp_depois) is True

    @pytest.mark.unit
    def test_nivel_apos_mix_de_respostas(self):
        """
        Simula 5 respostas rápidas + 5 lentas:
        5 × 100 + 5 × 25 = 625 XP → ainda no nível 1.
        """
        xp = 5 * calcular_xp(2.0) + 5 * calcular_xp(30.0)
        assert calcular_nivel(xp) == 1
