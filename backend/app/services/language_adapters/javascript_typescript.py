"""JavaScript and TypeScript Language Adapter."""

import json
import re
from typing import Dict, List, Any
from pathlib import Path
from backend.app.services.language_adapters.base import (
    BaseLanguageAdapter,
    LanguageCapabilities,
    DiagnosticFinding,
)


class JavaScriptTypeScriptLanguageAdapter(BaseLanguageAdapter):
    """Adapter for JavaScript, TypeScript, React, and Node.js ecosystems."""

    def __init__(self):
        super().__init__(
            LanguageCapabilities(
                language_id="javascript_typescript",
                display_name="JavaScript / TypeScript",
                file_extensions=[".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx"],
                manifest_files=["package.json", "tsconfig.json", "package-lock.json", "pnpm-lock.yaml", "yarn.lock"],
                syntax_highlighting=True,
                tree_sitter_parsing=True,
                lsp_intelligence=True,
                ast_diagnostics=True,
                security_scanning=True,
                dependency_analysis=True,
                execution_sandbox=True,
                testing_harness=True,
                deterministic_repair_verification=True,
                recommended_tools=["eslint", "tsc", "npm audit", "semgrep", "vitest", "jest"],
            )
        )

    def parse_syntax(self, code: str, filename: str) -> Dict[str, Any]:
        lines = code.split("\n")
        imports = [line.strip() for line in lines if line.strip().startswith("import ") or "require(" in line]
        return {
            "language": "javascript_typescript",
            "file": filename,
            "lines_count": len(lines),
            "imports_detected": len(imports),
            "status": "parsed",
        }

    def get_diagnostics(self, file_path: str, code: str) -> List[DiagnosticFinding]:
        diagnostics = []
        lines = code.split("\n")
        for idx, line in enumerate(lines, 1):
            if re.search(r"\bdangerouslySetInnerHTML\b", line):
                diagnostics.append(
                    DiagnosticFinding(
                        file_path=file_path,
                        line=idx,
                        severity="HIGH",
                        message="Use of dangerouslySetInnerHTML exposes component to Cross-Site Scripting (CWE-79).",
                        rule_id="react-xss-dangerously-set",
                        cwe_id="CWE-79",
                    )
                )
            elif re.search(r"\beval\s*\(", line):
                diagnostics.append(
                    DiagnosticFinding(
                        file_path=file_path,
                        line=idx,
                        severity="CRITICAL",
                        message="eval() in JavaScript can execute arbitrary code (CWE-95).",
                        rule_id="js-eval",
                        cwe_id="CWE-95",
                    )
                )
        return diagnostics

    def detect_dependencies(self, workspace_path: str) -> List[Dict[str, str]]:
        deps = []
        pkg_json = Path(workspace_path) / "package.json"
        if pkg_json.exists():
            try:
                data = json.loads(pkg_json.read_text(encoding="utf-8"))
                for name, ver in data.get("dependencies", {}).items():
                    deps.append({"type": "npm_dependency", "name": name, "version": ver, "manifest": "package.json"})
                for name, ver in data.get("devDependencies", {}).items():
                    deps.append({"type": "npm_dev_dependency", "name": name, "version": ver, "manifest": "package.json"})
            except Exception:
                pass
        return deps

