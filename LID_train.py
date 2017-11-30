from keras.models import Model
from keras.layers import Dense, Input, Dropout, MaxPooling1D, Conv1D
from keras.layers import LSTM, Lambda
from keras.layers import TimeDistributed, Bidirectional
from keras.layers.normalization import BatchNormalization
from utilities import *
from model import *
import numpy as np
import tensorflow as tf
import re
import keras.callbacks
import sys
import os


# record history of training
class LossHistory(keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        self.losses = []
        self.accuracies = []

    def on_batch_end(self, batch, logs={}):
        self.losses.append(logs.get('loss'))
        self.accuracies.append(logs.get('acc'))


total = len(sys.argv)
cmdargs = str(sys.argv)

print ("Script name: %s" % str(sys.argv[0]))
checkpoint = None
if len(sys.argv) == 2:
    if os.path.exists(str(sys.argv[1])):
        print ("Checkpoint : %s" % str(sys.argv[1]))
        checkpoint = str(sys.argv[1])

txt = ''

label_map = {}

lang = languageList()

counter = 0
for l in lang:
        label_map[l] = counter
        counter += 1

docs, labels = loadData('googleTrain')

for i in range(len(labels)):
	labels[i] = label_map[labels[i]]


num_sent = []
for doc in docs:
    num_sent.append(len(doc))
    for s in doc:
        txt += s

chars = set(txt)

print('total chars:', len(chars))
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))


maxlen = 512
max_sentences = 250

X = np.ones((len(docs), max_sentences, maxlen), dtype=np.int64) * -1
y = keras.utils.to_categorical(np.array(labels), num_classes = 104)

for i, doc in enumerate(docs):
    for j, sentence in enumerate(doc):
        if j < max_sentences:
            for t, char in enumerate(sentence[-maxlen:]):
                X[i, j, (maxlen - 1 - t)] = char_indices[char]

ids = np.arange(len(X))
np.random.shuffle(ids)

# shuffle
X = X[ids]
y = y[ids]

X_train = X[:15000]
X_test = X[15000:]

y_train = y[:15000]
y_test = y[15000:]


model = CL_LSTM(max_sentences, maxlen)

if checkpoint:
    model.load_weights(checkpoint)

file_name = os.path.basename(sys.argv[0]).split('.')[0]
check_cb = keras.callbacks.ModelCheckpoint('checkpoints/' + file_name + '.{epoch:02d}-{val_loss:.2f}.hdf5',
                                           monitor='val_loss',
                                           verbose=0, save_best_only=True, mode='min')
earlystop_cb = keras.callbacks.EarlyStopping(monitor='val_loss', patience=7, verbose=1, mode='auto')
history = LossHistory()
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(X_train, y_train, validation_data=(X_test, y_test), batch_size=10,
          epochs=5, shuffle=True, callbacks=[earlystop_cb, check_cb, history])

# just showing access to the history object
# print(history.losses)
# print(history.accuracies)
