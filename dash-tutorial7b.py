import json
import sqlite3
import time

from textblob import TextBlob
from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener
from unidecode import unidecode

ckey = ''
csecret = ''
atoken = ''
asecret = ''

conn = sqlite3.connect('twitter_b.db')
c = conn.cursor()


def create_table():
    try:
        c.execute('CREATE TABLE IF NOT EXISTS sentiment(unix REAL, tweet TEXT, sentiment REAL)')
        c.execute('CREATE INDEX fast_unix ON sentiment(unix)')
        c.execute('CREATE INDEX fast_tweet ON sentiment(tweet)')
        c.execute('CREATE INDEX fast_sentiment ON sentiment(sentiment)')
        conn.commit()
    except Exception as e:
        print(str(e))


create_table()


class listner(StreamListener):
    def on_data(self, data):
        try:
            data = json.loads(data)
            tweet = unidecode(data['text'])
            time_ms = data['timestamp_ms']

            analysis = TextBlob(tweet)
            sentiment = analysis.sentiment.polarity
            print(time_ms, tweet, sentiment)
            c.execute("INSERT INTO sentiment(unix, tweet, sentiment) VALUES (?, ?, ?)",
                      (time_ms, tweet, sentiment))
            conn.commit()
        except KeyError as e:
            print(str(e))
        return True

    def on_error(self, status):
        print(status)


while True:
    try:
        auth = OAuthHandler(ckey, csecret)
        auth.set_access_token(atoken, asecret)
        twitterStream = Stream(auth, listner())
        twitterStream.filter(track=['Hyderabad'])
    except Exception as e:
        print(str(e))
        time.sleep(5)