"""
auth.py
Supabase Auth (email + password) — signup, login, logout.

Uses the ANON key (safe for client-side use), NOT the service_role key that
api/tracker.py uses to write to the `users` tracking table. These are two
separate concerns:
  - Supabase Auth  -> real accounts, passwords, sessions (this file)
  - `users` table  -> LeetCode stats logging, keyed by LeetCode username


"""

import os
from typing import Optional


def _client():
    url = os.getenv("SUPABASE_URL", "").strip()
    key = os.getenv("SUPABASE_ANON_KEY", "").strip()
    if not url or not key:
        return None
    from supabase import create_client
    return create_client(url, key)


def sign_up(email: str, password: str) -> tuple[bool, str, Optional[dict]]:
    """Create a new account. Returns (success, message, user_dict)."""
    client = _client()
    if client is None:
        return False, "Auth isn't configured — set SUPABASE_URL and SUPABASE_ANON_KEY in .env.", None
    try:
        res = client.auth.sign_up({
            "email": email,
            "password": password
        })
        if res.user is None:
            return False, "Sign up failed — please try again.", None

        # Supabase requires email confirmation by default. If confirmations are
        # on, res.session is None until the user clicks the emailed link.
        if res.session is None:
            return True, "Account created! Check your email to confirm before logging in.", None

        return True, "Account created!", {
            "id": res.user.id,
            "email": res.user.email,
            "access_token": res.session.access_token,
            "refresh_token": res.session.refresh_token,
        }
    except Exception as e:
        return False, _friendly_error(str(e)), None


def sign_in(email: str, password: str) -> tuple[bool, str, Optional[dict]]:
    """Log in an existing account. Returns (success, message, user_dict)."""
    client = _client()
    if client is None:
        return False, "Auth isn't configured — set SUPABASE_URL and SUPABASE_ANON_KEY in .env.", None
    try:
        res = client.auth.sign_in_with_password({"email": email, "password": password})
        if res.user is None or res.session is None:
            return False, "Invalid email or password.", None
        return True, "Welcome back!", {
            "id": res.user.id,
            "email": res.user.email,
            "username": res.user.user_metadata.get("username") if res.user.user_metadata else None,
            "access_token": res.session.access_token,
            "refresh_token": res.session.refresh_token,
        }
    except Exception as e:
        return False, _friendly_error(str(e)), None


def sign_out(access_token: Optional[str] = None) -> None:
    client = _client()
    if client is None:
        return
    try:
        client.auth.sign_out()
    except Exception:
        pass


def _friendly_error(raw: str) -> str:
    r = raw.lower()
    if "already registered" in r or "already exists" in r or "user already" in r:
        return "An account with that email already exists — try logging in instead."
    if "invalid login credentials" in r:
        return "Invalid email or password."
    if "password should be at least" in r or "password is too short" in r:
        return "Password must be at least 6 characters."
    if "unable to validate email" in r or ("email" in r and "invalid" in r):
        return "That doesn't look like a valid email address."
    if "rate limit" in r:
        return "Too many attempts — please wait a moment and try again."
    return f"Something went wrong: {raw}"