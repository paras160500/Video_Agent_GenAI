import time
import streamlit as st
from dotenv import load_dotenv

from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarize import summarize, generate_title
from core.extractor import (
    extract_action_items,
    extract_key_decisions,
    extract_questions,
)
from core.rag_engine import build_rag_chain, ask_question

# =========================================================
# LOAD ENV
# =========================================================

load_dotenv()

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Meeting Assistant",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None

if "processed" not in st.session_state:
    st.session_state.processed = False

if "result" not in st.session_state:
    st.session_state.result = {}

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at top left, #1e3a8a 0%, transparent 30%),
        radial-gradient(circle at bottom right, #7c3aed 0%, transparent 30%),
        linear-gradient(135deg, #0f172a 0%, #111827 50%, #020617 100%);
    color: white;
}

/* Hide Streamlit Branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Main Title */
.main-title {
    font-size: 4rem;
    font-weight: 700;
    text-align: center;
    margin-top: 10px;
    background: linear-gradient(to right, #38bdf8, #8b5cf6, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.sub-title {
    text-align: center;
    color: #cbd5e1;
    margin-bottom: 40px;
    font-size: 1.1rem;
}

/* Cards */
.glass-card {
    background: rgba(255,255,255,0.07);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 24px;
    padding: 24px;
    margin-bottom: 24px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.35);
}

/* Section */
.section-title {
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 15px;
    color: white;
}

/* Metrics */
.metric-box {
    background: linear-gradient(
        135deg,
        rgba(59,130,246,0.15),
        rgba(139,92,246,0.15)
    );
    border-radius: 22px;
    padding: 24px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.08);
}

.metric-number {
    font-size: 2rem;
    font-weight: 700;
    color: #38bdf8;
}

.metric-label {
    color: #cbd5e1;
    margin-top: 8px;
}

/* Input Fields */
.stTextInput input {
    background: rgba(255,255,255,0.08) !important;
    color: white !important;
    border-radius: 14px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
}

/* Text Area */
.stTextArea textarea {
    background: rgba(255,255,255,0.08) !important;
    color: white !important;
    border-radius: 14px !important;
}

