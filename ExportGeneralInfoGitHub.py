__author__ = 'Abduljaleel'

import pprint
from pymongo import MongoClient
import xlwt
from collections import Counter

client = MongoClient()
database = client.stack_overflow
git_repos = database.repos

results = xlwt.Workbook(encoding="utf-8")
sheet1 = results.add_sheet('RedditGeneralInfo')

sheet_header = [
    'name',
    'language',
    'issues_count',
    'watchers',
    'forks',
    'stars',
    'owner_followers',
    'owner_followings',
    'owner_repos',
    'owner_type',
    'avg_comments_per_issue',
    'avg_owners_followers',
    'avg_owners_following',
    'avg_owners_repos',
    'avg_high_commenters_followers',
    'avg_high_commenters_following',
    'avg_high_commenters_repo',
    'iwhc_comment_count',
    'iwhc_owner_followers',
    'iwhc_owner_following',
    'iwhc_owner_repo',
    'iwhc_owner_type',
    'unique_commenters_percentage',
    'mpc_followers',
    'mpc_following',
    'mpc_repos',
    'mpc_type'
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
    for repo in git_repos.find():

        total_comments = sum(issue['issue_comments_count'] for issue in repo['repo_issues'])
        avg_issue_author_followers = sum(issue['issue_author']['followers_count'] for issue in repo['repo_issues'])
        avg_issue_author_followeing = sum(issue['issue_author']['following_count'] for issue in repo['repo_issues'])
        avg_issue_author_repo = sum(issue['issue_author']['repos_count'] for issue in repo['repo_issues'])

        high_commenters_followers = 0
        high_commenters_following = 0
        high_commenters_repo = 0

        mpc = None

        for issue in repo['repo_issues']:
            if issue['issue_comments']:
                high_commenter = max(issue['issue_comments'], key=lambda x:x['comment_author']['followers_count'])
                high_commenters_followers += high_commenter['comment_author']['followers_count']
                high_commenters_following += high_commenter['comment_author']['following_count']
                high_commenters_repo += high_commenter['comment_author']['repos_count']

        iwhc = max(repo['repo_issues'], key=lambda x:x['issue_comments_count'])
        unique_commenters = Counter(r['is_issue_author'] is False for r in iwhc['issue_comments'])[1]

        if iwhc['issue_comments']:
            mpc = max(iwhc['issue_comments'], key=lambda x:x['comment_author']['followers_count'] if x['is_issue_author'] is False else 0)

        data_object = {
            'name': repo['repo_name'],
            'language': repo['repo_langauge'],  # it should be language, but the db has it misspelled
            'issues_count': repo['repo_issues_count'],
            'watchers': repo['repo_watchers'],
            'forks': repo['repo_forks'],
            'stars': repo['repo_stars'],
            'owner_followers': repo['repo_owner']['followers_count'],
            'owner_followings': repo['repo_owner']['following_count'],
            'owner_repos': repo['repo_owner']['repos_count'],
            'owner_type': repo['repo_owner']['type'],
            'avg_comments_per_issue' : total_comments / float(len(repo['repo_issues'])),
            'avg_owners_followers' : avg_issue_author_followers / float(len(repo['repo_issues'])),
            'avg_owners_following' : avg_issue_author_followeing / float(len(repo['repo_issues'])),
            'avg_owners_repos' : avg_issue_author_repo / float(len(repo['repo_issues'])),

            'avg_high_commenters_followers': high_commenters_followers / float(len(repo['repo_issues'])),
            'avg_high_commenters_following': high_commenters_following / float(len(repo['repo_issues'])),
            'avg_high_commenters_repo': high_commenters_repo / float(len(repo['repo_issues'])),

            # iwhc = issue with the highest number of comments
            'iwhc_comment_count': iwhc['issue_comments_count'],
            'iwhc_owner_followers': iwhc['issue_author']['followers_count'],
            'iwhc_owner_following': iwhc['issue_author']['following_count'],
            'iwhc_owner_repo': iwhc['issue_author']['repos_count'],
            'iwhc_owner_type': iwhc['issue_author']['type'],
            'unique_commenters_percentage': unique_commenters / float(len(iwhc['issue_comments'])) if iwhc['issue_comments'] else None,

            # # mpc = most popular commenter on iwhc that is not the owner of the comment
            'mpc_followers': mpc['comment_author']['followers_count'] if mpc else None,
            'mpc_following': mpc['comment_author']['following_count'] if mpc else None,
            'mpc_repos': mpc['comment_author']['repos_count'] if mpc else None,
            'mpc_type': mpc['comment_author']['type'] if mpc else None
        }

        pprint.pprint(data_object)
        print '*'*100
        export_to_sheet(data_object, ii)
        ii += 1
    results.save("GitHubGeneralInfo.xls")


# The main function
found = 0
if __name__ == "__main__":
    extract_general_info()



