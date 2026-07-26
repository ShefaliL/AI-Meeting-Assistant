AI Meeting Assistant: Multilingual RAG Meeting Intelligence System

The AI Meeting Assistant is a high-performance, end-to-end AI pipeline designed to transform raw meeting recordings—from local files or YouTube links—into searchable, actionable organizational knowledge
. By combining state-of-the-art speech recognition, Large Language Models (LLMs), and Retrieval-Augmented Generation (RAG), this system eliminates manual note-taking and ensures no decision or action item is ever lost

🚀 Overview
Modern teams often suffer from "meeting fatigue," where hours of recordings are rarely reviewed and critical insights are buried
. This application provides a Streamlit-based interface to process these recordings, providing high-accuracy multilingual transcription, intelligent summarization, and a context-aware chat interface

✨ Key Features
Multilingual Transcription: Local processing for English using OpenAI Whisper and high-accuracy transcription/translation for Hindi and Hinglish via Sarvam AI
.Intelligent Summarization: Automated generation of concise meeting summaries using Mistral AI
.Insight Extraction: Automatically identifies and categorizes:
Action Items (with assigned owners and deadlines)
.Key Decisions and Open Questions
.Follow-up Tasks
.Conversational Search (RAG): A "Chat with Meeting" feature powered by LangChain and ChromaDB, allowing users to ask specific questions grounded in the actual meeting transcript
.Professional Export: Generate and download comprehensive meeting reports in PDF or TXT formats

🛠️ Technology Stack
Programming Language: Python
Speech Recognition: OpenAI Whisper (Local) & Sarvam AI (Cloud)
Large Language Model: Mistral AI
Orchestration Framework: LangChain LCEL
Vector Database: ChromaDB
Embeddings: HuggingFace Sentence Transformers
Frontend: Streamlit
Audio Utilities: yt-dlp, FFmpeg

🏗️ System Architecture
The system follows a sophisticated data pipeline to ensure accuracy and speed
: Ingestion: Accepts YouTube URLs or local audio/video uploads
.Audio Processing: Extracts and cleans audio using FFmpeg and yt-dlp
.Language Detection & Transcription: Routes audio to Whisper or Sarvam AI based on the detected language
.Meeting Intelligence: Mistral AI processes the transcript to extract summaries and structured insights
.Vector Storage: Transcripts are chunked, embedded, and stored in ChromaDB
.RAG Interaction: Users query the meeting through a retriever-generator loop for context-aware responses


💻 Installation & Setup
Prerequisites
Python 3.9+
FFmpeg installed on your system path
Steps
Clone the repository:
Install dependencies:
Configure Environment Variables: Create a .env file and add your API keys for Sarvam AI and Mistral AI.
Run the Application:

📈 Future Enhancements
Speaker Diarization: Identifying individual contributors by name
.Live Transcription: Integration for real-time meetings
.Platform Integration: Native support for Zoom, Google Meet, and Microsoft Teams
.Sentiment Analysis: Tracking the emotional tone and engagement of discussions


📝 Reflection
This project was developed as a graduate-level capstone to bridge the gap between AI theory and practical workplace utility
. It demonstrates the power of Retrieval-Augmented Generation in creating reliable, hallucination-free AI tools for professional environments
