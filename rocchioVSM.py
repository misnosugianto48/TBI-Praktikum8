#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 13:19:51 2023

@author: misno48
"""

import numpy as np

# Fungsi untuk menghitung bobot dokumen
def calculate_document_weights(query, documents):
    # Proses pembentukan vocabulary
    vocabulary = set(query.split())
    for doc in documents:
        vocabulary.update(doc.split())

    # Pembentukan representasi vektor dokumen dalam model ruang vektor
    document_vectors = []
    for doc in documents:
        vector = [doc.count(term) for term in vocabulary]
        document_vectors.append(vector)
    # Vektor query
    query_vector = [query.count(term) for term in vocabulary]
    return np.array(document_vectors), np.array(query_vector), list(vocabulary)


# Fungsi untuk menghitung relevansi dengan algoritma Rocchio
def rocchio_feedback(query_vector, relevant_vectors, non_relevant_vectors, alpha=1, beta=0.75, gamma=0.15):
    relevant_mean = np.mean(relevant_vectors, axis=0) if len(relevant_vectors) > 0 else np.zeros_like(query_vector)
    non_relevant_mean = np.mean(non_relevant_vectors, axis=0) if len(non_relevant_vectors) > 0 else np.zeros_like(query_vector)
    updated_query_vector = alpha * query_vector + beta * relevant_mean - gamma * non_relevant_mean
    return updated_query_vector

# Fungsi untuk menemukan dokumen terkait dengan Vector Space Model
def retrieve_documents(query_vector, document_vectors, k):
    # Perhitungan skor cosine similarity antara query dan dokumen
    scores = np.dot(document_vectors, query_vector) / (np.linalg.norm(document_vectors, axis=1) * np.linalg.norm(query_vector))
    # Pengurutan dokumen berdasarkan skor similarity
    ranked_documents = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
    # Mengambil k dokumen teratas
    top_k_documents = ranked_documents[:k]
    return top_k_documents