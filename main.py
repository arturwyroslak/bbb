import openai
import speech_recognition as sr

openai.api_key = "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"

def generate_response(prompt):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()

r = sr.Recognizer()

with sr.Microphone() as source:
    print("Mów teraz:")
    audio = r.listen(source)
    
try:
    text = r.recognize_google(audio, language="pl-PL")
    print("Zrozumiałem: " + text)
    response = generate_response(text)
    print("Odpowiedź: " + response)
except:
    print("Nie zrozumiałem, spróbuj ponownie")
