"""
LoreSnap - AI Visual Intelligence Fusion Tool
Combines: StudySnap + Meme Generator + Story Generator + Diagram Explainer
Upload any image → Get a full lore universe: story, characters, diagram breakdown,
meme captions, study flashcards, and an interactive narrative.
"""

import streamlit as st
import anthropic
import base64
import json
import time
from pathlib import Path
from PIL import Image
import io

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="LoreSnap ✦ Visual Intelligence Engine",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────
# STYLES
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,400&family=Space+Mono:wght@400;700&family=Inter:wght@300;400;500&display=swap');

:root {
    --bg: #07080f;
    --surface: #0f1020;
    --surface2: #161828;
    --accent: #6c63ff;
    --accent2: #ff6584;
    --gold: #f5c842;
    --text: #e8e6ff;
    --muted: #6b7280;
    --border: #1e2040;
}

.stApp {
    background: var(--bg) !important;
    color: var(--text) !important;
}

/* Hide default streamlit elements */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem !important; max-width: 1100px !important; }

/* Hero Header */
.loresnap-hero {
    text-align: center;
    padding: 3rem 0 2rem;
    position: relative;
}
.loresnap-title {
    font-family: 'Playfair Display', serif;
    font-size: 5rem;
    font-weight: 700;
    background: linear-gradient(135deg, #6c63ff 0%, #ff6584 50%, #f5c842 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -2px;
    line-height: 1;
    margin-bottom: 0.5rem;
}
.loresnap-subtitle {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 4px;
    color: var(--muted);
    text-transform: uppercase;
}
.loresnap-tagline {
    font-family: 'Inter', sans-serif;
    font-size: 1.05rem;
    color: #9ca3af;
    margin-top: 0.75rem;
    font-weight: 300;
}

/* Upload area */
.upload-zone {
    border: 2px dashed #2a2d55;
    border-radius: 12px;
    padding: 2.5rem;
    text-align: center;
    background: var(--surface);
    transition: all 0.3s ease;
    margin: 1rem 0;
}

/* Mode cards */
.mode-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0.75rem;
    margin: 1rem 0;
}
.mode-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    cursor: pointer;
    transition: all 0.2s;
}
.mode-card:hover {
    border-color: var(--accent);
    background: rgba(108, 99, 255, 0.08);
}
.mode-card.active {
    border-color: var(--accent);
    background: rgba(108, 99, 255, 0.12);
}
.mode-icon { font-size: 1.6rem; margin-bottom: 0.3rem; }
.mode-name {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    font-weight: 700;
    color: var(--text);
    text-transform: uppercase;
    letter-spacing: 1px;
}
.mode-desc { font-size: 0.72rem; color: var(--muted); margin-top: 0.2rem; line-height: 1.4; }

/* Result cards */
.result-section {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.25rem;
    position: relative;
    overflow: hidden;
}
.result-section::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
}
.section-badge {
    display: inline-block;
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 0.75rem;
    padding: 3px 10px;
    border: 1px solid var(--accent);
    border-radius: 20px;
}
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    color: var(--text);
    margin-bottom: 0.5rem;
    font-weight: 700;
}
.section-body {
    font-family: 'Inter', sans-serif;
    font-size: 0.9rem;
    color: #c4c6e0;
    line-height: 1.75;
}

/* Meme box */
.meme-box {
    background: #0a0b17;
    border: 1px solid #2a2d55;
    border-radius: 10px;
    padding: 1.5rem;
    text-align: center;
    margin: 0.75rem 0;
}
.meme-top {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: #f5c842;
    text-transform: uppercase;
    letter-spacing: -0.5px;
    margin-bottom: 0.5rem;
}
.meme-bottom {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: #ff6584;
    text-transform: uppercase;
    letter-spacing: -0.5px;
}

/* Flashcards */
.flashcard {
    background: #0a0b17;
    border: 1px solid #2a2d55;
    border-radius: 8px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.6rem;
    cursor: pointer;
    transition: all 0.2s;
}
.flashcard:hover { border-color: var(--accent); }
.flashcard-q {
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    color: var(--accent);
    margin-bottom: 0.5rem;
    font-weight: 700;
}
.flashcard-a {
    font-family: 'Inter', sans-serif;
    font-size: 0.85rem;
    color: #e8e6ff;
    line-height: 1.5;
}

