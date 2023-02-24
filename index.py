import openai
import speech_recognition as sr
import pyttsx3
import threading
from tkinter import *

# Ustawienia OpenAI API
openai.api_key = "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"
openai_model = "text-davinci-002"

# Ustawienia syntezy mowy
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 175)

# Ustawienia GUI
root = Tk()
root.title("OpenAI Chatbot")

chat_label = Label(root, text="Rozmowa z OpenAI Chatbotem", font=('Arial', 14))
chat_label.pack(pady=20)

scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)

chat = Text(root, yscrollcommand=scrollbar.set, height=20, width=50)
chat.pack(pady=10)

input_frame = Frame(root)
input_frame.pack()

input_field = Entry(input_frame, width=30)
input_field.pack(side=LEFT, padx=10)

def ask_question():
    question = input_field.get()
    if question:
        input_field.delete(0, END)
        answer = generate_answer(question)
        add_to_chat(f"Użytkownik: {question}")
        add_to_chat(f"OpenAI Chatbot: {answer}")
        speak(answer)

def add_to_chat(message):
    chat.insert(END, message + "\n")
    chat.see(END)

def generate_answer(question):
    response = openai.Completion.create(
        engine=openai_model,
        prompt=f"Q: {question}\nA:",
        temperature=0.5,
        max_tokens=1024,
        n=1,
        stop=None,
        timeout=15,
    )

    return response.choices[0].text.strip()

def speak(message):
    engine.say(message)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        add_to_chat("OpenAI Chatbot: Czekam na pytanie...")
        audio = recognizer.listen(source)

    try:
        question = recognizer.recognize_google(audio)
        add_to_chat(f"Użytkownik: {question}")
        answer = generate_answer(question)
        add_to_chat(f"OpenAI Chatbot: {answer}")
        speak(answer)
    except sr.UnknownValueError:
        add_to_chat("OpenAI Chatbot: Nie zrozumiałem, możesz powtórzyć?")
    except sr.RequestError as e:
        add_to_chat(f"OpenAI Chatbot: Wystąpił błąd: {e}")

listen_thread = threading.Thread(target=listen)

def on_enter(event):
    ask_question()

def on_button_click():
    listen_thread.start()

input_field.bind("<Return>", on_enter)

listen_button = Button(input_frame, text="Zadaj pytanie", command=on_button_click)
listen_button.pack(side=RIGHT, padx=10)

root.mainloop()

