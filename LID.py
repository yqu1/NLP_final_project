from utilities import *
from model import *
from sklearn.metrics import accuracy_score

label_map = {}

lang = languageList()

counter = 0
for l in lang:
	label_map[l] = counter
	counter += 1

docs, labels = loadData('test')
for i in range(len(labels)):
        labels[i] = label_map[labels[i]]

txt = ''
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
y = np.array(labels)

for i, doc in enumerate(docs):
    for j, sentence in enumerate(doc):
        if j < max_sentences:
            for t, char in enumerate(sentence[-maxlen:]):
                X[i, j, (maxlen - 1 - t)] = char_indices[char]



model = CL_LSTM(250, 512)

model.load_weights('checkpoints/LID.03-0.09.hdf5')

print(accuracy_score(model.predict(X), y))
