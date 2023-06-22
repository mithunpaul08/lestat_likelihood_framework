corpus = "Four score and twenty years ago our forefathers came into this land. This land of prosperity , and american dream."
from collections import Counter
#get vocab
#get stats for pairs
#pick highest pair
# merge

def get_vocab(data):
    vocab = {}
    for line in data:
        words = line.lower().split(" ")
        words_count=Counter(words)
        for key,val in words_count.items():
            newkey= " ".join(list(key)) + "</w>"
            vocab[newkey] = val
    return vocab

def get_stats(vocab):
    all_words = vocab.keys()
    pairs_2gram=[]
    for word in all_words:
        symbols = word.split()
        for i in range(1,len(symbols)):
            pair=symbols[i]+symbols[i-1]
            pairs_2gram.append(pair)
    pair_count = Counter(pairs_2gram)
    print(pair_count)
    return pair_count
#
def merge(pattern, vocab):
    new_vocab = {}
    for word, freq in vocab.items():
        symbols = word.split()
        new_word=[]
        
        for i in range(0,len(symbols)):
            if symbols[i]+symbols[i+1]==pattern:
                new_word.append(pattern)
                i=i+1
            else:
                new_word.append(symbols[i])


        new_word_str = " ".join(new_word)
        new_vocab[new_word_str] = 1
    return new_vocab








def get_bpe(corpus_split,n ):
    vocab = get_vocab(corpus_split)
    for i in range(n):
        pairs = get_stats(vocab)
        best_pair_freq = sorted(pairs.items(), key= lambda x:x[1],reverse=True)
        best_pair = best_pair_freq[0][0]
        vocab = merge(best_pair,vocab)
    return vocab

n = 1
corpus_split = corpus.split(".")
print(get_bpe(corpus_split,n))

