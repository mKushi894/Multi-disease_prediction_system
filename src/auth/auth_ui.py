"""
Streamlit authentication UI (Supabase email/password). Degrades gracefully
when Supabase is not configured.
"""
import streamlit as st

from src.auth.client import get_supabase, reset_supabase
from src.auth.storage import upsert_profile


def _set_session(client, auth_response):
    session = getattr(auth_response, "session", None)
    user = getattr(auth_response, "user", None)
    if user is None and isinstance(auth_response, dict):
        user = auth_response.get("user")
        session = auth_response.get("session")
    if user is not None:
        st.session_state.user = user
    if session is not None:
        access = getattr(session, "access_token", None)
        refresh = getattr(session, "refresh_token", None)
        try:
            client.auth.set_session(access, refresh)
        except Exception:
            pass
        if access and refresh:
            st.session_state["auth_tokens"] = (access, refresh)
            st.session_state["_auth_tokens_applied"] = True
        st.session_state.access_token = access


def render_auth(client):
    st.markdown(
        """
        <div class="auth-wrap">
            <div class="auth-mark">🩺</div>
            <h1 class="auth-title">Welcome back</h1>
            <p class="auth-sub">Sign in to save screenings, resume where you left off, and keep your health history in one place.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    tab_login, tab_signup = st.tabs(["Log in", "Create account"])

    with tab_login:
        email = st.text_input("Email", key="login_email", placeholder="you@example.com")
        password = st.text_input("Password", type="password", key="login_password", placeholder="••••••••")
        if st.button("Log in", key="login_btn", type="primary", width="stretch"):
            try:
                resp = client.auth.sign_in_with_password({"email": email, "password": password})
                _set_session(client, resp)
                if st.session_state.get("user") is None:
                    st.warning("Check your email to confirm your account, then log in again.")
                else:
                    upsert_profile(st.session_state.get("user"))
                    st.rerun()
            except Exception as e:
                msg = str(e)
                if "not confirmed" in msg.lower() or "email not confirmed" in msg.lower():
                    st.warning("Email not confirmed. Open the confirmation email, or disable 'Confirm email' in Supabase → Authentication → Providers → Email.")
                elif "nodename nor servname" in msg.lower() or "getaddrinfo" in msg.lower():
                    st.error("Supabase URL is invalid or unreachable. Copy the Project URL from Supabase → Project Settings → API Keys.")
                else:
                    st.error(f"Login failed: {msg}")

    with tab_signup:
        c1, c2 = st.columns(2)
        with c1:
            first_name = st.text_input("First name", key="signup_first_name", placeholder="Asha")
        with c2:
            last_name = st.text_input("Last name", key="signup_last_name", placeholder="Rao")
        email = st.text_input("Email", key="signup_email", placeholder="you@example.com")
        password = st.text_input("Password", type="password", key="signup_password", placeholder="At least 6 characters")
        if st.button("Create account", key="signup_btn", type="primary", width="stretch"):
            if not first_name.strip():
                st.warning("Please enter your first name so we can personalise your dashboard.")
            else:
                try:
                    resp = client.auth.sign_up({
                        "email": email,
                        "password": password,
                        "options": {"data": {"first_name": first_name.strip(), "last_name": last_name.strip()}},
                    })
                    _set_session(client, resp)
                    if st.session_state.get("user") is None:
                        st.success("Account created. Check your email to confirm it, then log in.")
                    else:
                        upsert_profile(st.session_state.get("user"))
                        st.rerun()
                except Exception as e:
                    msg = str(e)
                    if "nodename nor servname" in msg.lower() or "getaddrinfo" in msg.lower():
                        st.error("Supabase URL is invalid or unreachable. Copy the Project URL from Supabase → Project Settings → API Keys.")
                    else:
                        st.error(f"Sign up failed: {msg}")

    st.caption("Your inputs are private to your account and protected by row-level security.")


def require_login():
    client = get_supabase()
    if client is None:
        # Backend not configured: run anonymously.
        st.session_state.setdefault("user", None)
        return
    if st.session_state.get("user") is None:
        render_auth(client)
        st.stop()
    if st.session_state.get("profile") is None:
        from src.auth.storage import get_profile

        if get_profile() is None:
            upsert_profile(st.session_state.get("user"))


def current_user():
    return st.session_state.get("user")


def logout():
    client = get_supabase()
    if client is not None:
        try:
            client.auth.sign_out()
        except Exception:
            pass
    for key in (
        "user", "access_token", "profile", "chat_history", "last_prediction",
        "copilot_history", "copilot_open",
        "auth_tokens", "_supabase_client", "_auth_tokens_applied",
        "heart_data", "kidney_data", "liver_data", "lung_data", "bc_data",
    ):
        st.session_state.pop(key, None)
    reset_supabase()
    st.rerun()
