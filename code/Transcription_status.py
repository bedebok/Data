# Goal: Read through all .org files in folder (minus README.org) and output the following into a .csv:
# Title
# Manuscript
# Work
# Language
# Status
# Number of words

# Finally, output the number of transcriptions and number of words

# Step 1: Cycle through all files

import os

# filepath = ~/Documents/DFF/Data/Prayers/org or ../Prayers/org
path = "../Prayers/org"

# Change the directory
os.chdir(path)

# Read text file

def read_text_file(file):
    with open(file, 'r') as f:
        #print(f.readlines(1))
        for i, line in enumerate(f):

            # FIND TITLE 
            if "#+TITLE:" in line:
                title = line.replace('\n', '').split(' ', 1)[1:]
                #print("Title: ",title)

            # FIND STATUS
            elif "Status" in line:
                status = line.split('|')[2]
                print(status)

            # FIND MS
            elif "Manuscript" in line:
                try:
                    ms = line.split('|')[2]
                    print(ms)
                except IndexError:
                    print("Index error! ", file)

            # FIND LANG
            elif "Language" in line:
                try:
                    lang = line.split('|')[2]
                    print(lang)
                except IndexError:
                    print("Index error! ", file)

                

# Iterate all files
for file in os.listdir():
    if file.endswith(".org") and not file.startswith("README"):
        read_text_file(file)

        #NB: Also reads README!
        # FIXED

# Step 2: Read files


# Step 3: Count words after * Transcription
