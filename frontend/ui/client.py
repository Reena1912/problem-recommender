import streamlit as st
import requests
import os

DEFAULT_BASES = [
    os.getenv("API_BASE", "http://127.0.0.1:8000"),
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]

def _fetch_api(ep: str, method: str = "GET") -> dict | None:
    """Internal function to make requests to the backend FastAPI server with host fallbacks."""
    bases = []
    for b in DEFAULT_BASES:
        if b and b.rstrip("/") not in bases:
            bases.append(b.rstrip("/"))
            
    last_err = None
    for base in bases:
        try:
            url = f"{base}{ep}"
            r = requests.post(url, timeout=120) if method == "POST" else requests.get(url, timeout=35)
            if r.status_code == 200:
                return r.json()
            try:
                detail = r.json().get("detail", r.text)
            except Exception:
                detail = r.text or f"HTTP {r.status_code}"
            st.warning(f"⚠️ {detail}")
            return None
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            last_err = e
            continue
        except Exception as e:
            st.error(f"❌ Unexpected error: {e}")
            return None

    if isinstance(last_err, requests.exceptions.Timeout):
        st.error("⏱ Request timed out — the API may still be warming up (first load takes ~20 s). Refresh in a moment.")
    else:
        st.error("❌ API not reachable on port 8000. Ensure the FastAPI backend server is running.")
    return None

@st.cache_data(ttl=300, show_spinner=False)
def api(ep: str, method: str = "GET") -> dict | None:
    """Make fast cached requests to the backend FastAPI server."""
    return _fetch_api(ep, method=method)
