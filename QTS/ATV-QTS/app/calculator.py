"""Motor de cálculo e regras de subscrição do AutoSeguro."""

from dataclasses import dataclass


# ==============================================================================
# Exceções de Domínio
# ==============================================================================

class AutoSeguroError(Exception):
    """Exceção base para regras de negócio do AutoSeguro."""


class InvalidAgeError(AutoSeguroError):
    """Idade menor que a mínima permitida (18 anos)."""


class AgeLimitExceededError(AutoSeguroError):
    """Idade excede o limite aceito pela subscrição automática (80 anos)."""


class InvalidClaimsError(AutoSeguroError):
    """Quantidade de sinistros negativa."""


class HighRiskRejectedError(AutoSeguroError):
    """Condutor com 3 ou mais sinistros é considerado alto risco."""


class InvalidValueError(AutoSeguroError):
    """Valor do veículo menor ou igual a zero."""


class ValueOutOfBoundsError(AutoSeguroError):
    """Valor do veículo fora da faixa permitida (R$ 10.000 a R$ 200.000)."""


class InvalidInstallmentError(AutoSeguroError):
    """Número de parcelas inválido (permitido de 1 a 6)."""


# ==============================================================================
# Modelos de Dados
# ==============================================================================

@dataclass(frozen=True, slots=True)
class Driver:
    """Dados cadastrais e histórico do condutor."""

    age: int
    claims: int = 0

    def __post_init__(self) -> None:
        if not isinstance(self.age, int) or isinstance(self.age, bool):
            raise TypeError("A idade deve ser um número inteiro.")
        if not isinstance(self.claims, int) or isinstance(self.claims, bool):
            raise TypeError("A quantidade de sinistros deve ser um número inteiro.")
        if self.age < 18:
            raise InvalidAgeError("Idade mínima permitida é 18 anos.")
        if self.claims < 0:
            raise InvalidClaimsError("Sinistros não podem ser negativos.")


@dataclass(frozen=True, slots=True)
class Proposal:
    """Proposta com dados do condutor, veículo e parcelamento."""

    driver: Driver
    vehicle_value: float
    installments: int = 1

    def __post_init__(self) -> None:
        if not isinstance(self.driver, Driver):
            raise TypeError("Condutor deve ser uma instância de Driver.")
        if isinstance(self.vehicle_value, bool) or not isinstance(self.vehicle_value, (int, float)):
            raise TypeError("Valor do veículo deve ser numérico.")
        if not isinstance(self.installments, int) or isinstance(self.installments, bool):
            raise TypeError("Parcelas devem ser um número inteiro.")
        if self.vehicle_value <= 0:
            raise InvalidValueError("Valor do veículo deve ser maior que zero.")
        if self.installments < 1 or self.installments > 6:
            raise InvalidInstallmentError("Parcelas devem ser entre 1 e 6.")


@dataclass(frozen=True, slots=True)
class Quote:
    """Resultado detalhado da cotação."""

    base_premium: float
    age_factor: float
    claims_factor: float
    final_premium: float
    installment_value: float
    is_floor_applied: bool


# ==============================================================================
# Calculadora e Motor de Regras
# ==============================================================================

class AutoSeguroCalculator:
    """Regras de precificação e validações atuariais."""

    BASE_RATE: float = 0.04
    MIN_VALUE: float = 10_000.00
    MAX_VALUE: float = 200_000.00
    PREMIUM_FLOOR: float = 500.00

    @classmethod
    def get_age_factor(cls, age: int) -> float:
        """Determina o fator de risco etário."""
        if 18 <= age <= 25:
            return 1.30
        if 26 <= age <= 65:
            return 1.00
        return 1.20

    @classmethod
    def get_claims_factor(cls, claims: int) -> float:
        """Determina o fator de sinistralidade recente."""
        if claims == 0:
            return 0.90
        return 1.20

    @classmethod
    def validate_eligibility(cls, proposal: Proposal) -> None:
        """Valida a elegibilidade da proposta de seguro."""
        if proposal.driver.age > 80:
            raise AgeLimitExceededError("Idade excede o limite máximo de 80 anos.")
        if proposal.driver.claims >= 3:
            raise HighRiskRejectedError("Condutor com 3 ou mais sinistros não é aceito.")
        if proposal.vehicle_value < cls.MIN_VALUE or proposal.vehicle_value > cls.MAX_VALUE:
            raise ValueOutOfBoundsError("Valor fora da faixa de R$ 10.000,00 a R$ 200.000,00.")

    @classmethod
    def calculate_quote(cls, proposal: Proposal) -> Quote:
        """Executa a cotação determinística com piso e parcelamento."""
        cls.validate_eligibility(proposal)

        base_premium = round(proposal.vehicle_value * cls.BASE_RATE, 2)
        age_factor = cls.get_age_factor(proposal.driver.age)
        claims_factor = cls.get_claims_factor(proposal.driver.claims)

        raw_premium = round(base_premium * age_factor * claims_factor, 2)

        if raw_premium < cls.PREMIUM_FLOOR:
            final_premium = cls.PREMIUM_FLOOR
            is_floor = True
        else:
            final_premium = raw_premium
            is_floor = False

        if proposal.installments == 1:
            installment_val = round(final_premium * 0.95, 2)
        else:
            installment_val = round(final_premium / proposal.installments, 2)

        return Quote(
            base_premium=base_premium,
            age_factor=age_factor,
            claims_factor=claims_factor,
            final_premium=final_premium,
            installment_value=installment_val,
            is_floor_applied=is_floor,
        )
