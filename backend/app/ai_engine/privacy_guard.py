"""SAFECODIUM — Privacy Guard & Authorization Engine.

Enforces privacy modes: local_only, cloud_only, and hybrid.
Prevents unauthorized transmission of source code to external cloud LLMs.
"""

from enum import Enum
from typing import Optional
from fastapi import HTTPException
from pydantic import BaseModel


class PrivacyMode(str, Enum):
    LOCAL_ONLY = "local_only"
    CLOUD_ONLY = "cloud_only"
    HYBRID = "hybrid"


class PrivacyAuthorizationError(Exception):
    """Raised when a cloud AI operation violates user privacy configuration."""
    pass


class PrivacyPolicyManager:
    """Manages workspace privacy constraints and external transmission policies."""

    def __init__(self, mode: PrivacyMode = PrivacyMode.HYBRID):
        self._mode = mode
        self._cloud_transmission_authorized = False

    @property
    def mode(self) -> PrivacyMode:
        return self._mode

    def set_mode(self, mode: PrivacyMode, user_authorized_cloud: bool = False):
        """Update current privacy mode and cloud authorization flag."""
        self._mode = mode
        self._cloud_transmission_authorized = user_authorized_cloud

    def assert_provider_permitted(self, provider_name: str, has_explicit_consent: bool = False):
        """Verify whether the selected AI provider complies with current privacy policy."""
        clean_provider = provider_name.lower().strip()
        is_cloud = clean_provider in ("gemini", "openai", "claude")

        if self._mode == PrivacyMode.LOCAL_ONLY and is_cloud:
            raise PrivacyAuthorizationError(
                f"Privacy Violation: Provider '{provider_name}' is a cloud AI service. "
                f"Workspace is in 'LOCAL_ONLY' privacy mode. Code transmission blocked."
            )

        if is_cloud and not (self._cloud_transmission_authorized or has_explicit_consent):
            # In hybrid mode, cloud requires explicit authorization
            if self._mode == PrivacyMode.HYBRID:
                raise PrivacyAuthorizationError(
                    f"Privacy Guard: Cloud provider '{provider_name}' requires explicit user authorization "
                    f"before transmitting source code files."
                )


# Global privacy manager instance
privacy_manager = PrivacyPolicyManager(mode=PrivacyMode.HYBRID)

