"""Testes das regras de precificação e cálculo do AutoSeguro (Máximo 5 testes)."""

import pytest

from app.calculator import AutoSeguroCalculator, Driver, Proposal


# 1. Multiplicador de idade (Particionamento de Equivalência e Análise do Valor Limite)
@pytest.mark.unit
@pytest.mark.bva
@pytest.mark.parametrize(
    ("age", "expected_factor"),
    [
        (18, 1.30),  # Limite inferior jovem
        (25, 1.30),  # Limite superior jovem
        (26, 1.00),  # Limite inferior padrão
        (65, 1.00),  # Limite superior padrão
        (66, 1.20),  # Limite inferior sênior
        (80, 1.20),  # Limite superior sênior
    ],
)
def test_age_factor_ep_and_bva(age: int, expected_factor: float) -> None:
    # [Arrange]
    driver_age = age

    # [Act]
    factor = AutoSeguroCalculator.get_age_factor(driver_age)

    # [Assert]
    assert factor == expected_factor


# 2. Fator de sinistralidade (BVA)
@pytest.mark.unit
@pytest.mark.bva
@pytest.mark.parametrize(
    ("claims", "expected_factor"),
    [
        (0, 0.90),  # Bônus de 10% de desconto
        (1, 1.20),  # Agravo de 20%
        (2, 1.20),  # Limite máximo aceito com agravo
    ],
)
def test_claims_factor_ep_and_bva(claims: int, expected_factor: float) -> None:
    # [Arrange]
    driver_claims = claims

    # [Act]
    factor = AutoSeguroCalculator.get_claims_factor(driver_claims)

    # [Assert]
    assert factor == expected_factor


# 3. Modalidades de parcelamento: à vista com 5% de desconto e parcelado (EP & BVA)
@pytest.mark.unit
@pytest.mark.ep
@pytest.mark.parametrize(
    ("installments", "expected_installment_val"),
    [
        (1, 1710.00),  # À vista com 5% de desconto (1800 * 0.95)
        (4, 450.00),   # 4x sem juros (1800 / 4)
    ],
)
def test_installments_ep_and_bva(installments: int, expected_installment_val: float) -> None:
    # [Arrange]
    driver = Driver(age=30, claims=0)
    proposal = Proposal(driver=driver, vehicle_value=50_000.00, installments=installments)

    # [Act]
    quote = AutoSeguroCalculator.calculate_quote(proposal)

    # [Assert]
    assert quote.installment_value == expected_installment_val


# 4. Cálculo completo da cotação ponta a ponta (Padrão AAA)
@pytest.mark.unit
def test_standard_quote_calculation(standard_proposal: Proposal) -> None:
    # [Arrange]
    proposal = standard_proposal  # Veículo R$ 50k, taxa 4% = R$ 2000, 35 anos (1.00), 0 sinistros (0.90)

    # [Act]
    quote = AutoSeguroCalculator.calculate_quote(proposal)

    # [Assert]
    assert quote.base_premium == 2000.00
    assert quote.age_factor == 1.00
    assert quote.claims_factor == 0.90
    assert quote.final_premium == 1800.00
    assert quote.installment_value == 1710.00
    assert quote.is_floor_applied is False


# 5. Acionamento do piso mínimo protetivo (R$ 500,00)
@pytest.mark.unit
def test_minimum_floor_applied() -> None:
    # [Arrange]
    # Veículo de R$ 10.000 (taxa 4% = R$ 400), condutor 30 anos (1.00), 0 sinistros (0.90)
    # Prêmio bruto = 400 * 0.90 = R$ 360,00 (< R$ 500,00)
    cheap_driver = Driver(age=30, claims=0)
    proposal = Proposal(driver=cheap_driver, vehicle_value=10_000.00, installments=2)

    # [Act]
    quote = AutoSeguroCalculator.calculate_quote(proposal)

    # [Assert]
    assert quote.final_premium == 500.00
    assert quote.is_floor_applied is True
    assert quote.installment_value == 250.00
