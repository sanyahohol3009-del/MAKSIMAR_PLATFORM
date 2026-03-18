from __future__ import annotations


class ContractValidationEngineError(RuntimeError):
    """Base error for contract validation engine."""


class ContractDiscoveryError(ContractValidationEngineError):
    """Raised when contract discovery fails."""


class ContractLoadError(ContractValidationEngineError):
    """Raised when contract file loading fails."""


class ContractValidationError(ContractValidationEngineError):
    """Raised when one or more contracts fail validation."""
