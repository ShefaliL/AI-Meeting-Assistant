import os
import tempfile

import streamlit as st
from dotenv import load_dotenv

from main import run_pipeline
from core.rag import ask_question

load_dotenv()

st.set_page_config(page_title="AI Video Assistant", layout="wide")

# ---------------------------------------------------------------- theme
ACCENT = "#ef9f27"   # amber — primary
MUTED = "#9a948a"
CARD = "#201e1a"
LINE = "#2f2b26"

# secondary hues, used sparingly to distinguish sections
GREEN = "#97c459"
BLUE = "#7fb2e5"
VIOLET = "#a99ee8"

BODY = 19       # base text size in px
COLUMN = 1050   # content width in px

st.markdown(
    f"""
    <style>
      #MainMenu, footer, header {{visibility: hidden;}}

      .block-container {{max-width: {COLUMN}px; padding: 4rem 2rem 6rem;}}

      /* body text */
      .stMarkdown, .stMarkdown p, .stMarkdown li {{
        font-size: {BODY}px; line-height: 1.8;
      }}
      .stMarkdown p {{margin-bottom: 1rem;}}
      .stMarkdown li {{margin-bottom: .5rem;}}
      .stMarkdown ul, .stMarkdown ol {{padding-left: 1.6rem; margin: .8rem 0 1.4rem;}}
      .stMarkdown h1 {{font-size: {BODY + 13}px; font-weight: 500; margin: 2rem 0 1rem;}}
      .stMarkdown h2 {{font-size: {BODY + 7}px; font-weight: 500; margin: 2rem 0 .9rem;}}
      .stMarkdown h3 {{font-size: {BODY + 3}px; font-weight: 500; margin: 1.6rem 0 .8rem;}}

      /* masthead */
      .masthead {{
        border-left: 3px solid {ACCENT}; padding-left: 1.25rem; margin-bottom: 3.5rem;
      }}
      .masthead h1 {{margin: 0; font-size: {BODY + 13}px; font-weight: 500;}}
      .masthead p {{margin: .6rem 0 0; font-size: {BODY}px; color: {MUTED};}}

      /* document heading */
      .doc-title {{font-size: {BODY + 7}px; font-weight: 500; margin: 0 0 .5rem;}}
      .doc-sub {{
        font-size: {BODY - 4}px; color: {MUTED}; margin: 0 0 2.5rem;
        overflow-wrap: anywhere;
      }}

      /* cards */
      .card {{
        background: {CARD}; border-radius: 12px;
        padding: 1.75rem 2rem; margin-bottom: 1.5rem;
      }}
      .card h4 {{
        margin: 0 0 1.1rem; font-size: {BODY - 5}px; font-weight: 500;
        letter-spacing: .12em; text-transform: uppercase; color: {ACCENT};
        display: flex; align-items: center; gap: .6rem;
      }}
      .card h4::before {{
        content: ""; width: 7px; height: 7px; border-radius: 50%;
        background: currentColor;
      }}
      .card p, .card li {{font-size: {BODY}px; line-height: 1.8; margin: 0 0 .65rem;}}

      /* metrics */
      .stat {{
        background: {CARD}; border-radius: 12px; padding: 1.1rem 1.4rem 1.2rem;
      }}
      .stat-label {{
        margin: 0 0 .35rem; font-size: {BODY - 6}px; font-weight: 500;
        letter-spacing: .12em; text-transform: uppercase;
        display: flex; align-items: center; gap: .5rem;
      }}
      .stat-label::before {{
        content: ""; width: 6px; height: 6px; border-radius: 50%;
        background: currentColor;
      }}
      .stat-value {{margin: 0; font-size: {BODY + 9}px; font-weight: 500;}}

      /* tabs — match the button and everything inside it */
      .stTabs [data-baseweb="tab-list"] {{
        gap: 2.5rem !important; border-bottom: 1px solid {LINE}; margin-bottom: 2.75rem;
      }}
      .stTabs [data-baseweb="tab"] {{
        height: auto; padding: 0 0 1rem !important;
        background: transparent !important; border: none !important;
      }}
      .stTabs button[role="tab"] * {{
        font-size: {BODY + 3}px !important; font-weight: 500 !important;
        color: {MUTED} !important;
      }}
      .stTabs button[role="tab"]:hover * {{color: #d7d2c8 !important;}}
      .stTabs button[role="tab"][aria-selected="true"] * {{color: {ACCENT} !important;}}
      .stTabs [data-baseweb="tab-highlight"] {{
        background: {ACCENT}; height: 3px; border-radius: 999px;
      }}
      .stTabs [data-baseweb="tab-border"] {{display: none;}}

      /* controls */
      div.stButton > button, div.stDownloadButton > button {{
        border-radius: 8px; padding: .55rem 1rem;
      }}
      div.stButton > button p, div.stDownloadButton > button p {{
        font-size: {BODY - 3}px; font-weight: 500;
      }}
      [data-testid="stWidgetLabel"] p {{font-size: {BODY - 4}px; color: {MUTED};}}
      .stTextInput input, .stSelectbox div[data-baseweb="select"], .stRadio label p {{
        font-size: {BODY - 3}px;
      }}
      [data-testid="stChatInput"] textarea {{font-size: {BODY - 2}px;}}

      /* sidebar */
      section[data-testid="stSidebar"] {{border-right: 1px solid {LINE};}}
      section[data-testid="stSidebar"] .block-container {{padding: 3rem 1.5rem;}}
      .side-head {{
        font-size: {BODY - 5}px; font-weight: 500; letter-spacing: .12em;
        text-transform: uppercase; color: {MUTED}; margin: 0 0 1.75rem;
      }}

      /* transcript */
      .transcript {{
        max-height: 560px; overflow-y: auto;
        font-size: {BODY - 2}px; line-height: 1.9; white-space: pre-wrap;
      }}

      /* chat */
      .qa {{margin-bottom: 2.75rem;}}
      .qa .q {{
        font-size: {BODY}px; font-weight: 500; margin: 0 0 1rem;
        padding-left: 1.1rem; border-left: 2px solid {ACCENT};
      }}
      .qa .a {{
        font-size: {BODY}px; line-height: 1.85; color: #ddd8ce;
        margin: 0; padding-left: 1.1rem; border-left: 2px solid {LINE};
      }}
      .qa .pending {{
        color: {MUTED}; font-style: normal;
        padding-left: 1.1rem; border-left: 2px solid {LINE}; margin: 0;
      }}
      .empty {{color: {MUTED}; font-size: {BODY}px; margin-bottom: 1.5rem;}}
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------- helpers
def md(text: str) -> str:
    """Escape dollar signs so Streamlit doesn't parse them as LaTeX."""
    return str(text).replace("$", "\\$")


def html(text: str) -> str:
    """Same, for text going into a raw HTML block."""
    return str(text).replace("$", "&#36;")


def card(title: str, body: str, color: str = ACCENT):
    st.markdown(
        f'<div class="card"><h4 style="color:{color}">{title}</h4>{html(body)}</div>',
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------- state
for key, default in [("result", None), ("qa", []), ("source_label", "")]:
    st.session_state.setdefault(key, default)


# ---------------------------------------------------------------- sidebar
with st.sidebar:
    st.markdown('<p class="side-head">Input</p>', unsafe_allow_html=True)

    mode = st.radio("Source", ["YouTube URL", "Upload file"], horizontal=True)

    source = None
    label = ""

    if mode == "YouTube URL":
        url = st.text_input("Video URL", placeholder="https://youtube.com/watch?v=...")
        source = url.strip() or None
        label = url.strip()
    else:
        upload = st.file_uploader(
            "Audio or video file",
            type=["mp3", "wav", "m4a", "mp4", "mkv", "mov", "webm", "aac", "flac"],
        )
        if upload:
            label = upload.name
            source = os.path.join(tempfile.mkdtemp(), upload.name)
            with open(source, "wb") as f:
                f.write(upload.getbuffer())

    language = st.selectbox("Language", ["english", "hinglish"])

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
    run = st.button("Process", type="primary", use_container_width=True)

    if st.session_state.result:
        st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)
        if st.button("Clear session", use_container_width=True):
            st.session_state.result = None
            st.session_state.qa = []
            st.rerun()


# ---------------------------------------------------------------- header
st.markdown(
    """
    <div class="masthead">
      <h1>AI Video Assistant</h1>
      <p>Turn any meeting, lecture or video into a searchable record &mdash;
         a full transcript, a written summary, the decisions and action items
         that came out of it, and an assistant that answers questions from
         what was actually said.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------- run
if run:
    if not source:
        st.warning("Add a YouTube URL or upload a file first.")
    else:
        try:
            with st.status("Working on it", expanded=True) as status:
                st.write("Downloading and chunking audio")
                st.write("Transcribing")
                st.write("Summarizing and extracting insights")
                result = run_pipeline(source, language)
                status.update(label="Done", state="complete", expanded=False)

            st.session_state.result = result
            st.session_state.qa = []
            st.session_state.source_label = label
            st.rerun()
        except Exception as e:
            st.error(f"Something went wrong: {e}")


# ---------------------------------------------------------------- empty state
result = st.session_state.result

if not result:
    st.markdown(
        '<p class="empty">Add a video source in the sidebar and press Process to begin.</p>',
        unsafe_allow_html=True,
    )
    for title, desc, color in [
        ("Summary", "A clean overview of everything that was discussed.", ACCENT),
        ("Insights", "Action items, decisions and open questions, pulled out.", GREEN),
        ("Ask AI", "Ask anything about the video, answered from the transcript.", VIOLET),
    ]:
        card(title, f"<p>{desc}</p>", color)
    st.stop()


# ---------------------------------------------------------------- results
st.markdown(f'<p class="doc-title">{html(result["title"])}</p>', unsafe_allow_html=True)

if st.session_state.source_label:
    st.markdown(
        f'<p class="doc-sub">{st.session_state.source_label}</p>',
        unsafe_allow_html=True,
    )

words = len(result["transcript"].split())

stats = [
    ("Words", f"{words:,}", ACCENT),
    ("Read time", f"{max(1, words // 200)} min", BLUE),
    ("Language", language.title(), VIOLET),
]

for col, (label_text, value, color) in zip(st.columns(3, gap="medium"), stats):
    col.markdown(
        f'<div class="stat"><p class="stat-label" style="color:{color}">'
        f"{label_text}</p><p class=\"stat-value\">{value}</p></div>",
        unsafe_allow_html=True,
    )

st.markdown("<div style='height:2.5rem'></div>", unsafe_allow_html=True)

tab_summary, tab_insights, tab_transcript, tab_chat = st.tabs(
    ["Summary", "Insights", "Transcript", "Ask AI"]
)

with tab_summary:
    st.markdown(md(result["summary"]))

with tab_insights:
    card("Action items", result["action_items"], GREEN)
    card("Key decisions", result["key_decisions"], BLUE)
    card("Open questions", result["open_questions"], VIOLET)

with tab_transcript:
    st.download_button(
        "Download transcript",
        result["transcript"],
        file_name=f"{result['title'][:60].replace('/', '-')}.txt",
    )
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.markdown(
        f'<div class="card transcript">{html(result["transcript"])}</div>',
        unsafe_allow_html=True,
    )

with tab_chat:
    if not st.session_state.qa:
        st.markdown(
            '<p class="empty">Ask anything about this video. '
            "Answers come from the transcript, not from outside knowledge.</p>",
            unsafe_allow_html=True,
        )

    # render the full thread; the newest entry may still be awaiting an answer
    pending_slot = None
    for question, answer in st.session_state.qa:
        st.markdown(
            f'<div class="qa"><p class="q">{html(question)}</p>',
            unsafe_allow_html=True,
        )
        if answer is None:
            pending_slot = st.empty()
            pending_slot.markdown(
                '<p class="pending">Thinking…</p>', unsafe_allow_html=True
            )
        else:
            st.markdown(f'<p class="a">{html(answer)}</p>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    prompt = st.chat_input("Ask something about this video")

    if prompt:
        st.session_state.qa.append((prompt, None))
        st.rerun()

    # answer the pending question in place, with the question still on screen
    if pending_slot is not None:
        question = st.session_state.qa[-1][0]
        try:
            answer = ask_question(result["rag_chain"], question)
        except Exception as e:
            answer = f"Couldn't answer that: {e}"

        st.session_state.qa[-1] = (question, answer)
        pending_slot.markdown(
            f'<p class="a">{html(answer)}</p>', unsafe_allow_html=True
        )