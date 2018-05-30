import settings
import yaml
import tweepy
import dataset
from sqlalchemy.exc import ProgrammingError
import json
import csv


class StreamListener(tweepy.StreamListener):

    def on_status(self, status):
        if status.retweeted:
            return

        description = status.user.description
        loc = status.user.location
        text = status.text
        name = status.user.screen_name
        user_created = status.user.created_at
        followers = status.user.followers_count
        id_str = status.id_str
        created = status.created_at
        retweets = status.retweet_count
        hashtags = status.entities.get('hashtags')

        f = open("results.txt", "w+")
        f.write(user_created + name + text + '\n' + hashtags + '\n\n')
        f.close()

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False


with open('config.yaml', 'r') as f:
    doc = yaml.load(f)
    print(doc["base"]["API_accessKeyId"], doc["base"]["API_secretAccessKey"])
    print(doc["base"]["API_tokenKeyId"], doc["base"]["API_secretTokenKey"])

# Connection to Twitter API
try:
    auth = tweepy.OAuthHandler(doc["base"]["API_accessKeyId"], doc["base"]["API_secretAccessKey"])
    auth.set_access_token(doc["base"]["API_tokenKeyId"], doc["base"]["API_secretTokenKey"])
    api = tweepy.API(auth)
    print('Connected')
except:
    print('Not connected')


hashtags = settings.TRACK_TERMS
f = open("results.txt", "w+")

for keywords in hashtags:
    for tweet in tweepy.Cursor(api.search, q=keywords + " -filter:retweets", lang="en").items(5):
        f.write(str(tweet.created_at) + str(tweet.text.encode("utf-8")) + '\n' + str(tweet.entities.get('hashtags')) + '\n\n')
f.close()

# stream_listener = StreamListener()
# stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
# stream.filter(track=settings.TRACK_TERMS)
