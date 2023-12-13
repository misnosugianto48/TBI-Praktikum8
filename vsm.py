#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 13:30:09 2023

@author: misno48
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
#import nltk


#nltk.download('punkt')
# Tokenization and vocabulary creation
def tokenize_and_create_vocabulary(documents):

    vocabulary = set()
    tokenized_documents = []

    for (index, sura, aya, review) in documents:
        tokens = word_tokenize(review)
        tokens = [word.lower() for word in tokens if word.isalpha()]
        tokenized_documents.append(" ".join(tokens))
        vocabulary.update(tokens)
    return tokenized_documents, list(vocabulary)

def calculate_vsm(query, corpus):
    # Call tokenize_and_create_vocabulary function
    tokenized_docs, vocabulary = tokenize_and_create_vocabulary(corpus)
    # Term weighting with Term Frequency - Inverse Document Frequency (TF-IDF)
    vectorizer = TfidfVectorizer(vocabulary=vocabulary)
    tfidf_matrix = vectorizer.fit_transform(tokenized_docs)
    # Tokenization and term weighting for query
    query_tokens = word_tokenize(query)
    query_tokens = [word.lower() for word in query_tokens if word.isalpha()]
    query_vector = vectorizer.transform([" ".join(query_tokens)])
    # Similarity calculation with Cosine Similarity equation
    cosine_similarities = cosine_similarity(tfidf_matrix, query_vector)
    # Mengurutkan dokumen berdasarkan skor kesamaan kosinus
    ranked_documents = sorted(enumerate(cosine_similarities), key=lambda x: x[1], reverse=True)

    # Mengambil 7 dokumen teratas
    top_documents = ranked_documents[:7]
    return top_documents