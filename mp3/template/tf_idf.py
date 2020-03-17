# tf_idf_bayes.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 09/28/2018
# Modified by Jaewook Yeom 02/02/2020

"""
This is the main entry point for the Extra Credit Part of this MP. You should only modify code
within this file for the Extra Credit Part -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

import numpy as np
import math
from collections import defaultdict
import time



def compute_tf_idf(train_set, train_labels, dev_set):
    """
    train_set - List of list of words corresponding with each movie review
    example: suppose I had two reviews 'like this movie' and 'i fall asleep' in my training set
    Then train_set := [['like','this','movie'], ['i','fall','asleep']]

    train_labels - List of labels corresponding with train_set
    example: Suppose I had two reviews, first one was positive and second one was negative.
    Then train_labels := [1, 0]

    dev_set - List of list of words corresponding with each review that we are testing on
        It follows the same format as train_set

    Return: A list containing words with the highest tf-idf value from the dev_set documents
        Returned list should have same size as dev_set (one word from each dev_set document)
    """
    # TODO: Write your code here
    # find all words in all reviews and review counts (idf)
    all_words = set()
    for rev in train_set:
        for word in rev:
            all_words.add(word)
    word_freqs = defaultdict()
    for word in all_words:
        word_freqs[word] = 0
    for rev in train_set:
        for word in all_words:
            if word in rev:
                word_freqs[word] += 1
    train_len = len(train_set)

    # tf
    result = []
    for rev in dev_set:
        rev_len = len(rev)
        word_nums = defaultdict()
        for word in rev:
            if word_nums.get(word) == None:
                word_nums[word] = 1
            else:
                word_nums[word] = word_nums.get(word) + 1
        w = word_nums.keys()
        tf = defaultdict()
        for word in w:
            freq = 0
            if word_freqs.get(word) != None: # if word in dev set not in training set
                freq = word_freqs.get(word)
            tf[word] = (word_nums.get(word) / rev_len) * math.log10(train_len / (1 + freq))
        keys = list(tf.keys())
        vals = list(tf.values())
        keymax = keys[vals.index(max(vals))] # max value of dict: https://www.geeksforgeeks.org/python-get-key-with-maximum-value-in-dictionary/
        result.append(keymax)

    # return list of words (should return a list, not numpy array or similar)
    return result