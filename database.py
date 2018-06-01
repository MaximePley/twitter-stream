import redis
import yaml
import json

with open('config.yaml', 'r') as f:
    doc = yaml.load(f)


class storage(object):

    def factory(type):
        if type == "Redis":
            return redisDataStore()
        if type == "File":
            return textDataStore()
        raise AssertionError("Type error: " + type)


# Fonctions to store the user data
# 2 options: Store in Redis or store in text file
class redisDataStore(storage):
    def dataStore(self, user):
        r = redis.StrictRedis(host=doc["datastore"]["database"]["host"], port=doc["datastore"]["database"]["port"], db=0, charset="utf-8", decode_responses=True)
        r.hmset("Data_user", self.user)


class textDataStore(storage):
    def dataStore(self, user):
        js = json.dumps(self.user, default=str)
        f = open(doc["datastore"]["text"]["file_name"], "a")
        f.write(js + '\n')
        f.close()
        return

# Only for debugging
user = {"User id": "user_id", "Created": "created", "Tweet url": "urls"}
obj = storage.factory("File")
obj.dataStore(user)
