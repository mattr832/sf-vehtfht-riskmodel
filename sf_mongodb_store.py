from pymongo import MongoClient

uri = 'mongodb://heroku_3w4qsbm8:j4f5381j5808div420gtv6pckt@ds037768.mlab.com:37768/heroku_3w4qsbm8'

client = MongoClient(uri,
                     connectTimeoutMS=30000,
                     socketTimeoutMS=None,
                     socketKeepAlive=True,
                     retryWrites=False)

db = client.get_default_database()
col = db['response-store']

