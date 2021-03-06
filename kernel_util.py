from sklearn.feature_extraction.text import *
#from sklearn.kernel_approximation import Nystroem
import scipy.io
from scipy.linalg import *
import sys
import json
import numpy as np

def parse_json(json_file):
    corpus = []
    with open(json_file, 'r') as f:
        for l in f:
            corpus.append(json.loads(l)['reviewText'])
    return corpus

def compute_ngram_kernels(corpus, n_max):
    kernels = []
    for n in range(1, n_max+1):
        ngram_vectorizer = TfidfVectorizer(ngram_range=(n,n))
        ngram_TM = ngram_vectorizer.fit_transform(corpus)
        ngram_kernel = np.dot(ngram_TM, ngram_TM.T)
        kernels.append(ngram_kernel)
    return kernels

def dyad_library(kernels, p=10):
    # Obtain k_i from eigenvalue decompositions 
    # of given kernels. (Only p largest eigenvalues)
    for i in range(len(kernels)):
        try:
            kernels[i] = kernels[i].todense()
        except:
            continue

    n = kernels[0].shape[0]
    q = kernels[0].shape[1]
    w, K = eigh(kernels[0], eigvals=(q-p,q-1))
    for i in range(K.shape[1]):
        K[:,i] *= np.sqrt(w[i])
    for kernel in kernels[1:]:
        w, v = eigh(kernel, eigvals=(q-p,q-1))
        for i in range(v.shape[1]):
            v[:,i] *= np.sqrt(w[i])
        K = np.hstack((K, v))
    return K

