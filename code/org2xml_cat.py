# This program reads .org Catalogue files and converts them into TEI-conformant XML

# Step 1: Read and write the correct files
import sys
import re
import string

# write_file = open(sys.argv[1].replace('org','xml'), 'w')

file_id = sys.argv[1].replace('.org','').split('/')[-1] #Functions as document and file id

read_mode = "Header" # READING MODES: Physical, Binding, History, Quire, Contents, Bibliography

contents_items = { }

def get_locus(locus):
    # returns a locus_from and locus_to
    loci = locus.split(' ')
    if len(loci) == 2:
        locus_from = loci[0]
        locus_to = loci[1]
    else:
        locus_from = locus
        locus_to = "undefined"
    contents_items.update({"locus_from":locus_from, "locus_to":locus_to})

def rubricate(text):
    # Separates out the text items
    #print(text)
    rubric = ''
    latin_incipit = ''
    incipit = ''
    explicit = ''
    text = text.replace('[[','<hi>').replace(']]','</hi>').replace('(','<ex>').replace(')','</ex>')
    if "*" in text:
        #TODO final rubrics
        try:
            rubric = text.split("*",2)[1].strip("*")
            text = text.split("*",2)[2]
            contents_items.update({"rubric":rubric})
        except Exception:
            pass
    if "_" in text:
        print("Latin incipit found:")
        try:
            latin_incipit = text.split("_",2)[1].strip("_")
            print(latin_incipit)
            contents_items.update({"latin_incipit":latin_incipit})
            text = text.split("_",2)[2]
        except Exception:
            pass
    if "[...]" in text:
        try:
            incipit = text.split("[...]")[0]
            explicit = text.split("[...]")[1]
            contents_items.update({"incipit":incipit})
            contents_items.update({"explicit":explicit})
        except Exception:
            pass
    else:
        contents_items.update({"incipit":text})
    

def get_class(item):
    contents_items.update({"class":item})

def get_langs(lang):
    langs = lang.split(' ',1)
    contents_items.update({"mainLang":langs[0]})
    try:
        contents_items.update({"otherLangs":langs[1]})
    except Exception:
        pass

def get_level(this_level):
    global level
    level = int(this_level)
    global prev_level
    while prev_level >= level:
        write_file.write("</msItem>\n")
        prev_level -= 1
    prev_level = level
        
def get_title(text):
    try:
        title = text.split('][')[1].strip(']')
    except Exception:
        title = text
    contents_items.update({"title":title})

def get_key(titleKey):
    contents_items.update({"titleKey":titleKey})

def get_status(status):
    if "defect" in status:
        contents_items.update({"defective":"true"})

def add_note(note):
    contents_items.update({"note":note})

def find_author(author):
    try:
        author = author.split(' ',1)
        if author[0].isupper():
            contents_items.update({"authorKey":author[0]})
            author = author[1]
    except Exception:
        pass
    contents_items.update({"author":author})
            
        
    
functions = {
    "Loc" : get_locus,
    "Rub/Inc/Exp" : rubricate,
    "Type" : get_class,
    "Lang" : get_langs,
    "Level" : get_level,
    "Text" : get_title,
    "Key" : get_key,
    "Status" : get_status,
    "Note" : add_note,
    "Author" : find_author
    }


# Variables
head = ''

locus_from = ''
locus_to = ''
text_class = ''
prev_level = 0
level = 1

# Dictionaries
dictionaries = {
    "Physical" : {},
    "Binding" : {},
    "History" : {},
    }

supports = {
    "perg" : "parchment",
    "pap" : "paper",
    "perg pap" : "parchment and paper"
    }

quireIndex = []
quireStructure = {
    "Quires" : {},
    "Leaves" : {},
    "Structure" : {},
    "Changes" : {}
    }

contentsIndex = []
contents = {}

# Settlement and repository are based on how the file is named
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

