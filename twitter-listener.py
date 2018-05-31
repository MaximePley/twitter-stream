import yaml
import tweepy


class StreamListener(tweepy.StreamListener):

    def on_status(self, status):

        if not hasattr(status, 'retweeted_status'):
            hashtags = status.entities['hashtags']
            if hashtags != []:
                text = status.text
                name = status.user.screen_name
                user_id = status.user.id
                created = status.created_at

                # Test that reads the stream - put information in a text file
                f = open("results.txt", "a")
                f.write(str(name) + " " + str(user_id) + '\n' + str(created) + '\n' + str(text.encode("utf-8")) + '\n' + str(hashtags) + '\n\n')
                f.close()
                return

                # Follow request
                # API.create_friendship(user_id)

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False


# Read config parameters
with open('config.yaml', 'r') as f:
    doc = yaml.load(f)
hashtags = doc["base"]["TrackTerms"]

# Connection to Twitter API
try:
    auth = tweepy.OAuthHandler(doc["base"]["API_accessKeyId"], doc["base"]["API_secretAccessKey"])
    auth.set_access_token(doc["base"]["API_tokenKeyId"], doc["base"]["API_secretTokenKey"])
    api = tweepy.API(auth, wait_on_rate_limit=True)
    print('Connected')
except:
    print('Not connected')


# Stream listening
stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=hashtags, async=True)
