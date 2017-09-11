# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 10:51:25 2017

@author: Kun Li
"""

import re, os, codecs, sys
from math import log
import numpy as np

def readfile(path):
    vacabulary = []
    documentsNum = 0
    if os.path.isfile(path):
        f = open(path) 
        text = f.read()
        text = text.lower()
        text = re.sub('[^a-z]', ' ', text)
        vacabulary = text.strip().split()
        return vacabulary
    else:
        if os.path.exists(path):
            files = os.listdir(path) 
            for each in files:
                if not os.path.isdir(each):
                    f = open(path+"/"+each)
                    documentsNum += 1 
                    text = f.read()
                    text = text.lower()
                    text = re.sub('[^a-z]', ' ', text)
                    words_list = text.strip().split()
                    vacabulary.extend(words_list)
        else:
            print "path does noesn't exist."
            return
    return vacabulary, documentsNum

def removeStopwords(vac):
    DEFAULT_STOPWORD_PATH = './stopwords.txt'
    stopwords = []
    with codecs.open(DEFAULT_STOPWORD_PATH, "r", encoding="utf-8-sig") as f:
        stopwords = f.readlines()
        stopwords = map(lambda s : s.strip(), stopwords)  
    for word in vac:
        if word in stopwords:
            vac.remove(word)
    return vac

def generate_dict(vac):
    freq = {}
    for word in list(set(vac)):
        freq[word] = vac.count(word)
    return freq

def nb(spam_path, ham_path, flag = False):
    spam_vac, spam_docNum = readfile(spam_path)
    ham_vac, ham_docNum = readfile(ham_path)
    
    if flag:
        spam_vac = removeStopwords(spam_vac)
        ham_vac = removeStopwords(ham_vac)
    
    spam_dict = generate_dict(spam_vac)
    ham_dict = generate_dict(ham_vac)
    
    total_vac = spam_vac
    total_vac.extend(ham_vac)
    total_vac = list(set(total_vac))
    p_spam = {}
    spam_denominator = len(total_vac) + len(spam_vac)
    for word in total_vac:
        p_spam[word] = float(spam_dict.get(word, 0) + 1) / spam_denominator
    p_ham = {}
    ham_denominator = len(total_vac) + len(ham_vac)
    for word in total_vac:
        p_ham[word] = float(ham_dict.get(word, 0) + 1) / ham_denominator
        
    spam_prior = float(spam_docNum) / (spam_docNum + ham_docNum)
    ham_prior = 1 - spam_prior
    return spam_prior, ham_prior, p_spam, p_ham, spam_denominator, ham_denominator

def predict(spam_prior, ham_prior, p_spam, p_ham, spam_denominator, ham_denominator, path, flag, target):
    success = 0
    count = 0        
    filenames = np.array(os.listdir(path))
    filenames_path = [os.path.join(path, fn) for fn in filenames]
    for each in filenames_path:
        spam_score = log(spam_prior)
        ham_score = log(ham_prior)
        vac = readfile(each)
        if flag:
            removeStopwords(vac)
        for word in vac:
            if word in p_ham:
                #p_ham[word] = 1.0 / ham_denominator
                ham_score += log(p_ham[word])
            if word in p_spam:
                #p_spam[word] = 1.0 / spam_denominator
                spam_score += log(p_spam[word])
        if spam_score > ham_score:
            out = 'spam'
        else:
            out = 'ham'
        if out == target:
            success += 1
        count += 1
    print success, count
    return success, count

def main(flag):
    train_spam_path = r'train\spam'
    train_ham_path = r'train\ham'
    spam_prior, ham_prior, p_spam, p_ham, spam_denominator, ham_denominator = nb(train_spam_path, train_ham_path, flag=False)              
    
    test_spam_path = r'test\spam'
    test_ham_path = r'test\ham'
    #flag = True
    spam_success, spam_count = predict(spam_prior, ham_prior, p_spam, p_ham, spam_denominator, ham_denominator,
                                       test_spam_path, flag, target = 'spam')
    ham_success, ham_count = predict(spam_prior, ham_prior, p_spam, p_ham, spam_denominator, ham_denominator,
                                       test_ham_path, flag, target = 'ham')
    print flag, float(spam_success + ham_success) / (spam_count + ham_count)

if len(sys.argv()) > 2:
    main(sys.argv(2))      
    
    