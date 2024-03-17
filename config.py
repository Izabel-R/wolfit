import os

class Config(object):
    DEBUG = False
    TESTING = False
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/api/activities')
    MICROSERVICE_BASE_URL = os.getenv('MICROSERVICE_BASE_URL', 'http://0.0.0.0:5001')

