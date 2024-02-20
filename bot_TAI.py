import speech_recognition as sr
from nltk.classify import NaiveBayesClassifier
import csv
import pandas as pd
import pyttsx3 as tts
import numpy as np
from keras.models import Sequential
from keras.layers import Embedding, SimpleRNN, Dense
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from keras.models import load_model

version = "0.1.1"
author = "Bitrax"
message = ""
r = sr.Recognizer()
bot = tts.init()
bot.setProperty('rate', 150)
message = ""

with open("conversations.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)
    conversations = {row[0]: row[1] for row in reader}

questions = list(conversations.keys())
answers = list(conversations.values())
model = load_model('model_konwersacji.h5')

with open('countvectorizer_words.txt', 'r') as f:
    words = f.readlines()
words = [word.strip() for word in words]

vectorizer = CountVectorizer(vocabulary=words)

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

def pamiec(message):
    found = False
    X_input = vectorizer.transform([message])
    predicted_index = np.argmax(model.predict(X_input))
    predicted_response = answers[predicted_index]
    predicted_probabilities = model.predict(X_input)
    max_probability = np.max(predicted_probabilities)
    print("Prawdopodobieństwo:", max_probability)
    print("Bot:", predicted_response)

    if message in conversations:
        found = True
        dzwiek(conversations[message])

    if not found and message is not None and message != "":
        question = message
        dzwiek("Nie rozumiem. Prosze powiedz mi co mam odpowiadać w takim przypadku.")
        new_answer = nasluchiwanie()
        if new_answer is not None and new_answer != "":
            print(message)
            conversations[message] = new_answer
            label_mapping = {q: i for i, q in enumerate(questions)}
            y_train = np.array([label_mapping[q] for q in questions])
            X_train = vectorizer.transform(questions)
            model = Sequential()
            model.add(Embedding(input_dim=len(vectorizer.vocabulary_), output_dim=100, input_length=X_train.shape[1]))
            model.add(SimpleRNN(units=64))
            model.add(Dense(len(conversations), activation='softmax'))
            model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
            model.fit(X_train.toarray(), y_train, epochs=1, batch_size=1)
            dzwiek("Zapamiętam!")

            with open('conversations.csv', 'a', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([question, new_answer])
        else:
            dzwiek("Ignoruje ostatnie polecenie!")

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
        with open('countvectorizer_words.txt', 'w') as f:
            for word in vectorizer.get_feature_names_out():
                f.write(word + '\n')
        model.save('model_konwersacji.h5')
        print("Bot: Zapisano model.")
        dzwiek("Wyłączam się!")
