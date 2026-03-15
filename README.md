# ✦ LoreSnap — Visual Intelligence Engine

> The fusion of **StudySnap AI**, **AI Meme Generator**, **AI Story Generator**, and **AI Diagram Explainer** into one unified tool.

## What It Does

Upload **any image** — notes, diagrams, photos, textbook pages, whiteboards — and LoreSnap runs it through 4 AI engines simultaneously:

| Mode | What You Get |
|------|-------------|
| 🌌 **LoreSnap (Full Universe)** | All 4 engines combined — story lore, characters, meme, flashcards, diagram breakdown |
| 📖 **Story Mode** | Characters, world, conflict, plot twist, cliffhanger |
| 🎭 **Meme Mode** | 5 meme styles, roast, social caption, hashtags |
| 🧠 **Study Mode** | Flashcards, summary, exam questions, study tip |
| 🔍 **Diagram Mode** | Component breakdown, step-by-step, key insight, misconceptions |

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your Anthropic API key
export ANTHROPIC_API_KEY="your-key-here"

# 3. Run the app
streamlit run app.py
```

## Tech Stack

- **Frontend**: Streamlit with custom CSS (dark theme, Google Fonts)
- **Backend**: Python
- **AI Model**: Claude claude-opus-4-5 (Vision + Text)
- **Library**: `anthropic` Python SDK, `Pillow`

## Project Structure

```
loresnap/
├── app.py           # Main Streamlit application (all-in-one)
├── requirements.txt # Dependencies
└── README.md        # This file
```

## How It Works

1. User uploads an image (JPG, PNG, GIF, WebP)
2. Image is base64-encoded and sent to Claude claude-opus-4-5
3. A mode-specific prompt instructs Claude to return structured JSON
4. The JSON is parsed and rendered as beautiful UI cards
5. Results are cached in session state for re-display

## The Fusion Concept

Each original project solves one problem:
- **StudySnap** → notes to study material  
- **Meme Generator** → image to captions  
- **Story Generator** → image to narrative  
- **Diagram Explainer** → visual to explanation  

**LoreSnap** treats every image as a *universe* — it has lore (story), inhabitants (characters), visual logic (diagram), cultural artifacts (memes), and knowledge (flashcards). One upload, infinite dimensions.
