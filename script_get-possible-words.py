import pandas as pd 
import numpy as np 

# List of words to use
files = ["wordle-solver/data/words_3000_clean.csv",
         "wordle-solver/data/words_20000_clean.csv",
         "wordle-solver/data/words_all_clean.csv"]

# Init data storage 
output = pd.DataFrame()

# Narrow down word options by brute force
for file in files:  # Loop through each list of words 

    words = pd.read_csv(file, index_col=0)
    filtered = words  # Start with NO words filtered away 

    # Constants 
    WORD_LENGTH = 5
    SEARCHABLE_NDXS = np.arange(WORD_LENGTH)

    # Open txt file where user inputs their try information 
    ifh = open("wordle-solver/input.txt")

    for count, info in enumerate(ifh):  # Loop through try information

        info = info.strip()
        info = info.replace(' ', '')
            
        info_ndx = count%5  # Which letter ndx info is about 
        info_char = info[0]  # Which letter the user tried 
        color = info[2]  # What color that letter turned 

        # Green letter: brute-force word filtering algo
        if color=="g":

            col = 'char'+str(info_ndx)
            filtered = filtered[filtered[col] == info_char]  # Letter is in that column 
        
        # Yellow letter: brute-force word filtering algo
        if color=="y":

            not_col = 'char'+str(info_ndx)
            search_in = SEARCHABLE_NDXS[SEARCHABLE_NDXS != info_ndx]  # Letter could be in any other column

            posibilities = pd.DataFrame()  

            for i in search_in:  # Loop through columns that the letter could be in, and get possible words
                if i == search_in[0]:
                    col = 'char'+str(i)
                    posibilities = filtered[filtered[col] == info_char]
                else:
                    col = 'char'+str(i)
                    posibilities = filtered[filtered[col] == info_char].append(posibilities)

            filtered = posibilities.drop_duplicates()
            filtered = filtered[filtered[not_col] != info_char]  # Remove words where letter is in yellow column
        
        # Black/Grey letter: brute-force word filtering algo
        if color=="k":

            for i in SEARCHABLE_NDXS:  # Loop through all columns (letter ndx's)
                col = 'char'+str(i)
                filtered = filtered[filtered[col] != info_char]  # Drop all words that have that letter
                
    filtered = filtered.drop_duplicates()  

    # Identify the list of words where the current list of possibilities came from 
    source_str = file[file.find('words_')+6:]
    source_str = source_str[:source_str.find('_')]
    filtered.loc[:, ['source']] = source_str

    filtered = filtered.sort_values('score', ascending=False)  # Sort them by their frequency score 
    output = output.append(filtered)  # Append the filtered results from this word list to list of all possibilities

output = output.reset_index()  
output = output[['word', 'score', 'source']]
output.to_csv("wordle-solver/output.csv")  # txt file where user can easily see the recommended words
