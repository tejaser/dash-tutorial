import json
import sqlite3

from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener
from unidecode import unidecode
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

ckey = ''
csecret = ''
atoken = ''
asecret = ''

analyzer = SentimentIntensityAnalyzer()
conn = sqlite3.connect('twitter.db')
c = conn.cursor()


def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS sentiment(unix REAL, tweet TEXT, sentiment REAL)')
    conn.commit()


create_table()


class listner(StreamListener):
    def on_data(self, data):
        try:
            data = json.loads(data)
            tweet = unidecode(data['text'])
            time_ms = data['timestamp_ms']
            vs = analyzer.polarity_scores(tweet)
            sentiment = vs['compound']
            print(time_ms, tweet, sentiment)
            c.execute("INSERT INTO sentiment(unix, tweet, sentiment) VALUES (?, ?, ?)",
                      (time_ms, tweet, sentiment))
            conn.commit()
        except KeyError as e:
            print(str(e))
        return True


    def on_error(self, status):
        print(status)


auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listner())
twitterStream.filter(track=['car'])