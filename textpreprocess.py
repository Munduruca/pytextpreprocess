#!/usr/bin/python

import common.html2text
import common.tokenizer

from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

import string

def textpreprocess(txt, converthtml=True, sentencetokenize=True, removeblanklinks=True, wordtokenize=True, stem=True, lowercase=True, removestopwords=True):
    """
    Note: For html2text, one could also use NCleaner (common.html2text.batch_nclean)
    Note: One could improve the sentence tokenization, by using the
    original HTML formatting in the tokenization.
    Note: We use the Porter stemmer. (Optimization: Shouldn't rebuild
    the PorterStemmer object each time this function is called.)
    """
    if converthtml:
        txt = common.html2text.html2text(txt)

    if sentencetokenize:
        txts = common.tokenizer.tokenize(txt)
    else:
        txts = [txt]
    txt = None

    if removeblanklinks:
        newtxts = []
        for t in txts:
            if len(string.strip(t)) > 0:
                newtxts.append(t)
        txts = newtxts

    if wordtokenize:
        txtwords = [word_tokenize(t) for t in txts]
    else:
        txtwords = [string.split(t) for t in txts]
    txts = None

    if lowercase:
        txtwords = [[string.lower(w) for w in t] for t in txtwords]

    if stem:
        stemmer = PorterStemmer()
        txtwords = [[stemmer.stem(w) for w in t] for t in txtwords]

    if removestopwords:
        stoplist = stopwords.words("english")
        txtwords = [[w for w in t if w not in stoplist] for t in txtwords]

    txts = [string.join(words) for words in txtwords]

    return string.join(txts, sep="\n")

if __name__ == "__main__":
    import sys
    print textpreprocess(sys.stdin.read())