/* Character cards */
.char-card {
    background: #0a0b17;
    border: 1px solid #2a2d55;
    border-radius: 10px;
    padding: 1.1rem 1.3rem;
    margin-bottom: 0.6rem;
    border-left: 3px solid var(--accent2);
}
.char-name {
    font-family: 'Playfair Display', serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: #ff6584;
    margin-bottom: 0.2rem;
}
.char-role {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 0.5rem;
}
.char-desc { font-size: 0.83rem; color: #c4c6e0; line-height: 1.5; }

/* Concept pills */
.concept-pill {
    display: inline-block;
    background: rgba(108, 99, 255, 0.12);
    border: 1px solid rgba(108, 99, 255, 0.35);
    color: #c4b5fd;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-family: 'Space Mono', monospace;
    margin: 3px;
}

/* Diagram steps */
.diagram-step {
    display: flex;
    gap: 1rem;
    align-items: flex-start;
    margin-bottom: 0.75rem;
}
.step-num {
    width: 28px;
    height: 28px;
    min-width: 28px;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    font-weight: 700;
    color: white;
}
.step-text { font-size: 0.87rem; color: #c4c6e0; line-height: 1.5; padding-top: 4px; }

/* Generate button */
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #6c63ff, #ff6584) !important;
    color: white !important;
    border: none !important;
    padding: 0.85rem 2rem !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.85rem !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    border-radius: 8px !important;
    transition: all 0.2s !important;
    cursor: pointer !important;
}
.stButton > button:hover {
    opacity: 0.9 !important;
    transform: translateY(-1px) !important;
}
.stButton > button:disabled {
    background: #1e2040 !important;
    color: #4b5563 !important;
}

/* Radio buttons as mode selector */
.stRadio > label { display: none !important; }
.stRadio > div { display: flex !important; gap: 0.5rem !important; flex-wrap: wrap !important; }
.stRadio > div > label {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    padding: 0.5rem 1rem !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.72rem !important;
    color: var(--muted) !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
}
.stRadio > div > label:has(input:checked) {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
    background: rgba(108, 99, 255, 0.1) !important;
}

/* File uploader */
.stFileUploader > div {
    background: var(--surface) !important;
    border: 2px dashed #2a2d55 !important;
    border-radius: 10px !important;
}
.stFileUploader label {
    color: var(--muted) !important;
    font-family: 'Inter', sans-serif !important;
}

/* Spinner */
.stSpinner > div { border-top-color: var(--accent) !important; }

/* Divider */
hr { border-color: var(--border) !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: var(--surface) !important;
    border-radius: 8px !important;
    padding: 4px !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--muted) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 1px !important;
    border-radius: 6px !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #6c63ff, #ff6584) !important;
    color: white !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: transparent !important;
    padding: 1rem 0 !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: #2a2d55; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────
def image_to_base64(img_bytes: bytes) -> str:
    return base64.b64encode(img_bytes).decode("utf-8")


def get_media_type(filename: str) -> str:
    ext = Path(filename).suffix.lower()
    return {"jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png",
            ".gif": "image/gif", ".webp": "image/webp"}.get(ext, "image/jpeg")


def call_claude(image_b64: str, media_type: str, prompt: str) -> dict:
    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2500,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": image_b64}},
                {"type": "text", "text": prompt}
            ]
        }]
    )
    raw = response.content[0].text.strip()
    # Strip markdown fences if present
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1] if "\n" in raw else raw
        raw = raw.rsplit("```", 1)[0]
    return json.loads(raw)


