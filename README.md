# AI Video Meeting Assistant

Transform any video into actionable insights — accurate transcriptions, smart summaries, action items, key decisions, and a conversational chat interface powered by AI.

[![Deploy](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://v4k9dy2tl4gy6uxisxai5f.streamlit.app/)

> **Live Demo:** https://v4k9dy2tl4gy6uxisxai5f.streamlit.app/

## Features

- **Multilingual Transcription** — Whisper-powered speech-to-text with support for English, Hinglish, Hindi, Spanish, French, German, Portuguese, and Italian
- **AI Summaries** — Auto-generated concise summaries from long meeting transcripts
- **Action Items Extraction** — Pull out tasks and follow-ups automatically
- **Key Decisions** — Identify decisions that were finalised during the conversation
- **Open Questions** — Surface unresolved questions for later follow-up
- **Chat with Content (RAG)** — Ask any question about the video in natural language; the AI searches the full transcript to answer
- **Flexible Input** — Supports YouTube URLs and local audio/video files (MP4, MP3, WAV, M4A, WebM, MKV, AVI, MOV)

## Tech Stack

| Layer | Tools |
|-------|-------|
| **Speech-to-Text** | OpenAI Whisper (local), Sarvam STT-Translate API |
| **Translation** | Deep Translator |
| **LLM / Orchestration** | LangChain LCEL + Mistral AI (`mistral-small-latest`) |
| **RAG / Embeddings** | ChromaDB + Sentence Transformers + LangChain HuggingFace |
| **Frontend** | Streamlit (interactive web UI) |
| **CLI** | Python CLI entry point |
| **Audio Processing** | yt-dlp, pydub, ffmpeg-python, torchaudio |

## Installation

```bash
# Python 3.10+ recommended
git clone <your-repo-url>
cd video-agent

# Install dependencies
pip install -r requirements.txt

# Install FFmpeg (binary must be available on PATH)
#   - Windows: choco install ffmpeg
#   - macOS:   brew install ffmpeg
#   - Linux:   sudo apt-get install ffmpeg
```

## Configuration

Create a `.env` file in the project root:

```env
# Mistral AI API key (required for LLM)
MISTRAL_API_KEY=your-mistral-api-key

# Sarvam API key (required for Hindi → English translation)
SARVAM_API_KEY=your-sarvam-api-key

# Optional: Whisper model size — tiny, base, small, medium, large (default: small)
WHISPER_MODEL=small

# Optional: Sarvam STT model (default: saaras:v2.5)
SARVAM_STT_MODEL=saaras:v2.5
```

## Usage

### Streamlit UI (Recommended)

```bash
streamlit run app.py
```

The UI will open at `http://localhost:8501`. Paste a YouTube URL or upload a local file, select the language, and click **▶ Analyse**.

### CLI

```bash
python main.py
```

Follow the prompts to enter a YouTube URL or local file path and language.

## Project Structure

```
video-agent/
├── app.py                 # Streamlit web UI
├── main.py                # CLI entry point & pipeline orchestrator
├── requirements.txt       # Python dependencies
├── .env                   # API keys (create locally, do not commit)
├── core/
│   ├── transcriber.py     # Whisper + Sarvam transcription pipeline
│   ├── summarize.py       # Map-reduce summarisation via Mistral
│   ├── extractor.py       # Action items, key decisions, open questions
│   ├── vector_store.py    # ChromaDB vector store + embeddings
│   └── rag_engine.py      # RAG chain for conversational Q&A
├── utils/
│   └── audio_processor.py # Download & chunk audio/video input
└── README.md
```

## How It Works

1. **Input Processing** — Downloads audio from YouTube (`yt-dlp`) or reads from an uploaded file, chunks it into manageable pieces via `pydub`
2. **Transcription** — Runs OpenAI Whisper locally; optionally routes through Sarvam for Hindi/English translation
3. **Title Generation** — LLM generates a descriptive meeting title from the transcript
4. **Summarisation** — Uses LangChain map-reduce with Mistral to produce a concise executive summary
5. **Structured Extraction** — LLM extracts action items, key decisions, and open questions from the full transcript
6. **RAG Index** — Transcript is embedded with Sentence Transformers and stored in ChromaDB
7. **Conversational Chat** — Retrieval-augmented generation lets users ask questions grounded in the actual meeting content

## Supported Input Formats

- **Remote:** YouTube URLs
- **Local Files:** MP4, MP3, WAV, M4A, WebM, MKV, AVI, MOV

## Deployment

The project is deployed on Streamlit Community Cloud.

**URL:** https://v4k9dy2tl4gy6uxisxai5f.streamlit.app/

## License

MIT
