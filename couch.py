#!/usr/bin/python

import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from NBUtils import * 
import sys, getopt

def train_and_show_results(pos, neg, neu, pos_bigrams, neg_bigrams, neu_bigrams):
    negcutoff = len(neg)*3/4
    poscutoff = len(pos)*3/4
    neucutoff = len(neu)*3/4

    test_bag_of_words = neg[negcutoff:] + pos[poscutoff:] + neu[neucutoff:]
    train_corpora_bag_of_words = neg[:negcutoff] + pos[:poscutoff] + neu[:neucutoff]
    
    if (pos_bigrams != None and neg_bigrams != None):
        neg_bigrams_cutoff = len(neg_bigrams)*3/4
        pos_bigrams_cutoff = len(pos_bigrams)*3/4
        neu_bigrams_cutoff = len(neu_bigrams)*3/4

        test_bigrams = neg_bigrams[neg_bigrams_cutoff:] + pos_bigrams[pos_bigrams_cutoff:] + neu_bigrams[neu_bigrams_cutoff:]
        train_corpora_bigrams = neg_bigrams[:neg_bigrams_cutoff] + pos_bigrams[:pos_bigrams_cutoff] + neu_bigrams[:neu_bigrams_cutoff]
        
    print "negative corpus: ", len(neg) 
    print "positive corpus: ", len(pos)
    print "neutral corpus: ", len(neu)

    print 'Saving dataset - Naive Bayes' 
    naive_bayes = NaiveBayesClassifier.train(train_corpora_bag_of_words)
    save_dataset('naive_bayes.dat', naive_bayes)

    print 'Naive Bayesian results'
    print 'Accuracy:', nltk.classify.util.accuracy(naive_bayes, test_bag_of_words)
    naive_bayes.show_most_informative_features()  
    print_precision_recall(naive_bayes, test_bag_of_words) 


    if (pos_bigrams != None and neg_bigrams != None):
        print 'Saving bigram dataset - Naive Bayes' 
        naive_bayes_bigrams = NaiveBayesClassifier.train(train_corpora_bigrams)
        save_dataset('naive_bayes_bigrams.dat', naive_bayes_bigrams)

        print 'Naive Bayesian with bigram analysis results'
        print 'Accuracy:', nltk.classify.util.accuracy(naive_bayes_bigrams, test_bigrams)
        naive_bayes_bigrams.show_most_informative_features()  
        print_precision_recall(naive_bayes_bigrams, test_bigrams) 
        

def main():
    argv = sys.argv
    opts = args = None
    try:
        opts, args = getopt.getopt(argv[1:], "hlbp:n:m:s:") 
    except getopt.error, e:
        print "error: ", e
        print "usage %s -p path_positive_folder -n path_negative_folder -m path_neutral_folder [-l lowercase] [-b with-bigram analysis] [-s portuguese|english stopwords removal] [-l(ower case)]" % argv[0]
        sys.exit(-1)

    lower = bigram = positive_folder = negative_folder = neutral_folder = stpwords = None
    for option, value in opts:
        if option in ("-h", "--help"):
            raise Usage(help_message)
        if option in ("-l", "--lower"):
            lower = True
        if option in ("-b", "--with-bigram"):
            bigram = True
        if option in ("-p", "--positive_folder"):
            positive_folder = value
        if option in ("-n", "--negative_folder"):
            negative_folder = value
        if option in ("-m", "--neutral_folder"):
            neutral_folder = value
        if option in ("-s", "--stopwords"):
            stpwords = value

    neg = create_corpus_from_dir_and_tag(negative_folder, "negative", stpwords, lower)
    pos = create_corpus_from_dir_and_tag(positive_folder, "positive", stpwords, lower)
    neu = create_corpus_from_dir_and_tag(neutral_folder, "neutral", stpwords, lower)

    if (bigram):
        pos_bigrams = create_corpus_from_dir_and_tag(negative_folder, "negative", stpwords, lower, wordlist_to_bigrams_dict)
        neg_bigrams = create_corpus_from_dir_and_tag(positive_folder, "positive", stpwords, lower, wordlist_to_bigrams_dict)
        neu_bigrams = create_corpus_from_dir_and_tag(neutral_folder, "neutral", stpwords, lower, wordlist_to_bigrams_dict)

    train_and_show_results(pos, neg, neu, pos_bigrams, neg_bigrams, neu_bigrams)


if __name__ == "__main__":
    sys.exit(main())
