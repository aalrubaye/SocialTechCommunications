__author__ = 'Abduljaleel'

import pprint
from pymongo import MongoClient
import xlwt

client = MongoClient()
database = client.stack_overflow
stack_posts = database.stack

results = xlwt.Workbook(encoding="utf-8")
sheet1 = results.add_sheet('StackOverflowGeneralInfo')

sheet_header = [
    'title',
    'answer_count',
    'favorite_count',
    'view_count',
    'comment_count',
    'up_vote_count',
    'score',
    'owner_reputation',
    'owner_badge_counts_gold',
    'owner_badge_counts_silver',
    'owner_badge_counts_bronze',
    'avg_comments_per_answer',
    'avg_answer_score',
    'avg_answer_up_vote_count',
    'avg_answerer_reputation',
    'ha_score',
    'ha_up_vote_count',
    'ha_owner_reputation',
    'ha_comment_count',
    'ha_owner_badge_counts_gold',
    'ha_owner_badge_counts_silver',
    'ha_owner_badge_counts_bronze'
]


def export_to_sheet(entry, row):
    col = 0
    for i in range(0, len(sheet_header)):
        sheet1.write(row, col, str(entry[sheet_header[i]]))
        col += 1


def owner_badge_count(owner_badge_data):
    obcg = None
    obcs = None
    obcb = None

    if owner_badge_data:
        obc = owner_badge_data.get('badge_counts')
        if obc:
            obcg = owner_badge_data.get('badge_counts').get('gold')
            obcs = owner_badge_data.get('badge_counts').get('silver')
            obcb = owner_badge_data.get('badge_counts').get('bronze')

    return [obcg, obcs, obcb]


def extract_general_info():

    col = 0
    for i in range(0, len(sheet_header)):
        sheet1.write(0, col, str(sheet_header[i]))
        col += 1

    ii = 1
    for post in stack_posts.find():

        answer_array = post.get('answers')
        len_answer_array = len(answer_array) if answer_array else 0

        ha_score = None
        ha_bc = None
        owner_bc = owner_badge_count(post.get('owner'))

        if answer_array:
            avg_comments_per_answer = sum(answer['comment_count'] for answer in answer_array) / float(len_answer_array)
            avg_answer_score = sum(answer['score'] for answer in answer_array) / float(len_answer_array)
            avg_answer_up_vote_count = sum(answer['up_vote_count'] for answer in answer_array) / float(len_answer_array)
            sum_rep = 0
            for ans in answer_array:
                rep = ans.get('owner').get('reputation')
                if rep:
                    sum_rep += rep

            avg_answerer_reputation = sum_rep / float(len_answer_array) if sum_rep > 0 else 0

            ha_score = max(answer_array, key=lambda x:x['score'])
            ha_bc = owner_badge_count(ha_score.get('owner'))

        data_object = {
            'title': post['title'].encode("utf-8"),
            'answer_count': post['answer_count'],
            'favorite_count': post['favorite_count'],
            'view_count': post['view_count'],
            'comment_count': post['comment_count'],
            'up_vote_count': post['up_vote_count'],
            'score': post['score'],
            'owner_reputation': post.get('owner').get('reputation'),
            'owner_badge_counts_gold': owner_bc[0] ,
            'owner_badge_counts_silver': owner_bc[1],
            'owner_badge_counts_bronze': owner_bc[2],
            'avg_comments_per_answer': avg_comments_per_answer,
            'avg_answer_score': avg_answer_score,
            'avg_answer_up_vote_count': avg_answer_up_vote_count,
            'avg_answerer_reputation': avg_answerer_reputation,
            'ha_score': ha_score['score'] if answer_array else None,
            'ha_up_vote_count': ha_score.get('up_vote_count') if answer_array else None,
            'ha_owner_reputation': ha_score.get('owner').get('reputation') if answer_array else None,
            'ha_comment_count': ha_score.get('comment_count') if answer_array else None,
            'ha_owner_badge_counts_gold': ha_bc[0] if answer_array else None,
            'ha_owner_badge_counts_silver': ha_bc[1] if answer_array else None,
            'ha_owner_badge_counts_bronze': ha_bc[2] if answer_array else None
        }
        pprint.pprint(data_object)
        export_to_sheet(data_object, ii)
        ii += 1

    results.save("StackOverFlowGeneralInfo.xls")


# The main function
if __name__ == "__main__":
    extract_general_info()
