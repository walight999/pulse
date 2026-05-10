"""Stripe billing — Phase 1 stub.

Server-side helpers (run in your backend / edge function).
The desktop client just opens Stripe Checkout in a browser and polls for plan flip.
"""
from __future__ import annotations


# Stripe product/price IDs — set after creating in Stripe Dashboard
PRICE_PRO_MONTHLY  = "price_..."  # $9.00/mo
PRICE_PRO_ANNUAL   = "price_..."  # $89.00/yr
PRICE_PRO_LIFETIME = "price_..."  # $199 one-time
PRICE_TEAM_SEAT    = "price_..."  # $19.00/seat/mo


def create_checkout_session(account_id: str, price_id: str,
                             success_url: str, cancel_url: str) -> str:
    """Returns a Stripe Checkout URL to redirect the user to."""
    raise NotImplementedError("Phase 1 — `stripe.checkout.Session.create(...)`")


def handle_webhook(payload: bytes, signature: str, secret: str) -> dict:
    """Process incoming Stripe webhook. Returns parsed event for the caller
    to apply to the DB (set plan, extend pro_until, downgrade on cancel)."""
    raise NotImplementedError("Phase 1 — `stripe.Webhook.construct_event(...)`")


def cancel_subscription(stripe_subscription_id: str) -> None:
    raise NotImplementedError("Phase 1 — `stripe.Subscription.delete(...)`")


# Webhook events to wire up in your handler:
WEBHOOK_EVENTS_TO_HANDLE = [
    "checkout.session.completed",
    "customer.subscription.created",
    "customer.subscription.updated",
    "customer.subscription.deleted",
    "invoice.payment_succeeded",
    "invoice.payment_failed",
    "customer.deleted",
]
