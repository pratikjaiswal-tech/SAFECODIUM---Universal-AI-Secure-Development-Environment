"""SAFECODIUM — Universal Language Adapter Registry."""

from typing import Dict, List, Optional
from backend.app.services.language_adapters.base import BaseLanguageAdapter, LanguageCapabilities
from backend.app.services.language_adapters.c_cpp import CCppLanguageAdapter
from backend.app.services.language_adapters.python import PythonLanguageAdapter
from backend.app.services.language_adapters.javascript_typescript import JavaScriptTypeScriptLanguageAdapter
from backend.app.services.language_adapters.java import JavaLanguageAdapter
from backend.app.services.language_adapters.expansion import GoLanguageAdapter, RustLanguageAdapter


class LanguageRegistry:
    """Registry managing language adapters and capability lookups."""

    def __init__(self):
        self._adapters: Dict[str, BaseLanguageAdapter] = {}
        self._register_defaults()

    def _register_defaults(self):
        self.register(CCppLanguageAdapter())
        self.register(PythonLanguageAdapter())
        self.register(JavaScriptTypeScriptLanguageAdapter())
        self.register(JavaLanguageAdapter())
        self.register(GoLanguageAdapter())
        self.register(RustLanguageAdapter())

    def register(self, adapter: BaseLanguageAdapter):
        self._adapters[adapter.language_id] = adapter

    def get_adapter(self, language_id: str) -> Optional[BaseLanguageAdapter]:
        return self._adapters.get(language_id)

    def find_adapter_by_file(self, filename: str) -> Optional[BaseLanguageAdapter]:
        """Find matching adapter by checking file extension."""
        for adapter in self._adapters.values():
            if adapter.matches_file(filename):
                return adapter
        return None

    def list_capabilities(self) -> List[LanguageCapabilities]:
        """Return capabilities of all registered adapters."""
        return [adapter.capabilities for adapter in self._adapters.values()]


# Global registry singleton
language_registry = LanguageRegistry()

