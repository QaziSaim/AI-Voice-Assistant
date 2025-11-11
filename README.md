![Banner_Image](chatbot_image.png)

````markdown
# 🎙️ Riverwood AI Voice Agent

An intelligent **AI Voice Assistant** built for **Riverwood Projects LLP**, designed to handle natural conversations, provide daily construction updates, and build friendly, human-like engagement with users — inspired by the phrase _“Namaste Sir, aapne chai pi?”_ ☕

---

## 🚀 Live Demo
🔗 **Try it here:** [👉 Click to Open Streamlit App](https://ai-voice-assistant-ce9bdmcwv7ggnfjf5h383d.streamlit.app/)

---

## 🧠 Project Overview

This project was built as part of the **Riverwood AI Voice Agent Challenge**.  
The goal was to design a **voice-enabled AI assistant** that:
1. Greets the user naturally in Hindi or English.  
2. Waits for user input (voice or text).  
3. Understands and responds contextually using a Large Language Model (LLM).  
4. Speaks back in a natural, human-like voice.  
5. (Bonus) Remembers previous replies across turns.  
6. (Optional) Simulates construction updates or daily reminders.

---

## 🏗️ Architecture Overview

The app consists of two main components:

### 1. **Frontend (`app.py`)**
- Built using **Streamlit** for a clean and interactive UI.  
- Integrates **Streamlit Mic Recorder** for voice capture.  
- Uses **SpeechRecognition** and **pydub** for speech-to-text conversion.  
- Displays conversation history in a chat-style format.  
- Converts AI responses into **speech output** using **ElevenLabs API**.  

### 2. **Backend (`langgraph_backend.py`)**
- Built using **LangGraph** and **LangChain** for managing stateful conversations.  
- Uses **Google Gemini 2.5 Flash** model via `langchain_google_genai` for contextual understanding and generation.  
- Employs **InMemorySaver** for maintaining short-term conversational memory.  

---

## 🧰 Technologies Used

| Component | Technology |
|------------|-------------|
| Frontend | Streamlit |
| Voice Input | streamlit-mic-recorder, SpeechRecognition, pydub |
| LLM Model | Gemini 2.5 Flash (Google Generative AI) |
| Voice Output | ElevenLabs Text-to-Speech |
| Memory Management | LangGraph (InMemorySaver) |
| Environment Management | python-dotenv |
| Deployment | Streamlit Cloud |

---

## ⚙️ How It Works

1. **User speaks or types** a message.  
2. Audio is recorded and converted to text using `SpeechRecognition`.  
3. The text is passed to a **LangGraph-powered LLM** backend for generating a contextual reply.  
4. The response is shown on screen and **spoken aloud** using ElevenLabs API.  
5. The session remembers previous messages to create a natural flow.

---

## 💡 Features

✅ Real-time voice recognition (Speech-to-Text)  
✅ Conversational LLM replies  
✅ Text-to-Speech with natural voice  
✅ Chat memory persistence  
✅ Friendly & contextual flow (English + Hindi)  
✅ Deployed and accessible online  

---

## 🛠️ Setup Instructions

### 1. Clone the repository
```bash
git clone YOUR_REPO_LINK_HERE
cd riverwood-ai-voice-agent
````

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your API keys

Create a `.env` file with:

```bash
GOOGLE_API_KEY=your_google_api_key
ELEVEN_API_KEY=your_elevenlabs_api_key
```

### 4. Run the app locally

```bash
streamlit run app.py
```

---

## ☁️ Streamlit Deployment Setup

If deploying on **Streamlit Cloud**, include:

* `requirements.txt` → for Python libraries
* `packages.txt` → with the line:

  ```
  ffmpeg
  ```
* Add your API keys securely under **Settings → Secrets**.

---

## 📦 Folder Structure

```
├── app.py                  # Streamlit UI + Voice handling
├── langgraph_backend.py    # LangGraph + Gemini LLM backend
├── requirements.txt        # Python dependencies
├── packages.txt            # ffmpeg installation for audio processing
├── .env                    # API keys (local only)
└── README.md
```

---

## 👨‍💻 Developer

**Sahim Kazi**
📧 [kazisahim121@gmail.com](mailto:sahimkazi@gmail.com)
📱 8080004177
💼 [LinkedIn](https://www.linkedin.com/in/saim-qazi-1406431b9/)

---

## 🏁 Acknowledgement

This project was built as part of the
**Riverwood Projects LLP – AI Voice Agent Internship Challenge**
for creating India’s first **AI CRM Voice Assistant**.