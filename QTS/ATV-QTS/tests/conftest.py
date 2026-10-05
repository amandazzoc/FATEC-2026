"""Fixtures compartilhadas para a suíte de testes unitários."""

import pytest

from app.calculator import Driver, Proposal


@pytest.fixture
def standard_driver() -> Driver:
    """Condutor padrão: 35 anos, sem histórico de sinistros."""
    return Driver(age=35, claims=0)


@pytest.fixture
def standard_proposal(standard_driver: Driver) -> Proposal:
    """Proposta padrão: veículo de R$ 50.000,00 e 1 parcela."""
    return Proposal(driver=standard_driver, vehicle_value=50_000.00, installments=1)
