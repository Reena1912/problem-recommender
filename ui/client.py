import streamlit as st
import requests
import os

API_BASE = os.getenv("API_BASE", "http://127.0.0.1:8000")

def api(ep: str, method="GET") -> dict | None:
    """Make requests to the backend FastAPI server."""
    try:
        url = f"{API_BASE}{ep}"
        r = requests.post(url, timeout=120) if method == "POST" else requests.get(url, timeout=35)
        if r.status_code == 200:
            return r.json()
        try:
            detail = r.json().get("detail", r.text)
        except Exception:
            detail = r.text or f"HTTP {r.status_code}"
        st.warning(f"⚠️ {detail}")
        return None
    except requests.exceptions.ConnectionError:
        st.error("❌ API not reachable. Check that the API service is running and API_BASE is set correctly.")
        return None
    except requests.exceptions.Timeout:
        st.error("⏱ Request timed out — the API may still be warming up (first load takes ~40 s). Refresh in a moment.")
        return None
    except Exception as e:
        st.error(f"❌ Unexpected error: {e}")
        return None
