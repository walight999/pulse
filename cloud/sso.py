"""Enterprise SSO — SAML 2.0 + OIDC stubs.

Pulse Enterprise tier supports SAML 2.0 via Supabase Auth's enterprise plan,
or roll-your-own OIDC for self-hosted deployments.

Configuration per organization:
- saml_metadata_url        # IdP metadata XML URL
- saml_signing_cert         # PEM cert
- oidc_issuer / client_id / client_secret
- default_role              # 'member' | 'viewer' when JIT provisioning
- domain_allowlist          # email domains that auto-join

When fully implemented this module calls Supabase's `/auth/v1/sso/saml/...`
endpoints. For now it's a scaffold + admin UI helpers.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class SSOConfig:
    org_id: str
    protocol: str           # 'saml' | 'oidc'
    metadata_url: Optional[str]
    domain_allowlist: list[str]
    default_role: str       # 'member' | 'viewer'
    jit_provisioning: bool


def upsert_sso_config(config: SSOConfig) -> dict:
    """Admin call to set up SSO for an organization."""
    raise NotImplementedError(
        "SSO requires Supabase Pro plan or Auth0/Okta. "
        "Use admin dashboard or call /auth/v1/admin/sso/providers directly."
    )


def initiate_sso_login(domain: str) -> str:
    """Returns the redirect URL the user goes to authenticate."""
    raise NotImplementedError("Phase C — implement when first enterprise customer signs")


def handle_sso_callback(saml_response: bytes) -> dict:
    raise NotImplementedError("Phase C")
