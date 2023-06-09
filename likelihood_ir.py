

import nltk
from nltk.stem import PorterStemmer
from rank_bm25 import *
import warnings
import pysbd
warnings.filterwarnings('ignore')
import nltk
#nltk.download('punkt')
# adding words to stopwords
from nltk.tokenize import word_tokenize
from gensim.parsing.preprocessing import STOPWORDS
from collections import OrderedDict
from pathlib import Path
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--query", required=True)
parser.add_argument("--data_dir", required=True)
args = parser.parse_args()




#for each document retrieved from IR
#use pysbd to split it into list of sentences
# use clean _up to remove stray \n and strip
# use stopwprds_removal_gensim_custom tokenize and remove stop words and return it still as a single string or merged sentences
# so all_data (and lst1) in turn contains a list of documents again



source_dir= Path(args.data_dir)
files = source_dir.iterdir()
ps = PorterStemmer()




# adding custom words to the pre-defined stop words list
all_stopwords_gensim = STOPWORDS.union(set(['disease']))
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

def document_cleanup(document):
            document_sent=split_into_sentences(document)
            document_sent=clean_up(document_sent)
            document_sent=stopwords_removal_gensim_custom(document_sent)
            document_sent=" ".join(document_sent)
            return document_sent

def load_file(files):
    all_data=[]
    for file in files:
        with file.open('r') as f:
            document=f.read()
            doc_str=document_cleanup(document)
            all_data.append(doc_str)
    return all_data

corpus_stemmed=load_file(files)
tokenized_corpus = [doc.split(" ") for doc in corpus_stemmed]
bm25 = BM25Okapi(tokenized_corpus)

query = args.query
query=document_cleanup(query)
tokenized_query = query.split(" ")


doc_scores = bm25.get_scores(tokenized_query)
counter=0
for score in doc_scores:
    if score>0:
        counter+=1

print(f"total number of documents retrieved for the query is {counter}")

docs = bm25.get_top_n(tokenized_query, corpus_stemmed, n=5)
for doc in docs:
    print("\n******\n")
    print(doc)




