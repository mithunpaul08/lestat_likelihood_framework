#LDC has english and spanish files. This code will get only the english files since that is the only one to be used in IR

import collections

BASEDIR_PATH="/Users/mitch/Downloads/LDC2021E06_KAIROS_Schema_Learning_Corpus_Complex_Event_Source_Data_Part_4_V1.0/"
DOCUMENT_PROFILE_PATH="docs/document_profile.tab"
PARENT_CHILDREN_PATH="docs/parent_children.tab"



import os
dirs=os.walk(BASEDIR_PATH)


#get all the names of parent files which are in english
only_english_filenames=[]
with open(os.path.join(BASEDIR_PATH,DOCUMENT_PROFILE_PATH)) as f:
    lines=f.readlines()
    for line in lines:
        line_split = line.split("\t")
        if line_split[1] and line_split[2]:
            language=line_split[1]
            filename=line_split[2]
            if "english" in language.lower():
                only_english_filenames.append(filename.strip())
counter=collections.Counter(only_english_filenames)

#get all the names of parent files which are in english
only_english_filenames=[]
with open(os.path.join(BASEDIR_PATH,DOCUMENT_PROFILE_PATH)) as f:
    lines=f.readlines()
    for line in lines:
        line_split = line.split("\t")
        if line_split[1] and line_split[2]:
            language=line_split[1]
            filename=line_split[2]
            if "english" in language.lower():
                only_english_filenames.append(filename.strip())
counter=collections.Counter(only_english_filenames)


#get all the parent child maps
parent_child={}
with open(os.path.join(BASEDIR_PATH,PARENT_CHILDREN_PATH)) as f:
    lines = f.readlines()
    for line in lines:
        line_split = line.split("\t")
        parent=line_split[2]
        child=line_split[3]
        if parent in parent_child:
            parent_child[parent].append(child)
        else:
            parent_child[parent]=[child]

all_english_language_ltf_files=[]
for each_english_parent in counter.keys():
    if each_english_parent in parent_child:
        all_english_language_ltf_files.extend(parent_child[each_english_parent])



print(len(all_english_language_ltf_files))
