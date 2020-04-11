import numpy as np
import pandas as pd
import glob
import nltk
import re
import string
from nltk.tokenize import word_tokenize
from sklearn.metrics.pairwise import cosine_similarity
import ast

def get_main_points(fid, main_points):
    """
    Returns main points for both sides given fid and main_points table
    """
    for_points = main_points.loc[main_points['id'] == fid]['For_Main_Points'].item()
    for_points = ast.literal_eval(for_points)
    against_points = main_points.loc[main_points['id'] == fid]['against_Main_Points'].item()
    against_points = ast.literal_eval(against_points)
    return for_points, against_points

punctuations = string.punctuation
def tokenize_point(point):
    """
    Returns a list of lowercased tokens, without punctuations
    """
    tokens = [t for t in word_tokenize(point.lower()) if t not in punctuations]
    return tokens

def word2glove(word, embedding_index):
    """
    Returns GloVe embedding given a word, and embedding_index['unk'] if word does not exist in the dictionary
    """
    word = word.lower()
    try:
        word_vec = embedding_index[word]
    except:
        word_vec = embedding_index['unk']
    return word_vec

def point2gloves(point, embedding_index):
    """
    Returns a list of word embeddings given a sentence
    """
    word_vecs = np.array([word2glove(word, embedding_index) for word in tokenize_point(point)])
    return word_vecs

def attention_vector(word, embedding_index, title_vecs):
    """
    Returns the attention vector of a word w.r.t. the title (a_k in paper)
    """
    word_vec = word2glove(word, embedding_index)
    # normalized dot product, then softmax as weights
    weights = np.sum(word_vec * title_vecs, axis=1) / np.linalg.norm(title_vecs, axis=1)
    weights = np.exp(weights) / np.sum(np.exp(weights))
    attention_vec = np.matmul(title_vecs.T, weights.reshape((-1,1))).T[0]
    return attention_vec

def matching_vector(attention_vec, word, embedding_index):
    """
    Returns the matching vector of a word w.r.t. the title by concatenating the
    resulting attention vector and word embedding(m_k in paper)
    """
    matching_vec = np.concatenate((attention_vec, word2glove(word, embedding_index)), axis = None)
    return matching_vec

def point2mn(point, title, embedding_index):
    #point_vecs = point2gloves(point, embedding_index)
    words = tokenize_point(point)
    title_vecs = point2gloves(title, embedding_index)
    nn_inputs = []
    for word in words:
        attention_vec = attention_vector(word, embedding_index, title_vecs)
        matching_vec = matching_vector(attention_vec, word, embedding_index)
        nn_inputs.append(matching_vec)
    return np.array(nn_inputs)
