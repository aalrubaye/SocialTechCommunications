__author__ = 'Abduljaleel'

import pprint
from pymongo import MongoClient
import xlwt
from collections import Counter
import correlations

client = MongoClient()
database = client.stack_overflow
git_repos = database.repos


dd = []
i = 0
for issue in git_repos.find():
    for issues in issue['repo_issues']:
        for com in issues['issue_comments']:
             dd.append(com['comment_author']['followers_count'])
        ff = list(range(0, len(dd)))
        correlations.coeff(dd,ff)
        dd = []
        ff = []

        print ('..'*100)
        if i > 10:
            break
        else:
            i+=1
    break


