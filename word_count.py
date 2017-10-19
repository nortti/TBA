#!/usr/bin/env python
import pandas as pd
import json
import string
import plotly as py
import plotly.graph_objs as go
from nltk.stem.porter import *
from collections import Counter

# Parameters
num_top_words = 25
json_file = "json_data/realDonaldTrump.json"
stopWord_file = "stop-word-list.csv"

df = pd.read_json(json_file)[['text', 'retweet_count', 'favorite_count']]
# Stopwords
with open(stopWord_file) as f:
    stopwords = set(f.read().split(", "))

more_stopwords = {'amp'}
stopwords = stopwords.union(more_stopwords)

df['text'] = df['text'].apply(lambda row: ''.join(l for l in row.lower() if l not in string.punctuation))
df['text'] = df['text'].apply(lambda row: ' '.join([word for word in row.split() if word not in stopwords]))
ps = PorterStemmer()
df['text'] = df['text'].apply(lambda row: ' '.join([ps.stem(word) for word in row.split()]))

# Simple word count
wordfreq=[]
words = Counter();
	
for row in df['text']:
	wordlist = row.split()
	words.update(word for word in wordlist)
	for w in wordlist:
		wordfreq.append(wordlist.count(w))

print(words.most_common(num_top_words))
topW = words.most_common(num_top_words)

barplot = [go.Bar(
            x=[val[0] for val in topW],
            y=[val[1] for val in topW]
    )]

py.offline.plot(barplot, filename='Top_words.html')
