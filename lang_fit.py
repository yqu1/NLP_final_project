import sys
import re
from collections import Counter
from googletrans import Translator
from googletrans import LANGCODES

docroot = '/afs/crc.nd.edu/user/n/nsmith9/NLP_final_project/googleTrain'
trans = Translator()
tmp = trans.detect(open(sys.argv[1]).read())
scorrect = True
if tmp.lang not in LANGCODES.values():
    scorrect = False
def words(text): return re.findall(r'\w+', text.lower())
WORDS = Counter(words(docroot + '/' + tmp.lang + '.txt'))

def P(word, N=sum(WORDS.values())):
    "Probability of `word`."
    return WORDS[word] / N

def correction(word):
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word):
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words):
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word):
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

if __name__ == '__main__':
    trans = Translator()
    with open(sys.argv[1]) as f:
        for each in f:
            each = each.rstrip().split()
            if scorrect:
                line = []
                for word in each:
                    line.append(correction(word))
                result = trans.translate(' '.join(line))
            else:
                result = trans.translate(' '.join(each))
            print(result.text)