def build_prompt(mode: str) -> str:
    base = """Analyze this image carefully. Respond ONLY with a valid JSON object — no markdown, no preamble, no explanation outside the JSON.

"""
    prompts = {
        "🌌 LoreSnap (Full Universe)": base + """Generate a complete creative intelligence report. Return:
{
  "universe_name": "a dramatic name for the 'world' depicted in this image",
  "lore_summary": "a 3-4 sentence epic narrative framing this image as a story world or lore (educational or visual content becomes mythology)",
  "characters": [
    {"name": "character name derived from a concept/object/person in the image", "role": "their role in the lore", "description": "1-2 sentences about them"},
    {"name": "...", "role": "...", "description": "..."},
    {"name": "...", "role": "...", "description": "..."}
  ],
  "diagram_breakdown": {
    "title": "what this image is about",
    "steps": ["step 1 explanation", "step 2 explanation", "step 3 explanation", "step 4 explanation"]
  },
  "meme": {
    "top": "meme top text (short, punchy, uppercase worthy)",
    "bottom": "meme punchline (the twist)"
  },
  "flashcards": [
    {"q": "question about a key concept", "a": "clear answer"},
    {"q": "question", "a": "answer"},
    {"q": "question", "a": "answer"}
  ],
  "key_concepts": ["concept1", "concept2", "concept3", "concept4", "concept5"],
  "story_opening": "the first 2-3 sentences of a short story inspired by this image (any genre)",
  "exam_question": "one insightful exam question this image could generate",
  "plot_twist": "a shocking but educational plot twist that connects the visual content to a deeper truth"
}""",

        "📖 Story Mode": base + """Turn this image into story material. Return:
{
  "title": "dramatic story title",
  "genre": "detected or suggested genre",
  "opening": "compelling 4-5 sentence story opening inspired by the image",
  "characters": [
    {"name": "character name", "role": "protagonist/antagonist/mentor etc.", "description": "brief description"},
    {"name": "...", "role": "...", "description": "..."}
  ],
  "world_description": "2-3 sentences describing the story world",
  "conflict": "the central conflict of the story",
  "plot_twist": "a surprising plot twist",
  "closing_hook": "a cliffhanger sentence to end the opening chapter"
}""",

        "🎭 Meme Mode": base + """Generate viral meme content from this image. Return:
{
  "main_meme": {"top": "top text", "bottom": "bottom punchline"},
  "alt_memes": [
    {"style": "Sarcastic", "top": "...", "bottom": "..."},
    {"style": "Wholesome", "top": "...", "bottom": "..."},
    {"style": "Gen Z", "top": "...", "bottom": "..."},
    {"style": "Deep Thought", "top": "...", "bottom": "..."}
  ],
  "caption": "a short social media caption for this image",
  "hashtags": ["hashtag1", "hashtag2", "hashtag3", "hashtag4", "hashtag5"],
  "roast": "a savage but funny one-liner about what's happening in this image"
}""",

        "🧠 Study Mode": base + """Extract structured learning material from this image. Return:
{
  "topic": "main topic of the image",
  "summary": "3-4 sentence educational summary of all content visible",
  "key_concepts": ["concept1", "concept2", "concept3", "concept4", "concept5"],
  "flashcards": [
    {"q": "question", "a": "answer"},
    {"q": "question", "a": "answer"},
    {"q": "question", "a": "answer"},
    {"q": "question", "a": "answer"}
  ],
  "diagram_steps": ["step 1", "step 2", "step 3", "step 4"],
  "exam_questions": ["question 1", "question 2", "question 3"],
  "study_tip": "a specific study tip based on this content",
  "difficulty": "Beginner / Intermediate / Advanced"
}""",

        "🔍 Diagram Mode": base + """Explain this diagram or visual in detail. Return:
{
  "diagram_type": "what kind of diagram/chart/image this is",
  "title": "title or topic",
  "overview": "2-3 sentence plain-language explanation of what this shows",
  "components": [
    {"name": "component name", "description": "what it does or represents"},
    {"name": "...", "description": "..."},
    {"name": "...", "description": "..."}
  ],
  "step_by_step": ["step 1 explanation", "step 2", "step 3", "step 4"],
  "key_insight": "the most important thing to understand from this diagram",
  "common_misconception": "a common mistake people make about this topic",
  "real_world_example": "a real-world analogy or application"
}"""
    }
    return prompts[mode]


