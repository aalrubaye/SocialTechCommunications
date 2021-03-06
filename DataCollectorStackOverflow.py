import json
from pymongo import MongoClient
from stackapi import StackAPI
import pprint

__author__ = 'Abduljaleel'

secrets = json.loads(open('secrets.json').read())

client = MongoClient()
database = client.stack_overflow
stack_posts = database.stack

# deep-learning
# ROS
# ros2
# robotics
# reinforcement-learning
# machine-learning
# artificial-intelligence


start = '2020-3-01'
end = '2020-6-01'
keyword = 'ros2'
page = 1
pagesize = 1
filter_hash = '!2q)rrCiT-WWuvgZ)48hoMxZcWe.y.W8V49EpapgZBZ'
access_token = secrets['so_access_token']
key = secrets['so_key']

try:

    SITE = StackAPI('stackoverflow', key=key, access_token=access_token, fromdate=start, todate=end)
    questions = SITE.fetch('questions', tagged=keyword, sort='activity', filter=filter_hash)
    for items in questions['items']:
        stack_posts.insert_one(items)

except Exception as er:
    print(er.message)

# https://api.stackexchange.com/docs/questions#pagesize=2&fromdate=2021-09-01&todate=2021-09-02&order=desc&sort=activity&tagged=python&filter='!*2jH4-Ro4R6O1fNfYER_IE7eKjFeWIivbBiwM*vq6'&site=stackoverflow
