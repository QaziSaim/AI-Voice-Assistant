import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from elevenlabs import ElevenLabs
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
from pydub import AudioSegment
import io, os
from langgraph_backend import chatbot

load_dotenv()

# Initialize ElevenLabs client
eleven_client = ElevenLabs(api_key=os.getenv("ELEVEN_API_KEY"))

# Chat model configuration
config = {'configurable': {'thread_id': 'thread_id-1'}}

# Initialize message history
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

st.title("🎙️ AI Voice Chatbot")
st.caption("Speak or type to chat with your AI assistant!")

# Display previous chat
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

# 🎤 Record Audio
st.subheader("🎙️ Speak your command")
audio_bytes = mic_recorder(
    start_prompt="Start Talking 🎤",
    stop_prompt="Stop Recording",
    just_once=True,
    use_container_width=True
)

user_input = None

if audio_bytes and isinstance(audio_bytes, dict) and "bytes" in audio_bytes:
    # Save temporary audio
    with open("temp_input.webm", "wb") as f:
        f.write(audio_bytes["bytes"])
    st.audio(audio_bytes["bytes"], format="audio/wav")

    # Convert WebM → WAV for recognition
    sound = AudioSegment.from_file("temp_input.webm")
    sound.export("input.wav", format="wav")

    # Speech Recognition
    r = sr.Recognizer()
    with sr.AudioFile("input.wav") as source:
        audio_data = r.record(source)
        try:
            text = r.recognize_google(audio_data, language="en-IN")
            user_input = text
            st.success(f"🗣️ You said: **{text}**")
        except sr.UnknownValueError:
            st.error("Could not understand audio.")
        except sr.RequestError as e:
            st.error(f"Speech Recognition API error: {e}")

# ✏️ Or use text input
if not user_input:
    user_input = st.chat_input("Type your message...")

# Process user message
if user_input:
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    response = chatbot.invoke({'messages': [HumanMessage(content=user_input)]}, config=config)
    ai_message = response['messages'][-1].content
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})

    with st.chat_message('assistant'):
        st.text(ai_message)

    # 🔊 Text-to-Speech with ElevenLabs
    try:
        audio_stream = eleven_client.text_to_speech.convert(
            voice_id=os.getenv("ADAM_VOICE"),  # Replace with your valid voice ID
            model_id="eleven_turbo_v2",
            text=ai_message
        )
        audio_bytes = b"".join(audio_stream)
        st.audio(io.BytesIO(audio_bytes), format="audio/mp3")
    except Exception as e:
        st.warning(f"TTS Error: {e}")
