from Markov import *
from LyricFetcher import *


# Reformats output into rap
def paragraphtorap(s):
    # print(s)  # debug
    lines = s.split(". ")
    ret = []
    for line in lines:
        if line != "":
            ret.append(line.capitalize().replace(".", ""))
    return "\n".join(ret)


def main():
    # Create lyric fetcher
    fetcher = LyricFetcher()
    # Get artist name
    artistname = input("Enter name of Artist: ")

    while artistname.lower() != "quit":
        # Get lyrics for Artist
        lyrics = fetcher.getLyrics(artistname)

        # Feed into model & generate new lyrics
        model = Markov(lyrics)
        print("\nBigram\n")
        print(paragraphtorap(model.bigram_generate()))
        print("\nTrigram\n")
        print(paragraphtorap(model.ngram_generate(3)))
        print("\n4-gram\n")
        print(paragraphtorap(model.ngram_generate(4)))

        # Start again
        artistname = input("Enter name of Artist: ")

if __name__ == "__main__":
    main()
