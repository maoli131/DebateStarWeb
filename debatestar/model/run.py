import numpy as np
import pandas as pd
import nltk
import re
from nltk import sent_tokenize
from nltk.corpus import stopwords
import sys
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from .point2mn import point2mn
from .point2mn import get_main_points
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
torch.manual_seed(1)

# relative paths
import os
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Extract word vectors
embedding_index = {}
f = open(os.path.join(__location__, 'glove.6B.100d.txt'))
for line in f:
    values = line.split()
    word = values[0]
    coefs = np.asarray(values[1:],dtype='float32')
    embedding_index[word] = coefs
f.close()

with open(os.path.join(__location__, 'boilerplates.txt')) as f:
    boilerplates = [l.strip() for l in f.readlines()]

stop_words = stopwords.words('english')
def remove_stopwords(sen):
    sen_new = " ".join([i for i in sen if i not in stop_words])
    return sen_new

def text_rank_summarize(paragraph, boilerplates = boilerplates):
    sentences = [s.strip() for s in sent_tokenize(paragraph) if s not in boilerplates]
    k = min(int(np.floor(np.sqrt(len(sentences)))), 5)
    clean_sentences = pd.Series(sentences).str.replace("[^a-zA-Z]", " ")
    clean_sentences = [s.lower() for s in clean_sentences]
    clean_sentences = [remove_stopwords(r.split()) for r in clean_sentences]
    sentence_vectors = []
    for i in clean_sentences:
        if len(i) != 0:
            v = sum([embedding_index.get(w, embedding_index['unk']) for w in i.split()])/(len(i.split())+0.001)
        else:
            v = np.zeros((100,))
        sentence_vectors.append(v)
    sim_mat = np.zeros([len(sentences), len(sentences)])
    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i != j:
                sim_mat[i][j] = cosine_similarity(sentence_vectors[i].reshape(1,100), \
                                                  sentence_vectors[j].reshape(1,100))[0,0]
    nx_graph = nx.from_numpy_array(sim_mat)
    scores = nx.pagerank(nx_graph)
    ranked_sentences = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)
    return [s[1] for s in ranked_sentences[:k]]

def run_lstm_one_sentence(sentence, title, lstm, hidden, embedding_index):
    inputs = point2mn(sentence, title, embedding_index)
    tensor_input = [torch.tensor([x]) for x in inputs]
    tensor_input = torch.cat(tensor_input).view(1, len(tensor_input), -1)
    tensor_output, hidden = lstm(tensor_input, hidden)
    return hidden

def run_lstm_on_fid(title, for_main_points, against_main_points, embedding_index, lstm, hidden, combine_func = [torch.mean, torch.max]):
    """
    Given fid, find main points for the debate and for each sentence, pass corresponding 
    matching vectors to lstm and get hidden state in the end. Gather the hidden states
    in a list and do combine_func.
    -combine_func: the funtion applied to combine lstm outputs from one side elementwisely
    """
    

    for_output_list = []
    against_output_list = []
    
    for sentence in for_main_points:
        hidden_state, cell_state = run_lstm_one_sentence(sentence, title, lstm, hidden, embedding_index)
        for_output_list.append(hidden_state)
        
    for sentence in against_main_points:
        hidden_state, cell_state = run_lstm_one_sentence(sentence, title, lstm, hidden, embedding_index)
        against_output_list.append(hidden_state)
    for_torchs = []
    against_torchs = []
    for combine_f in combine_func:
        if combine_f == torch.mean:
            for_torch = combine_f(torch.stack(for_output_list), dim = 0, keepdim = True)#[0]
            against_torch = combine_f(torch.stack(against_output_list), dim = 0, keepdim = True)#[0]
        else:
            for_torch = combine_f(torch.stack(for_output_list), dim = 0, keepdim = True)[0]
            against_torch = combine_f(torch.stack(against_output_list), dim = 0, keepdim = True)[0]
        for_torchs.append(for_torch)
        against_torchs.append(against_torch)
    if len(for_torchs) == 2:
        t1 = torch.cat((for_torchs[0], for_torchs[1]), dim = 2)
        t2 = torch.cat((against_torchs[0], against_torchs[1]), dim = 2)
        return torch.cat((t1, t2), dim = 2)
    return torch.cat((for_torchs[0], against_torchs[0]), dim = 2)

class LSTMNet(nn.Module):
    def __init__(self, output_size_1, output_size_2, n_layers, embedding_dim, hidden_dim, combine_funcs, hidden, drop_prob=0.5):
        super(LSTMNet, self).__init__()
        self.output_size_1 = output_size_1
        self.output_size_2 = output_size_2
        self.hidden_dim = hidden_dim
        self.n_layers = n_layers
        self.combine_funcs = combine_funcs
        self.hidden = hidden

        self.lstm = nn.LSTM(embedding_dim, hidden_dim, batch_first=True)
        self.dropout = nn.Dropout(drop_prob)
        self.fc1 = nn.Linear(hidden_dim * 2 * len(self.combine_funcs), self.output_size_1)
        self.fc2 = nn.Linear(output_size_1, self.output_size_2)
        self.sigmoid = nn.Sigmoid()
        
    def forward(self, titles, all_for_main_points, all_against_main_points):
        batch_size = len(titles)
        lstm_out = torch.stack([run_lstm_on_fid(titles[i], all_for_main_points[i], all_against_main_points[i], \
         embedding_index, self.lstm, self.hidden, combine_func = self.combine_funcs) for i in range(len(titles))])
    
        lstm_out = lstm_out.contiguous().view(-1, len(self.combine_funcs) * 2 * self.hidden_dim)
        out = self.dropout(lstm_out)
        out = self.fc1(out)
        out = self.fc2(out)
        out = self.sigmoid(out)
        
        out = out.view(batch_size, -1)
        out = out[:,-1]
        return out

def load_model():
    EMBEDDING_DIM = 200
    HIDDEN_DIM = 50
    OUTPUT_SIZE_1 = 20
    COMBINE_FUNCS =[torch.mean, torch.max]
    OUTPUT_SIZE_2 = 1
    N_LAYERS = 1
    DROPOUT_PROB = 0.5
    HIDDEN_INITIAL = (torch.randn(1, 1, HIDDEN_DIM), torch.randn(1, 1, HIDDEN_DIM))
    loaded_model = LSTMNet(OUTPUT_SIZE_1, OUTPUT_SIZE_2, N_LAYERS, EMBEDDING_DIM, HIDDEN_DIM, \
                COMBINE_FUNCS, HIDDEN_INITIAL,DROPOUT_PROB)
    loaded_model.load_state_dict(torch.load(os.path.join(__location__, 'best_model.pt')))
    return loaded_model
    
    
def predict(title, for_script, against_script):
    model = load_model()
    for_main_points = text_rank_summarize(for_script)
    against_main_points = text_rank_summarize(against_script)
    model.eval()
    output = model([title], [for_main_points], [against_main_points])
    return output.item()
    
    