import json
from pymongo import MongoClient

__author__ = 'Abduljaleel'

client = MongoClient()
database = client.stack_overflow
stack_posts = database.stack


unique_ids=[]
for post in stack_posts.find():
    post_id = post['question_id']
    if post_id not in unique_ids:
        unique_ids.append(post_id)
    else:
        print (post['_id'])
        stack_posts.delete_one({"_id": post['_id']})

print (len(unique_ids))
