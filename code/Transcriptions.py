# Goal: Input either manuscript (m) or text (t) and get a count of how many files contain it, what language, and word count.

#Cycle through all files

import os


# path = "../Prayers/org"
# os.chdir(path)
# number_of_files = 0

#Error message for index error
def index_error_message(file):
    print("Index error for file ", file)

count_mode = None

while count_mode not in {"m", "t", "a"}:
    count_mode = input("Count from [m]anuscript, [t]ext or [a]ll: ")

if count_mode == "m":
    print ("Counting from manuscripts")
elif count_mode == "t":
    print ("Counting from texts")
elif count_mode == "a":
    print ("Counting from all files")
#    import Transcription_status.py
    
