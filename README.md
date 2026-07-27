 # AI Meeting Assistant: Multilingual RAG Meeting Intelligence System

## 📖 Project Overview

The **AI Meeting Assistant** is a high-performance, end-to-end AI application that transforms meeting recordings into searchable, actionable organizational knowledge. Whether processing a local audio/video file or a YouTube recording, the system leverages state-of-the-art Speech Recognition, Large Language Models (LLMs), and Retrieval-Augmented Generation (RAG) to eliminate manual note-taking and ensure that important decisions, discussions, and action items are never lost.

The application provides a simple **Streamlit** interface where users can upload recordings, generate meeting intelligence, and interact with the transcript through an AI-powered chat interface.

---

## 🚀 Features

### 🌍 Multilingual Transcription
- English transcription using **OpenAI Whisper** (local)
- Hindi and Hinglish transcription & translation using **Sarvam AI**

### 📝 Intelligent Meeting Summaries
- AI-generated meeting summaries powered by **Mistral AI**

### 📌 Meeting Insights
Automatically extracts:
- ✅ Action Items
- 👤 Assigned Owners
- 📅 Deadlines
- 🤝 Key Decisions
- ❓ Open Questions
- 🔄 Follow-up Tasks

### 💬 Chat with Your Meeting (RAG)
Ask natural language questions about your meeting using:
- LangChain
- ChromaDB
- HuggingFace Embeddings

The assistant retrieves relevant transcript sections before generating responses, reducing hallucinations and improving accuracy.

### 📄 Export Reports
Generate downloadable meeting reports in:
- PDF
- TXT

---

# 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| Programming Language | Python |
| Frontend | Streamlit |
| Speech Recognition | OpenAI Whisper, Sarvam AI |
| Large Language Model | Mistral AI |
| RAG Framework | LangChain (LCEL) |
| Vector Database | ChromaDB |
| Embeddings | HuggingFace Sentence Transformers |
| Audio Processing | FFmpeg, yt-dlp |

---

# 🏗️ System Architecture

```
YouTube URL / Local Audio
            │
            ▼
     Audio Extraction
    (yt-dlp / FFmpeg)
            │
            ▼
 Language Detection
            │
     ┌──────┴──────┐
     │             │
     ▼             ▼
 Whisper      Sarvam AI
 (English)   (Hindi/Hinglish)
      │
      ▼
 Meeting Transcript
      │
      ▼
   Mistral AI
      │
      ▼
Summary + Action Items +
Decisions + Questions
      │
      ▼
Chunking & Embeddings
      │
      ▼
    ChromaDB
      │
      ▼
 LangChain RAG Pipeline
      │
      ▼
 Chat with Meeting
```

---

# 💻 Installation

## Prerequisites

- Python 3.9+
- FFmpeg installed and added to your system PATH
- Git

---

## Clone the Repository

```bash
git clone https://github.com/ShefaliL/AI-Meeting-Assistant.git

cd AI-Meeting-Assistant
```

---

## Create a Virtual Environment

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file in the project root.

```env
MISTRAL_API_KEY=your_mistral_api_key
SARVAM_API_KEY=your_sarvam_api_key
```

> **Note:** Keep your API keys private. Never commit the `.env` file to GitHub.

---

# ▶️ Running the Application

Launch the Streamlit application:

```bash
streamlit run app.py
```

Once the application starts:

1. Upload a local audio/video recording **or**
2. Paste a YouTube URL
3. Generate the transcript
4. View AI-generated summaries and insights
5. Chat with your meeting using the RAG interface
6. Export the meeting report as PDF or TXT

---

# 📂 Project Structure

```
AI-Meeting-Assistant/
│
├── app.py
├── requirements.txt
├── .env.example
├── README.md
├── audio_process.py
├── utils/
├── data/
├── vector_store/
└── reports/
```

---

# 👥 Team Members

| Name | GitHub |
|------|---------|
| Shefali Luley | https://github.com/ShefaliL |
| Mitaali Dayal | https://github.com/mitaalidayal |

---

# ⚙️ Important Setup Instructions

- Install **FFmpeg** before running the project.
- Ensure Python **3.9 or higher** is installed.
- Add your **Mistral AI** and **Sarvam AI** API keys to the `.env` file.
- Do **not** commit your `.env` file or API keys to GitHub.
- If processing YouTube videos, ensure `yt-dlp` is installed through the project dependencies.

---

# 📈 Future Enhancements

- 🎙️ Speaker Diarization
- ⚡ Live Meeting Transcription
- 📹 Zoom, Google Meet, and Microsoft Teams Integration
- 😊 Sentiment Analysis
- 📅 Calendar & Task Manager Integration
- 📧 Automatic Email Meeting Summaries

---

# 📝 Reflection

This project was developed as a graduate-level capstone to bridge the gap between modern AI research and practical workplace productivity. By combining multilingual speech recognition, Retrieval-Augmented Generation (RAG), vector search, and Large Language Models, the AI Meeting Assistant demonstrates how AI can create reliable, context-aware meeting intelligence while minimizing hallucinations and improving information retrieval for professional teams.

---

## 📄 License

This project is intended for educational and research purposes.

---
⭐ If you found this project useful, consider giving it a star on GitHub!
