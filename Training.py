import random
import json
import pickle
import nltk
import tensorflow as tf
import numpy as np
from nltk.stem import WordNetLemmatizer
from keras.models import load_model
import os

class Training:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.intents = json.loads(open('intents.json').read())
        
        if os.path.exists('classes.pkl') and os.path.exists('words.pkl'):
            self.words = pickle.load(open('words.pkl','rb'))
            self.classes = pickle.load(open('classes.pkl','rb'))
        else:
            self.words = []
            self.classes = []
            
        self.documents = []
        self.ignoreLetters = ['?', '!', '.', ',',]
    
    def preprocess_data(self):
        for intent in self.intents['intents']:
            for pattern in intent['patterns']:
                wordList = nltk.word_tokenize(pattern)
                self.words.extend(wordList)
                self.documents.append((wordList,intent['tag']))

                if intent['tag'] not in self.classes:
                    self.classes.append(intent['tag'])

        self.words = [self.lemmatizer.lemmatize(word) for word in self.words if word not in self.ignoreLetters]

        self.words = sorted(set(self.words))
        self.classes = sorted(set(self.classes))

        pickle.dump(self.words, open('words.pkl','wb'))
        pickle.dump(self.classes, open('classes.pkl','wb'))
    
    def get_training_data(self):
        training = []
        outputEmpty = [0] * len(self.classes)

        for document in self.documents:
            bag = []
            wordPatterns = document[0]
            wordPatterns = [self.lemmatizer.lemmatize(word.lower()) for word in wordPatterns]

            for word in self.words:
                bag.append(1) if word in wordPatterns else bag.append(0)
            
            outputRow = list(outputEmpty)
            outputRow[self.classes.index(document[1])] = 1
            training.append(bag + outputRow)

        random.shuffle(training)
        training = np.array(training)

        trainX = training[:, :len(self.words)]
        trainY = training[:, len(self.words):]
        
        return trainX, trainY
    
    def Train_Model(self):
        self.preprocess_data()
        trainX,trainY = self.get_training_data()
        
        if os.path.exists("chatbot_model.h5"):
            model = load_model("chatbot_model.h5")
            print("Loading the Existing Model")
        else:
            model = tf.keras.Sequential()
            model.add(tf.keras.layers.Dense(128, input_shape=(len(trainX[0]),), activation = 'relu'))
            model.add(tf.keras.layers.Dropout(0.5))
            model.add(tf.keras.layers.Dense(64, activation = 'relu'))
            model.add(tf.keras.layers.Dropout(0.5))
            model.add(tf.keras.layers.Dense(len(trainY[0]), activation='softmax'))

            sgd = tf.keras.optimizers.SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
            model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

        hist = model.fit(np.array(trainX), np.array(trainY), epochs=200, batch_size=5, verbose=1)
        model.save('chatbot_model.h5', hist)
        print('Created New Model')

obj = Training()
obj.Train_Model()