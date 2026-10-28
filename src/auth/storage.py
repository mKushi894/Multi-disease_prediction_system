"""
Persistence helpers for diagnosis runs and chat messages (Supabase).
All functions no-op when Supabase or user is unavailable.
"""
from datetime import datetime, timezone
import streamlit as st

from src.auth.client import get_supabase


def _user_id():
    user = st.session_state.get("user")
    if user is None:
        return None
    return getattr(user, "id", None) or (user.get("id") if isinstance(user, dict) else None)


def get_profile():
    client = get_supabase()
    uid = _user_id()
    if client is None or uid is None:
        return None
    try:
        res = client.table("profiles").select("*").eq("user_id", uid).limit(1).execute()
        if res.data:
            st.session_state.profile = res.data[0]
            return res.data[0]
    except Exception:
        pass
    return None


def upsert_profile(user=None):
    client = get_supabase()
    uid = _user_id()
    if client is None or uid is None:
        return None
    user = user or st.session_state.get("user")
    meta = getattr(user, "user_metadata", None) or (user.get("user_metadata") if isinstance(user, dict) else {}) or {}
    first = (meta.get("first_name") or "").strip()
    last = (meta.get("last_name") or "").strip()
    if not first and not last:
        return None
    try:
        client.table("profiles").upsert(
            {"user_id": uid, "first_name": first, "last_name": last}
        ).execute()
        st.session_state.profile = {"first_name": first, "last_name": last}
    except Exception:
        pass
    return None


def display_name(user=None):
    user = user or st.session_state.get("user")
    profile = st.session_state.get("profile") or {}
    first = (profile.get("first_name") or "").strip()
    last = (profile.get("last_name") or "").strip()
    if not first:
        meta = getattr(user, "user_metadata", None) or (user.get("user_metadata") if isinstance(user, dict) else {}) or {}
        first = (meta.get("first_name") or "").strip()
        last = (meta.get("last_name") or "").strip()
    name = f"{first} {last}".strip()
    if name:
        return name
    return getattr(user, "email", None) or (user.get("email") if isinstance(user, dict) else "User")


def _to_json_compatible(val):
    """
    Recursively converts NumPy and Pandas objects to native JSON-serializable Python types.
    """
    if isinstance(val, dict):
        return {str(k): _to_json_compatible(v) for k, v in val.items()}
    if isinstance(val, (list, tuple, set)):
        return [_to_json_compatible(x) for x in val]
    try:
        import numpy as np
        if isinstance(val, np.ndarray):
            return [_to_json_compatible(x) for x in val.tolist()]
        if isinstance(val, (np.generic,)):
            return val.item()
    except Exception:
        pass
    if hasattr(val, "tolist") and callable(val.tolist):
        return [_to_json_compatible(x) for x in val.tolist()]
    if hasattr(val, "item") and callable(val.item) and not hasattr(val, "__len__"):
        try:
            return val.item()
        except Exception:
            pass
    return val


def save_diagnosis_run(disease, inputs, result):
    clean_inputs = _to_json_compatible(inputs)
    clean_result = _to_json_compatible(result)
    local_runs = st.session_state.setdefault("local_runs", [])
    now_iso = datetime.now(timezone.utc).isoformat()
    run_obj = {
        "id": f"local_{len(local_runs)+1}_{int(datetime.now().timestamp())}",
        "disease": disease,
        "inputs": clean_inputs,
        "result": clean_result,
        "created_at": now_iso,
    }
    local_runs.insert(0, run_obj)

    client = get_supabase()
    uid = _user_id()
    if client is None or uid is None:
        return True
    try:
        res = client.table("diagnosis_runs").insert(
            {"user_id": uid, "disease": disease, "inputs": clean_inputs, "result": clean_result}
        ).execute()
        if res.data and len(res.data) > 0:
            run_obj["id"] = res.data[0].get("id")
        return True
    except Exception as e:
        st.warning(f"Could not save diagnosis history: {e}")
    return True


def get_last_inputs(disease):
    client = get_supabase()
    uid = _user_id()
    if client is None or uid is None:
        for r in st.session_state.get("local_runs", []):
            if r.get("disease") == disease:
                return r.get("inputs")
        return None
    try:
        res = (
            client.table("diagnosis_runs")
            .select("inputs")
            .eq("user_id", uid)
            .eq("disease", disease)
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )
        if res.data:
            return res.data[0].get("inputs")
    except Exception:
        for r in st.session_state.get("local_runs", []):
            if r.get("disease") == disease:
                return r.get("inputs")
        return None
    return None


def list_runs(limit=50):
    client = get_supabase()
    uid = _user_id()
    if client is None or uid is None:
        return st.session_state.get("local_runs", [])[:limit]
    try:
        res = (
            client.table("diagnosis_runs")
            .select("*")
            .eq("user_id", uid)
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )
        runs = res.data or []
        local = st.session_state.get("local_runs", [])
        if local and not runs:
            return local[:limit]
        return runs
    except Exception:
        return st.session_state.get("local_runs", [])[:limit]


def delete_run(run_id):
    """Delete a single diagnosis run by ID from Supabase and local session state."""
    success = False
    run_id_str = str(run_id)

    # 1. Remove from local session state
    if "local_runs" in st.session_state:
        before = len(st.session_state["local_runs"])
        st.session_state["local_runs"] = [
            r for r in st.session_state["local_runs"]
            if str(r.get("id")) != run_id_str and str(r.get("created_at")) != run_id_str
        ]
        if len(st.session_state["local_runs"]) < before:
            success = True

    # 2. Delete from Supabase if connected
    client = get_supabase()
    uid = _user_id()
    if client is not None and uid is not None and not run_id_str.startswith("local_"):
        try:
            client.table("diagnosis_runs").delete().eq("id", run_id).eq("user_id", uid).execute()
            success = True
        except Exception:
            pass
    return success


def clear_all_runs():
    """Clear all saved diagnosis runs for the active user."""
    st.session_state["local_runs"] = []

    client = get_supabase()
    uid = _user_id()
    if client is not None and uid is not None:
        try:
            client.table("diagnosis_runs").delete().eq("user_id", uid).execute()
            return True
        except Exception:
            return False
    return True


def save_feedback(rating, comments):
    client = get_supabase()
    uid = _user_id()
    if client is None or uid is None:
        return False
    try:
        client.table("feedback").insert(
            {"user_id": uid, "rating": rating, "comments": comments}
        ).execute()
        return True
    except Exception:
        return False


def save_chat_message(role, content):
    client = get_supabase()
    uid = _user_id()
    if client is None or uid is None:
        return None
    try:
        client.table("chat_messages").insert(
            {"user_id": uid, "role": role, "content": content}
        ).execute()
    except Exception:
        pass
    return None
