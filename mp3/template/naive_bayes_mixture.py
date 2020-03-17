# naive_bayes.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 09/28/2018
# Modified by Jaewook Yeom 02/02/2020

"""
This is the main entry point for Part 2 of this MP. You should only modify code
within this file for Part 2 -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""


import numpy as numpy
import math
from collections import Counter





def naiveBayesMixture(train_set, train_labels, dev_set, bigram_lambda, unigram_smoothing_parameter, bigram_smoothing_parameter, pos_prior):
    """
    train_set - List of list of words corresponding with each movie review
    example: suppose I had two reviews 'like this movie' and 'i fall asleep' in my training set
    Then train_set := [['like','this','movie'], ['i','fall','asleep']]

    train_labels - List of labels corresponding with train_set
    example: Suppose I had two reviews, first one was positive and second one was negative.
    Then train_labels := [1, 0]

    dev_set - List of list of words corresponding with each review that we are testing on
              It follows the same format as train_set

    bigram_lambda - float between 0 and 1

    unigram_smoothing_parameter - Laplace smoothing parameter for unigram model (between 0 and 1)

    bigram_smoothing_parameter - Laplace smoothing parameter for bigram model (between 0 and 1)

    pos_prior - positive prior probability (between 0 and 1)
    """
    # TODO: Write your code here
    # Source for generating bigrams:
    # https://stackoverflow.com/questions/5850986/joining-pairs-of-elements-of-a-list-python
    
    num_train = len(train_set)
    num_pos = 0 # number of reviews
    num_neg = 0
    pos_words = 0 # number of words
    neg_words = 0
    pos_bigs = 0 # number of bigrams
    neg_bigs = 0
    pos_counter = Counter()
    neg_counter = Counter()
    pos_bigram_counter = Counter()
    neg_bigram_counter = Counter()
    for i in range(num_train):
        rev = train_set[i] # rev is a list
        bigrams = [i+j for i,j in zip(rev, rev[1::])]
        if train_labels[i] == 1: # positive review
            num_pos += 1
            pos_counter.update(rev)
            pos_words += len(rev)
            pos_bigram_counter.update(bigrams)
            pos_bigs += len(bigrams)
        else: # negative review
            num_neg += 1
            neg_counter.update(rev)
            neg_words += len(rev)
            neg_bigram_counter.update(bigrams)
            neg_bigs += len(bigrams)

    reviews = [] # for dev set 
    for rev in dev_set:
        pos_prob = math.log10(pos_prior) # init to prior
        neg_prob = math.log10(1 - pos_prior)
        pos_big_prob = pos_prob
        neg_big_prob = neg_prob
        for word in rev:
            pos_prob += math.log10((pos_counter[word] + unigram_smoothing_parameter)/(unigram_smoothing_parameter * 2 + pos_words))
            neg_prob += math.log10((neg_counter[word] + unigram_smoothing_parameter)/(unigram_smoothing_parameter * 2 + neg_words))
        bigrams = [i+j for i,j in zip(rev, rev[1::])]
        for bigram in bigrams:
            pos_big_prob += math.log10((pos_bigram_counter[bigram] + bigram_smoothing_parameter)/(bigram_smoothing_parameter * 2 + pos_bigs))
            neg_big_prob += math.log10((neg_bigram_counter[bigram] + bigram_smoothing_parameter)/(bigram_smoothing_parameter * 2 + neg_bigs))
        if pos_prob*(1 - bigram_lambda) + pos_big_prob*bigram_lambda > neg_prob*(1 - bigram_lambda) + neg_big_prob*bigram_lambda: # review positive
            reviews.append(1)
        else: # review negative
            reviews.append(0)


    # return predicted labels of development set (make sure it's a list, not a numpy array or similar)
    return reviews