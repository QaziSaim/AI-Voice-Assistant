import streamlit as st
import os, io
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_core.messages import trim_messages
from elevenlabs import ElevenLabs
from dotenv import load_dotenv
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
from pydub import AudioSegment
# Load environment variables
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Initialize clients
eleven_client = ElevenLabs(api_key=os.getenv("ELEVEN_API_KEY"))
model = init_chat_model(model="gemini-2.5-flash", model_provider="google_genai")

# Memory & prompt setup
trimmer = trim_messages(max_tokens=500, strategy="last", token_counter=model, allow_partial=False, start_on="human")
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are Riverwood AI, a friendly English assistant that can handle daily demo tasks."),
    MessagesPlaceholder(variable_name="messages")
])

def call_model(state: MessagesState):
    trimmed_messages = trimmer.invoke(state["messages"])
    prompt = prompt_template.invoke({"messages": trimmed_messages})
    response = model.invoke(prompt)
    return {"messages": response}

workflow = StateGraph(state_schema=MessagesState)
workflow.add_node("model", call_model)
workflow.add_edge(START, "model")

memory = MemorySaver()
chatbot = workflow.compile(checkpointer=memory)

# Streamlit UI
st.set_page_config(page_title="🎤 Riverwood AI Voice Assistant", page_icon="🤖", layout="centered")
st.title("🎤 Riverwood AI Voice Assistant")
st.caption("Powered by Gemini + SpeechRecognition + ElevenLabs")

yesterday_tasks = [
    "Check the construction update for Riverwood site.",
    "Summarize yesterday's client demo outcomes.",
    "Send polite thank-you notes for yesterday’s meetings."
]

today_tasks = [
    "List today's demo tasks and priorities.",
    "Prepare talking points for client A.",
    "Remind me to check team progress at 3 PM."
]

# Initialize session state
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.chat_history = []
    st.session_state["thread_id"] = "session_" + str(os.getpid())

    st.session_state.chat_history.append(("📅 Yesterday’s Tasks", "\n".join(yesterday_tasks)))
    st.session_state.chat_history.append(("🗓️ Today’s Tasks", "\n".join(today_tasks)))



config = {"configurable": {"thread_id": st.session_state["thread_id"]}}

# Record Audio
st.subheader("🎙️ Speak your command (auto mode)")
audio_bytes = mic_recorder(start_prompt="Start Talking 🎤", stop_prompt="Stop", just_once=True, use_container_width=True)

user_input = None

if audio_bytes and isinstance(audio_bytes, dict) and "bytes" in audio_bytes:
    # Save audio
    with open("temp_input.webm", "wb") as f:
        f.write(audio_bytes["bytes"])
    st.audio(audio_bytes["bytes"], format="audio/wav")

    # Convert speech → text using SpeechRecognition
    sound = AudioSegment.from_file("temp_input.webm")
    sound.export("input.wav",format="wav")
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

else:
    user_input = st.chat_input("Or type your message...")

# Process user input
if user_input:
    st.session_state.chat_history.append(("🧍‍♂️ You", user_input))
    output = chatbot.invoke({"messages": [("user", user_input)]}, config)
    response = output["messages"][-1].content
    st.session_state.chat_history.append(("🤖 Riverwood", response))

    # ElevenLabs speech output
    audio_stream = eleven_client.text_to_speech.convert(
        voice_id="N2al4jd45e882svx17SU",  # Replace with your valid voice_id
        model_id="eleven_turbo_v2",
        text=response
    )

    audio_bytes = b"".join(audio_stream)
    st.audio(io.BytesIO(audio_bytes), format="audio/mp3")

# Display chat history
for sender, message in st.session_state.chat_history:
    with st.chat_message("user" if sender == "🧍‍♂️ You" else "assistant"):
        st.markdown(f"**{sender}:** {message}")
