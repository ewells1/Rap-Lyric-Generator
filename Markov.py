from nltk.tokenize import word_tokenize
from random import choice
import string


class Markov:

    def __init__(self, examples):
        examples = ". " + examples
        self.trainingset = word_tokenize(examples)

    def bigram_generate(self, n=100):
        bigrams = self.bigrams()

        ret = ""
        current = "."
        nexttoken = ""
        i = 1
        while i < n or current != ".":
            nexttoken = choice(bigrams[current])
            if nexttoken not in string.punctuation and i > 1:
                ret += " "
            ret += nexttoken
            current = nexttoken
            i += 1
        return ret

    def trigram_generate(self, n=100):
        bigrams = self.bigrams()
        trigrams = self.trigrams()

        current1 = "."
        current2 = choice(bigrams[current1])
        nexttoken = ""
        ret = current2
        i = 2
        while i < n or current2 != ".":
            nexttoken = choice(trigrams[(current1, current2)])
            if nexttoken[0] not in string.punctuation:
                ret += " "
            ret += nexttoken
            current1 = current2
            current2 = nexttoken
            i += 1
        return ret

    def training_set(self):
        print(self.trainingset)

    def bigrams(self):
        bgs = []
        for i in range(len(self.trainingset) - 1):
            bgs.append([self.trainingset[i], self.trainingset[i + 1]])
        # print(bgs) # debug

        ret = {}
        for bg in bgs:
            if bg[0] in ret:
                ret[bg[0]].append(bg[1])
            else:
                ret[bg[0]] = []
                ret[bg[0]].append(bg[1])
        return ret

    def trigrams(self):
        tgs = []
        for i in range(len(self.trainingset) - 2):
            tgs.append([self.trainingset[i], self.trainingset[i + 1], self.trainingset[i + 2]])
        # print(ret) # debug

        ret = {}
        for tg in tgs:
            if (tg[0], tg[1]) in ret:
                ret[(tg[0], tg[1])].append(tg[2])
            else:
                ret[(tg[0], tg[1])] = []
                ret[(tg[0], tg[1])].append(tg[2])
        return ret
