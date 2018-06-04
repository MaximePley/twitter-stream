import database
import logging
import os.path
import sys
import twitterlistener
import yaml


def configRead():

    trackTerms = []
    twitter = []
    datastore = []
    logLevel = []

    if os.path.isfile('config.yaml'):
        with open('config.yaml', 'r') as f:
            doc = yaml.load(f)
        trackTerms = doc['trackTerms']
        twitter = doc['twitter']
        datastore = doc['datastore']
        logLevel = doc['logLevel']
        return trackTerms, twitter, datastore, logLevel
    else:
        sys.exit('No config file')


def logger(logLevel='INFO'):

    logging.basicConfig(filename='execution.log', format='%(asctime)s, %(message)s', level=logging.INFO)
    logging.getLogger().setLevel(logLevel)
    return logger


if __name__ == "__main__":
    configRead()
    logger(configRead()[3]['level'])
    api = twitterlistener.connect(configRead()[1]['apiAccessKeyId'], configRead()[1]['apiSecretAccessKey'], configRead()[1]['apiTokenKeyId'], configRead()[1]['apiSecretTokenKey'])
    twitterlistener.startStreaming(api, configRead()[0])
    # Call function that creates the datastore: datastore = storage.factory(config.datastore.type)
