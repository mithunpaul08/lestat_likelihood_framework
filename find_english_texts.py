#LDC has english and spanish files. This code will get only the english files since that is the only one to be used in IR

from collections import *
import os
import shutil

BASEDIR_PATH="/Users/mitch/research/lestat/LDC"
DOCUMENT_PROFILE_PATH="/docs/document_profile.tab"
PARENT_CHILDREN_PATH="/docs/parent_children.tab"
DATA_FOLDER_BASE="/data/ltf"
ONLY_ENGLISH_LTF_FILES="/Users/mitch/research/lestat/LDC/only_english_ltf_files/"

all_english_language_ltf_files=[]



#open up each of the 4 parts of LDC data corpus
for eachfolder in os.scandir(BASEDIR_PATH):
    if "LDC" in eachfolder.name:

        DOCUMENT_PROFILE_FILE = eachfolder.path + DOCUMENT_PROFILE_PATH
        PARENT_CHILDREN_FILE = eachfolder.path +  PARENT_CHILDREN_PATH
        DATA_FOLDER_FILE_BASE = eachfolder.path + DATA_FOLDER_BASE




        #get all the names of parent files which are in english
        only_english_filenames=[]

        with open(DOCUMENT_PROFILE_FILE) as f:
            lines=f.readlines()
            for line in lines:
                line_split = line.split("\t")
                if line_split[1] and line_split[2]:
                    language=line_split[1]
                    filename=line_split[2]
                    if "english" in language.lower():
                        only_english_filenames.append(filename.strip())
        counter=Counter(only_english_filenames)



        #get all the parent child maps
        parent_child={}
        with open(PARENT_CHILDREN_FILE) as f:
            lines = f.readlines()
            for line in lines:
                line_split = line.split("\t")
                parent=line_split[2]
                child=line_split[3]
                child_file_type = line_split[5]
                if "ltf" in child_file_type:
                    if parent in parent_child:
                        parent_child[parent].append(child)
                    else:
                        parent_child[parent]=[child]

        #find which one of the english parents have children and move all those children files separately into another folder
        for each_english_parent in counter.keys():
            if each_english_parent in parent_child:
                all_english_language_ltf_files.extend(parent_child[each_english_parent])






all_english_language_ltf_files=set(all_english_language_ltf_files)
print(len(all_english_language_ltf_files))
unique_all_english_language_ltf_files = Counter(all_english_language_ltf_files)


temp=Counter()

#go through all ltf.xml files in the data directory of that corpus and see if
for eachfolder in os.scandir(BASEDIR_PATH):
    if "LDC" in eachfolder.name:
        DOCUMENT_PROFILE_FILE = eachfolder.path + DOCUMENT_PROFILE_PATH
        PARENT_CHILDREN_FILE = eachfolder.path +  PARENT_CHILDREN_PATH
        DATA_FOLDER_FILE_BASE = eachfolder.path + DATA_FOLDER_BASE
        dirs = os.walk(DATA_FOLDER_FILE_BASE)
        for dirpath, dirnames, filenames in dirs:
                for each_file in filenames:
                    if "ltf.xml" in each_file:
                        if each_file.split(".")[0] in unique_all_english_language_ltf_files:
                            if not each_file in temp:
                                temp[each_file]=1
                                full_path_child_file_name = os.path.join(dirpath, each_file)
                                #shutil.copy(full_path_child_file_name, ONLY_ENGLISH_LTF_FILES)


                           #


print(temp)
print(len(temp))