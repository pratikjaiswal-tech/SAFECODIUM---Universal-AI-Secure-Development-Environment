"""SAFECODIUM — Tests for Unified Security Suite (Gitleaks, OSV, Semgrep)."""

import pytest
from pathlib import Path
from backend.app.services.analysis.unified_scanner import (
    GitleaksScanner,
    OsvDependencyScanner,
    UnifiedScannerOrchestrator,
)


def test_gitleaks_secret_detection(tmp_path: Path):
    """Verify detection of hardcoded AWS keys and tokens (CWE-798)."""
    vuln_file = tmp_path / "config.py"
    vuln_file.write_text(
        'AWS_ACCESS_KEY = "AKIA1111111111111111"\nDB_PASSWORD = "secret_token_1234567890"\n',
        encoding="utf-8",
    )

    findings = GitleaksScanner.scan_file(vuln_file, "config.py")
    assert len(findings) >= 1
    aws_finding = next((f for f in findings if "AWS" in f.title), None)
    assert aws_finding is not None
    assert aws_finding.cwe_id == "CWE-798"
    assert aws_finding.severity == "CRITICAL"


def test_osv_vulnerable_dependency_detection(tmp_path: Path):
    """Verify OSV scanner detects vulnerable versions in requirements.txt."""
    req_file = tmp_path / "requirements.txt"
    req_file.write_text("requests==2.20.0\npytest==8.0.0\n", encoding="utf-8")

    findings = OsvDependencyScanner.scan_manifest(req_file, "requirements.txt")
    assert len(findings) == 1
    req_finding = findings[0]
    assert "requests@2.20.0" in req_finding.title
    assert req_finding.scanner == "osv_scanner"
    assert req_finding.cwe_id == "CWE-200"


def test_unified_workspace_scanner(tmp_path: Path):
    """Verify orchestrator discovers secrets and dependency flaws simultaneously."""
    (tmp_path / "app").mkdir()
    (tmp_path / "app" / "credentials.json").write_text('{"api_key": "secret_key_1234567890abcdef"}', encoding="utf-8")
    (tmp_path / "package.json").write_text('{"dependencies": {"lodash": "4.17.15"}}', encoding="utf-8")

    findings = UnifiedScannerOrchestrator.scan_workspace(tmp_path)
    assert len(findings) >= 2
    scanners = {f.scanner for f in findings}
    assert "gitleaks" in scanners
    assert "osv_scanner" in scanners