/* Buttons */
.stButton button {
    width: 100%;
    height: 52px;
    border-radius: 14px;
    border: none;
    font-weight: 600;
    color: white;
    background: linear-gradient(to right, #2563eb, #7c3aed);
    transition: 0.3s;
}

.stButton button:hover {
    transform: scale(1.02);
}

/* Chat */
.chat-user {
    background: rgba(59,130,246,0.18);
    padding: 16px;
    border-radius: 18px;
    margin-bottom: 14px;
    border-left: 4px solid #3b82f6;
}

.chat-ai {
    background: rgba(139,92,246,0.18);
    padding: 16px;
    border-radius: 18px;
    margin-bottom: 14px;
    border-left: 4px solid #8b5cf6;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="main-title">
    🎙️ AI Meeting Assistant
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="sub-title">
    Transcribe • Summarize • Extract Insights • Ask Questions using RAG AI
</div>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## ⚙️ Settings")

    language = st.selectbox(
        "Language",
        ["english", "hinglish"]
    )

    st.markdown("---")

    st.markdown("""
### 🚀 Features

- AI Transcription
- AI Summary
- Action Item Extraction
- Key Decisions
- Open Questions
- Chat with Meeting
- RAG AI Search
""")

# =========================================================
# INPUT
# =========================================================

st.markdown('<div class="glass-card">', unsafe_allow_html=True)

source = st.text_input(
    "🎥 Enter YouTube URL or Local File Path",
    placeholder="https://youtube.com/... OR /Users/file.mp3"
)

process_btn = st.button("🚀 Process Meeting")

st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# PROCESSING
# =========================================================

if process_btn:

    if not source.strip():
        st.error("Please enter a valid source.")
        st.stop()

    try:

        with st.spinner("⚡ Processing Meeting..."):

            progress = st.progress(0)

            # STEP 1
            st.info("🎧 Processing Audio...")
            chunks = process_input(source)
            progress.progress(20)

            # STEP 2
            st.info("🧠 Transcribing...")
            transcript = transcribe_all(
                chunks=chunks,
                language=language
            )
            progress.progress(40)

            # STEP 3
            st.info("✨ Generating AI Insights...")

            title = generate_title(transcript)
            summary = summarize(transcript)

            action_items = extract_action_items(transcript)
            key_decisions = extract_key_decisions(transcript)
            open_questions = extract_questions(transcript)

            progress.progress(70)

            # STEP 4
            st.info("🔍 Building RAG Engine...")
            rag_chain = build_rag_chain(transcript)

            progress.progress(100)

            # SAVE SESSION
            st.session_state.rag_chain = rag_chain
            st.session_state.processed = True

            st.session_state.result = {
                "title": title,
                "summary": summary,
                "transcript": transcript,
                "action_items": action_items,
                "key_decisions": key_decisions,
                "open_questions": open_questions,
            }

            time.sleep(1)

            st.success("✅ Meeting processed successfully!")

    except Exception as e:
        st.error(f"❌ ERROR: {str(e)}")

# =========================================================
# RESULTS
# =========================================================

if st.session_state.processed:

    result = st.session_state.result

    # TITLE
    st.markdown(f"""
    <div class="glass-card">
        <div class="section-title">📌 Meeting Title</div>
        <h2>{result['title']}</h2>
    </div>
    """, unsafe_allow_html=True)

    # METRICS
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-number">
                {len(result['transcript'].split())}
            </div>
            <div class="metric-label">
                Words
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-number">
                {len(str(result['action_items']).splitlines())}
            </div>
            <div class="metric-label">
                Action Items
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-number">
                {len(str(result['open_questions']).splitlines())}
            </div>
            <div class="metric-label">
                Questions
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # SUMMARY
    st.markdown(f"""
    <div class="glass-card">
        <div class="section-title">📋 Summary</div>
        <p>{result['summary']}</p>
    </div>
    """, unsafe_allow_html=True)

    # ACTIONS + DECISIONS
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class="glass-card">
            <div class="section-title">✅ Action Items</div>
            <p>{result['action_items']}</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="glass-card">
            <div class="section-title">🔑 Key Decisions</div>
            <p>{result['key_decisions']}</p>
        </div>
        """, unsafe_allow_html=True)

    # QUESTIONS
    st.markdown(f"""
    <div class="glass-card">
        <div class="section-title">❓ Open Questions</div>
        <p>{result['open_questions']}</p>
    </div>
    """, unsafe_allow_html=True)

    # TRANSCRIPT
    with st.expander("📜 Full Transcript"):

        st.text_area(
            "",
            value=result["transcript"],
            height=400
        )

    # =====================================================
    # CHAT SECTION
    # =====================================================

    st.markdown("""
    <div class="glass-card">
        <div class="section-title">
            💬 Chat with your Meeting
        </div>
    """, unsafe_allow_html=True)

    question = st.text_input(
        "Ask anything about the meeting...",
        key="question_input"
    )

    ask_btn = st.button("🤖 Ask AI")

    # =====================================================
    # ASK AI
    # =====================================================

    if ask_btn and question:

        with st.spinner("🤖 AI Thinking..."):

            try:

                answer = ask_question(
                    st.session_state.rag_chain,
                    question
                )

                # SAFETY FIX
                if answer is None:
                    answer = "I could not generate an answer."

                answer = str(answer)

            except Exception as e:
                answer = f"Error: {str(e)}"

            st.session_state.messages.append(
                ("user", question)
            )

            st.session_state.messages.append(
                ("assistant", answer)
            )

    # =====================================================
    # CHAT HISTORY
    # =====================================================

    for role, message in st.session_state.messages:

        if role == "user":

            st.markdown(f"""
            <div class="chat-user">
                <b>🧑 You:</b><br><br>
                {message}
            </div>
            """, unsafe_allow_html=True)

        else:

            st.markdown(f"""
            <div class="chat-ai">
                <b>🤖 Assistant:</b><br><br>
                {message}
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div style='text-align:center; color:#94a3b8; padding:20px;'>
    Built with ❤️ using Streamlit + AI
</div>
""", unsafe_allow_html=True)