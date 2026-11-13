"""Tests for Universal Language Adapters & Capabilities."""

import pytest
from backend.app.services.language_adapters.registry import language_registry
from backend.app.services.language_adapters.base import DiagnosticFinding


def test_registered_language_adapters():
    """Verify all 6 core language adapters are loaded with explicit capability models."""
    caps = language_registry.list_capabilities()
    assert len(caps) >= 6

    ids = [c.language_id for c in caps]
    assert "c_cpp" in ids
    assert "python" in ids
    assert "javascript_typescript" in ids
    assert "java" in ids
    assert "go" in ids
    assert "rust" in ids


def test_python_ast_diagnostics():
    """Verify Python adapter detects arbitrary eval execution."""
    adapter = language_registry.get_adapter("python")
    assert adapter is not None

    vulnerable_code = """
import os

def run_command(payload):
    result = eval(payload)
    return result
"""
    diagnostics = adapter.get_diagnostics("handler.py", vulnerable_code)
    assert len(diagnostics) > 0
    eval_diag = next((d for d in diagnostics if d.cwe_id == "CWE-95"), None)
    assert eval_diag is not None
    assert eval_diag.line == 5


def test_c_cpp_ast_diagnostics():
    """Verify C/C++ adapter flags legacy buffer copy functions."""
    adapter = language_registry.get_adapter("c_cpp")
    assert adapter is not None

    vulnerable_code = """
#include <stdio.h>
#include <string.h>

void process_buffer(char *input) {
    char dest[32];
    strcpy(dest, input);
}
"""
    diagnostics = adapter.get_diagnostics("firmware.c", vulnerable_code)
    assert len(diagnostics) > 0
    cwe120 = next((d for d in diagnostics if d.cwe_id == "CWE-120"), None)
    assert cwe120 is not None


def test_extension_matching():
    """Verify adapter discovery by file extension."""
    c_adapter = language_registry.find_adapter_by_file("sensor.c")
    assert c_adapter is not None
    assert c_adapter.language_id == "c_cpp"

    ts_adapter = language_registry.find_adapter_by_file("Component.tsx")
    assert ts_adapter is not None
    assert ts_adapter.language_id == "javascript_typescript"

    rust_adapter = language_registry.find_adapter_by_file("main.rs")
    assert rust_adapter is not None
    assert rust_adapter.language_id == "rust"

