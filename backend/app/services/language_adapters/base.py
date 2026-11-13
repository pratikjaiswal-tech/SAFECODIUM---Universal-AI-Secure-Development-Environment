"""SAFECODIUM — Universal Language Adapter Protocol & Capability Registry.

Declares explicit language capabilities to ensure no false support claims.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class LanguageCapabilities(BaseModel):
    """Explicit declaration of language-specific toolchain and IDE capabilities."""
    language_id: str
    display_name: str
    file_extensions: List[str]
    manifest_files: List[str]
    
    # Capabilities (True/False based on actual toolchain availability)
    syntax_highlighting: bool = True
    tree_sitter_parsing: bool = False
    lsp_intelligence: bool = False
    ast_diagnostics: bool = False
    security_scanning: bool = False
    dependency_analysis: bool = False
    execution_sandbox: bool = False
    testing_harness: bool = False
    deterministic_repair_verification: bool = False
    
    # Toolchain details
    recommended_tools: List[str] = Field(default_factory=list)


class DiagnosticFinding(BaseModel):
    """Language-agnostic diagnostic item."""
    file_path: str
    line: int
    column: int = 1
    severity: str = "WARNING"  # ERROR, WARNING, INFO
    message: str
    rule_id: Optional[str] = None
    cwe_id: Optional[str] = None


class BaseLanguageAdapter(ABC):
    """Abstract Base Class for modular programming language adapters."""

    def __init__(self, capabilities: LanguageCapabilities):
        self.capabilities = capabilities

    @property
    def language_id(self) -> str:
        return self.capabilities.language_id

    @property
    def extensions(self) -> List[str]:
        return self.capabilities.file_extensions

    def matches_file(self, filename: str) -> bool:
        """Check if file matches this language adapter by extension."""
        return any(filename.lower().endswith(ext.lower()) for ext in self.extensions)

    @abstractmethod
    def parse_syntax(self, code: str, filename: str) -> Dict[str, Any]:
        """Perform syntax tree inspection or AST validation."""
        pass

    @abstractmethod
    def get_diagnostics(self, file_path: str, code: str) -> List[DiagnosticFinding]:
        """Produce semantic or linting diagnostics."""
        pass

    @abstractmethod
    def detect_dependencies(self, workspace_path: str) -> List[Dict[str, str]]:
        """Detect declared dependencies and manifests."""
        pass

