"""Python Language Adapter with AST analysis, Bandit/Semgrep support, and pytest."""

import ast
from typing import Dict, List, Any
from pathlib import Path
from backend.app.services.language_adapters.base import (
    BaseLanguageAdapter,
    LanguageCapabilities,
    DiagnosticFinding,
)


class PythonLanguageAdapter(BaseLanguageAdapter):
    """Adapter for Python security, syntax, and dependency analysis."""

    def __init__(self):
        super().__init__(
            LanguageCapabilities(
                language_id="python",
                display_name="Python",
                file_extensions=[".py", ".pyw"],
                manifest_files=["requirements.txt", "Pipfile", "pyproject.toml", "setup.py"],
                syntax_highlighting=True,
                tree_sitter_parsing=True,
                lsp_intelligence=True,
                ast_diagnostics=True,
                security_scanning=True,
                dependency_analysis=True,
                execution_sandbox=True,
                testing_harness=True,
                deterministic_repair_verification=True,
                recommended_tools=["ast", "pytest", "bandit", "semgrep", "ruff", "pip-audit"],
            )
        )

    def parse_syntax(self, code: str, filename: str) -> Dict[str, Any]:
        """Parse Python source code using Python's native AST engine."""
        try:
            tree = ast.parse(code, filename=filename)
            functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
            return {
                "language": "python",
                "file": filename,
                "status": "valid",
                "function_count": len(functions),
                "class_count": len(classes),
                "functions": functions[:20],
            }
        except SyntaxError as e:
            return {
                "language": "python",
                "file": filename,
                "status": "syntax_error",
                "error_line": e.lineno,
                "error_offset": e.offset,
                "error_msg": str(e),
            }

    def get_diagnostics(self, file_path: str, code: str) -> List[DiagnosticFinding]:
        diagnostics = []
        try:
            tree = ast.parse(code, filename=file_path)
            for node in ast.walk(tree):
                # Detect eval() calls
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "eval":
                    diagnostics.append(
                        DiagnosticFinding(
                            file_path=file_path,
                            line=node.lineno,
                            column=node.col_offset,
                            severity="CRITICAL",
                            message="Use of 'eval' allows arbitrary code execution (CWE-94 / CWE-95).",
                            rule_id="py-eval-detected",
                            cwe_id="CWE-95",
                        )
                    )
                # Detect shell=True in subprocess
                elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr in ("Popen", "run", "call", "check_output"):
                    for kw in node.keywords:
                        if kw.arg == "shell" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                            diagnostics.append(
                                DiagnosticFinding(
                                    file_path=file_path,
                                    line=node.lineno,
                                    column=node.col_offset,
                                    severity="HIGH",
                                    message="Subprocess invocation with 'shell=True' is vulnerable to command injection (CWE-78).",
                                    rule_id="py-subprocess-shell-true",
                                    cwe_id="CWE-78",
                                )
                            )
        except SyntaxError as e:
            diagnostics.append(
                DiagnosticFinding(
                    file_path=file_path,
                    line=e.lineno or 1,
                    column=e.offset or 1,
                    severity="ERROR",
                    message=f"Syntax Error: {e.msg}",
                    rule_id="py-syntax-error",
                )
            )
        return diagnostics

    def detect_dependencies(self, workspace_path: str) -> List[Dict[str, str]]:
        deps = []
        path = Path(workspace_path)
        req_file = path / "requirements.txt"
        if req_file.exists():
            for line in req_file.read_text(encoding="utf-8", errors="ignore").splitlines():
                clean = line.strip()
                if clean and not clean.startswith("#"):
                    parts = clean.split("==")
                    pkg = parts[0].strip()
                    ver = parts[1].strip() if len(parts) > 1 else "latest"
                    deps.append({"type": "python_pkg", "name": pkg, "version": ver, "manifest": "requirements.txt"})
        return deps

