"""
Docsy Clinical AI Copilot — Slide-Over Right Drawer & Floating Trigger.
Exact mirror of the OmniShell design system from Garageplug:
- Circular violet floating action button (FAB) at bottom-right with glow
- 500px slide-over drawer (expandable to full screen)
- Real-time client-side dialogue with Gemini (zero page reloads or flicker)
- Keyboard shortcuts: ⌘J / Ctrl+J to toggle, Esc to close
- Single DOM instance attached to document.body (100% reliably clickable)
"""
import json
import streamlit as st

from src.chatbot.api_server import ensure_api_server_started


def render_copilot():
    """Renders the client-side Docsy Copilot widget into the DOM."""
    # Ensure background API server is running
    api_port = ensure_api_server_started(8503)

    # Sync any active prediction context from session state to Docsy
    last_pred = st.session_state.get("last_prediction")
    context_json = "null"
    if last_pred:
        dis = last_pred.get("disease", "")
        res = last_pred.get("result", {}) or {}
        context_data = {
            "disease": dis,
            "result_label": res.get("result_label", ""),
            "confidence": res.get("confidence", ""),
            "probability_positive": res.get("probability_positive", ""),
            "inputs": res.get("user_inputs") or res.get("input_features", {}),
            "summary": f"{dis.replace('_', ' ').title()} — {res.get('result_label', '')} ({res.get('confidence', '')}%)",
        }
        context_json = json.dumps(context_data)

    html_code = f"""
<div id="docsy-template" style="display: none;">
    <!-- Docsy Floating Trigger Button (Single place, bottom-right) -->
    <div id="docsy-fab-container" class="docsy-fab-container">
        <button id="docsy-fab-btn" class="docsy-fab-btn" title="Open Docsy (⌘J)" aria-label="Open Docsy">
            <svg class="docsy-sparkle-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/>
                <path d="M5 3v4"/><path d="M19 17v4"/><path d="M3 5h4"/><path d="M17 19h4"/>
            </svg>
        </button>
        <span class="docsy-fab-label">DOCSY</span>
    </div>

    <!-- Docsy Slide-Over Drawer Panel -->
    <div id="docsy-panel" class="docsy-panel">
        <!-- Panel Header -->
        <div class="docsy-header">
            <div class="docsy-brand">
                <div class="docsy-brand-icon">
                    <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/>
                    </svg>
                </div>
                <div class="docsy-brand-title">
                    <span class="docsy-title-main">Docsy</span>
                    <span id="docsy-header-status" class="docsy-title-sub">clinical copilot</span>
                </div>
            </div>

            <div class="docsy-header-actions">
                <button id="docsy-btn-new" class="docsy-hdr-btn" title="New chat (Reset)">
                    <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 5v14M5 12h14"/></svg>
                    <span>New</span>
                </button>
                <button id="docsy-btn-expand" class="docsy-hdr-btn icon-only" title="Maximize panel">
                    <svg id="docsy-exp-icon" viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"/>
                    </svg>
                </button>
                <button id="docsy-btn-close" class="docsy-hdr-btn icon-only" title="Close (Esc)">
                    <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6 6 18M6 6l12 12"/></svg>
                </button>
            </div>
        </div>

        <!-- Active Clinical Context Chip -->
        <div id="docsy-context-bar" class="docsy-context-bar">
            <span class="docsy-ctx-tag">Context:</span>
            <div id="docsy-ctx-badge" class="docsy-ctx-badge">
                <span class="docsy-ctx-dot"></span>
                <span id="docsy-ctx-text">None</span>
            </div>
            <button id="docsy-ctx-clear" class="docsy-ctx-clear" title="Clear Context">clear</button>
        </div>

        <!-- Scrollable Chat Body -->
        <div id="docsy-body" class="docsy-body">
            <!-- Empty state hero -->
            <div id="docsy-hero" class="docsy-hero">
                <div class="docsy-hero-icon-wrap">
                    <div class="docsy-hero-ring"></div>
                    <div class="docsy-hero-ring delay"></div>
                    <div class="docsy-hero-box">
                        <svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/>
                        </svg>
                    </div>
                </div>

                <div class="docsy-hero-title">Docsy — your clinical copilot</div>
                <div class="docsy-hero-sub">
                    I can explain diagnostic screening results, biomarker patterns, renal & cardiovascular risk, and prevention protocols.
                </div>
                <div class="docsy-hero-shortcut">⌘J to toggle · Esc to close · Enter to send</div>

                <!-- Suggestions Grid -->
                <div class="docsy-sug-grid">
                    <button class="docsy-sug-chip" data-prompt="Explain the active clinical screening result and key risk contributors.">
                        <span class="docsy-sug-icon">📊</span>
                        <span>Explain current screening</span>
                    </button>
                    <button class="docsy-sug-chip" data-prompt="Review key cardiac biomarkers: Oldpeak ST depression, Thalassemia defect, and vessel fluoroscopy.">
                        <span class="docsy-sug-icon">🫀</span>
                        <span>Review cardiac biomarkers</span>
                    </button>
                    <button class="docsy-sug-chip" data-prompt="Explain the clinical difference between Prehypertension and Stage 1/2 Hypertension.">
                        <span class="docsy-sug-icon">🩸</span>
                        <span>Blood pressure stages</span>
                    </button>
                    <button class="docsy-sug-chip" data-prompt="How do Serum Creatinine, Blood Urea, and Albumin indicate renal filtration capacity?">
                        <span class="docsy-sug-icon">🫘</span>
                        <span>Renal filtration markers</span>
                    </button>
                    <button class="docsy-sug-chip" data-prompt="What do elevated SGOT (AST), SGPT (ALT), and Alkaline Phosphatase indicate clinically?">
                        <span class="docsy-sug-icon">🧪</span>
                        <span>Liver enzyme thresholds</span>
                    </button>
                    <button class="docsy-sug-chip" data-prompt="What are evidence-based lifestyle habits to lower cardiovascular and renal risk?">
                        <span class="docsy-sug-icon">🥗</span>
                        <span>Evidence-based prevention</span>
                    </button>
                </div>
            </div>

            <!-- Messages Thread Container -->
            <div id="docsy-messages" class="docsy-messages"></div>

            <!-- Thinking Indicator -->
            <div id="docsy-thinking" class="docsy-thinking">
                <div class="docsy-thinking-ping">
                    <span class="ping-wave"></span>
                    <span class="ping-dot"></span>
                </div>
                <span>Thinking</span>
                <span class="docsy-thinking-dots">
                    <span class="dot"></span><span class="dot"></span><span class="dot"></span>
                </span>
            </div>
        </div>

        <!-- Input Footer -->
        <div class="docsy-footer">
            <form id="docsy-input-form" class="docsy-input-form">
                <textarea
                    id="docsy-textarea"
                    class="docsy-textarea"
                    placeholder="Ask Docsy... (Shift+Enter for newline)"
                    rows="1"
                ></textarea>
                <button id="docsy-btn-send" type="submit" class="docsy-send-btn" title="Send (Enter)">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/>
                    </svg>
                </button>
            </form>
            <div class="docsy-footer-hint">⌘J to toggle · Esc to close · Enter to send · Shift+Enter for newline</div>
        </div>
    </div>
</div>

<style>
/* ==========================================================================
   DOCSY CLINICAL COPILOT — LIGHT CLINICAL MEDICAL DESIGN SYSTEM
   Matches MDPS palette: crisp medical white, slate borders, ocean blue accents.
   ========================================================================== */

/* ── Floating Action Button (FAB) ── */
.docsy-fab-container {{
    position: fixed !important;
    right: 24px !important;
    bottom: 28px !important;
    z-index: 2147483640 !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    gap: 5px !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    cursor: pointer !important;
    user-select: none !important;
}}

.docsy-fab-btn {{
    width: 48px !important;
    height: 48px !important;
    border-radius: 50% !important;
    background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
    border: 1px solid rgba(255, 255, 255, 0.5) !important;
    color: #ffffff !important;
    cursor: pointer !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-shadow: 0 4px 18px rgba(2, 132, 199, 0.45), 0 0 0 1px rgba(2, 132, 199, 0.2) !important;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
    pointer-events: auto !important;
}}

.docsy-fab-btn:hover {{
    transform: scale(1.08) !important;
    box-shadow: 0 6px 24px rgba(2, 132, 199, 0.6) !important;
}}

.docsy-sparkle-icon {{
    width: 20px !important;
    height: 20px !important;
    color: #ffffff !important;
    pointer-events: none !important;
}}

.docsy-fab-label {{
    font-size: 10px !important;
    font-weight: 700 !important;
    color: #475569 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    pointer-events: none !important;
}}

/* ── Slide-Over Panel ── */
.docsy-panel {{
    position: fixed !important;
    right: 0 !important;
    top: 0 !important;
    bottom: 0 !important;
    width: 500px !important;
    max-width: 92vw !important;
    height: 100vh !important;
    background: #ffffff !important;
    border-left: 1px solid #e2e8f0 !important;
    box-shadow: -12px 0 45px rgba(15, 23, 42, 0.12) !important;
    z-index: 2147483647 !important;
    display: flex !important;
    flex-direction: column !important;
    overflow: hidden !important;
    transform: translateX(105%) !important;
    transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), width 0.2s ease !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    color: #0f172a !important;
}}

.docsy-panel.open {{
    transform: translateX(0) !important;
}}

.docsy-panel.maximized {{
    width: 100vw !important;
    max-width: 100vw !important;
}}

/* ── Header ── */
.docsy-header {{
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    padding: 12px 16px !important;
    border-bottom: 1px solid #e2e8f0 !important;
    background: #f8fafc !important;
    flex-shrink: 0 !important;
}}

.docsy-brand {{
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
}}

.docsy-brand-icon {{
    width: 26px !important;
    height: 26px !important;
    border-radius: 6px !important;
    background: #e0f2fe !important;
    border: 1px solid #bae6fd !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    color: #0284c7 !important;
}}

.docsy-brand-title {{
    display: flex !important;
    align-items: baseline !important;
    gap: 6px !important;
}}

.docsy-title-main {{
    font-size: 14.5px !important;
    font-weight: 700 !important;
    color: #0f172a !important;
    letter-spacing: -0.01em !important;
}}

.docsy-title-sub {{
    font-size: 10.5px !important;
    font-weight: 500 !important;
    color: #64748b !important;
}}

.docsy-header-actions {{
    display: flex !important;
    align-items: center !important;
    gap: 4px !important;
}}

.docsy-hdr-btn {{
    display: inline-flex !important;
    align-items: center !important;
    gap: 4px !important;
    padding: 4px 8px !important;
    border-radius: 5px !important;
    background: transparent !important;
    border: 1px solid transparent !important;
    color: #475569 !important;
    font-size: 11px !important;
    font-weight: 500 !important;
    cursor: pointer !important;
    transition: all 0.15s ease !important;
}}

.docsy-hdr-btn.icon-only {{
    padding: 5px !important;
    width: 28px !important;
    height: 28px !important;
    justify-content: center !important;
}}

.docsy-hdr-btn:hover {{
    background: #e2e8f0 !important;
    color: #0f172a !important;
}}

/* ── Context Bar ── */
.docsy-context-bar {{
    display: none;
    align-items: center !important;
    gap: 8px !important;
    padding: 7px 16px !important;
    border-bottom: 1px solid #e2e8f0 !important;
    background: #f8fafc !important;
    font-size: 11px !important;
    flex-shrink: 0 !important;
}}

.docsy-ctx-tag {{
    text-transform: uppercase !important;
    font-size: 9.5px !important;
    font-weight: 600 !important;
    color: #64748b !important;
    letter-spacing: 0.05em !important;
}}

.docsy-ctx-badge {{
    display: inline-flex !important;
    align-items: center !important;
    gap: 6px !important;
    background: #e0f2fe !important;
    border: 1px solid #bae6fd !important;
    color: #0369a1 !important;
    padding: 2px 8px !important;
    border-radius: 4px !important;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
    font-size: 10.5px !important;
    font-weight: 500 !important;
    max-width: 320px !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    white-space: nowrap !important;
}}

.docsy-ctx-dot {{
    width: 5px !important;
    height: 5px !important;
    border-radius: 50% !important;
    background: #10b981 !important;
    box-shadow: 0 0 4px #10b981 !important;
}}

.docsy-ctx-clear {{
    margin-left: auto !important;
    background: transparent !important;
    border: none !important;
    color: #94a3b8 !important;
    font-size: 10px !important;
    cursor: pointer !important;
}}

.docsy-ctx-clear:hover {{
    color: #475569 !important;
}}

/* ── Body & Hero ── */
.docsy-body {{
    flex: 1 !important;
    min-height: 0 !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
    padding: 16px !important;
    display: flex !important;
    flex-direction: column !important;
    gap: 14px !important;
    background: #ffffff !important;
}}

.docsy-hero {{
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    padding: 24px 8px 12px !important;
    gap: 12px !important;
    margin: auto 0 !important;
}}

.docsy-hero-icon-wrap {{
    position: relative !important;
    width: 60px !important;
    height: 60px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}}

.docsy-hero-ring {{
    position: absolute !important;
    inset: 0 !important;
    border-radius: 18px !important;
    background: rgba(14, 165, 233, 0.15) !important;
}}

.docsy-hero-box {{
    position: relative !important;
    width: 56px !important;
    height: 56px !important;
    border-radius: 16px !important;
    background: linear-gradient(135deg, #e0f2fe 0%, #ede9fe 100%) !important;
    border: 1px solid #bae6fd !important;
    box-shadow: 0 4px 16px rgba(2, 132, 199, 0.15) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    color: #0284c7 !important;
}}

.docsy-hero-title {{
    font-size: 15px !important;
    font-weight: 700 !important;
    color: #0f172a !important;
}}

.docsy-hero-sub {{
    font-size: 12px !important;
    color: #475569 !important;
    line-height: 1.5 !important;
    max-width: 380px !important;
}}

.docsy-hero-shortcut {{
    font-size: 10px !important;
    color: #94a3b8 !important;
    font-family: ui-monospace, SFMono-Regular, monospace !important;
}}

/* ── Suggestions Grid ── */
.docsy-sug-grid {{
    display: grid !important;
    grid-template-columns: repeat(2, 1fr) !important;
    gap: 8px !important;
    width: 100% !important;
    margin-top: 6px !important;
}}

.docsy-sug-chip {{
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
    padding: 10px 12px !important;
    border-radius: 8px !important;
    background: #f8fafc !important;
    border: 1px solid #e2e8f0 !important;
    color: #334155 !important;
    font-size: 11.5px !important;
    font-weight: 500 !important;
    text-align: left !important;
    cursor: pointer !important;
    transition: all 0.15s ease !important;
}}

.docsy-sug-chip:hover {{
    background: #f1f5f9 !important;
    border-color: #0284c7 !important;
    color: #0369a1 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 3px 10px rgba(2, 132, 199, 0.1) !important;
}}

.docsy-sug-icon {{
    font-size: 13px !important;
    flex-shrink: 0 !important;
}}

/* ── Chat Messages ── */
.docsy-messages {{
    display: flex !important;
    flex-direction: column !important;
    gap: 12px !important;
    width: 100% !important;
}}

.docsy-msg-row {{
    display: flex !important;
    flex-direction: column !important;
    width: 100% !important;
}}

.docsy-msg-row.user {{
    align-items: flex-end !important;
}}

.docsy-msg-row.assistant {{
    align-items: flex-start !important;
}}

.docsy-msg-bubble {{
    max-width: 90% !important;
    font-size: 13px !important;
    line-height: 1.55 !important;
    word-break: break-word !important;
}}

.docsy-msg-row.user .docsy-msg-bubble {{
    background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
    color: #ffffff !important;
    padding: 9px 14px !important;
    border-radius: 14px 14px 3px 14px !important;
    box-shadow: 0 3px 10px rgba(2, 132, 199, 0.25) !important;
}}

.docsy-msg-row.assistant .docsy-msg-bubble {{
    background: #f8fafc !important;
    border: 1px solid #e2e8f0 !important;
    color: #1e293b !important;
    padding: 11px 15px !important;
    border-radius: 14px 14px 14px 3px !important;
}}

.docsy-msg-bubble p {{
    margin: 0 0 6px 0 !important;
}}
.docsy-msg-bubble p:last-child {{
    margin-bottom: 0 !important;
}}
.docsy-msg-bubble strong {{
    color: #0f172a !important;
    font-weight: 600 !important;
}}
.docsy-msg-bubble ul, .docsy-msg-bubble ol {{
    margin: 4px 0 6px 16px !important;
    padding: 0 !important;
}}
.docsy-msg-bubble li {{
    margin-bottom: 3px !important;
}}

/* ── Thinking Indicator (Hidden by default, shown ONLY on active prompt) ── */
.docsy-thinking {{
    display: none !important;
    align-items: center !important;
    gap: 8px !important;
    padding: 8px 14px !important;
    border-radius: 12px !important;
    background: #f1f5f9 !important;
    border: 1px solid #e2e8f0 !important;
    color: #64748b !important;
    font-size: 12px !important;
    align-self: flex-start !important;
}}

.docsy-thinking.active {{
    display: inline-flex !important;
}}

.docsy-thinking-ping {{
    position: relative !important;
    width: 8px !important;
    height: 8px !important;
}}

.ping-wave {{
    position: absolute !important;
    inset: 0 !important;
    border-radius: 50% !important;
    background: #38bdf8 !important;
    animation: ping 1.2s cubic-bezier(0, 0, 0.2, 1) infinite !important;
}}

.ping-dot {{
    position: relative !important;
    display: block !important;
    width: 8px !important;
    height: 8px !important;
    border-radius: 50% !important;
    background: #0284c7 !important;
}}

@keyframes ping {{
    75%, 100% {{ transform: scale(2.2); opacity: 0; }}
}}

.docsy-thinking-dots .dot {{
    display: inline-block !important;
    width: 3px !important;
    height: 3px !important;
    border-radius: 50% !important;
    background: #0284c7 !important;
    margin-left: 2px !important;
    animation: bounce 1.2s infinite ease-in-out !important;
}}
.docsy-thinking-dots .dot:nth-child(2) {{ animation-delay: 0.15s !important; }}
.docsy-thinking-dots .dot:nth-child(3) {{ animation-delay: 0.3s !important; }}

@keyframes bounce {{
    0%, 80%, 100% {{ transform: scale(0.6); opacity: 0.4; }}
    40% {{ transform: scale(1.2); opacity: 1; }}
}}

/* ── Footer Input ── */
.docsy-footer {{
    padding: 12px 14px 10px !important;
    border-top: 1px solid #e2e8f0 !important;
    background: #ffffff !important;
    flex-shrink: 0 !important;
}}

.docsy-input-form {{
    display: flex !important;
    align-items: flex-end !important;
    gap: 8px !important;
    position: relative !important;
}}

.docsy-textarea {{
    flex: 1 !important;
    min-height: 38px !important;
    max-height: 180px !important;
    background: #f8fafc !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 8px !important;
    color: #0f172a !important;
    font-size: 13px !important;
    font-family: inherit !important;
    padding: 9px 12px !important;
    resize: none !important;
    outline: none !important;
    line-height: 1.4 !important;
    transition: all 0.2s ease !important;
}}

.docsy-textarea:focus {{
    border-color: #0284c7 !important;
    box-shadow: 0 0 0 2px rgba(2, 132, 199, 0.15) !important;
    background: #ffffff !important;
}}

.docsy-textarea::placeholder {{
    color: #94a3b8 !important;
}}

.docsy-send-btn {{
    width: 38px !important;
    height: 38px !important;
    border-radius: 8px !important;
    background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
    border: none !important;
    color: #ffffff !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    cursor: pointer !important;
    flex-shrink: 0 !important;
    transition: all 0.15s ease !important;
}}

.docsy-send-btn:hover {{
    background: #0369a1 !important;
    transform: translateY(-1px) !important;
}}

.docsy-send-btn:disabled {{
    opacity: 0.4 !important;
    cursor: not-allowed !important;
    transform: none !important;
}}

.docsy-footer-hint {{
    font-size: 9.5px !important;
    color: #94a3b8 !important;
    margin-top: 6px !important;
    padding-left: 2px !important;
    font-family: ui-monospace, SFMono-Regular, monospace !important;
}}
</style>

<script>
(function() {{
    const API_PORT = {api_port};
    let ACTIVE_CONTEXT = {context_json};

    // If Docsy is already mounted and active in document.body, simply update context & return
    if (window.__docsyMounted) {{
        if (window.__docsyUpdateContext) {{
            window.__docsyUpdateContext(ACTIVE_CONTEXT);
        }}
        return;
    }}

    // Mount to document.body so it is independent of Streamlit's container tree
    const template = document.getElementById("docsy-template");
    if (!template) return;

    // Remove any stale remnants
    const oldRoot = document.getElementById("docsy-widget-root");
    if (oldRoot) oldRoot.remove();

    const root = document.createElement("div");
    root.id = "docsy-widget-root";
    root.innerHTML = template.innerHTML;
    document.body.appendChild(root);
    template.remove();
    window.__docsyMounted = true;

    // Elements
    const fab = document.getElementById("docsy-fab-btn");
    const fabContainer = document.getElementById("docsy-fab-container");
    const panel = document.getElementById("docsy-panel");
    const btnClose = document.getElementById("docsy-btn-close");
    const btnExpand = document.getElementById("docsy-btn-expand");
    const btnNew = document.getElementById("docsy-btn-new");
    const textarea = document.getElementById("docsy-textarea");
    const form = document.getElementById("docsy-input-form");
    const body = document.getElementById("docsy-body");
    const hero = document.getElementById("docsy-hero");
    const messagesContainer = document.getElementById("docsy-messages");
    const thinking = document.getElementById("docsy-thinking");
    const ctxBar = document.getElementById("docsy-context-bar");
    const ctxText = document.getElementById("docsy-ctx-text");
    const ctxClear = document.getElementById("docsy-ctx-clear");
    const headerStatus = document.getElementById("docsy-header-status");

    let isExpanded = false;
    let isThinking = false;
    let chatHistory = [];

    // Load persisted chat history from localStorage
    try {{
        const stored = localStorage.getItem("docsy_chat_history_v2");
        if (stored) {{
            chatHistory = JSON.parse(stored);
        }}
    }} catch (e) {{}}

    // Global toggle function
    window.toggleDocsy = function() {{
        if (!panel) return;
        const isOpen = panel.classList.contains("open");
        if (isOpen) {{
            closePanel();
        }} else {{
            openPanel();
        }}
    }};

    function openPanel() {{
        panel.classList.add("open");
        fabContainer.style.display = "none";
        setTimeout(() => textarea && textarea.focus(), 150);
    }}

    function closePanel() {{
        panel.classList.remove("open");
        fabContainer.style.display = "flex";
    }}

    // Make BOTH the FAB button AND container clickable properly
    if (fab) {{
        fab.addEventListener("click", function(e) {{
            e.preventDefault();
            e.stopPropagation();
            openPanel();
        }});
    }}
    if (fabContainer) {{
        fabContainer.addEventListener("click", function(e) {{
            e.preventDefault();
            e.stopPropagation();
            openPanel();
        }});
    }}

    if (btnClose) {{
        btnClose.onclick = (e) => {{
            e.preventDefault();
            closePanel();
        }};
    }}

    if (btnExpand) {{
        btnExpand.onclick = (e) => {{
            e.preventDefault();
            isExpanded = !isExpanded;
            panel.classList.toggle("maximized", isExpanded);
            btnExpand.title = isExpanded ? "Restore panel" : "Maximize panel";
        }};
    }}

    if (btnNew) {{
        btnNew.onclick = (e) => {{
            e.preventDefault();
            chatHistory = [];
            try {{ localStorage.removeItem("docsy_chat_history_v2"); }} catch (err) {{}}
            renderMessages();
            if (textarea) textarea.value = "";
        }};
    }}

    // Keyboard Shortcuts: ⌘J / Ctrl+J, Esc
    window.addEventListener("keydown", (e) => {{
        if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "j") {{
            e.preventDefault();
            window.toggleDocsy();
        }} else if (e.key === "Escape" && panel && panel.classList.contains("open")) {{
            e.preventDefault();
            closePanel();
        }}
    }});

    // Context updating bridge
    window.__docsyUpdateContext = function(newCtx) {{
        ACTIVE_CONTEXT = newCtx;
        if (ACTIVE_CONTEXT && ACTIVE_CONTEXT.summary) {{
            if (ctxBar && ctxText) {{
                ctxBar.style.display = "flex";
                ctxText.textContent = ACTIVE_CONTEXT.summary;
            }}
        }} else {{
            if (ctxBar) ctxBar.style.display = "none";
        }}
    }};

    window.__docsyUpdateContext(ACTIVE_CONTEXT);

    if (ctxClear) {{
        ctxClear.onclick = () => {{
            if (ctxBar) ctxBar.style.display = "none";
        }};
    }}

    // Auto-grow textarea
    if (textarea) {{
        textarea.addEventListener("input", () => {{
            textarea.style.height = "auto";
            textarea.style.height = Math.min(textarea.scrollHeight, 180) + "px";
        }});

        textarea.addEventListener("keydown", (e) => {{
            if (e.key === "Enter" && !e.shiftKey) {{
                e.preventDefault();
                submitPrompt();
            }}
        }});
    }}

    // Form submit
    if (form) {{
        form.onsubmit = (e) => {{
            e.preventDefault();
            submitPrompt();
        }};
    }}

    // Suggestion chips
    document.querySelectorAll(".docsy-sug-chip").forEach((chip) => {{
        chip.onclick = () => {{
            const p = chip.getAttribute("data-prompt");
            if (p) sendUserMessage(p);
        }};
    }});

    function submitPrompt() {{
        if (!textarea) return;
        const text = textarea.value.trim();
        if (!text || isThinking) return;
        textarea.value = "";
        textarea.style.height = "auto";
        sendUserMessage(text);
    }}

    function parseMarkdown(md) {{
        if (!md) return "";
        let text = md
            .replace(/&/g, "&amp;")
            .replace(/\\x3c/g, "&lt;")
            .replace(/>/g, "&gt;");
        // bold
        text = text.replace(/\\*\\*(.*?)\\*\\*/g, "\\x3cstrong>$1\\x3c/strong>");
        // italic
        text = text.replace(/\\*(.*?)\\*/g, "\\x3cem>$1\\x3c/em>");
        // bullet lines
        text = text.replace(/^\\s*[-*]\\s+(.*)$/gm, "\\x3cli>$1\\x3c/li>");
        text = text.replace(/(\\x3cli>.*\\x3c\\/li>)/s, "\\x3cul>$1\\x3c/ul>");
        // paragraph line breaks
        text = text.replace(/\\n\\n+/g, "\\x3c/p>\\x3cp>");
        text = text.replace(/\\n/g, "\\x3cbr>");
        return "\\x3cp>" + text + "\\x3c/p>";
    }}

    function renderMessages() {{
        if (!messagesContainer || !hero) return;
        if (chatHistory.length === 0) {{
            hero.style.display = "flex";
            messagesContainer.innerHTML = "";
            return;
        }}
        hero.style.display = "none";
        messagesContainer.innerHTML = chatHistory.map((m) => {{
            const bubbleContent = m.role === "assistant" ? parseMarkdown(m.content) : m.content;
            return `
                \\x3cdiv class="docsy-msg-row ${{m.role}}">
                    \\x3cdiv class="docsy-msg-bubble">
                        ${{bubbleContent}}
                    \\x3c/div>
                \\x3c/div>
            `;
        }}).join("");
        body.scrollTop = body.scrollHeight;
    }}

    async function sendUserMessage(prompt) {{
        chatHistory.push({{ role: "user", content: prompt }});
        renderMessages();

        isThinking = true;
        if (thinking) thinking.classList.add("active");
        if (headerStatus) headerStatus.textContent = "thinking...";
        body.scrollTop = body.scrollHeight;

        try {{
            const res = await fetch(`http://127.0.0.1:${{API_PORT}}/api/chat`, {{
                method: "POST",
                headers: {{ "Content-Type": "application/json" }},
                body: JSON.stringify({{
                    message: prompt,
                    history: chatHistory.slice(0, -1),
                    context: ACTIVE_CONTEXT ? ACTIVE_CONTEXT.summary : null
                }})
            }});

            const data = await res.json();
            const reply = data.reply || "No response received.";
            chatHistory.push({{ role: "assistant", content: reply }});

            try {{
                localStorage.setItem("docsy_chat_history_v2", JSON.stringify(chatHistory));
            }} catch (e) {{}}
        }} catch (err) {{
            chatHistory.push({{
                role: "assistant",
                content: "⚠️ Could not connect to Docsy clinical server. Please verify your connection."
            }});
        }} finally {{
            isThinking = false;
            if (thinking) thinking.classList.remove("active");
            if (headerStatus) headerStatus.textContent = "clinical copilot";
            renderMessages();
        }}
    }}

    // Initial render
    if (thinking) thinking.classList.remove("active");
    renderMessages();
}})();
</script>
"""
    st.html(html_code, unsafe_allow_javascript=True)
