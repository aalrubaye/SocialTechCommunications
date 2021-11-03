__author__ = 'Abduljaleel'

import json
import praw
import pprint
import time
from pymongo import MongoClient

client = MongoClient()
database = client.reddit
reddit_posts = database.submissions

# Load API secrets from an external JSON file
secrets = json.loads(open('secrets.json').read())

my_client_id = secrets['reddit_client_id']
my_client_secret = secrets['reddit_client_secret']
my_user_agent = secrets['reddit_user_agent']
user_name = secrets['reddit_user_name']
password = secrets['reddit_password']


reddit = praw.Reddit(
    client_id=my_client_id,
    client_secret=my_client_secret,
    password=password,
    user_agent=my_user_agent,
    username=user_name
)

def get(object, attribute):
    return getattr(object, attribute, None)

def write(text):
    file = open("ids.txt","w")
    file.write(text)
    file.close()

def wait(seconds):
    time.sleep(seconds)

file = open("ids.txt","r")
fetched_posts = file.read()
file.close()

# ROS
# MachineLearning
# robotics
# deeplearning
# reinforcementlearning
# artificial



sub = "MachineLearning"
subreddit = reddit.subreddit(sub)
hot_python = subreddit.hot(limit = 1000)

submission_index = 1

try:
    for submission in hot_python:

        if not get(submission, 'stickied'):

            author = get(submission, 'author')
            submission_id = get(submission, 'id')

            if submission_id not in fetched_posts:
                # wait(2)
                fetched_posts += str(submission_id) + ', '

                comments_array = []
                comments = get(submission, 'comments')

                if comments:
                    for com in comments:

                        reply_array = []
                        replies = get(com,'replies')
                        reply_counts = 0

                        if replies:
                            reply_counts = len(replies)
                            for rep in get(com,'replies'):
                                rep_auth = get(rep,'author')
                                rep_entry = {
                                    'id' : get(rep,'id'),
                                    'author' : {
                                        'id' : get(rep_auth, 'id'),
                                        'name' : get(rep_auth,'name'),
                                        'comment_karma' : get(rep_auth, 'comment_karma'),
                                        'created_utc' : get(rep_auth, 'created_utc'),
                                        'is_gold': get(rep_auth, 'is_gold')
                                    },
                                    'body' : get(rep, 'body'),
                                    'created_utc' : get(rep, 'created_utc'),
                                    'is_submitter' : get(rep, 'is_submitter'),
                                    'parent_id' : get(rep, 'parent_id'),
                                    'score' : get(rep, 'score')
                                }
                                reply_array.append(rep_entry)

                        com_auth = get(com, 'author')
                        com_entry = {
                            'id' : get(com, 'id'),
                            'author' : {
                                'id' : get(com_auth, 'id'),
                                'name' : get(com_auth,'name'),
                                'comment_karma' : get(com_auth, 'comment_karma'),
                                'created_utc' : get(com_auth, 'created_utc'),
                                'is_gold': get(com_auth, 'is_gold')
                            },
                            'body' : get (com, 'body'),
                            'created_utc' : get(com, 'created_utc'),
                            'is_submitter' : get (com, 'is_submitter'),
                            'parent_id' : get (com, 'parent_id'),
                            'score' : get (com, 'score'),
                            'replies_count' : reply_counts,
                            'replies' : reply_array
                        }
                        comments_array.append(com_entry)


                data_object = {
                    'id' : submission_id,
                    'title' : get (submission, 'title'),
                    'author' : {
                        'id' : get(author, 'id'),
                        'name' : get(author,'name'),
                        'full_name' : get(submission, 'author_fullname'),
                        'flair_text' : get(submission, 'author_flair_text'),
                        'comment_karma' : get(author, 'comment_karma'),
                        'created_utc' : get(author, 'created_utc'),
                        'premium' : get(submission, 'author_premium'),
                        'is_gold': get(author, 'is_gold')
                    },
                    'num_comments_and_replies': get(submission,'num_comments'),
                    'num_comments': len(comments_array),
                    'created_utc' : get(submission,'created_utc'),
                    'ups' : get(submission,'ups'),
                    'downs' : get(submission,'downs'),
                    'upvote_ratio' : get(submission,'upvote_ratio'),
                    'is_original_content' : get(submission,'is_original_content'),
                    'is_video' : get(submission,'is_video'),
                    'is_self' : get(submission,'is_self'),
                    'likes' : get(submission,'likes'),
                    'media' : get(submission,'media'),
                    'media_only' : get(submission,'media_only'),
                    'name' : get(submission,'name'),
                    'score' : get(submission,'score'),
                    'subreddit' : sub,
                    'total_awards_received' : get(submission,'total_awards_received'),
                    'view_count' : get(submission,'view_count'),
                    'url' : "https://www.reddit.com"+str(get(submission,'permalink')),
                    'comments' : comments_array
                }

                pprint.pprint(dir(submission))
                pprint.pprint(data_object)
                print ('*'*100)
                # reddit_posts.insert_one(data_object)
                print (str(submission_index)+' -> '+ str(submission_id))
                submission_index += 1

except Exception as er:
    write(fetched_posts)
    print(er)

write(fetched_posts)
print ('done with this subreddit')



# find users that have Github link in their self_text
# parse comments and replies


# submission object
# https://praw.readthedocs.io/en/stable/code_overview/models/submission.html
# comment object
# https://praw.readthedocs.io/en/stable/code_overview/models/comment.html?highlight=comment
