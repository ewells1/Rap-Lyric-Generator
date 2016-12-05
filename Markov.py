from nltk.tokenize import word_tokenize
from random import choice
import string


class Markov:

    def __init__(self, examples):
        examples = ". " + examples
        self.trainingset = word_tokenize(examples)

    # Generates using bigrams
    def bigram_generate(self, n=100):
        bigrams = self.ngrams(self.trainingset, 2)  # Get bigrams
        ret = ""  # Initialize ret
        current = "."  # Start as if we just ended a line
        i = 1
        while i < n or current != ".":  # Continue if we haven't reached n yet and/or if we're in the middle of a line
            # Choose next token
            nexttoken = choice(bigrams[current])
            # Add to ret
            if nexttoken not in string.punctuation and i > 1:
                ret += " "
            ret += nexttoken
            # Update vars for next iteration
            current = nexttoken
            i += 1
        return ret

    # Generates using ngrams for any n >= 2, default is trigrams
    def ngram_generate(self, n, numWords=100):
        # Catch if n is too small to work
        if n < 2:
            return "N is too small."

        currentTokens = ['.']  # Start as if we just ended a line

        # If we need more than word in the first key, generate them
        if n > 2:
            for i in range(2, n):
                key = " ".join(currentTokens)
                igrams = self.ngrams(self.trainingset, i)
                currentTokens.append(choice(igrams[key]))

        # Start ret with everything we've got so far except the new line marker
        ret = " ".join(currentTokens[1:])
        # print(ret)  # debug

        # Generate the ngrams we need
        ngrams = self.ngrams(self.trainingset, n)
        # Generate text based on previous words
        i = n - 1
        while i < numWords or currentTokens[n - 2] != ".":  # Continue if we haven't reached n yet and/or if we're in the middle of a line
            key = " ".join(currentTokens)
            # Pick next token, correct format, and add to ret
            nexttoken = choice(ngrams.get(key, ["."]))
            if nexttoken[0] not in string.punctuation:
                ret += " "
            ret += nexttoken

            # Update key for next iteration
            for j in range(0, n - 2):
                currentTokens[j] = currentTokens[j + 1]
            currentTokens[n - 2] = nexttoken
            i += 1

        return ret

    def ngrams(self, tokens, n=3):
        ngs = {}
        for i in range(len(tokens) - n + 1):
            key = " ".join(tokens[i:i + n - 1])
            val = tokens[i + n - 1]
            if key not in ngs.keys():
                ngs[key] = []
            ngs[key].append(val)
        return ngs

    def training_set(self):
        print(self.trainingset)
