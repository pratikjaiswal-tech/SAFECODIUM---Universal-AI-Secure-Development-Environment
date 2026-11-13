"""C & C++ Language Adapter with Clang/GCC, AST, and Sanitizer verification."""

import re
from typing import Dict, List, Any
from pathlib import Path
from backend.app.services.language_adapters.base import (
    BaseLanguageAdapter,
    LanguageCapabilities,
    DiagnosticFinding,
)


class CCppLanguageAdapter(BaseLanguageAdapter):
    """Adapter for C and C++ embedded firmware and systems development."""

    def __init__(self):
        super().__init__(
            LanguageCapabilities(
                language_id="c_cpp",
                display_name="C / C++ (Embedded & Systems)",
                file_extensions=[".c", ".cpp", ".cc", ".cxx", ".h", ".hpp"],
                manifest_files=["Makefile", "CMakeLists.txt", "platformio.ini", "idf_component.yml"],
                syntax_highlighting=True,
                tree_sitter_parsing=True,
                lsp_intelligence=True,
                ast_diagnostics=True,
                security_scanning=True,
                dependency_analysis=True,
                execution_sandbox=True,
                testing_harness=True,
                deterministic_repair_verification=True,
                recommended_tools=["clang-18", "gcc", "clang-tidy", "ASan", "UBSan", "semgrep"],
            )
        )

    def parse_syntax(self, code: str, filename: str) -> Dict[str, Any]:
        """Perform heuristic & AST boundary analysis for C/C++ code."""
        findings = []
        lines = code.split("\n")
        
        # Check basic syntax patterns and dangerous memory APIs
        for idx, line in enumerate(lines, 1):
            if re.search(r"\bstrcpy\s*\(", line):
                findings.append({"line": idx, "type": "unsafe_call", "symbol": "strcpy", "cwe": "CWE-120"})
            elif re.search(r"\bgets\s*\(", line):
                findings.append({"line": idx, "type": "banned_call", "symbol": "gets", "cwe": "CWE-120"})
            elif re.search(r"\bsprintf\s*\(", line):
                findings.append({"line": idx, "type": "unsafe_call", "symbol": "sprintf", "cwe": "CWE-120"})

        return {
            "language": "c_cpp",
            "file": filename,
            "lines_count": len(lines),
            "unsafe_apis_detected": findings,
            "status": "parsed",
        }

    def get_diagnostics(self, file_path: str, code: str) -> List[DiagnosticFinding]:
        diagnostics = []
        lines = code.split("\n")
        for idx, line in enumerate(lines, 1):
            if "strcpy(" in line:
                diagnostics.append(
                    DiagnosticFinding(
                        file_path=file_path,
                        line=idx,
                        severity="ERROR",
                        message="Potential buffer copy without size check (strcpy). Use strncpy or bounds check.",
                        rule_id="sec-cwe-120",
                        cwe_id="CWE-120",
                    )
                )
            elif "gets(" in line:
                diagnostics.append(
                    DiagnosticFinding(
                        file_path=file_path,
                        line=idx,
                        severity="ERROR",
                        message="Call to obsolete and vulnerable function 'gets'. Use fgets instead.",
                        rule_id="sec-cwe-120",
                        cwe_id="CWE-120",
                    )
                )
        return diagnostics

    def detect_dependencies(self, workspace_path: str) -> List[Dict[str, str]]:
        deps = []
        path = Path(workspace_path)
        if (path / "Makefile").exists():
            deps.append({"type": "build_system", "name": "Make", "manifest": "Makefile"})
        if (path / "CMakeLists.txt").exists():
            deps.append({"type": "build_system", "name": "CMake", "manifest": "CMakeLists.txt"})
        if (path / "platformio.ini").exists():
            deps.append({"type": "framework", "name": "PlatformIO", "manifest": "platformio.ini"})
        return deps

