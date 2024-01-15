import speech_recognition as sr
from nltk.classify import NaiveBayesClassifier
import csv
import pandas as pd
import pyttsx3 as tts 

version = "0.1.0"
author = "Bitrax"
message = ""
r = sr.Recognizer()
bot = tts.init()
bot.setProperty('rate', 150)
message = ""

with open("conversations.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)
    conversations = [(row[0], row[1]) for row in reader]

def nasluchiwanie(language="pl-PL"):
    with sr.Microphone() as source:
        print("Nasłuchiwanie:")
        try:
            audio = r.listen(source, timeout=5)
            message = r.recognize_google(audio, language=language)
            message = message.lower()
            print("Rozpoznawanie mowy Google myśli, że powiedziałeś: " + message)
            return message
        except sr.WaitTimeoutError:
            print("Czas minął. Nie wykryto żadnej wypowiedzi.")
            timeout = 1
        except sr.UnknownValueError:
            print("Rozpoznawanie mowy Google nie może zrozumieć dźwięku")
        except sr.RequestError as e:
            print("Nie można zażądać wyników z usługi rozpoznawania mowy Google; {0}".format(e))

def dzwiek(label):
    print(f"Bot: {label}")
    bot.say(label)
    bot.runAndWait()

def extract_features(message):
    return {'message': message}
    
features = [
    (extract_features(message), label)
    for message, label in conversations
]

def pamiec(message):
    found = False
    for conversation in conversations:
        if message in conversation:
            found = True
            dzwiek(conversation[1])
            break

    if not found and message is not None and message != "":
        question = message
        dzwiek("Nie rozumiem. Prosze powiedz mi co mam odpowiadać w takim przypadku.")
        odpowiedz = nasluchiwanie()
        if odpowiedz is not None and odpowiedz != "":
            print(message , 1)
            conversations.append((question, odpowiedz))
            dzwiek("Zapamiętam!")

            with open('conversations.csv', 'a', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([question, odpowiedz])
        else:
            dzwiek("Ignoruje ostatnie polecenie!")

classifier = NaiveBayesClassifier.train(features)

print("Prowadź konwersacje po Polsku!") 

while message != "zakończ":
    message = nasluchiwanie("en-US")
    timeout = 0

    if message == "thai":
        dzwiek("Słucham.")
        while True:
            message = nasluchiwanie()
            if timeout == 1 or message == "pa" or message is None or message.strip() == "":
                timeout = 0
                print("Czuwam...")
                break
            if message == "zakończ":
                break
            pamiec(message)

    if message == "zakończ":
        dzwiek("Wyłączam się!")
