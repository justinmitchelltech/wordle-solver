from tools.loading import print_loading_bar
import pandas as pd 


fh = open("wordle-solver/data/words_3000_raw.txt")
LENGTH = len(fh.readlines())  # get number of words 
fh = open("wordle-solver/data/words_3000_raw.txt")  # reopen file handle 

words = pd.DataFrame()

WORD_LENGTH = 5

for i, word in enumerate(fh): 

    print_loading_bar(i, LENGTH, title="Reading words: ", size=100, no_newline=True)

    word = word.strip().lower()

    if len(word) == WORD_LENGTH:
        words.loc[i, 'word'] = word 
        for j in range(WORD_LENGTH):
            col = 'char'+str(j)
            words.loc[i, col] = word[j]

words.to_csv("wordle-solver/data/words_3000_clean.csv")
