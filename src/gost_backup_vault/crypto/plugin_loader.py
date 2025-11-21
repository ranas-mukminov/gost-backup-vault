import importlib
from typing import Type
from .base import CryptoProvider
from .local_software_gost import LocalSoftwareGostProvider

class PluginLoader:
    @staticmethod
    def load_provider(provider_name: str) -> Type[CryptoProvider]:
        if provider_name == "local_software":
            return LocalSoftwareGostProvider
        
        # Try to load from external package
        try:
            module = importlib.import_module(f"gost_backup_vault_plugins.{provider_name}")
            return getattr(module, "Provider")
        except (ImportError, AttributeError):
            # Fallback or raise error
            raise ValueError(f"Unknown crypto provider: {provider_name}")
