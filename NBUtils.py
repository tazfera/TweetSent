# there is code inspired by steamhacker.com - jacker
# there is code inspired by sentiment_analysis - gleicon moraes

from nltk.stem import RSLPStemmer, PorterStemmer
from nltk.corpus import stopwords
from collections import defaultdict
from nltk.metrics import BigramAssocMeasures
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import precision, recall, f_measure
import codecs
import os, glob
import itertools
import pickle

# stopwords
g_stopwords = defaultdict(lambda: None)
g_stopwords.update({"portuguese": stopwords.words('portuguese'), 
                    "english": stopwords.words('english')})

# saving dataset
def save_dataset(filename, classifier):
    f = open(filename,"wb") 
    pickle.dump(classifier, f,1) 
    f.close() 

# loading dataset
def load_dataset(filename):
    f = open(filename,"rb") 
    c = pickle.load(f) 
    f.close() 
    return c

# bag of words (sentences)
def wordlist_to_dict(words):
    return defaultdict(lambda: None, [(word, True) for word in words])

# bigrams
def wordlist_to_bigrams_dict(words, score_fn=BigramAssocMeasures.chi_sq, n=200):
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)
    return defaultdict(lambda: None, [(ngram, True) for ngram in itertools.chain(words, bigrams)])

# IR filters
def check_stopwords(data, sw):
    ret = []
    for a in data:
        if a.lower().encode('utf-8') not in g_stopwords[sw]:
           ret.append(a)
    return " ".join(ret)

def lower_case(b):
    r=[]
    for w in b:
        r.append(w.lower())
    return r

# buffer handling
def create_corpus_from_file_list(allfiles, tag, stpwords, lower, feat_extractor=wordlist_to_dict):
    if stopwords: sw = g_stopwords[stpwords]
    corpus = []
    for infile in allfiles:
        n = apply_filters_to_file(tag, infile, stpwords, lower)
        corpus.append((feat_extractor(n), tag))
    return corpus 

# file handling
def create_corpus_from_dir_and_tag(folder, tag, stpwords, lower, feat_extractor=wordlist_to_dict):
    allfiles = glob.glob(os.path.join(folder, '*.txt'))
    return create_corpus_from_file_list(allfiles, tag, stpwords, lower, feat_extractor)
    
def apply_filters_to_file(tag, infile, sw, l):
    body = get_body(infile)
    if body == None:
        print 'empty file: ', infile
        return
    if l != None:
        body = lower_case(body)
    if sw != None:
        body = check_stopwords(body, sw)

    return body.split()

def get_body(filename):
    try:
        f = codecs.open(filename, "r", "utf-8" )
        b = f.read()
        f.close()
        return b.split()
    except IOError:
        print "File not found"
        return None

def classify(tweets):
    c = load_dataset('naive_bayes.dat')
    classi = []
    for t in range(len(tweets)):
        feats = dict([(word, True) for word in tweets[t].split()])
        classi.append(c.classify(feats))

    return classi

def print_precision_recall(classifier, test_dict):
    refsets = defaultdict(set)
    testsets = defaultdict(set)
    for i, (feats, label) in enumerate(test_dict):
        refsets[label].add(i)
        observed = classifier.classify(feats)
        testsets[observed].add(i)
    print 'pos precision:', precision(refsets['positive'], testsets['positive'])
    print 'pos recall:', recall(refsets['positive'], testsets['positive'])
    print 'pos F-measure:', f_measure(refsets['positive'], testsets['positive'])
    print 'neg precision:', precision(refsets['negative'], testsets['negative'])
    print 'neg recall:', recall(refsets['negative'], testsets['negative'])
    print 'neg F-measure:', f_measure(refsets['negative'], testsets['negative'])
    print 'neu precision:', precision(refsets['neutral'], testsets['neutral'])
    print 'neu recall:', recall(refsets['neutral'], testsets['neutral'])
    print 'neu F-measure:', f_measure(refsets['neutral'], testsets['neutral'])


