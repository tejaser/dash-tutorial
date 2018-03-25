from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

threshold = 0.5
analyzer = SentimentIntensityAnalyzer()

pos_count_text = 0
pos_correct_text = 0
pos_count_vader = 0
pos_correct_vader = 0
pos_count_opt = 0
pos_correct_opt = 0


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
        if not vs['neg'] > 0.1:
            if vs['pos'] - vs['neg'] >= 0:
                pos_correct_opt += 1
            pos_count_opt += 1

neg_count_text = 0
neg_correct_text = 0
neg_count_vader = 0
neg_correct_vader = 0
neg_count_opt = 0
neg_correct_opt = 0

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
        if not vs['pos'] > 0.1:
            if vs['pos'] - vs['neg'] <= 0:
                neg_correct_opt += 1
            neg_count_opt += 1


def print_score(type, postivie_correct, positive_sample, negative_correct, negative_sample):
    print('*' * 80)
    print('Positive accuracy with {} = {}% via {} samples.'.format(type, postivie_correct / positive_sample * 100.00,
                                                                   positive_sample))
    print('Negative accuracy with {} = {}% via {} samples.'.format(type, negative_correct / negative_sample * 100.00,
                                                                   negative_sample))


print_score('TextBlob', pos_correct_text, pos_count_text,neg_correct_text,neg_count_text)
print_score('VaderSentiment', pos_correct_vader, pos_count_vader, neg_correct_vader, neg_count_vader)
print_score('VaderOptimized', pos_correct_opt, pos_count_opt, neg_correct_opt, neg_count_opt)
