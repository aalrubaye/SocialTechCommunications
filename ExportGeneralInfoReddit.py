__author__ = 'Abduljaleel'

import pprint
from pymongo import MongoClient
import xlwt
import correlations

client = MongoClient()
database = client.reddit
reddit_posts = database.submissions

results = xlwt.Workbook(encoding="utf-8")
sheet1 = results.add_sheet('RedditGeneralInfo')

sheet_header = ['subreddit',
                'title',
                'score',
                'ups',
                'upvote_ratio',
                'total_awards_received',
                'is_original_content',
                'is_video',
                'media_only',
                'ack',
                'auth_premium',
                'auth_gold',
                'comments',
                'replies',
                'comments_with_replies',
                'avg_replies_per_comment',
                'avg_comment_score',
                'avg_commenter_ack',
                'hc_score',
                'hc_ack',
                'hc_reply_count',
                'hc_hr_score',
                'hc_hr_ack',
                'hr_score',
                'hr_ack',
                'hr_parent_comment_score',
                'hr_parent_comment_ack',
                'correl_r',
                'correl_p',
                'hc_order',
                'hc_comments_count'
                ]


def export_to_sheet(entry, row):
    col = 0
    for i in range(0, len(sheet_header)):
        sheet1.write(row, col, str(entry[sheet_header[i]]))
        col += 1


def extract_general_info():

    col = 0
    for i in range(0, len(sheet_header)):
        sheet1.write(0, col, str(sheet_header[i]))
        col += 1

    ii = 1
    for subs in reddit_posts.find():
        comments = subs['num_comments']
        com_reply = subs['num_comments_and_replies']
        replies = com_reply - comments
        comments_array = subs['comments']

        comments_with_replies = 0
        avg_comment_score = 0
        avg_commenter_ack = 0
        hc_score = 0
        hc_ack = 0
        hc_reply_count = 0
        hc_hr_score = 0
        hc_hr_ack = 0
        hr_score = 0
        hr_ack = 0
        hr_parent_comment_score = 0
        hr_parent_comment_ack = 0
        correl_r = None
        correl_p = None
        hc_order = None
        hc_comments_count = None

        if comments_array:
            highest_comment = max(comments_array, key=lambda x:x['score'])
            hc_score = highest_comment['score']
            hc_ack = highest_comment['author']['comment_karma']
            hc_reply_count = len(highest_comment['replies'])

            dd = []
            ind = 0
            hc_comments_count = 0
            for comnts in comments_array:
                dd.append(comnts['author']['comment_karma'])
                if comnts['author']['id'] == highest_comment['author']['id']:
                    hc_order = ind
                    hc_comments_count += 1
                ind += 1

            ff = list(range(0, len(dd)))
            correl = correlations.coeff(dd, ff)
            correl_r = correl[0]
            correl_p = correl[1]

            if highest_comment['replies']:
                hc_hr = max(highest_comment['replies'], key=lambda x:x['score'])
                hc_hr_score = hc_hr['score']
                hc_hr_ack = hc_hr['author']['comment_karma']

            comments_with_replies = sum([1 for com in comments_array if len(com['replies']) > 0])
            avg_comment_score = float(sum(com['score'] for com in comments_array)) / len(comments_array)
            avg_commenter_ack = float(sum(com['author']['comment_karma'] for com in comments_array)) / len(comments_array)

            hr_array = []
            for com in comments_array:
                reps = com['replies']
                if reps:
                    mx_tmp = max(reps, key=lambda x:x['score'])
                    if mx_tmp['score']:
                        hr_array.append(mx_tmp)

            if hr_array:
                print (hr_array)
                highest_reply = max(hr_array, key=lambda x:x['score'])
                hr_score = highest_reply['score']
                hr_ack = highest_reply['author']['comment_karma']
                parent_id = highest_reply['parent_id']
                parent_id_clean = parent_id [3:len(parent_id)]
                hr_parent = next(item for item in comments_array if item['id'] == parent_id_clean)
                hr_parent_comment_score = hr_parent['score']
                hr_parent_comment_ack = hr_parent['author']['comment_karma']

        data_object = {
                        'subreddit' : subs['subreddit'],
                        'title': subs['title'].encode("utf-8"),
                        'score': subs['score'],
                        'ups' : subs['ups'],
                        'upvote_ratio': subs['upvote_ratio'],
                        'total_awards_received' : subs['total_awards_received'],
                        'is_original_content' : subs['is_original_content'],
                        'is_video' : subs['is_original_content'],
                        'media_only' : subs['media_only'],
                        'ack': subs['author']['comment_karma'],
                        'auth_premium': subs['author']['premium'],
                        'auth_gold': subs['author']['is_gold'],
                        'comments': comments,
                        'replies': replies,
                        'comments_with_replies': comments_with_replies,
                        'avg_replies_per_comment': 0 if comments == 0 else replies / float(comments),
                        'avg_comment_score': avg_comment_score,
                        'avg_commenter_ack': avg_commenter_ack,
                        'hc_score': hc_score,
                        'hc_ack': hc_ack,
                        'hc_reply_count': hc_reply_count,
                        'hc_hr_score': hc_hr_score,
                        'hc_hr_ack': hc_hr_ack,
                        'hr_score': hr_score,
                        'hr_ack': hr_ack,
                        'hr_parent_comment_score': hr_parent_comment_score,
                        'hr_parent_comment_ack': hr_parent_comment_ack,
                        # correl_r: shows the R value of the correlation between the commentors popularity and the order of their comment
                        # the more positive the correlation is the more popular commentors are commenting toward the end of the conversation
                        'correl_r': correl_r,
                        'correl_p': correl_p,
                        'hc_order': hc_order,
                        'hc_comments_count': hc_comments_count
        }

        export_to_sheet(data_object, ii)

        pprint.pprint(data_object)
        print ('*'*100)
        # if ii > 4:
        #     break
        ii += 1

    results.save("RedditGeneralInfo.xls")


# The main function
found = 0
if __name__ == "__main__":
    extract_general_info()
