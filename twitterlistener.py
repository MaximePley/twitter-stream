import yaml
import tweepy
import logging
import database

# Set the log config
logging.basicConfig(filename='execution.log', format='%(asctime)s')

# Read config parameters
with open('config.yaml', 'r') as f:
    doc = yaml.load(f)
hashtags = doc["base"]["TrackTerms"]

# Need to add the storage type argument

class StreamListener(tweepy.StreamListener):

    def on_status(self, status):

        if hasattr(status, 'retweeted_status'):
            return

        hashtags = status.entities['hashtags']
        if hashtags == []:
            return

        user_id = status.user.id
        created = status.created_at
        urls = status.entities['urls']
        user = {"User id": user_id, "Created": created, "Tweet url": urls}
        database.textDataStore(user)

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False


# Follow request
def follow(user_id):

    api.create_friendship(user_id)


# Connection to Twitter API
try:
    auth = tweepy.OAuthHandler(doc["base"]["API_accessKeyId"], doc["base"]["API_secretAccessKey"])
    auth.set_access_token(doc["base"]["API_tokenKeyId"], doc["base"]["API_secretTokenKey"])
    api = tweepy.API(auth, wait_on_rate_limit=True)
    logging.warning('Connected to the API')
except:
    logging.warning('Connection problem')


# Stream listening
stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=hashtags, async=True)
