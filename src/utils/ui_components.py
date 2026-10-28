"""
Shared UI helpers: design system, page headers, disclaimers, and result cards.
"""
import json
import os
from typing import Any, Dict

import streamlit as st

BASE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@500;600;700;800&display=swap');

:root {
    --ink: #0b1220;
    --muted: #5b6779;
    --line: #e4e9f2;
    --brand: #0ea5e9;
    --brand-2: #6366f1;
    --ok: #10b981;
    --warn: #f59e0b;
    --bad: #f43f5e;
}

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}
h1, h2, h3, h4, h5 {
    font-family: 'Outfit', sans-serif;
    letter-spacing: -0.01em;
    color: var(--ink);
}
.stApp {
    background:
        radial-gradient(1100px 520px at 8% -12%, #e0f2fe 0%, transparent 55%),
        radial-gradient(900px 480px at 100% -5%, #ede9fe 0%, transparent 50%),
        #f5f7fb;
}
[data-testid="stHeader"] { background: transparent; height: 0; min-height: 0; overflow: hidden; }
#MainMenu, .stAppDeployButton, [data-testid="stStatusWidget"] { display: none; }
[data-testid="stMainBlockContainer"] {
    padding-top: .6rem;
    padding-bottom: 2rem;
    max-width: 1180px;
}
body:has(.auth-wrap) [data-testid="stMainBlockContainer"] { max-width: 560px; padding-top: 7vh; }

/* ---------- auth ---------- */
body:has(.auth-wrap) .block-container { max-width: 560px; padding-top: 7vh; }
.auth-wrap { text-align: center; margin-bottom: 18px; }
.auth-mark {
    width: 56px; height: 56px; margin: 0 auto 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 26px; border-radius: 8px;
    background: linear-gradient(135deg, #0ea5e9, #6366f1);
    box-shadow: 0 10px 25px -10px rgba(79, 70, 229, .6);
}
.auth-title { font-size: 1.85rem; margin: 0 0 6px; }
.auth-sub { color: var(--muted); font-size: .95rem; line-height: 1.55; max-width: 420px; margin: 0 auto; }

/* ---------- sidebar ---------- */
[data-testid="stSidebar"] { background: #ffffff; border-right: 1px solid var(--line); width: 260px !important; min-width: 260px !important; max-width: 260px !important; }
[data-testid="stSidebarUserContent"] { padding: 0.4rem 0.9rem 1.4rem; }
[data-testid="stSidebarHeader"] { padding-bottom: 0; min-height: 0; }
[data-testid="stSidebar"] .block-container { padding-top: 0; }
[data-testid="stSidebar"] hr { margin: 0.9rem 0; border-color: var(--line); }
.brand { display: flex; align-items: center; gap: 10px; padding: 0 2px 10px; }
.brand-mark {
    width: 38px; height: 38px; border-radius: 6px; flex: none;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px; background: linear-gradient(135deg, #0ea5e9, #6366f1);
    box-shadow: 0 6px 16px -8px rgba(14, 165, 233, .6);
}
.brand-name { font-family: 'Outfit', sans-serif; font-weight: 700; font-size: 1.05rem; color: var(--ink); line-height: 1.1; }
.brand-sub { font-size: .68rem; color: #7c8aa0; letter-spacing: .09em; text-transform: uppercase; margin-top: 2px; }
.user-chip {
    display: flex; align-items: center; gap: 8px;
    background: #f8fafc; border: 1px solid var(--line); border-radius: 6px;
    padding: 6px 8px; margin: 0 0 8px;
}
.avatar {
    width: 32px; height: 32px; border-radius: 50%; flex: none;
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; color: #fff;
    background: linear-gradient(135deg, #0ea5e9, #6366f1);
}
.user-name { font-weight: 600; font-size: .88rem; color: var(--ink); line-height: 1.25; }
.user-state { font-size: .7rem; color: var(--ok); }
.nav-group {
    font-size: .62rem; letter-spacing: .14em; text-transform: uppercase;
    color: #94a3b8; font-weight: 700; margin: .6rem 0 .2rem;
}
[data-testid="stSidebar"] [data-testid="stPageLink"] a,
[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"] {
    padding: .32rem .5rem; border-radius: 6px; color: #334155;
    font-size: .84rem; font-weight: 500; transition: background .15s ease;
}
[data-testid="stSidebar"] [data-testid="stPageLink"] a:hover,
[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"]:hover { background: #f1f5f9; }
[data-testid="stSidebar"] [data-testid="stPageLink"] a[aria-current="page"],
[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"][aria-current="page"] {
    background: #e0f2fe;
    color: #0369a1; font-weight: 600;
}
.status-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; margin-right: 6px; }
.status-dot.on { background: var(--ok); box-shadow: 0 0 0 3px rgba(16, 185, 129, .15); }
.status-dot.off { background: var(--warn); box-shadow: 0 0 0 3px rgba(245, 158, 11, .15); }

/* ---------- top header bar ---------- */
.header-brand {
    font-family: 'Outfit', sans-serif; font-weight: 700; font-size: 1.05rem;
    color: var(--ink); padding: .45rem 0; letter-spacing: -0.01em;
}
.header-rule { height: 1px; background: var(--line); margin: 0 0 .4rem; border: none; }
[data-testid="stMainBlockContainer"] [data-testid="stVerticalBlock"] { gap: .5rem; }
.header-left-spacer { height: 0; }
[data-testid="stHeader"] { background: transparent; }

/* ---------- empty state ---------- */
.empty-state { text-align: center; padding: 2.2rem 1rem; border: 1px dashed var(--line); border-radius: 8px; background: #fafbfe; margin: 1rem 0; }
.empty-icon { font-size: 2.2rem; margin-bottom: 8px; }
.empty-title { font-family: 'Outfit', sans-serif; font-weight: 700; font-size: 1.15rem; color: var(--ink); margin-bottom: 4px; }
.empty-sub { color: var(--muted); font-size: .9rem; max-width: 480px; margin: 0 auto; line-height: 1.5; }

/* ---------- page header ---------- */
.page-head { display: flex; align-items: center; gap: 10px; margin: 0 0 8px; }
.page-head-icon {
    width: 34px; height: 34px; border-radius: 6px; flex: none;
    display: flex; align-items: center; justify-content: center; font-size: 18px;
    background: #fff; border: 1px solid var(--line);
    box-shadow: 0 6px 12px -8px rgba(15, 23, 42, .18);
}
.page-head h1 { font-size: 1.35rem; margin: 0 0 1px; line-height: 1.2; }
.page-head p { color: var(--muted); font-size: .85rem; margin: 0; max-width: 760px; line-height: 1.45; }

/* ---------- hero ---------- */
.app-hero {
    position: relative; overflow: hidden; margin-bottom: 20px;
    border: 1px solid var(--line); border-radius: 8px;
    background: #ffffff;
    padding: 30px 34px;
    box-shadow: 0 10px 25px -15px rgba(15, 23, 42, .12);
}
.hero-eyebrow {
    display: inline-flex; align-items: center; gap: 6px;
    font-size: .72rem; font-weight: 700; letter-spacing: .1em; text-transform: uppercase;
    color: #0369a1; background: #f0f9ff; border: 1px solid #bae6fd;
    padding: 4px 10px; border-radius: 4px; margin-bottom: 12px;
}
.hero-title {
    font-family: 'Outfit', sans-serif; font-size: 2.1rem; line-height: 1.15;
    font-weight: 700; color: var(--ink); max-width: 680px; margin: 0 0 10px;
}
.hero-sub { color: #526075; font-size: .98rem; max-width: 640px; line-height: 1.55; margin: 0 0 16px; }
.hero-tags { display: flex; flex-wrap: wrap; gap: 8px; }
.hero-tag {
    font-size: .75rem; color: #334155; background: #f8fafc; border: 1px solid var(--line);
    border-radius: 4px; padding: 4px 10px; font-weight: 500;
}

/* ---------- stats ---------- */
.stat-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 12px; margin: 4px 0 22px; }
.stat-tile { background: #fff; border: 1px solid var(--line); border-radius: 8px; padding: 14px 16px; box-shadow: 0 4px 12px -6px rgba(15, 23, 42, .08); }
.stat-kicker { font-size: .66rem; letter-spacing: .08em; text-transform: uppercase; color: #94a3b8; font-weight: 700; }
.stat-value { font-family: 'Outfit', sans-serif; font-size: 1.45rem; font-weight: 700; color: var(--ink); margin-top: 3px; }
.stat-hint { font-size: .75rem; color: var(--muted); margin-top: 2px; }

/* ---------- module cards ---------- */
[data-testid="stVerticalBlockBorderWrapper"] { border-radius: 8px; }
[data-testid="stVerticalBlockBorderWrapper"] > div { border-radius: 8px; }
.module-top { display: flex; align-items: center; gap: 12px; }
.module-icon {
    width: 44px; height: 44px; border-radius: 6px; flex: none;
    display: flex; align-items: center; justify-content: center; font-size: 22px;
    border: 1px solid transparent;
}
.module-icon.heart { background: #fff1f2; border-color: #fecdd3; }
.module-icon.kidney { background: #fffbeb; border-color: #fde68a; }
.module-icon.liver { background: #ecfdf5; border-color: #a7f3d0; }
.module-icon.lung { background: #f0f9ff; border-color: #bae6fd; }
.module-icon.breast { background: #f5f3ff; border-color: #ddd6fe; }
.module-title { font-family: 'Outfit', sans-serif; font-size: 1.05rem; font-weight: 700; color: var(--ink); margin: 0; }
.module-desc { font-size: .85rem; color: var(--muted); line-height: 1.5; margin: 10px 0 12px; min-height: 52px; }
.pill {
    display: inline-block; padding: 3px 8px; border-radius: 4px;
    font-size: .7rem; font-weight: 600; margin-right: 6px;
}
.pill.model { background: #eef2ff; color: #4338ca; }
.pill.acc { background: #ecfdf5; color: #047857; }
.card-link { font-size: .85rem; font-weight: 600; color: #0284c7; }

/* ---------- workflow / team ---------- */
.section-head { margin: 8px 0 12px; }
.section-head h3 { font-size: 1.25rem; margin: 0; }
.section-head p { color: var(--muted); font-size: .85rem; margin: 2px 0 0; }
.steps { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; margin-bottom: 10px; }
.step { background: #fff; border: 1px solid var(--line); border-radius: 8px; padding: 16px; }
.step-num {
    width: 26px; height: 26px; border-radius: 6px; margin-bottom: 8px;
    display: flex; align-items: center; justify-content: center;
    background: #eef2ff; color: #4338ca; font-weight: 700; font-size: .8rem;
}
.step-title { font-weight: 700; color: var(--ink); font-size: .9rem; margin-bottom: 4px; }
.step-desc { font-size: .78rem; color: var(--muted); line-height: 1.5; }
.team-panel {
    display: grid; grid-template-columns: 1fr 1.5fr; gap: 20px;
    background: #fff; border: 1px solid var(--line); border-radius: 8px;
    padding: 18px 20px; margin-top: 8px;
}
.team-label { font-size: .66rem; letter-spacing: .08em; text-transform: uppercase; color: #94a3b8; font-weight: 700; margin-bottom: 4px; }
.team-name { font-weight: 600; color: var(--ink); font-size: .92rem; }
.team-list { color: #475569; font-size: .84rem; line-height: 1.7; }

/* ---------- results & console placeholder ---------- */
.result-hero {
    display: flex; align-items: center; gap: 20px;
    border: 1px solid; border-radius: 8px; padding: 22px 24px; margin: 12px 0;
}
.result-hero.positive { background: #fff5f5; border-color: #fecdd3; }
.result-hero.negative { background: #f0fdf4; border-color: #bbf7d0; }
.result-copy { flex: 1; }
.risk-chip {
    display: inline-block; font-size: .68rem; font-weight: 700; letter-spacing: .08em;
    text-transform: uppercase; padding: 4px 8px; border-radius: 4px; margin-bottom: 8px;
}
.result-hero.positive .risk-chip { background: #ffe4e6; color: #be123c; }
.result-hero.negative .risk-chip { background: #d1fae5; color: #047857; }
.result-title { font-size: 1.35rem; font-weight: 700; margin: 0 0 6px; }
.result-hero.positive .result-title { color: #9f1239; }
.result-hero.negative .result-title { color: #065f46; }
.result-text { color: #475569; font-size: .88rem; line-height: 1.5; margin: 0; }
.conf-ring {
    --p: 50; --ring: #0ea5e9;
    width: 96px; height: 96px; border-radius: 50%; flex: none;
    background: conic-gradient(var(--ring) calc(var(--p) * 1%), #e6ebf3 0);
    display: flex; align-items: center; justify-content: center;
}
.conf-ring-inner {
    width: 78px; height: 78px; border-radius: 50%; background: #fff;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
}
.conf-num { font-family: 'Outfit', sans-serif; font-size: 1.25rem; font-weight: 700; color: var(--ink); }
.conf-lbl { font-size: .56rem; letter-spacing: .08em; text-transform: uppercase; color: #94a3b8; font-weight: 600; }
.prob-row { display: flex; justify-content: space-between; font-size: .76rem; color: var(--muted); margin: 8px 0 4px; }
.prob-bar { height: 8px; border-radius: 4px; background: #e6ebf3; overflow: hidden; }
.prob-fill { height: 100%; border-radius: 4px; background: #0284c7; }

/* Cockpit empty state placeholder */
.result-placeholder {
    background: #ffffff;
    border: 1px dashed var(--line);
    border-radius: 8px;
    padding: 34px 24px;
    text-align: center;
    box-shadow: 0 4px 14px -6px rgba(15, 23, 42, .06);
}
.placeholder-icon { font-size: 2.2rem; margin-bottom: 10px; }
.placeholder-title { font-family: 'Outfit', sans-serif; font-size: 1.15rem; font-weight: 700; color: var(--ink); margin-bottom: 6px; }
.placeholder-sub { font-size: .85rem; color: var(--muted); line-height: 1.5; max-width: 340px; margin: 0 auto 18px; }
.placeholder-meta {
    display: grid; grid-template-columns: repeat(3, 1fr);
    border-top: 1px solid var(--line);
    padding-top: 14px; margin-top: 10px;
    font-size: .75rem; color: var(--muted);
}
.placeholder-meta span { display: block; font-size: .66rem; text-transform: uppercase; letter-spacing: .08em; }
.placeholder-meta strong { display: block; color: var(--ink); margin-top: 2px; }

/* ---------- widgets ---------- */
[data-testid="stForm"] {
    background: #fff; border: 1px solid var(--line); border-radius: 8px;
    padding: 20px 22px; box-shadow: 0 6px 18px -8px rgba(15, 23, 42, .08);
}
[data-testid="stBaseButton-primary"], button[kind="primary"] {
    background: #0284c7;
    color: #fff; border: none; border-radius: 6px; font-weight: 600;
    padding: .55rem 1.2rem;
    box-shadow: 0 4px 10px -2px rgba(2, 132, 199, .4);
}
[data-testid="stBaseButton-primary"]:hover, button[kind="primary"]:hover { background: #0369a1; color: #fff; }
[data-testid="stBaseButton-secondary"], button[kind="secondary"] {
    background: #fff; color: #0f172a; border: 1px solid #cbd5e1;
    border-radius: 6px; font-weight: 600; padding: .52rem 1rem;
}
[data-testid="stBaseButton-secondary"]:hover, button[kind="secondary"]:hover {
    border-color: #94a3b8; color: #0369a1; background: #f8fafc;
}
[data-testid="stExpander"] details { border: 1px solid var(--line); border-radius: 8px; background: #fff; overflow: hidden; }
[data-testid="stExpander"] summary { font-weight: 600; color: var(--ink); }
button[data-baseweb="tab"] { font-weight: 600; color: var(--muted); }
button[data-baseweb="tab"][aria-selected="true"] { color: #0369a1; }
[data-baseweb="tab-highlight"] { background: #0284c7; }
[data-baseweb="input"], [data-baseweb="select"] > div, [data-baseweb="textarea"] { border-radius: 6px !important; }
[data-testid="stChatMessage"] { background: #f8fafc; border: 1px solid #eef2f7; border-radius: 8px; }
.main [data-testid="stPageLink-NavLink"] { color: #0284c7; font-weight: 600; }
.main [data-testid="stPageLink-NavLink"]:hover { color: #0369a1; }
[data-testid="stMetric"] { background: #fff; border: 1px solid var(--line); border-radius: 8px; padding: 10px 12px; }
[data-testid="stDataFrame"] { border: 1px solid var(--line); border-radius: 8px; }

/* ---------- disclaimer ---------- */
.disclaimer-box {
    background: #fffbeb; border: 1px solid #fde68a; border-left: 3px solid #f59e0b;
    border-radius: 6px; padding: 12px 16px; font-size: .8rem; color: #7c5a10;
    line-height: 1.5; margin: 14px 0;
}
[data-testid="stAlert"] { border-radius: 6px; }

/* ---------- responsive ---------- */
@media (max-width: 900px) {
    .app-hero { padding: 26px 22px; }
    .hero-title { font-size: 1.75rem; }
    .hero-art { display: none; }
    .page-head h1 { font-size: 1.45rem; }
    .team-panel { grid-template-columns: 1fr; }
}
</style>
"""

DARK_CSS = """
<style>
.stApp {
    background:
        radial-gradient(900px 420px at 8% -12%, rgba(14, 165, 233, .12), transparent 55%),
        radial-gradient(700px 380px at 100% -5%, rgba(99, 102, 241, .12), transparent 50%),
        #080f1d;
}
h1, h2, h3, h4, h5, .brand-name, .user-name, .hero-title, .module-title,
.stat-value, .step-title, .team-name, .conf-num, .page-head h1 { color: #f1f5f9 !important; }
p, label, .hero-sub, .module-desc, .stat-hint, .step-desc, .page-head p { color: #a8b3c4; }
[data-testid="stSidebar"] { background: #0c1526; border-right-color: #1e293b; }
[data-testid="stSidebar"] [data-testid="stPageLink"] a,
[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"] { color: #cbd5e1; }
[data-testid="stSidebar"] [data-testid="stPageLink"] a:hover,
[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"]:hover { background: #132038; }
[data-testid="stSidebar"] [data-testid="stPageLink"] a[aria-current="page"],
[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"][aria-current="page"] {
    background: linear-gradient(90deg, #0b2a45, #1b1f45); color: #7dd3fc;
}
.user-chip, .stat-tile, .step, .team-panel, .page-head-icon, [data-testid="stMetric"] {
    background: #101b2f !important; border-color: #1e293b !important;
}
.app-hero { background: linear-gradient(120deg, #0f1a2e, #0b2537 55%, #171a3a); border-color: #1e293b; }
.empty-state { background: #0c1526; border-color: #24334a; }
.hero-sub { color: #a8b3c4; }
.hero-tag { background: #0c1526; border-color: #24334a; color: #cbd5e1; }
.module-desc, .result-text, .team-list { color: #a8b3c4; }
.module-icon.heart, .module-icon.kidney, .module-icon.liver, .module-icon.lung, .module-icon.breast {
    background: #0c1526; border-color: #24334a;
}
[data-testid="stForm"], [data-testid="stExpander"] details, [data-testid="stVerticalBlockBorderWrapper"] > div {
    background: #101b2f !important; border-color: #1e293b !important;
}
[data-testid="stChatMessage"] { background: #0c1526; border-color: #1e293b; }
.result-hero.positive { background: linear-gradient(120deg, #2a1219, #1d1015); border-color: #7f1d3a; }
.result-hero.negative { background: linear-gradient(120deg, #0c241c, #0a1a16); border-color: #166534; }
.conf-ring-inner { background: #101b2f; }
.disclaimer-box { background: #221c0d; border-color: #4d3d13; color: #e3c77a; }
[data-testid="stAlert"] { background: #101b2f; color: #cbd5e1; }
</style>
"""


def inject_custom_css():
    """Inject the design system plus user display preferences."""
    size = st.session_state.get("ui_font_size", "Medium")
    base_px = {"Small": 14, "Medium": 16, "Large": 18}.get(size, 16)
    theme = st.session_state.get("ui_theme", "Light")
    contrast = st.session_state.get("ui_high_contrast", False)
    large_buttons = st.session_state.get("ui_large_buttons", False)

    extra = ""
    if contrast:
        extra += """
        <style>
        html, body, .stApp { background: #ffffff !important; color: #000000 !important; }
        p, label, .hero-sub, .module-desc, .stat-hint, .step-desc, .page-head p,
        .user-name, .brand-name, .hero-title, .module-title, .stat-value,
        .step-title, .team-name, .team-list, .conf-num { color: #000000 !important; }
        .app-hero, .stat-tile, .step, .team-panel, .page-head-icon,
        [data-testid="stForm"], [data-testid="stExpander"] details { background: #ffffff !important; border-color: #000000 !important; }
        .app-hero::after { display: none; }
        [data-testid="stBaseButton-primary"], button[kind="primary"] { background: #000000 !important; color: #ffffff !important; }
        </style>
        """
    if theme == "Dark":
        extra += DARK_CSS
    if large_buttons:
        extra += """
        <style>
        [data-testid="stBaseButton-primary"], [data-testid="stBaseButton-secondary"],
        button[kind="primary"], button[kind="secondary"] {
            font-size: 1.02rem !important; padding: .85rem 1.7rem !important;
        }
        </style>
        """

    override = f"<style>html {{ font-size: {base_px}px !important; }}</style>"
    st.markdown(BASE_CSS + override + extra, unsafe_allow_html=True)


def page_header(icon: str, title: str, subtitle: str):
    st.markdown(
        f"""
        <div class="page-head">
            <div class="page-head-icon">{icon}</div>
            <div>
                <h1>{title}</h1>
                <p>{subtitle}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(title: str, subtitle: str = ""):
    st.markdown(
        f"""
        <div class="section-head">
            <h3>{title}</h3>
            {f"<p>{subtitle}</p>" if subtitle else ""}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_disclaimer(full: bool = False):
    if full:
        st.markdown(
            """
            <div class="disclaimer-box">
                <strong>⚠️ Medical Disclaimer:</strong> This system is an academic machine-learning
                screening prototype developed for educational and research demonstration. It is
                <strong>NOT</strong> a certified medical device and its predictions are <strong>NOT</strong>
                a substitute for professional clinical diagnosis or consultation. Always consult a
                licensed healthcare practitioner.
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.caption("⚠️ Academic ML screening prototype — not a medical device. Not a substitute for professional clinical diagnosis.")


def render_model_info_expander(disease: str):
    """Expandable section with live metrics loaded from metadata.json."""
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    meta_path = os.path.join(base_dir, "models", disease, "metadata.json")

    if not os.path.exists(meta_path):
        st.info("Model metrics metadata not available.")
        return

    with open(meta_path, "r") as f:
        meta = json.load(f)

    with st.expander(f"📊 Model information & evaluation metrics ({meta.get('model_name', 'Model')})", expanded=False):
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Algorithm", meta.get("model_name", "N/A"))
        c2.metric("Accuracy", f"{meta.get('accuracy', 0)*100:.2f}%")
        c3.metric("F1 score", f"{meta.get('f1_score', 0)*100:.2f}%")
        c4.metric("ROC-AUC", f"{meta.get('roc_auc', 0)*100:.2f}%")

        st.caption(
            f"Dataset records: **{meta.get('dataset_rows', 0)}** "
            f"(train {meta.get('train_rows', 0)} / test {meta.get('test_rows', 0)}) · "
            f"Last trained: {meta.get('last_trained', 'N/A')}"
        )

        if disease == "kidney":
            st.info("CKD markers in the UCI cohort are strongly separable; reported accuracy reflects this dataset. Stratified 5-fold CV ≈ 99.1% ± 0.8%. Interpret with clinical caution.")

        if "candidate_comparison" in meta:
            st.markdown("##### Candidate algorithm comparison")
            comp = meta["candidate_comparison"]
            rows = []
            for alg, scores in comp.items():
                rows.append({
                    "Algorithm": alg,
                    "Accuracy": f"{scores['accuracy']*100:.2f}%",
                    "Precision": f"{scores['precision']*100:.2f}%",
                    "Recall": f"{scores['recall']*100:.2f}%",
                    "F1 Score": f"{scores['f1_score']*100:.2f}%",
                    "ROC-AUC": f"{scores['roc_auc']*100:.2f}%",
                })
            st.dataframe(rows, width="stretch", hide_index=True)

        cm = meta.get("confusion_matrix")
        if cm:
            import pandas as pd

            st.markdown("##### Confusion matrix")
            cm_df = pd.DataFrame(
                cm,
                index=["Actual Negative", "Actual Positive"],
                columns=["Predicted Negative", "Predicted Positive"],
            )
            try:
                st.dataframe(cm_df.style.background_gradient(cmap="Blues"), width="stretch")
            except Exception:
                st.dataframe(cm_df, width="stretch")


def render_empty_prediction_placeholder(disease: str):
    """Clean empty state placeholder on the right cockpit panel before prediction is run."""
    from src.utils.constants import DISEASE_METADATA
    meta = DISEASE_METADATA.get(disease, {})
    st.markdown(
        f"""
        <div class="result-placeholder">
            <div class="placeholder-icon">{meta.get('icon', '🩺')}</div>
            <div class="placeholder-title">Diagnostic Screening Console</div>
            <div class="placeholder-sub">
                Select a demonstration preset on the left or enter patient parameters and click 
                <strong>Run Prediction</strong> to generate a risk assessment.
            </div>
            <div class="placeholder-meta">
                <div><span>Module</span> <strong>{meta.get('name', 'Model')}</strong></div>
                <div><span>Pipeline</span> <strong>Classical ML</strong></div>
                <div><span>Status</span> <strong>Ready</strong></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_prediction_result(res: Dict[str, Any]):
    """Rich result card with confidence ring, probabilities and explanation."""
    if res["status"] != "success":
        st.error(f"Prediction error: {res.get('message', 'Unknown failure')}")
        for err in res.get("errors", []) or []:
            st.warning(f"• {err}")
        return

    is_pos = res["is_positive"]
    variant = "positive" if is_pos else "negative"
    ring = "#f43f5e" if is_pos else "#10b981"
    confidence = float(res["confidence"])
    risk_prob = float(res["probability_positive"])

    st.markdown(
        f"""
        <div class="result-hero {variant}">
            <div class="result-copy">
                <span class="risk-chip">{res['risk_level']}</span>
                <div class="result-title">{res['result_label']}</div>
                <p class="result-text">{res['recommendation']}</p>
            </div>
            <div class="conf-ring" style="--p:{confidence:.0f}; --ring:{ring};">
                <div class="conf-ring-inner">
                    <div class="conf-num">{confidence:.1f}%</div>
                    <div class="conf-lbl">confidence</div>
                </div>
            </div>
        </div>
        <div class="prob-row">
            <span>Normal probability · {res['probability_negative']}%</span>
            <span>Risk probability · {res['probability_positive']}%</span>
        </div>
        <div class="prob-bar"><div class="prob-fill" style="width:{risk_prob:.1f}%;"></div></div>
        """,
        unsafe_allow_html=True,
    )

    top_features = res.get("top_features") or []
    if top_features:
        with st.expander("🔍 Top contributing factors", expanded=False):
            import pandas as pd

            df = pd.DataFrame(top_features).rename(
                columns={
                    "feature": "Factor",
                    "value": "Patient value",
                    "contribution": "Risk impact (pp)",
                }
            )
            # Mixed str/number values in one column break Arrow serialization on Cloud.
            df["Patient value"] = df["Patient value"].astype(str)
            st.dataframe(df, width="stretch", hide_index=True)
            try:
                chart_df = df.set_index("Factor")[["Risk impact (pp)"]]
                st.bar_chart(chart_df, color="#0ea5e9")
            except Exception:
                pass

    from src.utils.reports import generate_diagnostic_report_pdf, generate_diagnostic_report_text

    pdf_bytes = generate_diagnostic_report_pdf(res)
    txt_content = generate_diagnostic_report_text(res)
    dis_id = res.get("disease", "diagnosis")

    c_dl1, c_dl2 = st.columns([1.5, 1])
    with c_dl1:
        st.download_button(
            label="📥 Download Clinical Report (PDF)",
            data=pdf_bytes,
            file_name=f"{dis_id}_screening_report.pdf",
            mime="application/pdf",
            type="primary",
            width="stretch",
            help="Download official publication-grade clinical diagnostic screening report in PDF format.",
        )
    with c_dl2:
        st.download_button(
            label="📄 Text Summary (.txt)",
            data=txt_content,
            file_name=f"{dis_id}_screening_report.txt",
            mime="text/plain",
            width="stretch",
            help="Download plain-text diagnostic summary report.",
        )
