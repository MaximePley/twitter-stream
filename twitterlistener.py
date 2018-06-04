import logging
import tweepy


class StreamListener(tweepy.StreamListener):

    def on_status(self, status):

        if hasattr(status, 'retweeted_status'):
            return

        hashtags = status.entities['hashtags']
        if hashtags == []:
            return

        user_id = status.user.id
        created = str(status.created_at)
        urls = status.entities['urls']
        user = {"User id": user_id, "Created": created, "Tweet url": urls}
        return user

    def on_error(self, status_code):
        if status_code == 420:
            return logging.warning('API rate limit reached')


# Follow request
def follow(api, user_id):

    api.create_friendship(user_id)


# Connection to Twitter API
def connect(apiAccessKeyId, apiSecretAccessKey, apiTokenKeyId, apiSecretTokenKey):

    try:
        auth = tweepy.OAuthHandler(apiAccessKeyId, apiSecretAccessKey)
        auth.set_access_token(apiTokenKeyId, apiSecretTokenKey)
        api = tweepy.API(auth, wait_on_rate_limit=True)
        logging.info('Connected to the API')
        return api
    except:
        logging.warning('Connection problem')


# Stream listening
def startStreaming(api, hashtags):

    try:
        stream_listener = StreamListener()
        stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
        stream.filter(track=hashtags, async=True)
        logging.info('Reading the stream')
    except:
        logging.warning('Stream broken')
