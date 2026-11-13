"""SAFECODIUM — Language Adapters API endpoints."""

from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from backend.app.services.language_adapters.registry import language_registry
from backend.app.services.language_adapters.base import LanguageCapabilities, DiagnosticFinding

router = APIRouter(prefix="/languages", tags=["Languages"])


class ParseCodeRequest(BaseModel):
    filename: str
    code: str


@router.get("/capabilities", response_model=Dict[str, Any])
async def get_language_capabilities():
    """Retrieve capability matrix for all supported programming languages."""
    caps = language_registry.list_capabilities()
    return {
        "status": "success",
        "total_languages": len(caps),
        "data": [c.model_dump() for c in caps],
    }


@router.post("/diagnostics", response_model=Dict[str, Any])
async def get_file_diagnostics(payload: ParseCodeRequest):
    """Run language-specific parser and static diagnostics on provided code snippet."""
    adapter = language_registry.find_adapter_by_file(payload.filename)
    if not adapter:
        return {
            "status": "unsupported_language",
            "message": f"No dedicated language adapter registered for '{payload.filename}'.",
            "diagnostics": [],
        }

    syntax_data = adapter.parse_syntax(payload.code, payload.filename)
    diagnostics = adapter.get_diagnostics(payload.filename, payload.code)

    return {
        "status": "success",
        "language_id": adapter.language_id,
        "syntax": syntax_data,
        "diagnostics": [d.model_dump() for d in diagnostics],
    }