# ─────────────────────────────────────────
# RENDER RESULTS
# ─────────────────────────────────────────
def render_loresnap(data: dict):
    # Universe header
    st.markdown(f"""
    <div class="result-section">
        <span class="section-badge">✦ Universe Discovered</span>
        <div class="section-title">{data.get('universe_name', 'Unknown Realm')}</div>
        <div class="section-body">{data.get('lore_summary', '')}</div>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        # Characters
        st.markdown('<div class="result-section"><span class="section-badge">⚔ Characters</span>', unsafe_allow_html=True)
        for c in data.get("characters", []):
            st.markdown(f"""
            <div class="char-card">
                <div class="char-name">{c['name']}</div>
                <div class="char-role">{c['role']}</div>
                <div class="char-desc">{c['description']}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Meme
        meme = data.get("meme", {})
        st.markdown(f"""
        <div class="result-section">
            <span class="section-badge">🎭 The Meme</span>
            <div class="meme-box">
                <div class="meme-top">{meme.get('top', '')}</div>
                <div style="color: #4b5563; font-size: 0.7rem; margin: 0.4rem 0; font-family: 'Space Mono', monospace;">[ image ]</div>
                <div class="meme-bottom">{meme.get('bottom', '')}</div>
            </div>
        </div>""", unsafe_allow_html=True)

        # Story opening
        st.markdown(f"""
        <div class="result-section">
            <span class="section-badge">📖 Story Opening</span>
            <div class="section-body" style="font-style: italic; color: #d1d5db;">"{data.get('story_opening', '')}"</div>
        </div>""", unsafe_allow_html=True)

    with col2:
        # Diagram breakdown
        diagram = data.get("diagram_breakdown", {})
        st.markdown(f'<div class="result-section"><span class="section-badge">🔍 Visual Breakdown</span><div style="font-family: \'Space Mono\', monospace; font-size: 0.8rem; color: #c4b5fd; margin-bottom: 0.75rem;">{diagram.get("title", "")}</div>', unsafe_allow_html=True)
        for i, step in enumerate(diagram.get("steps", []), 1):
            st.markdown(f"""
            <div class="diagram-step">
                <div class="step-num">{i}</div>
                <div class="step-text">{step}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Flashcards
        st.markdown('<div class="result-section"><span class="section-badge">🃏 Flashcards</span>', unsafe_allow_html=True)
        for fc in data.get("flashcards", []):
            st.markdown(f"""
            <div class="flashcard">
                <div class="flashcard-q">Q: {fc['q']}</div>
                <div class="flashcard-a">↳ {fc['a']}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Bottom row: concepts, exam Q, plot twist
    concepts_html = "".join(f'<span class="concept-pill">{c}</span>' for c in data.get("key_concepts", []))
    st.markdown(f"""
    <div class="result-section">
        <span class="section-badge">🧠 Key Concepts</span><br><br>
        {concepts_html}
    </div>""", unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown(f"""
        <div class="result-section">
            <span class="section-badge">📝 Exam Question</span>
            <div class="section-body">{data.get('exam_question', '')}</div>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="result-section" style="border-left: 3px solid #f5c842;">
            <span class="section-badge" style="color: #f5c842; border-color: #f5c842;">⚡ Plot Twist</span>
            <div class="section-body" style="font-style: italic;">{data.get('plot_twist', '')}</div>
        </div>""", unsafe_allow_html=True)


def render_story(data: dict):
    st.markdown(f"""
    <div class="result-section">
        <span class="section-badge">📖 {data.get('genre', 'Story')}</span>
        <div class="section-title">{data.get('title', '')}</div>
        <div class="section-body" style="font-style: italic; font-size: 1rem; line-height: 1.9;">"{data.get('opening', '')}"</div>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="result-section"><span class="section-badge">⚔ Characters</span>', unsafe_allow_html=True)
        for c in data.get("characters", []):
            st.markdown(f"""
            <div class="char-card">
                <div class="char-name">{c['name']}</div>
                <div class="char-role">{c['role']}</div>
                <div class="char-desc">{c['description']}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="result-section">
            <span class="section-badge">🌍 World</span>
            <div class="section-body">{data.get('world_description', '')}</div>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="result-section">
            <span class="section-badge">⚡ Central Conflict</span>
            <div class="section-body">{data.get('conflict', '')}</div>
        </div>
        <div class="result-section" style="border-left: 3px solid #f5c842;">
            <span class="section-badge" style="color: #f5c842; border-color: #f5c842;">🌀 Plot Twist</span>
            <div class="section-body" style="font-style: italic;">{data.get('plot_twist', '')}</div>
        </div>
        <div class="result-section" style="border-left: 3px solid #ff6584;">
            <span class="section-badge" style="color: #ff6584; border-color: #ff6584;">🪝 Closing Hook</span>
            <div class="section-body" style="font-style: italic; font-size: 1.05rem;">"{data.get('closing_hook', '')}"</div>
        </div>""", unsafe_allow_html=True)


def render_meme(data: dict):
    main = data.get("main_meme", {})
    st.markdown(f"""
    <div class="result-section">
        <span class="section-badge">🎭 Hero Meme</span>
        <div class="meme-box" style="padding: 2rem;">
            <div class="meme-top" style="font-size: 1.8rem;">{main.get('top', '')}</div>
            <div style="color: #4b5563; font-size: 0.7rem; margin: 0.6rem 0; font-family: 'Space Mono', monospace;">[ your image here ]</div>
            <div class="meme-bottom" style="font-size: 1.8rem;">{main.get('bottom', '')}</div>
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="result-section"><span class="section-badge">🎨 Alt Styles</span><br><br>', unsafe_allow_html=True)
    cols = st.columns(2)
    for i, alt in enumerate(data.get("alt_memes", [])):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="meme-box" style="margin: 0 0 0.6rem;">
                <div style="font-family: 'Space Mono', monospace; font-size: 0.65rem; color: var(--muted); margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 2px;">{alt.get('style','')}</div>
                <div style="font-size: 1rem; font-weight: 700; color: #f5c842; text-transform: uppercase; font-family: 'Playfair Display', serif;">{alt.get('top','')}</div>
                <div style="font-size: 1rem; font-weight: 700; color: #ff6584; text-transform: uppercase; font-family: 'Playfair Display', serif; margin-top: 0.4rem;">{alt.get('bottom','')}</div>
            </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        hashtags = " ".join(f"#{h.strip('#')}" for h in data.get("hashtags", []))
        st.markdown(f"""
        <div class="result-section">
            <span class="section-badge">📱 Caption</span>
            <div class="section-body">{data.get('caption', '')}</div>
            <div style="color: #6c63ff; font-size: 0.82rem; margin-top: 0.75rem; font-family: 'Space Mono', monospace;">{hashtags}</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="result-section" style="border-left: 3px solid #ff6584;">
            <span class="section-badge" style="color: #ff6584; border-color: #ff6584;">🔥 Roast</span>
            <div class="section-body" style="font-style: italic;">{data.get('roast', '')}</div>
        </div>""", unsafe_allow_html=True)


def render_study(data: dict):
    diff_color = {"Beginner": "#22c55e", "Intermediate": "#f5c842", "Advanced": "#ff6584"}.get(data.get("difficulty", ""), "#6c63ff")
    st.markdown(f"""
    <div class="result-section">
        <span class="section-badge">🧠 {data.get('topic', 'Study Analysis')}</span>
        <div style="float: right; font-family: 'Space Mono', monospace; font-size: 0.7rem; color: {diff_color}; padding: 3px 10px; border: 1px solid {diff_color}; border-radius: 20px;">{data.get('difficulty', '')}</div>
        <div class="section-body" style="margin-top: 0.5rem;">{data.get('summary', '')}</div>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="result-section"><span class="section-badge">🃏 Flashcards</span>', unsafe_allow_html=True)
        for fc in data.get("flashcards", []):
            st.markdown(f"""
            <div class="flashcard">
                <div class="flashcard-q">Q: {fc['q']}</div>
                <div class="flashcard-a">↳ {fc['a']}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="result-section"><span class="section-badge">🔍 Visual Steps</span>', unsafe_allow_html=True)
        for i, step in enumerate(data.get("diagram_steps", []), 1):
            st.markdown(f"""
            <div class="diagram-step">
                <div class="step-num">{i}</div>
                <div class="step-text">{step}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="result-section"><span class="section-badge">📝 Exam Questions</span>', unsafe_allow_html=True)
        for i, q in enumerate(data.get("exam_questions", []), 1):
            st.markdown(f'<div class="section-body" style="margin-bottom: 0.5rem;"><strong style="color: #6c63ff;">{i}.</strong> {q}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    concepts_html = "".join(f'<span class="concept-pill">{c}</span>' for c in data.get("key_concepts", []))
    st.markdown(f"""
    <div class="result-section">
        <span class="section-badge">💡 Key Concepts</span><br><br>{concepts_html}
        <div style="margin-top: 1rem; padding: 0.75rem; background: rgba(245,200,66,0.07); border-radius: 8px; border-left: 3px solid #f5c842;">
            <span style="font-size: 0.7rem; color: #f5c842; font-family: 'Space Mono', monospace; text-transform: uppercase; letter-spacing: 2px;">Study Tip</span>
            <div class="section-body" style="margin-top: 0.4rem;">{data.get('study_tip', '')}</div>
        </div>
    </div>""", unsafe_allow_html=True)


def render_diagram(data: dict):
    st.markdown(f"""
    <div class="result-section">
        <span class="section-badge">🔍 {data.get('diagram_type', 'Diagram Analysis')}</span>
        <div class="section-title">{data.get('title', '')}</div>
        <div class="section-body">{data.get('overview', '')}</div>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="result-section"><span class="section-badge">🧩 Components</span>', unsafe_allow_html=True)
        for comp in data.get("components", []):
            st.markdown(f"""
            <div class="char-card" style="border-left-color: #6c63ff;">
                <div class="char-name" style="color: #c4b5fd;">{comp['name']}</div>
                <div class="char-desc">{comp['description']}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="result-section"><span class="section-badge">📋 Step-by-Step</span>', unsafe_allow_html=True)
        for i, step in enumerate(data.get("step_by_step", []), 1):
            st.markdown(f"""
            <div class="diagram-step">
                <div class="step-num">{i}</div>
                <div class="step-text">{step}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="result-section" style="border-left: 3px solid #6c63ff;">
            <span class="section-badge">⚡ Key Insight</span>
            <div class="section-body">{data.get('key_insight', '')}</div>
        </div>""", unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown(f"""
        <div class="result-section" style="border-left: 3px solid #ff6584;">
            <span class="section-badge" style="color: #ff6584; border-color: #ff6584;">⚠ Common Misconception</span>
            <div class="section-body">{data.get('common_misconception', '')}</div>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="result-section" style="border-left: 3px solid #f5c842;">
            <span class="section-badge" style="color: #f5c842; border-color: #f5c842;">🌍 Real-World Example</span>
            <div class="section-body">{data.get('real_world_example', '')}</div>
        </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# MAIN APP
# ─────────────────────────────────────────
def main():
    # Hero
    st.markdown("""
    <div class="loresnap-hero">
        <div class="loresnap-title">LoreSnap</div>
        <div class="loresnap-subtitle">✦ Visual Intelligence Engine ✦</div>
        <div class="loresnap-tagline">Upload any image. Get stories, memes, study material & diagram breakdowns.</div>
    </div>
    """, unsafe_allow_html=True)

    # Layout
    left, right = st.columns([1, 1.6], gap="large")

    with left:
        st.markdown("##### 📁 Upload Image")
        uploaded = st.file_uploader(
            "Drop your image here",
            type=["jpg", "jpeg", "png", "gif", "webp"],
            label_visibility="collapsed"
        )

        if uploaded:
            st.image(uploaded, use_container_width=True, caption=uploaded.name)

        st.markdown("---")
        st.markdown("##### ⚡ Choose Mode")

        mode = st.radio(
            "Mode",
            ["🌌 LoreSnap (Full Universe)", "📖 Story Mode", "🎭 Meme Mode", "🧠 Study Mode", "🔍 Diagram Mode"],
            label_visibility="collapsed"
        )

        mode_info = {
            "🌌 LoreSnap (Full Universe)": "All 4 engines combined — story, meme, study & diagram in one epic report",
            "📖 Story Mode": "Turns your image into a full short story with characters, world, conflict & plot twist",
            "🎭 Meme Mode": "Generates multiple meme captions, a roast, social caption & hashtags",
            "🧠 Study Mode": "Extracts flashcards, summaries, exam questions & study tips",
            "🔍 Diagram Mode": "Breaks down diagrams & visual content step-by-step with key insights",
        }
        st.markdown(f"""
        <div style="background: rgba(108,99,255,0.07); border: 1px solid rgba(108,99,255,0.2);
             border-radius: 8px; padding: 0.75rem 1rem; margin: 0.5rem 0;">
            <div style="font-size: 0.78rem; color: #9ca3af; line-height: 1.5;">{mode_info[mode]}</div>
        </div>""", unsafe_allow_html=True)

        st.markdown("")
        generate = st.button("✦ ANALYZE IMAGE", disabled=not uploaded)

    with right:
        if not uploaded:
            st.markdown("""
            <div style="display: flex; align-items: center; justify-content: center; height: 400px;
                 border: 2px dashed #1e2040; border-radius: 12px; flex-direction: column; gap: 1rem;">
                <div style="font-size: 3rem;">✦</div>
                <div style="font-family: 'Space Mono', monospace; font-size: 0.75rem; color: #4b5563;
                     text-align: center; text-transform: uppercase; letter-spacing: 2px;">
                    Upload an image to begin<br>your lore journey
                </div>
            </div>""", unsafe_allow_html=True)

        elif generate:
            img_bytes = uploaded.read()
            media_type = get_media_type(uploaded.name)
            img_b64 = image_to_base64(img_bytes)
            prompt = build_prompt(mode)

            with st.spinner(f"✦ Analyzing image with {mode}..."):
                try:
                    data = call_claude(img_b64, media_type, prompt)
                    st.session_state["result"] = data
                    st.session_state["mode"] = mode
                except json.JSONDecodeError as e:
                    st.error(f"JSON parse error: {e}")
                except Exception as e:
                    st.error(f"Analysis failed: {e}")

        # Show cached result
        if "result" in st.session_state and not generate:
            data = st.session_state["result"]
            mode_used = st.session_state.get("mode", mode)
            st.markdown(f"""
            <div style="font-family: 'Space Mono', monospace; font-size: 0.65rem; color: #4b5563;
                 text-transform: uppercase; letter-spacing: 2px; margin-bottom: 1rem;">
                ✦ Results from: {mode_used}
            </div>""", unsafe_allow_html=True)
            if "universe_name" in data:
                render_loresnap(data)
            elif "opening" in data and "genre" in data:
                render_story(data)
            elif "main_meme" in data:
                render_meme(data)
            elif "flashcards" in data and "study_tip" in data:
                render_study(data)
            elif "diagram_type" in data:
                render_diagram(data)

        elif generate and "result" in st.session_state:
            data = st.session_state["result"]
            if "universe_name" in data:
                render_loresnap(data)
            elif "opening" in data and "genre" in data:
                render_story(data)
            elif "main_meme" in data:
                render_meme(data)
            elif "flashcards" in data and "study_tip" in data:
                render_study(data)
            elif "diagram_type" in data:
                render_diagram(data)

    # Footer
    st.markdown("""
    <div style="text-align: center; padding: 3rem 0 1rem; border-top: 1px solid #1e2040; margin-top: 3rem;">
        <div style="font-family: 'Playfair Display', serif; font-size: 1.2rem; background: linear-gradient(135deg, #6c63ff, #ff6584);
             -webkit-background-clip: text; -webkit-text-fill-color: transparent;">LoreSnap</div>
        <div style="font-family: 'Space Mono', monospace; font-size: 0.6rem; color: #374151; margin-top: 0.3rem;
             text-transform: uppercase; letter-spacing: 3px;">
            StudySnap · Meme Generator · Story Generator · Diagram Explainer — Unified
        </div>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
