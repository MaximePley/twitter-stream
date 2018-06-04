import json
import redis


class storage(object):

    def factory(type):
        if type == "Redis":
            return redisDataStore()
        if type == "File":
            return textDataStore()
        raise AssertionError("Type error: " + type)


class redisDataStore(storage):
    def insertUser(self, user, host, port):
        r = redis.StrictRedis(host=host, port=port, db=0, charset="utf-8", decode_responses=True)
        r.hmset("Data_user", self.user)


class textDataStore(storage):
    def insertUser(self, user, fileName):
        js = json.dumps(self.user, default=str)
        f = open(fileName, "a")
        f.write(js + '\n')
        f.close()
        return


# # Only for debugging
# user = {"User id": "user_id", "Created": "created", "Tweet url": "urls"}
# dataStore = storage.factory("File")
# dataStore.insertUser(user, 'resu.txt')
