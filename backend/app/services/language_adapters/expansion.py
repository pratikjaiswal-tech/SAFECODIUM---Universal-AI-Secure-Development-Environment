"""Go, Rust, and General Expansion Language Adapters."""

import re
from typing import Dict, List, Any
from pathlib import Path
from backend.app.services.language_adapters.base import (
    BaseLanguageAdapter,
    LanguageCapabilities,
    DiagnosticFinding,
)


class GoLanguageAdapter(BaseLanguageAdapter):
    """Adapter for Golang microservices and systems."""

    def __init__(self):
        super().__init__(
            LanguageCapabilities(
                language_id="go",
                display_name="Go",
                file_extensions=[".go"],
                manifest_files=["go.mod", "go.sum"],
                syntax_highlighting=True,
                tree_sitter_parsing=True,
                lsp_intelligence=True,
                ast_diagnostics=True,
                security_scanning=True,
                dependency_analysis=True,
                execution_sandbox=True,
                testing_harness=True,
                deterministic_repair_verification=True,
                recommended_tools=["gosec", "govulncheck", "go test", "golangci-lint"],
            )
        )

    def parse_syntax(self, code: str, filename: str) -> Dict[str, Any]:
        package_match = re.search(r"^\s*package\s+(\w+)", code, re.MULTILINE)
        return {"language": "go", "file": filename, "package": package_match.group(1) if package_match else "main"}

    def get_diagnostics(self, file_path: str, code: str) -> List[DiagnosticFinding]:
        diagnostics = []
        for idx, line in enumerate(code.splitlines(), 1):
            if "exec.Command(" in line and ("bash" in line or "sh" in line):
                diagnostics.append(
                    DiagnosticFinding(
                        file_path=file_path,
                        line=idx,
                        severity="HIGH",
                        message="Command execution via shell invocation can lead to command injection (CWE-78).",
                        rule_id="go-command-exec",
                        cwe_id="CWE-78",
                    )
                )
        return diagnostics

    def detect_dependencies(self, workspace_path: str) -> List[Dict[str, str]]:
        deps = []
        mod = Path(workspace_path) / "go.mod"
        if mod.exists():
            deps.append({"type": "go_module", "name": "go.mod", "manifest": "go.mod"})
        return deps


class RustLanguageAdapter(BaseLanguageAdapter):
    """Adapter for Rust memory-safe and systems development."""

    def __init__(self):
        super().__init__(
            LanguageCapabilities(
                language_id="rust",
                display_name="Rust",
                file_extensions=[".rs"],
                manifest_files=["Cargo.toml", "Cargo.lock"],
                syntax_highlighting=True,
                tree_sitter_parsing=True,
                lsp_intelligence=True,
                ast_diagnostics=True,
                security_scanning=True,
                dependency_analysis=True,
                execution_sandbox=True,
                testing_harness=True,
                deterministic_repair_verification=True,
                recommended_tools=["cargo-audit", "cargo-clippy", "cargo test", "semgrep"],
            )
        )

    def parse_syntax(self, code: str, filename: str) -> Dict[str, Any]:
        has_unsafe = "unsafe {" in code or "unsafe fn" in code
        return {"language": "rust", "file": filename, "contains_unsafe_blocks": has_unsafe}

    def get_diagnostics(self, file_path: str, code: str) -> List[DiagnosticFinding]:
        diagnostics = []
        for idx, line in enumerate(code.splitlines(), 1):
            if "unsafe {" in line or "unsafe fn" in line:
                diagnostics.append(
                    DiagnosticFinding(
                        file_path=file_path,
                        line=idx,
                        severity="INFO",
                        message="Unsafe block declared. Bypasses Rust compiler borrow checker guarantees.",
                        rule_id="rust-unsafe-block",
                    )
                )
        return diagnostics

    def detect_dependencies(self, workspace_path: str) -> List[Dict[str, str]]:
        deps = []
        cargo = Path(workspace_path) / "Cargo.toml"
        if cargo.exists():
            deps.append({"type": "cargo_crate", "name": "Cargo.toml", "manifest": "Cargo.toml"})
        return deps

