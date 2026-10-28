"""
Secret lookup that works even when Streamlit is started from another folder.

Order: st.secrets -> environment -> project .streamlit/secrets.toml.
"""
import os
import tomllib

import streamlit as st

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_file_cache = {}


def _file_secrets():
    path = os.path.join(PROJECT_ROOT, ".streamlit", "secrets.toml")
    try:
        mtime = os.path.getmtime(path)
        if _file_cache.get("mtime") != mtime:
            with open(path, "rb") as f:
                _file_cache["data"] = tomllib.load(f)
            _file_cache["mtime"] = mtime
        return _file_cache.get("data") or {}
    except Exception:
        return {}


def get_secret(key):
    try:
        value = st.secrets[key]
        if value:
            return value
    except Exception:
        pass
    value = os.environ.get(key)
    if value:
        return value
    return _file_secrets().get(key)
