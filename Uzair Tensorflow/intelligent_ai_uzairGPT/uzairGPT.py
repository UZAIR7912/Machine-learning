import random
import pickle
import nltk
import json
import numpy as np
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model #type: ignore

lemmatizer = WordNetLemmatizer()
intents = json.loads(open("intents.json").read())
words = pickle.load(open("words.pkl","rb"))
classes = pickle.load(open("classes.pkl","rb"))
model = load_model("chatbot.h5")

def clean_up_sentence(sentence):
    sentence_words = nltk.tokenize.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return(sentence_words)

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                bag[i] = 1
    return(np.array(bag))

def class_predict(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    error_threshold = 0.1
    results = [[i,r] for i,r in enumerate(res) if r > error_threshold]
    results.sort(key=lambda x: x[1] , reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]] , "probability": str(r[1])})
    return(return_list)

def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

print("Go! Bot is running!")

while True:
    message = input("you: ")
    ints = class_predict(message)
    res = get_response(ints,intents)
    print(f"Bot: {res}")
