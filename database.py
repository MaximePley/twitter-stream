import json
import redis
import logging


def storageType(type, fileName, host, port):
    if type == 'redis':
        return redisDataStore(host, port)
    if type == 'file':
        return textDataStore(fileName)
    raise AssertionError("Type error: " + type)


class redisDataStore(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self._r = redis.StrictRedis(host=self.host, port=self.port, db=0, charset="utf-8", decode_responses=True)
        logging.info('Connected to Redis')

    def insertUser(self, user):
        self._r.append("Data_user", user)
        logging.info('Data stored in Redis')


class textDataStore(object):

    def __init__(self, fileName):
        self.fileName = fileName

    def insertUser(self, user):
        js = json.dumps(user, default=str)
        f = open(self.fileName, "a")
        f.write(js + '\n')
        f.close()
        logging.info('Data stored in file')
        return
