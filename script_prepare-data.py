import pandas as pd 
from tools.loading import print_loading_bar


data_source_str = "wordle-solver/data/words_3000"  # Designates data to process

# Open list of words
fh = open(data_source_str + "_raw.txt")
LENGTH = len(fh.readlines())  # get number of words 
fh = open(data_source_str + "_raw.txt")  # reopen file handle 

# Load letter frequency lookup table
freqs = pd.read_csv("wordle-solver/data/lookup_char-freqs.csv", index_col=0)

# Initialize data storage 
words = pd.DataFrame()

WORD_LENGTH = 5  # Word length setting (Wordle is currently a 5-letter game)

# Process list of words 
for i, word in enumerate(fh): 

    print_loading_bar(i, LENGTH, title="Preparing word data: ", size=100, no_newline=True)

    word = word.strip().lower()

    if len(word) == WORD_LENGTH:
        words.loc[i, 'word'] = word 
        score = 0
        for j in range(WORD_LENGTH):
            col = 'char'+str(j)
            words.loc[i, col] = word[j]
            score = freqs.loc[word[j], col] + score
        words.loc[i, 'score'] = score

words = words.sort_values('score', ascending=False)
words.to_csv(data_source_str + "_clean.csv")
