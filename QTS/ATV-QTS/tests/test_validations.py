"""Testes de validação defensiva e fronteiras de erro do AutoSeguro (Máximo 5 testes)."""

import pytest

from app.calculator import (
    AgeLimitExceededError,
    AutoSeguroCalculator,
    Driver,
    HighRiskRejectedError,
    InvalidAgeError,
    InvalidClaimsError,
    InvalidInstallmentError,
    InvalidValueError,
    Proposal,
    ValueOutOfBoundsError,
)


# 1. Fronteiras de idade: menor de 18 e acima de 80 anos (BVA)
@pytest.mark.unit
@pytest.mark.bva
@pytest.mark.parametrize(
    ("age", "expected_exc"),
    [
        (17, InvalidAgeError),          # Limite inferior ilegal (< 18)
        (81, AgeLimitExceededError),     # Limite superior extrapolado (> 80)
    ],
)
def test_driver_age_boundaries(age: int, expected_exc: type[Exception]) -> None:
    # [Arrange] / [Act] / [Assert]
    if age < 18:
        with pytest.raises(expected_exc):
            Driver(age=age)
    else:
        proposal = Proposal(driver=Driver(age=age), vehicle_value=50_000.00)
        with pytest.raises(expected_exc):
            AutoSeguroCalculator.validate_eligibility(proposal)


# 2. Fronteiras de sinistros: negativo e alto risco com 3 ou mais (BVA)
@pytest.mark.unit
@pytest.mark.bva
@pytest.mark.parametrize(
    ("claims", "expected_exc"),
    [
        (-1, InvalidClaimsError),        # Sinistros negativos
        (3, HighRiskRejectedError),      # Limite de recusa por alto risco (>= 3)
    ],
)
def test_driver_claims_boundaries(claims: int, expected_exc: type[Exception]) -> None:
    # [Arrange] / [Act] / [Assert]
    if claims < 0:
        with pytest.raises(expected_exc):
            Driver(age=30, claims=claims)
    else:
        proposal = Proposal(driver=Driver(age=30, claims=claims), vehicle_value=50_000.00)
        with pytest.raises(expected_exc):
            AutoSeguroCalculator.validate_eligibility(proposal)


# 3. Fronteiras do valor do veículo: zero, abaixo do piso e acima do teto (BVA)
@pytest.mark.unit
@pytest.mark.bva
@pytest.mark.parametrize(
    ("value", "is_valid", "expected_exc"),
    [
        (0.00, False, InvalidValueError),             # Valor não positivo
        (9_999.99, False, ValueOutOfBoundsError),      # Abaixo de R$ 10.000,00
        (10_000.00, True, None),                       # Limite mínimo exato válido
        (200_000.01, False, ValueOutOfBoundsError),    # Acima de R$ 200.000,00
    ],
)
def test_vehicle_value_boundaries(
    value: float,
    is_valid: bool,
    expected_exc: type[Exception] | None,
    standard_driver: Driver,
) -> None:
    # [Arrange] / [Act] / [Assert]
    if value <= 0:
        with pytest.raises(InvalidValueError):
            Proposal(driver=standard_driver, vehicle_value=value)
    elif not is_valid:
        prop = Proposal(driver=standard_driver, vehicle_value=value)
        with pytest.raises(expected_exc):  # type: ignore[arg-type]
            AutoSeguroCalculator.validate_eligibility(prop)
    else:
        prop = Proposal(driver=standard_driver, vehicle_value=value)
        AutoSeguroCalculator.validate_eligibility(prop)
        assert prop.vehicle_value == value


# 4. Fronteiras de parcelamento: menor que 1 e maior que 6 (BVA)
@pytest.mark.unit
@pytest.mark.bva
@pytest.mark.parametrize("invalid_installments", [0, 7])
def test_installments_boundaries(invalid_installments: int, standard_driver: Driver) -> None:
    # [Arrange] / [Act] / [Assert]
    with pytest.raises(InvalidInstallmentError):
        Proposal(driver=standard_driver, vehicle_value=50_000.00, installments=invalid_installments)


# 5. Adivinhação de erros (Error Guessing): defesa contra booleano como inteiro e tipos incorretos
@pytest.mark.unit
@pytest.mark.error_guessing
def test_error_guessing_type_defense(standard_driver: Driver) -> None:
    # [Arrange] / [Act] / [Assert] - Em Python bool herda de int; teste garante bloqueio
    with pytest.raises(TypeError):
        Driver(age=True)
    with pytest.raises(TypeError):
        Driver(age="30")  # type: ignore[arg-type]

    with pytest.raises(TypeError):
        Driver(age=30, claims=True)
    with pytest.raises(TypeError):
        Driver(age=30, claims="0")  # type: ignore[arg-type]

    with pytest.raises(TypeError):
        Proposal(driver="invalido", vehicle_value=50_000.00)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        Proposal(driver=standard_driver, vehicle_value=True)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        Proposal(driver=standard_driver, vehicle_value="50000")  # type: ignore[arg-type]

    with pytest.raises(TypeError):
        Proposal(driver=standard_driver, vehicle_value=50_000.00, installments=True)
    with pytest.raises(TypeError):
        Proposal(driver=standard_driver, vehicle_value=50_000.00, installments="3")  # type: ignore[arg-type]
