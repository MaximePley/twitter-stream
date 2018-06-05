import database
import logging
import os.path
import sys
import twitterlistener
import yaml


def configRead():

    if os.path.isfile('config.yaml'):
        with open('config.yaml', 'r') as f:
            doc = yaml.load(f)
        config = {'trackTerms': doc['trackTerms'], 'twitter': doc['twitter'], 'datastore': doc['datastore'], 'logLevel': doc['logLevel']}
        return config
    else:
        sys.exit('No config file')


def setupLogger(logLevel='INFO'):

    logging.basicConfig(filename='execution.log', format='%(asctime)s, %(message)s')
    logging.getLogger().setLevel(logLevel)
    return setupLogger


if __name__ == "__main__":
    # Read the config
    config = configRead()
    # Set the logger
    logger = setupLogger(configRead()['logLevel']['level'])
    # Connect to the api
    api = twitterlistener.connect(configRead()['twitter']['apiAccessKeyId'], configRead()['twitter']['apiSecretAccessKey'], configRead()['twitter']['apiTokenKeyId'], configRead()['twitter']['apiSecretTokenKey'])
    # Connect the data storage
    datastore = database.storageType(configRead()['datastore']['type'], configRead()['datastore']['text']['fileName'], configRead()['datastore']['database']['host'], configRead()['datastore']['database']['port'])
    # Read the stream twitter
    twitterlistener.startStreaming(api, configRead()['trackTerms'], datastore)
