"""Portable local mobile app memory contracts.

This package defines local app memory records, store boundaries, retention
policy, and encryption requirements. It does not persist data, open network
connections, write MAKSIMAR core, or define global project memory truth.
"""

from shared_mobile_core.app_memory.app_memory_encryption_contract import (
    AppMemoryEncryptionContract,
)
from shared_mobile_core.app_memory.app_memory_record_contract import (
    AppMemoryRecordContract,
)
from shared_mobile_core.app_memory.app_memory_retention_policy import (
    AppMemoryRetentionPolicy,
)
from shared_mobile_core.app_memory.app_memory_store_contract import (
    AppMemoryStoreContract,
)

__all__ = (
    "AppMemoryEncryptionContract",
    "AppMemoryRecordContract",
    "AppMemoryRetentionPolicy",
    "AppMemoryStoreContract",
)
