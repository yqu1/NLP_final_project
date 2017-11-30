from googletrans import Translator
import sys

if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        translator = Translator()
        for each in f:
            line = []
            each = each.rstrip().split()
            for word in each:
                ttext = translator.translate(word,src = sys.argv[2])
                line.append(ttext.text)
            print(' '.join(line))
