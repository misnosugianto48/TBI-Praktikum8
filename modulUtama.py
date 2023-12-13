#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 13:48:04 2023

@author: misno48
"""

import db
import textPrePropcessing
import rocchioVSM
import vsm

# Ambil data nomor index, surat, ayat, dan teks ayat dari tabel id_indonesian
query = "SELECT * FROM id_indonesian limit 100"
data = db.getData(query)

# Pra-pemrosesan text: punctuation removal, lowercase operation,
# stopwords removal, dan operasi stemming
corpus = textPrePropcessing.textProcessing(data)

documents = []
for (index, sura, aya, text) in corpus:
    documents.append(text)

# Program utama
if __name__ == "__main__":
    # Pengguna menginputkan query
    query = input("Masukkan query: ")
    # Menampilkan hasil awal Vector Space Model (VSM)
    top_documents = vsm.calculate_vsm(query, corpus)

    print("\n7 Peringkat Dokumen Teratas:")
    for doc_idx, i in top_documents:
      if(i != 0. and i != 0.1):
            print(f"No. index {doc_idx}: Score {i}. {data[doc_idx]}")
            print()

    # Pengguna menginputkan dokumen hasil pencarian relevan dan tidak relevan
    try:
        relevant_indices = [int(idx) - 1 for idx in input("Masukkan nomor index dokumen relevan (pisahkan dengan spasi): ").split()]

    except ValueError:
        print("Input tidak valid. Masukkan nomor dokumen yang valid.")
        exit()

    try:
        non_relevant_indices = [int(idx) - 1 for idx in input("Masukkan nomor index dokumen tidak relevan (pisahkan dengan spasi):").split()]

    except ValueError:
        print("Input tidak valid. Masukkan nomor dokumen yang valid.")
        exit()

    # Menghitung bobot dokumen dan query
    document_vectors, query_vector, vocabulary = rocchioVSM.calculate_document_weight(query, documents)

    # Melakukan relevance feedback dengan algoritma Rocchio
    updated_query_vector = rocchioVSM.rocchio_feedback(query_vector, document_vectors[relevant_indices],document_vectors[non_relevant_indices])

    # Menggunakan vektor query yang telah di-update untuk mencari dokumen terkait
    updated_top_documents = rocchioVSM.retrieve_documents(updated_query_vector, document_vectors, 7)

    # Menampilkan hasil
    print("\nDokumen hasil relevance feedback:")


    for i, doc in updated_top_documents:
        print(type(doc))
        if(doc != 0.):
            print(f"No. index {i}: Score {doc}. ayat: {data[i]}")
            print()