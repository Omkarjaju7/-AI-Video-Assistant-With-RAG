"""
AI Video Meeting Assistant — Streamlit UI
Wraps the existing pipeline from main.py into a rich, interactive web app.
"""

import streamlit as st
from dotenv import load_dotenv
import time

# ── Page config (must be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="AI Video Assistant",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_dotenv()

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* ── Google Fonts ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* ── Root & Theme ── */
    :root {
        --bg-primary:    #0d0f14;
        --bg-secondary:  #13161e;
        --bg-card:       #1a1d27;
        --bg-card-hover: #1f2335;
        --accent:        #6c63ff;
        --accent-glow:   rgba(108,99,255,0.25);
        --accent-soft:   rgba(108,99,255,0.12);
        --success:       #22d3a5;
        --warning:       #f59e0b;
        --danger:        #ef4444;
        --text-primary:  #e8eaf0;
        --text-secondary:#9aa0b4;
        --border:        rgba(255,255,255,0.07);
        --gradient:      linear-gradient(135deg, #6c63ff 0%, #a855f7 50%, #ec4899 100%);
    }

    /* ── Global ── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: var(--bg-primary);
        color: var(--text-primary);
    }

    /* ── Streamlit overrides ── */
    .main .block-container {
        padding: 2rem 2rem 4rem;
        max-width: 1400px;
    }
    section[data-testid="stSidebar"] {
        background: var(--bg-secondary);
        border-right: 1px solid var(--border);
    }
    section[data-testid="stSidebar"] .block-container {
        padding: 1.5rem 1rem;
    }

    /* ── Hero header ── */
    .hero-header {
        background: var(--gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.4rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        line-height: 1.2;
        margin-bottom: 0.2rem;
    }
    .hero-sub {
        color: var(--text-secondary);
        font-size: 1rem;
        font-weight: 400;
        margin-bottom: 2rem;
    }

    /* ── Cards ── */
    .glass-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1rem;
        transition: box-shadow 0.25s ease, border-color 0.25s ease;
    }
    .glass-card:hover {
        box-shadow: 0 0 24px var(--accent-glow);
        border-color: rgba(108,99,255,0.3);
    }
    .card-title {
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: var(--accent);
        margin-bottom: 0.6rem;
    }
    .card-content {
        font-size: 0.95rem;
        line-height: 1.7;
        color: var(--text-primary);
    }

    /* ── Badge chips ── */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 0.4rem;
        margin-bottom: 0.4rem;
    }
    .badge-purple { background: var(--accent-soft); color: var(--accent); border: 1px solid rgba(108,99,255,0.3); }
    .badge-green  { background: rgba(34,211,165,0.12); color: var(--success); border: 1px solid rgba(34,211,165,0.3); }
    .badge-amber  { background: rgba(245,158,11,0.12); color: var(--warning); border: 1px solid rgba(245,158,11,0.3); }

    /* ── Bullet list items ── */
    .bullet-item {
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
        padding: 0.6rem 0.8rem;
        border-radius: 8px;
        margin-bottom: 0.4rem;
        background: rgba(255,255,255,0.025);
        transition: background 0.2s;
    }
    .bullet-item:hover { background: rgba(255,255,255,0.05); }
    .bullet-dot {
        flex-shrink: 0;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-top: 7px;
    }
    .dot-purple { background: var(--accent); }
    .dot-green  { background: var(--success); }
    .dot-amber  { background: var(--warning); }
    .dot-pink   { background: #ec4899; }
    .bullet-text { font-size: 0.92rem; line-height: 1.6; color: var(--text-primary); }

    /* ── Stat counters ── */
    .stats-row {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
        margin-bottom: 1.5rem;
    }
    .stat-box {
        flex: 1;
        min-width: 120px;
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1rem 1.2rem;
        text-align: center;
    }
    .stat-value {
        font-size: 1.8rem;
        font-weight: 700;
        background: var(--gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .stat-label {
        font-size: 0.72rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-top: 0.2rem;
    }

    /* ── Chat bubbles ── */
    .chat-container {
        max-height: 420px;
        overflow-y: auto;
        padding: 0.5rem 0;
        margin-bottom: 1rem;
        scroll-behavior: smooth;
    }
    .chat-container::-webkit-scrollbar { width: 5px; }
    .chat-container::-webkit-scrollbar-track { background: transparent; }
    .chat-container::-webkit-scrollbar-thumb { background: var(--border); border-radius: 10px; }
    .bubble-user {
        display: flex;
        justify-content: flex-end;
        margin-bottom: 0.8rem;
    }
    .bubble-user .msg {
        background: var(--accent);
        color: #fff;
        border-radius: 18px 18px 4px 18px;
        padding: 0.65rem 1rem;
        max-width: 72%;
        font-size: 0.9rem;
        line-height: 1.5;
    }
    .bubble-bot {
        display: flex;
        justify-content: flex-start;
        margin-bottom: 0.8rem;
    }
    .bubble-bot .avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: var(--gradient);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.9rem;
        flex-shrink: 0;
        margin-right: 0.6rem;
        margin-top: 2px;
    }
    .bubble-bot .msg {
        background: var(--bg-card);
        border: 1px solid var(--border);
        color: var(--text-primary);
        border-radius: 4px 18px 18px 18px;
        padding: 0.65rem 1rem;
        max-width: 72%;
        font-size: 0.9rem;
        line-height: 1.6;
    }

    /* ── Transcript box ── */
    .transcript-box {
        background: #0a0b10;
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
        line-height: 1.75;
        color: #b8bdd0;
        max-height: 340px;
        overflow-y: auto;
        white-space: pre-wrap;
        word-break: break-word;
    }
    .transcript-box::-webkit-scrollbar { width: 5px; }
    .transcript-box::-webkit-scrollbar-thumb { background: var(--border); border-radius: 10px; }

    /* ── Progress / Status ── */
    .status-step {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.5rem 0;
        font-size: 0.88rem;
        color: var(--text-secondary);
    }
    .status-step.done  { color: var(--success); }
    .status-step.doing { color: var(--accent); }
    .step-icon { font-size: 1rem; }

    /* ── Sidebar extras ── */
    .sidebar-label {
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: var(--text-secondary);
        margin-bottom: 0.4rem;
        margin-top: 1.2rem;
    }
    .sidebar-tip {
        background: var(--accent-soft);
        border-left: 3px solid var(--accent);
        border-radius: 0 8px 8px 0;
        padding: 0.6rem 0.8rem;
        font-size: 0.8rem;
        color: var(--text-secondary);
        line-height: 1.5;
    }

    /* ── Tab styling ── */
    div[data-testid="stTabs"] button {
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.88rem !important;
    }

    /* ── Divider ── */
    hr { border-color: var(--border); margin: 1.5rem 0; }

    /* ── Animations ── */
    @keyframes pulse-dot {
        0%, 100% { opacity: 1; }
        50%       { opacity: 0.3; }
    }
    .pulse { animation: pulse-dot 1.4s ease-in-out infinite; }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(8px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .fade-in { animation: fadeIn 0.4s ease forwards; }

    /* ── Stray Streamlit padding fix ── */
    div[data-testid="stVerticalBlock"] > div:has(> div.element-container > div.stMarkdown) {
        gap: 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# Session-state initialisation
# ─────────────────────────────────────────────────────────────────────────────
def _init_state():
    defaults = {
        "result": None,
        "chat_history": [],   # list of {"role": "user"|"assistant", "content": str}
        "processing": False,
        "error": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init_state()


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────
def _bullet_list(items_text: str, dot_class: str = "dot-purple") -> str:
    """Convert newline-separated lines into styled bullet HTML."""
    lines = [l.strip("•·- \t") for l in items_text.strip().splitlines() if l.strip()]
    html = ""
    for line in lines:
        if not line:
            continue
        # strip leading numbered markers like "1." "2)" etc.
        import re
        line = re.sub(r"^\d+[\.\)]\s*", "", line)
        if not line:
            continue
        html += (
            f'<div class="bullet-item">'
            f'<span class="bullet-dot {dot_class}"></span>'
            f'<span class="bullet-text">{line}</span>'
            f'</div>'
        )
    return html or f'<p style="color:var(--text-secondary);font-size:0.9rem">Nothing extracted.</p>'


def _word_count(text: str) -> int:
    return len(text.split()) if text else 0


def _run_pipeline(source: str, language: str):
    """Import and run the core pipeline, updating session state."""
    st.session_state["processing"] = True
    st.session_state["error"] = None
    st.session_state["result"] = None
    st.session_state["chat_history"] = []

    try:
        from utils.audio_processor import process_input
        from core.transcriber import transcribe_all
        from core.summarize import summarize, generate_title
        from core.extractor import extract_action_items, extract_key_decisions, extract_questions
        from core.rag_engine import build_rag_chain

        chunks = process_input(source)
        transcript = transcribe_all(chunks, language)
        title = generate_title(transcript)
        summary_text = summarize(transcript)
        action_item = extract_action_items(transcript)
        decisions = extract_key_decisions(transcript)
        questions_text = extract_questions(transcript)
        rag_chain = build_rag_chain(transcript)

        st.session_state["result"] = {
            "title": title,
            "transcript": transcript,
            "summary": summary_text,
            "action_items": action_item,
            "key_decisions": decisions,
            "open_questions": questions_text,
            "rag_chain": rag_chain,
        }
    except Exception as exc:
        st.session_state["error"] = str(exc)
    finally:
        st.session_state["processing"] = False


# ─────────────────────────────────────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        '<div style="font-size:1.4rem;font-weight:700;margin-bottom:0.1rem">🎬 AI Video<br>Assistant</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div style="font-size:0.78rem;color:var(--text-secondary);margin-bottom:1.4rem">'
        'Transcribe · Summarise · Chat</div>',
        unsafe_allow_html=True,
    )
    st.divider()

    st.markdown('<p class="sidebar-label">Source</p>', unsafe_allow_html=True)
    source_type = st.radio(
        "Input type",
        ["YouTube URL", "Local File"],
        label_visibility="collapsed",
        horizontal=True,
    )

    if source_type == "YouTube URL":
        source_input = st.text_input(
            "YouTube URL",
            placeholder="https://www.youtube.com/watch?v=...",
            label_visibility="collapsed",
        )
    else:
        uploaded = st.file_uploader(
            "Upload audio / video",
            type=["mp4", "mp3", "wav", "m4a", "webm", "mkv", "avi", "mov"],
            label_visibility="collapsed",
        )
        source_input = None
        if uploaded:
            import tempfile, os, pathlib
            suffix = pathlib.Path(uploaded.name).suffix
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
            tmp.write(uploaded.read())
            tmp.flush()
            source_input = tmp.name
            st.caption(f"📎 `{uploaded.name}`")

    st.markdown('<p class="sidebar-label">Language</p>', unsafe_allow_html=True)
    language_input = st.selectbox(
        "Language",
        ["english", "hinglish", "hindi", "spanish", "french", "german", "portuguese", "italian"],
        label_visibility="collapsed",
    )

    st.markdown('<br>', unsafe_allow_html=True)
    run_btn = st.button(
        "▶  Analyse",
        use_container_width=True,
        type="primary",
        disabled=st.session_state["processing"] or not source_input,
    )

    if st.session_state["result"]:
        st.divider()
        if st.button("🔄  New Analysis", use_container_width=True):
            st.session_state["result"] = None
            st.session_state["chat_history"] = []
            st.session_state["error"] = None
            st.rerun()

    st.divider()
    st.markdown(
        '<div class="sidebar-tip">'
        '💡 Supports YouTube links, MP4, MP3, WAV, M4A and more. '
        'Hinglish mode handles code-switched audio.'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown(
        '<div style="font-size:0.7rem;color:var(--text-secondary);text-align:center">'
        'Powered by Whisper · LangChain · RAG'
        '</div>',
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Trigger pipeline
# ─────────────────────────────────────────────────────────────────────────────
if run_btn and source_input:
    _run_pipeline(source_input, language_input)
    st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# Main area — hero
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    '<h1 class="hero-header">AI Video Meeting Assistant</h1>'
    '<p class="hero-sub">Drop a video, get instant insights — transcriptions, summaries, action items, and a conversational AI to chat with your content.</p>',
    unsafe_allow_html=True,
)

# ── Error state ───────────────────────────────────────────────────────────────
if st.session_state["error"]:
    st.error(f"⚠️ **Error:** {st.session_state['error']}")

# ── Processing state ──────────────────────────────────────────────────────────
if st.session_state["processing"]:
    st.markdown("---")
    steps = [
        ("🎧", "Downloading & chunking audio…"),
        ("📝", "Transcribing with Whisper…"),
        ("🏷️", "Generating title…"),
        ("📋", "Summarising…"),
        ("✅", "Extracting action items…"),
        ("🔑", "Extracting key decisions…"),
        ("❓", "Extracting open questions…"),
        ("🔗", "Building RAG index…"),
    ]
    progress_bar = st.progress(0)
    status_placeholder = st.empty()
    for i, (icon, label) in enumerate(steps):
        progress_bar.progress(int((i + 1) / len(steps) * 100))
        status_placeholder.markdown(
            f'<div class="status-step doing">'
            f'<span class="step-icon pulse">{icon}</span> {label}'
            f'</div>',
            unsafe_allow_html=True,
        )
        time.sleep(0.3)

# ── Empty / Landing state ─────────────────────────────────────────────────────
elif st.session_state["result"] is None and not st.session_state["error"]:
    col1, col2, col3 = st.columns(3)
    features = [
        ("🎙️", "Accurate Transcription", "Whisper-powered speech-to-text with multilingual support including Hinglish."),
        ("📋", "Smart Summaries", "AI-generated titles, concise summaries, action items, decisions & open questions."),
        ("💬", "Chat with Content", "RAG-powered chat lets you ask any question about the video in natural language."),
    ]
    for col, (icon, title, desc) in zip([col1, col2, col3], features):
        with col:
            st.markdown(
                f'<div class="glass-card fade-in" style="text-align:center;min-height:160px">'
                f'<div style="font-size:2.2rem;margin-bottom:0.6rem">{icon}</div>'
                f'<div style="font-weight:600;margin-bottom:0.5rem">{title}</div>'
                f'<div style="font-size:0.85rem;color:var(--text-secondary)">{desc}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown('<br>', unsafe_allow_html=True)
    st.info("👈  Paste a YouTube URL or upload a local file in the sidebar, then click **▶ Analyse**.")


# ─────────────────────────────────────────────────────────────────────────────
# Results
# ─────────────────────────────────────────────────────────────────────────────
elif st.session_state["result"]:
    result = st.session_state["result"]

    # ── Title banner ─────────────────────────────────────────────────────────
    st.markdown(
        f'<div class="glass-card fade-in" style="border-left: 4px solid var(--accent);padding: 1rem 1.4rem;">'
        f'<div class="card-title">Meeting Title</div>'
        f'<div style="font-size:1.35rem;font-weight:600">{result["title"]}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # ── Stats row ─────────────────────────────────────────────────────────────
    wc = _word_count(result["transcript"])
    import re
    ai_count = len([l for l in result["action_items"].splitlines() if l.strip()])
    kd_count = len([l for l in result["key_decisions"].splitlines() if l.strip()])
    oq_count = len([l for l in result["open_questions"].splitlines() if l.strip()])

    st.markdown(
        f'<div class="stats-row">'
        f'<div class="stat-box"><div class="stat-value">{wc:,}</div><div class="stat-label">Words</div></div>'
        f'<div class="stat-box"><div class="stat-value">{ai_count}</div><div class="stat-label">Action Items</div></div>'
        f'<div class="stat-box"><div class="stat-value">{kd_count}</div><div class="stat-label">Key Decisions</div></div>'
        f'<div class="stat-box"><div class="stat-value">{oq_count}</div><div class="stat-label">Open Questions</div></div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # ── Tabs ─────────────────────────────────────────────────────────────────
    tab_summary, tab_actions, tab_decisions, tab_questions, tab_transcript, tab_chat = st.tabs(
        ["📋 Summary", "✅ Action Items", "🔑 Key Decisions", "❓ Open Questions", "📄 Transcript", "💬 Chat"]
    )

    # ── Summary tab ──────────────────────────────────────────────────────────
    with tab_summary:
        st.markdown(
            f'<div class="glass-card fade-in">'
            f'<div class="card-title">Executive Summary</div>'
            f'<div class="card-content">{result["summary"]}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    # ── Action Items tab ─────────────────────────────────────────────────────
    with tab_actions:
        st.markdown(
            f'<div class="glass-card fade-in">'
            f'<div class="card-title">✅ Action Items</div>'
            f'{_bullet_list(result["action_items"], "dot-green")}'
            f'</div>',
            unsafe_allow_html=True,
        )

    # ── Key Decisions tab ────────────────────────────────────────────────────
    with tab_decisions:
        st.markdown(
            f'<div class="glass-card fade-in">'
            f'<div class="card-title">🔑 Key Decisions</div>'
            f'{_bullet_list(result["key_decisions"], "dot-amber")}'
            f'</div>',
            unsafe_allow_html=True,
        )

    # ── Open Questions tab ───────────────────────────────────────────────────
    with tab_questions:
        st.markdown(
            f'<div class="glass-card fade-in">'
            f'<div class="card-title">❓ Open Questions</div>'
            f'{_bullet_list(result["open_questions"], "dot-pink")}'
            f'</div>',
            unsafe_allow_html=True,
        )

    # ── Transcript tab ───────────────────────────────────────────────────────
    with tab_transcript:
        st.markdown(
            '<div class="card-title" style="margin-bottom:0.6rem">Raw Transcript</div>',
            unsafe_allow_html=True,
        )
        col_dl, _ = st.columns([1, 4])
        with col_dl:
            st.download_button(
                label="⬇ Download .txt",
                data=result["transcript"],
                file_name="transcript.txt",
                mime="text/plain",
                use_container_width=True,
            )
        st.markdown(
            f'<div class="transcript-box fade-in">{result["transcript"]}</div>',
            unsafe_allow_html=True,
        )

    # ── Chat tab ─────────────────────────────────────────────────────────────
    with tab_chat:
        st.markdown(
            '<div class="card-title" style="margin-bottom:0.4rem">💬 Chat with your Meeting</div>'
            '<div style="font-size:0.82rem;color:var(--text-secondary);margin-bottom:1rem">'
            'Ask anything about the video — the AI searches the full transcript to answer.</div>',
            unsafe_allow_html=True,
        )

        # render chat history
        chat_html = '<div class="chat-container" id="chat-scroll">'
        for msg in st.session_state["chat_history"]:
            if msg["role"] == "user":
                chat_html += (
                    f'<div class="bubble-user"><div class="msg">{msg["content"]}</div></div>'
                )
            else:
                chat_html += (
                    f'<div class="bubble-bot">'
                    f'<div class="avatar">🤖</div>'
                    f'<div class="msg">{msg["content"]}</div>'
                    f'</div>'
                )
        if not st.session_state["chat_history"]:
            chat_html += (
                '<div style="text-align:center;padding:2rem;color:var(--text-secondary);font-size:0.88rem">'
                '🔍 Start by asking a question about the meeting…'
                '</div>'
            )
        chat_html += '</div>'
        st.markdown(chat_html, unsafe_allow_html=True)

        # Input row
        chat_col, send_col = st.columns([5, 1])
        with chat_col:
            user_question = st.text_input(
                "Ask a question",
                placeholder="e.g. What were the main decisions made?",
                label_visibility="collapsed",
                key="chat_input",
            )
        with send_col:
            send_btn = st.button("Send →", use_container_width=True, type="primary")

        if send_btn and user_question.strip():
            from core.rag_engine import ask_question as _ask
            with st.spinner("Thinking…"):
                answer = _ask(result["rag_chain"], user_question.strip())
            st.session_state["chat_history"].append({"role": "user", "content": user_question.strip()})
            st.session_state["chat_history"].append({"role": "assistant", "content": answer})
            st.rerun()

        # Quick-ask suggestion chips
        if not st.session_state["chat_history"]:
            st.markdown('<div style="margin-top:0.6rem">', unsafe_allow_html=True)
            suggestions = [
                "What was the main topic discussed?",
                "Who were the key speakers?",
                "What decisions were finalised?",
                "List the follow-up tasks.",
            ]
            cols = st.columns(len(suggestions))
            for col, suggestion in zip(cols, suggestions):
                with col:
                    if st.button(suggestion, use_container_width=True, key=f"sug_{suggestion[:20]}"):
                        from core.rag_engine import ask_question as _ask
                        with st.spinner("Thinking…"):
                            answer = _ask(result["rag_chain"], suggestion)
                        st.session_state["chat_history"].append({"role": "user", "content": suggestion})
                        st.session_state["chat_history"].append({"role": "assistant", "content": answer})
                        st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
