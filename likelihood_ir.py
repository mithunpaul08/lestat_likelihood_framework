import os

#for each document retrieved from IR
#use pysbd to split it into list of sentences
# use clean _up to remove stray \n and strip
# use stopwprds_removal_gensim_custom tokenize and remove stop words and return it still as a single string or merged sentences
# so all_data (and lst1) in turn contains a list of documents again




import nltk
from nltk.stem import PorterStemmer
from rank_bm25 import *
import warnings
import pysbd
warnings.filterwarnings('ignore')
#uncomment 1st run
# nltk.download('punkt')
from tqdm import tqdm
# adding words to stopwords
from nltk.tokenize import word_tokenize
from gensim.parsing.preprocessing import STOPWORDS
from collections import OrderedDict
from pathlib import Path
import argparse
OUTPUT_FILE="data/retrieved_docs.txt"
TOPN=74


parser = argparse.ArgumentParser()
parser.add_argument("--query")
parser.add_argument("--queries",help="If you want to pass multiple queries",)
parser.add_argument("--data_dir", required=True)
args = parser.parse_args()




source_dir= Path(args.data_dir)
files = source_dir.iterdir()
list_of_file_names=os.listdir(source_dir)
ps = PorterStemmer()




# adding custom words to the pre-defined stop words list
all_stopwords_gensim = STOPWORDS.union(set(['']))
def stopwords_removal_gensim_custom(lst):
    lst1 =list()
    for str in lst:
        text_tokens = word_tokenize(str)
        text_tokens=unique_words_only(text_tokens)
        text_tokens = [word for word in text_tokens if not word in all_stopwords_gensim]
        #text_tokens=stem_words(text_tokens)
        str_t = " ".join(text_tokens)
        lst1.append(str_t)
    return lst1

def stem_words(words):
    return [ps.stem(word) for word in words]

def split_into_sentences(text):
    seg = pysbd.Segmenter(language="en", clean=False)
    return seg.segment(text)

def unique_words_only(words):
    ord=OrderedDict()
    ordk=ord.fromkeys(words)
    ordkl=[x for x in ordk.keys()]
    return ordkl


def clean_up(list_sent):
    cleaned_sent=[]
    for lst in list_sent:
        str=lst.strip()
        str=str.replace("\n"," ")
        if len(str)>0:
            cleaned_sent.append(str.lower())
    return cleaned_sent

def cleanup(document):
            document_sent=split_into_sentences(document)
            document_sent=clean_up(document_sent)
            document_sent=stopwords_removal_gensim_custom(document_sent)
            document_sent=" ".join(document_sent)
            return document_sent.lower()

filename_plaintext={}
def load_file(files):
    all_data=[]
    for file in tqdm(files, desc="Loading files",total=len(list_of_file_names)):
        with file.open('r') as f:
            document=f.read()
            filename_plaintext[file.name.lower()] = document
            doc_str=cleanup(file.name.lower()+"\t"+document)
            all_data.append(doc_str)
    return all_data


def printRelevantFilesCount(tokenized_query):
    doc_scores = bm25.get_scores(tokenized_query)
    counter = 0
    for score in doc_scores:
        if score > 0:
            counter += 1
    print(f"total number of documents retrieved for the query {tokenized_query} is {counter}")


def initializeDiskFile(filename):
    with open(filename,'w') as f:
        f.write("")
        f.close()

def writeToDisk(filename, docs, tokenized_query) :
    with open(filename,'a') as f:
        f.write("\n\n\n\n**************************************************************************************************************\n")
        query_combined=" ".join(tokenized_query)
        f.write(f"query = {query_combined}\n")
        for index,doc in enumerate(docs):
            #get the filename and write the actual plain text, not the stemmed/cleaned version, to disk for readability
            if ".rsd" in doc:
                source_file=doc.split()[0]
                if source_file in filename_plaintext:
                    text_to_write=filename_plaintext[source_file]
                    f.write(f"document number {index+1}: {text_to_write}\n\n\n\n#####################\n\n\n\n")
        f.close()


corpus_stemmed = load_file(files)
tokenized_corpus = [doc.split(" ") for doc in corpus_stemmed]
bm25 = BM25Okapi(tokenized_corpus)
tokenized_query=""


initializeDiskFile(OUTPUT_FILE)

if args.queries:
    for query in args.queries.split(","):
        query = cleanup(query)
        tokenized_query = query.split(" ")
        printRelevantFilesCount(tokenized_query)
        if tokenized_query != "":
            docs = bm25.get_top_n(tokenized_query, corpus_stemmed,TOPN)
            writeToDisk(OUTPUT_FILE, docs,tokenized_query)
else:
    query = args.query
    query = cleanup(query)
    tokenized_query = query.split(" ")
    printRelevantFilesCount(tokenized_query)
    if tokenized_query != "":
        docs = bm25.get_top_n(tokenized_query, corpus_stemmed, TOPN)
        writeToDisk(OUTPUT_FILE, docs,tokenized_query)




