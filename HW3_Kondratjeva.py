import codecs
import collections
import sys
import json
import wikipedia
from math import log
from itertools import islice, tee


def tokenize(text):
    return text.split(' ')


def counting_detection(text, langs):
    tokens = tokenize(text)
    counters = {}
    
    for lang, probs in langs.items():
        i = 0
        
        for token in tokens:
            if token in probs.keys():
                i +=1
        
        counters[lang] = i
    
    counters = sorted(counters, key=lambda n: counters[n], reverse=True)

    return counters[0]


def make_ngrams(text):
    N = 3 # задаем длину n-граммы
    ngrams = zip(*(islice(seq, index, None) for index, seq in enumerate(tee(text, N))))
    ngrams = [''.join(x) for x in ngrams]
    return ngrams


def ngrams_detection(text, langs):
    ngrams = make_ngrams(text)
    counters = {}
    
    for lang, probs in langs.items():
        i = 0
        
        for ng in ngrams:
            if ng in probs.keys():
                i +=1
        
        counters[lang] = i
    
    counters = sorted(counters, key=lambda n: counters[n], reverse=True)

    return counters[0]


def main():
    text = sys.argv[1]

    with open(text, 'r', encoding='utf-8') as file:
        text = file.read()

    count_langs = json.load(open('count_method.json', 'r', encoding='utf-8'))
    ngrams_langs = json.load(open('ngrams_method.json', 'r', encoding='utf-8'))

    count_result = counting_detection(text, count_langs)
    ngrams_result = ngrams_detection(text, ngrams_langs)

    print("Результат для метода частотных слов: %s" % (count_result))
    print("Результат для метода нграмм: %s" % (ngrams_result))


if __name__ == '__main__':
    main()