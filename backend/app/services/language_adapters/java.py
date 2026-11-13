"""Java Language Adapter for JVM applications, Android, and Spring architectures."""

import re
from typing import Dict, List, Any
from pathlib import Path
from backend.app.services.language_adapters.base import (
    BaseLanguageAdapter,
    LanguageCapabilities,
    DiagnosticFinding,
)


class JavaLanguageAdapter(BaseLanguageAdapter):
    """Adapter for Java Enterprise and Android development."""

    def __init__(self):
        super().__init__(
            LanguageCapabilities(
                language_id="java",
                display_name="Java (Enterprise & Android)",
                file_extensions=[".java", ".jar"],
                manifest_files=["pom.xml", "build.gradle", "build.gradle.kts"],
                syntax_highlighting=True,
                tree_sitter_parsing=True,
                lsp_intelligence=True,
                ast_diagnostics=True,
                security_scanning=True,
                dependency_analysis=True,
                execution_sandbox=True,
                testing_harness=True,
                deterministic_repair_verification=True,
                recommended_tools=["javac", "spotbugs", "semgrep", "checkstyle", "mvn", "gradle"],
            )
        )

    def parse_syntax(self, code: str, filename: str) -> Dict[str, Any]:
        lines = code.split("\n")
        package_match = re.search(r"^\s*package\s+([\w\.]+);", code, re.MULTILINE)
        classes = re.findall(r"\bpublic\s+(?:class|interface|enum)\s+(\w+)", code)
        return {
            "language": "java",
            "file": filename,
            "package": package_match.group(1) if package_match else None,
            "classes": classes,
            "status": "parsed",
        }

    def get_diagnostics(self, file_path: str, code: str) -> List[DiagnosticFinding]:
        diagnostics = []
        lines = code.split("\n")
        for idx, line in enumerate(lines, 1):
            if "Runtime.getRuntime().exec(" in line:
                diagnostics.append(
                    DiagnosticFinding(
                        file_path=file_path,
                        line=idx,
                        severity="CRITICAL",
                        message="Direct call to Runtime.exec() is vulnerable to command injection (CWE-78). Use ProcessBuilder with arguments.",
                        rule_id="java-runtime-exec",
                        cwe_id="CWE-78",
                    )
                )
            elif "DESKeySpec" in line or "DESedeKeySpec" in line:
                diagnostics.append(
                    DiagnosticFinding(
                        file_path=file_path,
                        line=idx,
                        severity="HIGH",
                        message="Use of broken cryptographic algorithm DES/3DES (CWE-327). Use AES-GCM.",
                        rule_id="java-broken-crypto-des",
                        cwe_id="CWE-327",
                    )
                )
        return diagnostics

    def detect_dependencies(self, workspace_path: str) -> List[Dict[str, str]]:
        deps = []
        path = Path(workspace_path)
        if (path / "pom.xml").exists():
            deps.append({"type": "build_tool", "name": "Maven", "manifest": "pom.xml"})
        if (path / "build.gradle").exists() or (path / "build.gradle.kts").exists():
            deps.append({"type": "build_tool", "name": "Gradle", "manifest": "build.gradle"})
        return deps

