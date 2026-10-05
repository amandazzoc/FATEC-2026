"""Pacote app: Motor de Precificação AutoSeguro."""

from app.calculator import (
    AgeLimitExceededError,
    AutoSeguroCalculator,
    AutoSeguroError,
    Driver,
    HighRiskRejectedError,
    InvalidAgeError,
    InvalidClaimsError,
    InvalidInstallmentError,
    InvalidValueError,
    Proposal,
    Quote,
    ValueOutOfBoundsError,
)

__all__ = [
    "AutoSeguroCalculator",
    "AutoSeguroError",
    "InvalidAgeError",
    "AgeLimitExceededError",
    "InvalidClaimsError",
    "HighRiskRejectedError",
    "InvalidValueError",
    "ValueOutOfBoundsError",
    "InvalidInstallmentError",
    "Driver",
    "Proposal",
    "Quote",
]
