# The following code takes .org input files written on every second line and processes them into TEI P5 XML (diplomatic level transcription)

import sys
import re
import string
write_file = open(sys.argv[1].replace('org','xml'), 'w')

file_id = sys.argv[1].replace('.org','').split('/')[-1]
ms_id = file_id.split('_')[0]

line_break = 1
page_break = ''
word_count = 1
start_text_level = 0

transcribe = False
header_written = False # Set to False until we write the header (after catching metadata)
broken_word = False # checks to see if words are broken across lines or pages
break_line = False # checks to see if there is a line break

# Possible updates
# sentence = False # checks whether text can be divided into further sentences
# The idea here is to catch [[ ]] highlights as the start of a new sentence. The problem is it would also catch if only the first letter of the entire text is highlighted. Could be a boolean input "Sentence divisions y/n"?

repositories = {
    "AM" : ["KBH", "AMS"],
    "GK" : ["KBH", "KBK"],
    "NK" : ["KBH", "KBK"],
    "Ho" : ["STH", "KBS"],
    "Lu" : ["LUN", "LUB"],
    "Ka" : ["KAL", "KSB"],
    "Li" : ["LNK", "LSB"],
    "UU" : ["UPS", "UUB"]
    }

city, repository = repositories.get(file_id[0:2])


# MAIN RUN-THROUGH OF LINES
with open(sys.argv[1].replace('.org','') + '.org', 'r') as read_file:
    print("First gathering metadata for teiHeader")
    for i, line in enumerate(read_file):


        # Before the "* Transcription" line, check for all important metadata:
        # idno (key), title (text), titleKey (key), locus_from, locus_to, language (key)
        # These will all go into the teiHeader
        
        if transcribe == False:
            if "* Transcription" in line:
                transcribe = True
            elif "#+TITLE" in line:
                title = line.split(' ',1)[1].replace('\n','')
                print("Title:",title)
            elif "Manuscript" in line:
                idno = line.split('|')[2].strip()
                print("Manuscript key:",idno)
            elif "Locus" in line:
                locus = line.split()
                locus_from = locus[3]
                if ":" in locus_from:
                    line_break = int(locus_from.split(':')[1])
                    try:
                        word_count = int(locus_from.split(':')[2])
                    except Exception:
                        pass
                    locus_from = locus_from.split(':')[0]
                locus_to = locus[4]
                if ":" in locus_to:
                    locus_to = locus_to.split(':')[0]
                print("Locus: from",locus_from,"to",locus_to)
                locus_Decl = "<locus from=\""+locus_from+"\" to=\""+locus_to+"\"/>"
                page_break = locus_from
            elif "Work" in line:
                if len(line.split()) == 5:
                    is_titleKey = True
                    titleKey = line.split()[3]
                    print("Title key:",titleKey)
                else:
                    print("No title key. Using #other instead")
                    titleKey = "#other"
            elif "Language" in line:
                mainLang = line.split()[3]
                print("Language:",mainLang)
                if len(line.split()) > 5:
                    otherLangs = " " .join(line.split()[4:-1])
                    print("Other Langauges:",otherLangs)
                    lang_Decl = "<textLang mainLang=\""+mainLang+"\" otherLangs=\""+otherLangs+"\"/>"
                else:
                    lang_Decl = "<textLang mainLang=\""+mainLang+"\"/>"
                    print("No other languages recorded")

        # From here is where we work on the actual transcription
        elif transcribe == True:
            # First write the header and then set variable to "True"
            if header_written == False:
                print("Okay, now writing the teiHeader into the XML file.")
                write_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<?xml-stylesheet type=\"text/css\" href=\"textDisplay.css\"?>\n<TEI xmlns=\"http://www.tei-c.org/ns/1.0\" xml:id=\""+file_id+"\" type=\"text\">\n<teiHeader>\n<fileDesc>\n<titleStmt>\n<title>"+title+"</title>\n<respStmt xml:id=\"SDV\">\n<resp when=\"2024\">Catalogue</resp>\n<persName>Seán D. Vrieland</persName>\n</respStmt>\n</titleStmt>\n<publicationStmt>\n<authority>When Danes Prayed in German</authority>\n</publicationStmt>\n")

                #Source Description
                write_file.write("<sourceDesc>\n<msDesc>\n<msIdentifier>\n<settlement key=\""+city+"\"/>\n<repository key=\""+repository+"\"/>\n<idno corresp=\""+ms_id+"\">"+idno+"</idno>\n</msIdentifier>\n")

                #Contents
                write_file.write("<msContents>\n<msItem>\n"+locus_Decl+"\n<title key=\""+titleKey+"\">"+title+"</title>\n"+lang_Decl+"\n</msItem>\n</msContents>\n</msDesc>\n</sourceDesc>\n</fileDesc>\n</teiHeader>\n<text>\n<body>\n")
                

                #This is the original I am working from
