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
path = "../Texts/org"
num_files = 0

# Change the directory
os.chdir(path)

# Error message for index error
def index_error_message(file):
    print("Index error for file ", file)

# Wordcount
count = False
wordcount = 0
def count_words(line):
    global wordcount
    words = len(line.split(' '))
    if line.endswith('-\n'):
        #print("Minus one word at line ", line)
        words =- 1
    wordcount += words
    return words

# Write .csv file
f = open("Status.csv", "w")
f.write("filename,manuscript,prayer,work,language,status,wordcount\n")
f.close()

def append_to_csv(filename, ms, title, work, lang, status, num_words):
    f = open("Status.csv", "a")
    items = [filename, ms, title, work, lang, status, str(num_words)]
    combined_string = ",".join(items)
    f.write(combined_string + "\n")
    f.close()
    

# Read text file

def read_text_file(file):
    global count
    global num_files
    num_files += 1
    with open(file, 'r') as f:
        #print(f.readlines(1))
        work = ""
        status = ""
        ms = ""
        locus = ""
        lang = ""
        title = ""
        num_words = 0
        for i, line in enumerate(f):

            # Before calling the count_words() function, which is triggered by the line "* Transcription", collect all metadata:
            # 

            if count == False:
                if "* Transcription" in line:
                    count = True
                    
            # FIND TITLE, WORK, LANG 
                elif "#+TITLE:" in line:
                    try:
                        title_item = line.replace('\n', '').split(' ', 1)[1:]
                        title = title_item[0].strip()
                        print(title)
                    except IndexError:
                        index_error_message(file)

                elif "Work" in line:
                    try:
                        work = line.split('|')[2].strip()
                    except IndexError:
                        index_error_message(file)

                elif "Language" in line:
                    try:
                        lang = line.split('|')[2].strip()
                    except IndexError:
                        index_error_message(file)
    

            # FIND MS, LOCUS
                elif "Manuscript" in line:
                    try:
                        ms = line.split('|')[2].strip()
                        print(ms)
                    except IndexError:
                        index_error_message(file)
                elif "Locus" in line:
                    try:
                        locus = line.split('|')[2].strip()
                        print(locus)
                    except IndexError:
                        index_error_message(file)

            # FIND STATUS, WORDCOUNT
                elif "Status" in line:
                    try:
                        status = line.split('|')[2].strip()
                    except IndexError:
                        index_error_message(file)


            # CALL WORDCOUNT FUNCTION PER LINE
            elif count == True:
                if not line.startswith("---") and not line.startswith("*"):
                    num_words = num_words + count_words(line)
                    

        # AT END
        try:
            print("Wordcount: ", num_words)
        except UnboundLocalError:
            print("Wordcount error in file ", file)
        print("----------")
        append_to_csv(file, ms, title, work, lang, status, num_words)
        count = False

# Iterate all files
for file in os.listdir():
    if file.endswith(".org") and not file.startswith("README") and not file.startswith("."):
        read_text_file(file)


# Final Summary:
print("#############\nFinal Summary\n#############")
print("Total files: ", num_files)
print("Total words: ", wordcount)
