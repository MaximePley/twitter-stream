import yaml
import tweepy


class StreamListener(tweepy.StreamListener):

    def on_status(self, status):

        if hasattr(status, 'retweeted_status'):
            return

        hashtags = status.entities['hashtags']
        if hashtags == []:
            return

        text = status.text
        name = status.user.screen_name
        user_id = status.user.id
        created = status.created_at

        test("results.txt", name, user_id, created, text, hashtags)

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False


# Test that reads the stream - put information in a text file
def test(file_name, name, user_id, created, text, hashtags):

    f = open(file_name, "a")
    f.write(str(name) + " " + str(user_id) + '\n' + str(created) + '\n' + str(text.encode("utf-8")) + '\n' + str(hashtags) + '\n\n')
    f.close()
    return


# Follow request
def follow(user_id):

    API.create_friendship(user_id)


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
