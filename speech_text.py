import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
    print("Speek now...")
    audio = r.listen(source)

text = r.recognize_google(audio,language='en-IN')
print("You said:",text)