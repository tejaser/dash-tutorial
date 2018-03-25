from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

threshold = 0.5
analyzer = SentimentIntensityAnalyzer()

pos_count_text = 0
pos_correct_text = 0
pos_count_vader = 0
pos_correct_vader = 0

with open('./data/positive.txt', 'r') as f:
    for line in f.read().split('\n'):
        analysis = TextBlob(line)
        vs = analyzer.polarity_scores(line)
        if analysis.sentiment.subjectivity > 0.8:
            if analysis.sentiment.polarity > 0:
                pos_correct_text += 1
            pos_count_text += 1
        if vs['compound'] >= threshold or vs['compound'] <= -threshold:
            if vs['compound'] > 0:
                pos_correct_vader += 1
            pos_count_vader += 1

neg_count_text = 0
neg_correct_text = 0
neg_count_vader = 0
neg_correct_vader = 0

with open('./data/negative.txt', 'r') as f:
    for line in f.read().split('\n'):
        analysis = TextBlob(line)
        vs = analyzer.polarity_scores(line)
        if analysis.sentiment.subjectivity > 0.8:
            if analysis.sentiment.polarity <= 0:
                neg_correct_text += 1
            neg_count_text += 1
        if vs['compound'] >= threshold or vs['compound'] <= -threshold:
            if vs['compound'] <= 0:
                neg_correct_vader += 1
            neg_count_vader += 1

print('*'*80)
print('Positive accuracy with TextBlob = {}% via {} samples.'.format(pos_correct_text/pos_count_text*100.00, pos_count_text))
print('Negative accuracy with TextBlob = {}% via {} samples.'.format(neg_correct_text/neg_count_text*100.00, neg_count_text))
print('*'*80)
print('Positive accuracy with vaderSentiment = {}% via {} samples.'.format(pos_correct_vader/pos_count_vader*100.00, pos_count_vader))
print('Negative accuracy with vaderSentiment = {}% via {} samples.'.format(neg_correct_vader/neg_count_vader*100.00, neg_count_vader))
print('*'*80)