with open(sys.argv[1], 'r') as read_file:
    for i, line in enumerate(read_file):
       if line.startswith("|-"):
           print("Skipping line", i)
           continue
       if line.startswith("*"):
           read_mode = line.split(' ')[1].strip('\n')
           print("Okay, now changing reading mode to:", read_mode)
           if read_mode in dictionaries:
               print("Yes,", read_mode, "is in dictionaries")
           else:
               print("No,", read_mode, "is not in dictionaries")
       elif read_mode == "Header":
           if "TITLE" in line:
               if "(" in line:
                   long_title = line.split(' ',1)[1].strip('\n').split('(',1)
                   title = long_title[0]
                   summary = long_title[1].strip(')')
               else:
                   title = line.split(' ',1)[1].strip('\n')
                   summary = None
               print("Document title:", title)
               print("Summary:", summary)
           else:
               if not "[[.." in line and head == '':
                   head = line.strip('\n')
                   head = re.sub(r'/(.+)/','<title>\\1</title>',head)
                   if "][" in head:
                       print("There seems to be a name in the header")
                       head = head.split('][')
                       for item in range(len(head)):
                           head[item] = re.sub(r'\[\[(.+)',r'<name key="\1">',head[item])
                           head[item] = re.sub(r'\]\]',r'</name>',head[item])
                       head = ' '.join(head)
                   print("There is now a header:", head)
                   # TODO: Header needs to be formatted perhaps?
       elif read_mode in dictionaries:
           line_items = [x.strip() for x in line.split('|')]
           try:
               dictionaries[read_mode].update({line_items[1][0:3]:line_items[2]})
           except Exception:
               pass
       elif read_mode == "Quire":
           line_items = [x.strip() for x in line.split('|')]
           if "Quires" in line_items:
               quireIndex = line_items
               print(quireIndex)
           elif len(line_items) == len(quireIndex):
               for item in line_items:
                   try:
                       item_key = quireIndex[line_items.index(item)]
                       #print(item_key, item)
                       #print(quireStructure[item_key])
                       quireStructure[item_key].append({i:item})
                   except Exception:
                       pass
       elif read_mode == "Contents":
           line_items = [x.strip() for x in line.split('|')]
           if "Rub/Inc/Exp" in line_items:
               contentsIndex = line_items
               print(contentsIndex)
               for item in line_items:
                   contents.update({item:{}})
           elif len(line_items) == len(contentsIndex):
               for item in line_items:
                   try:
                       item_key = contentsIndex[line_items.index(item)]
                       contents[item_key].update({i:item})
                   except Exception:
                       pass

  
