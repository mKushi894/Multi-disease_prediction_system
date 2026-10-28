"""
Supabase client factory. One client per Streamlit session so the signed-in
token survives across reruns. Returns None when credentials are missing, so
the app keeps working (without auth/history) in unconfigured deploys.
"""
import streamlit as st

from src.utils.settings import get_secret


def get_supabase():
    url = get_secret("SUPABASE_URL")
    key = get_secret("SUPABASE_ANON_KEY")
    if not url or not key:
        return None

    client = st.session_state.get("_supabase_client")
    if client is None:
        try:
            from supabase import create_client

            client = create_client(url, key)
            st.session_state["_supabase_client"] = client
        except Exception:
            return None

    tokens = st.session_state.get("auth_tokens")
    if tokens and not st.session_state.get("_auth_tokens_applied"):
        try:
            client.auth.set_session(tokens[0], tokens[1])
            st.session_state["_auth_tokens_applied"] = True
        except Exception:
            pass
    return client


def reset_supabase():
    st.session_state.pop("_supabase_client", None)
    st.session_state.pop("_auth_tokens_applied", None)


def is_configured():
    return bool(get_secret("SUPABASE_URL") and get_secret("SUPABASE_ANON_KEY"))