#                                write_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<TEI xmlns=\"http://www.tei-c.org/ns/1.0\">\n<teiHeader>\n<fileDesc>\n<titleStmt>\n<title>"+title+"</title>\n<respStmt xml:id=\"SDV\">\n<resp when=\"2024\">Catalogue</resp>\n<persName>Seán D. Vrieland</persName>\n</respStmt>\n</titleStmt>\n<publicationStmt>\n<authority>When Danes Prayed in German</authority>\n</publicationStmt>\n<sourceDesc>\n<msDesc>\n<msIdentifier>\n<idno xml:id=\""+idno+"\"/>\n</msIdentifier>\n<msContents>\n<msItem>\n<locus from=\""+locus_from+"\" to=\""+locus_to+"\"/>\n<title key=\""+titleKey+"\">"+title.replace('\n','')+"</title>\n<textLang mainLang=\""+xmlLang+"\"/>\n</msItem>\n</msContents>\n</msDesc>\n</sourceDesc>\n</fileDesc>\n</teiHeader>\n<text>\n<body>\n")
                                
                header_written = True
            # Check for new section types beginning with "*"
            # TODO: Make different levels of section
            # HOW: Variable of "start_tag" and "end_tag"
            # Text: start_tag = <p>

            # Check for new lines
            if line == "\n":
                #write_file.write("<lb n=\""+str(line_break + 1)+"\"/>")
                #if broken_word == False:
                #    write_file.write("\n")
                line_break += 1
                word_count = 1
                break_line = True
                # ISSUE: Catches last blank of page as new line
                # Issue resolved by pushing the writing of the lb to later.

            elif "*" in line[0]:
                text_level = line.split()[0].count('*') - 1
                text_type = line.split()[1]
                print("New text type on line",str(i+1)+":",text_type,"(level:",str(text_level),"of",str(start_text_level)+")")
                if start_text_level != 0:
                    write_file.write("</p>")
                    if text_level <= start_text_level:
                        for i in range(start_text_level - text_level + 1):
                            write_file.write("</div>\n")
                write_file.write("<div type=\""+text_type.lower()+"\">\n")
                if len(line.split()) > 2:
                    text_name = line.split()[2].replace(":",'').capitalize().replace('_',' ')
                    write_file.write("<head>"+text_name+"</head>")
                write_file.write("<p>\n")
                start_text_level = text_level

            # Check for page break of style "---2r---"
            elif line[0] == "-":
                page_break = line.split()[0].replace('-','')
                write_file.write("<pb n=\""+page_break+"\"/>")
                if broken_word == False:
                    write_file.write("\n")
                line_break = 0
                break_line = False

            else:
                if break_line == True:
                    write_file.write("<lb n=\""+str(line_break)+"\"/>")
                    if broken_word == False:
                        write_file.write("\n")
                    break_line = False
                # First I need to check for highlights in words. They look like this:
                # [[3 red blue][M]] ...
                line = re.sub(r" (?=[^][]*\])", "_", line)
                line = re.sub(r"\[\[(.+?)\]\[(.)\]\]",r'<hi_rend="\1">\2</hi>', line)
                line = re.sub(r"\[\[(.*)",r'<hi>\1</hi>', line)
                line = re.sub(r"\]\]", r'</hi>', line)
                # Next I need to look for supplied text in words. They look like this:
                # xxx[x]xxx
                line = re.sub(r"\[#(.*)!(.*)\]", r'<supplied_source="#\1">\2</supplied>', line)
                line = re.sub(r"\[", r"<supplied>", line)
                line = re.sub(r"\]", r"</supplied>", line)
                # Then I also need to check for editorial corrections. They look like this:
                # {sic/corr}
                line = re.sub(r"{(.*)/(.*)}", r"<choice><sic>\1</sic><corr>\2</corr></choice>", line)
                words = line.split()
                is_note = False
                for i, word in enumerate(words, 1):
                    word = word.replace('_', ' ').replace('(','<ex>').replace(')','</ex>').replace('⸠','<del>').replace('⸡', '</del>').replace('⸌', '<add>').replace('⸍', '</add>')
                    word_id = str(ms_id)+"_" + page_break+"." + str(line_break)+"."+str(word_count)
                    word_count += 1
                    if is_note == True:
                        next
                    elif "fn::" in word:
                        is_note = True
                        print("There is a note on line",str(i+1)+". I'll skip that for now.")
                    elif broken_word == True:
                        write_file.write(word+"</w>\n")
                        broken_word = False
                    elif word[-1:] == "-":
                        write_file.write("<w xml:id=\""+word_id+"\">"+word.replace('-',''))
                        broken_word = True
                    elif "<supplied source" in word:
                        write_file.write(word+"\n")
                    else:
                        write_file.write("<w xml:id=\""+word_id+"\">"+word+"</w>\n")
                        
                    
        


# CLOSE FILE

# Start by closing last paragraph
write_file.write("</p>")
# Then count down the divs
while start_text_level != 0:
    write_file.write("\n</div>")
    start_text_level -= 1
write_file.write("\n</body>\n</text>\n</TEI>")