# BIBLIOGRAPHY        
with open(sys.argv[1].replace('org','xml'), 'w') as write_file:
    # First write the header
    write_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<?xml-stylesheet type=\"text/css\" href=\"msDesc.css\"?>\n<TEI xmlns=\"http://www.tei-c.org/ns/1.0\" xml:id=\""+file_id+"\" type=\"manuscript\">\n<teiHeader>\n<fileDesc>\n<titleStmt>\n<title>"+title+"</title>\n<respStmt xml:id=\"SDV\">\n<resp when=\"2024\">Catalogue</resp>\n<persName>Seán D. Vrieland</persName>\n</respStmt>\n</titleStmt>\n<publicationStmt>\n<authority>When Danes Prayed in German</authority>\n</publicationStmt>\n")

     #Source Description
    write_file.write("<sourceDesc>\n<msDesc>\n<msIdentifier>\n<settlement key=\""+city+"\"/>\n<repository key=\""+repository+"\"/>\n<idno corresp=\""+title+"\"/>\n</msIdentifier>\n")

    #Write the header
    write_file.write("<head>\n"+head+"\n</head>\n")

    #Write contents
    

    # Check for summary
    if summary != None:
        write_file.write("<msContents>\n<summary>"+summary+"</summary>\n")
    else:
        write_file.write("<msContents>\n")

    # TODO: Nest in levels
    starting_line = min([min(contents[item]) for item in contents])
    ending_line = max([max(contents[item]) for item in contents])
    print("Contents found on lines",starting_line,"to",ending_line)
    item_nr = 1
    for line in range(starting_line, ending_line):
        #print (type(contents))
        if line not in contents["Level"]:
            in_keys = False
            for item in contents:
                if line in contents[item]:
                    in_keys = True
            if in_keys == True:
                print("Level not found on line",line,". Treating as 1.")
                get_level(1)
            else:
                print("Skipping line",line)
                continue
        for item in contents:
            try: 
                func = functions.get(item)
                if callable(func):
                    func(contents[item][line])                    
            except Exception:
                pass
            # Start writing msItem
        if "class" not in contents_items.keys():
            contents_items.update({"class":"undefined"})

        write_file.write("<msItem class=\""+contents_items['class']+"\" n=\""+str(item_nr)+"\"")
        if "defective" in contents_items.keys():
            write_file.write(" defective=\"true\"")
        write_file.write(">\n")
        if "locus_from" in contents_items.keys():
            write_file.write("<locus from=\""+contents_items['locus_from']+"\" to=\""+contents_items['locus_to']+"\"/>\n")
        try:
            write_file.write("<title key=\""+contents_items['titleKey']+"\">"+contents_items['title']+"</title>\n")
        except Exception:
            try:
                write_file.write("<title>"+contents_items['title']+"</title>\n")
            except Exception:
                write_file.write("<title/>\n")
        if "rubric" in contents_items.keys():
            write_file.write("<rubric>"+contents_items['rubric']+"</rubric>\n")
        if "latin_incipit" in contents_items.keys():
             write_file.write("<incipit type=\"latin\">"+contents_items['latin_incipit']+"</incipit>\n")
        if "incipit" in contents_items.keys():
            write_file.write("<incipit>"+contents_items['incipit']+"</incipit>\n")
        if "explicit" in contents_items.keys():
            write_file.write("<explicit>"+contents_items['explicit']+"</explicit>\n")

        if "mainLang" in contents_items.keys():
            write_file.write("<textLang mainLang=\""+contents_items['mainLang']+"\"")
            if "otherLangs" in contents_items.keys():
                write_file.write(" otherLangs=\""+contents_items['otherLangs']+"\"")
            write_file.write("/>\n")
        if "note" in contents_items.keys():
            write_file.write("<note>"+contents_items[note]+"</note>\n")
        if "author" in contents_items.keys():
            try:
                write_file.write("<author key=\""+contents_items['authorKey']+"\">"+contents_items['author']+"</author>\n")
            except Exception:
                write_file.write("<author>"+contents_items['author']+"</author>\n")

        
        
        contents_items.clear()
        item_nr += 1
    while level >= 1:
        write_file.write("</msItem>\n")
        level -= 1
    # close contents
    write_file.write("</msContents>\n")

    print("Finished writing contents. Now moving on to Physical Description.")

    write_file.write("<physDesc>\n<objectDesc>\n")
    #SupportDesc
    print(dictionaries["Physical"])
    try:
        write_file.write("<supportDesc material=\""+dictionaries["Physical"]["SUP"]+"\">\n<support>"+supports[dictionaries["Physical"]["SUP"]]+"</support>\n")
    except Exception:
        write_file.write("<supportDesc>\n")
        print("Cannot find support. Skipping for now.")
        pass

    try:
        write_file.write("<extent>"+dictionaries["Physical"]["NUM"]+".")
    except Exception:
        write_file.write("<extent>")
        print("Cannot find extent. Skipping for now.")
        pass
    try:
        write_file.write("<dimensions>\n<height>"+dictionaries["Physical"]["SIZ"].split(' ')[0]+"</height>\n<width>"+dictionaries["Physical"]["SIZ"].split(' ')[1]+"</width>\n</dimensions></extent>\n")
    except Exception:
        write_file.write("</extent>\n")
        print("Cannot find dimensions. Skipping for now.")

    #Close Support Desc
    write_file.write("</supportDesc>\n")
    write_file.write("</objectDesc>\n")
    write_file.write("</physDesc>\n")
    
    # close rest of file
    write_file.write("</msDesc>\n</sourceDesc>\n</fileDesc>\n</teiHeader>\n<facsimile>\n<surface/>\n</facsimile>\n</TEI>")
