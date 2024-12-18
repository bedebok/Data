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
        print(f.readlines(1))

# Iterate all files
for file in os.listdir():
    if file.endswith(".org"):
        read_text_file(file)

# Step 2: Read files

# Step 3: Count words after * Transcription
