import random
import json
import pickle
import numpy as np
import nltk
from tensorflow import keras
from nltk.stem import WordNetLemmatizer
from keras.models import load_model

class Model:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.intents = json.loads(open('intents.json').read())

        self.words = pickle.load(open('words.pkl','rb'))
        self.classes = pickle.load(open('classes.pkl','rb'))
        self.model = load_model('chatbot_model.h5')
        

    def clean_up_sentence(self, sentence):
        self.sentence_words = nltk.word_tokenize(sentence)
        self.sentence_words = [self.lemmatizer.lemmatize(word) for word in self.sentence_words]

    def bag_of_words(self, sentence):
        self.clean_up_sentence(sentence)
        self.bag = [0] * len(self.words)

        for w in self.sentence_words:
            for i,word in enumerate(self.words):
                if word == w:
                    self.bag[i] = 1
        
        return np.array(self.bag)

    def predict_class(self, sentence):
        bow = self.bag_of_words(sentence)
        res = self.model.predict(np.array([bow]))[0]
        ERROR_THRESHOLD = 0.25
        results = [[i,r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
        results.sort(key=lambda x : x[1], reverse=True)

        return_list = []
        for r in results:
            return_list.append({'intent':self.classes[r[0]], 'probability':str(r[1])})
        
        return return_list

    def get_response(self, intents_list, intents_json):
        tag = intents_list[0]['intent']
        list_of_intents = intents_json['intents']

        for i in list_of_intents:
            if i['tag'] == tag:
                result = random.choice(i['responses'])
                break
        
        return result












