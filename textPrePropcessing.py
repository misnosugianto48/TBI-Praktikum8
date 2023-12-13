#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 13:08:37 2023

@author: misno48
"""

'''
perform text pre processing: punctuation removal, lowercase operation,
stopwords removal, and stemming operation
'''

def textProcessing(data):
    #Regular expression operations: https://docs.python.org/3/library/re.html
    import re

    #Dokumentasi Sastrawi Stemmer: https://pypi.org/project/Sastrawi/
    #import StopWordRemoverFactory class
    from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
    factory = StopWordRemoverFactory()
    stopword = factory.create_stop_word_remover()

    #Create stemmer
    from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    #Create an empty list of corpus
    corpus = []
    for (index, sura, aya, text) in data:
        # [^a-zA-Z] means: eliminate number and punctuation, except alphabet and A-Z
        review = re.sub('[^a-zA-Z]', ' ', text)
        #Lowercase operation
        review = review.lower()
        #Stopwords removal operation
        review = stopword.remove(review)
        jumlah_kata_awal = len(review.split())
        kondisi = True
        while(kondisi):
            review = re.sub(' +', ' ', review)
            review = stopword.remove(review)
            jumlah_kata_baru = len(review.split())
            if(jumlah_kata_awal == jumlah_kata_baru):
                kondisi = False
            else:
                jumlah_kata_awal = jumlah_kata_baru
        #Stemming operation
        review = stemmer.stem(review)
        #Add data quran verses to List
        corpus.append((index, sura, aya, review))
    return corpus