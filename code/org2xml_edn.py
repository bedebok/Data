# The following code takes .org input files written on every second line and processes them into TEI P5 XML (diplomatic level transcription)

import sys
import re
import string
write_file = open(sys.argv[1] + '.xml', 'w')

# WRITE HEADER
write_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<TEI xmlns=\"http://www.tei-c.org/ns/1.0\">")

line_break = 1
header = 0
delete = 0
next_page = ''
pagebreak = ''
transcribe = False

# MAIN RUN-THROUGH OF LINES
with open(sys.argv[1] + '.org', 'r') as read_file:
    for line in read_file:
        if line[0:8] == "#+TITLE:":
            title = line[9:-1]
            print(title)
        elif line[0:14] == "| Manuscript |":
            print(line[15:-2])
        elif line[0:7] == "| Locus":
            locus = line[15:-2]
            print(locus)
        


# CLOSE FILE
write_file.write("</body>\n</text>\n</TEI>")
