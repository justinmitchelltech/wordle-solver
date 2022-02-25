import pandas as pd 
import numpy as np 

files = ["wordle-solver/data/words_3000_clean.csv", 
         "wordle-solver/data/words_all_clean.csv"]

output = pd.DataFrame()
for file in files:
    words = pd.read_csv(file, index_col=0)
    filtered = words

    WORD_LENGTH = 5
    SEARCHABLE_NDXS = np.arange(WORD_LENGTH)

    ifh = open("wordle-solver/input.txt")

    for count, info in enumerate(ifh):

        info = info.strip()
        info = info.replace(' ', '')
            
        info_ndx = count%5
        info_char = info[0]
        color = info[2]

        if color=="g":

            col = 'char'+str(info_ndx)
            filtered = filtered[filtered[col] == info_char]
        
        if color=="y":

            not_col = col = 'char'+str(info_ndx)
            search_in = SEARCHABLE_NDXS[SEARCHABLE_NDXS != info_ndx] 

            posibilities = pd.DataFrame()
            for i in search_in:
                if i == search_in[0]:
                    col = 'char'+str(i)
                    posibilities = filtered[filtered[col] == info_char]
                else:
                    col = 'char'+str(i)
                    posibilities = filtered[filtered[col] == info_char].append(posibilities)

            filtered = posibilities.drop_duplicates()
            filtered = filtered[filtered[not_col] != info_char]
        
        if color=="w":
            for i in SEARCHABLE_NDXS:
                col = 'char'+str(i)
                filtered = filtered[filtered[col] != info_char]
                
    filtered = filtered.drop_duplicates()

    source_str = file[file.find('words_')+6:]
    source_str = source_str[:source_str.find('_')]
    filtered.loc[:, ['source']] = source_str

    output = output.append(filtered)

output = output.reset_index()
output = output[['word', 'source']]
output.to_csv("wordle-solver/output.csv")
