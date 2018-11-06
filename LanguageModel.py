import os
import sys
import glob
import copy
import pickle
from tqdm import trange
from nltk import ConditionalFreqDist
import re


class LanguageModel(object):
    def __init__(self, corpuses=None, n=3, path='./data', maxlength=15):        
        self.__n = n
        self.__corpus = self.__load_corpus(corpuses, path)
        self.__ngram = self.__get_ngram()
        self.__cdf = self.__get_conditional_freq_dist()
        self.__maxlength = maxlength


    def generate_response(self, a_str):
        a_str = clean_tweet(a_str)
        return generate_sent(self.__cdf, a_str, self.__n, self.__maxlength)

    def __load_corpus(self, corpuses, path):
        if corpuses:
            corpus = []
            if 'MIM' in corpuses:
                print('Getting Corpus from: Mörkuð íslensk málheild')
                for child_directory in next(os.walk(f'{path}/MIM'))[1]:
                    print(f'Loading: {child_directory.title()}')
                    corpus.extend(self.__get_corpus(f'{path}/MIM/{child_directory}')) 
            if 'ISL' in corpuses:
                print('Getting Corpus from: Íslensk orðtíðnibók')
                corpus = self.__get_corpus(f'{path}/ISL')
            return corpus
        else:
            return []

    def __get_ngram(self):
        ngram = []
        t = trange(len(self.__corpus), desc=f'Creating {self.__n}-gram')
        for i in t:
            sequences = [self.__corpus[i][j:] for j in range(self.__n)]
            ngram.extend(list(zip(*sequences)))
        sys.stdout.flush()
        return ngram

    def __get_conditional_freq_dist(self):
        t = trange(len(self.__ngram), desc=f'Creating Conditional frequency distributions for {len(self.__ngram[0])}-gram')
        condition_pairs = []
        for i in t:
            words = self.__ngram[i]
            condition_pairs.append((tuple(words[:-1]), words[-1]))
        return ConditionalFreqDist(condition_pairs)

        
    def __get_corpus(self, path):
        file_names = glob.glob(os.path.join(path, '*.txt'))
        corpus = []
        t = trange(len(file_names))
        for i in t:
            fin = open(file_names[i], 'r', encoding='utf-8')
            tokens = []
            punctuation = [".", ",", ";", ":", "?", "!"]
            for line in fin:
                if line.strip() and line.split()[0].strip() not in punctuation:
                    tokens.append(line.split()[0].strip())
                else:
                    if tokens:
                        corpus.append(copy.deepcopy(tokens))
                    tokens = []
            sys.stdout.flush()
        return corpus

def clean_tweet(a_str):
    if a_str == '':
        return a_str

    a_str = re.sub(r"@[A-z]+\w", '', a_str)
    a_str = re.sub(r"\bhttps:.*\b", '', a_str)
    a_str = re.sub(r"\bRT\b", '', a_str)
    punctuation = [".", ",", ";", ":", "?", "!"]
    a_str = ''.join([char for char in a_str if char not in punctuation])
    a_str = a_str.strip()

    return a_str


def generate_sent(cdf, sent, n, max_words):
    words = sent.split()
    words = words[-(n-1):]
    out_words = []
    for _ in range(max_words):
        try:
            words = words[-(n-1):] + [cdf[tuple(words[-(n-1):])].max()] 
            out_words.append(words[-1])
        except ValueError:
            break
    sent = ' '.join(out_words)
    if sent.strip():
        return f'...{sent.strip()}.'
    return ''    



def testModel():
    # TRigram with Only ISL
    # try:
    #     with open(f'./models/LanguageModel3_ISL.pkl', "rb") as model_pickle:
    #         model = pickle.load(model_pickle)
    # except:
    #     model = LanguageModel(corpuses=['ISL'], n=3)
    #     with open(f'./models/LanguageModel3_ISL.pkl', "wb") as model_pickle:
    #         pickle.dump(model, model_pickle, pickle.HIGHEST_PROTOCOL)
    # print(model.generate_response('Hvað er þetta'))
    # ...ekki lengur til klukkunnar í trúboðsstöðinni.
    
    
    # try:
    # with open(f'./models/LanguageModel4_ISLMIM.pkl', "rb") as model_pickle:
    #     model = pickle.load(model_pickle)
    # except:
    model = LanguageModel(corpuses=['ISL', 'MIM'], n=4)
    with open(f'./models/LanguageModel4_ISLMIM.pkl', "wb") as model_pickle:
        pickle.dump(model, model_pickle, pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
    testModel()