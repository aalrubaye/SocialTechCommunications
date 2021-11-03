import pprint
import requests
import time
from pymongo import MongoClient

__author__ = 'Abduljaleel Al Rubaye'

client = MongoClient()
database = client.stack_overflow
git_repos = database.repos

with open('.env') as privateVar:
    auth_keys = [line.rstrip() for line in privateVar]

headers = {
    'Authorization': auth_keys[2],
}


def fetch_remaining():
    global remaining_calls
    rate_limit = requests.get("https://api.github.com/rate_limit", headers=headers).json()
    remaining_calls = rate_limit['rate']['remaining']


def fetch(from_url):
    global remaining_calls

    if remaining_calls < 10:
        while remaining_calls < 10:
            print 'rate limit is almost exceeded... waiting'
            time.sleep(20)
            fetch_remaining()

    remaining_calls -= 1
    try:
        return requests.get(from_url, headers=headers).json()
    except Exception as er:
        print "error in fetching the url :" + str(er.message)
        return None


def extract_owner_info(user):

    owner = fetch(user['url']+"?page="+str(1)+"&per_page=100")

    obj = {
        "id": user['id'],
        "name": user['login'],
        "type": user['type'],
        "url": user['url'],
        "created_at": owner['created_at'],
        "followers_count": owner['followers'],
        "following_count": owner['following'],
        "repos_count": owner['public_repos']
    }

    return obj


def extract_issue_data_from_repo(url):

    try:

        auth_ids = []
        auth_objs = []

        response = fetch(url+"?page=1&per_page=100")
        print '-'*50
        print "repo ("+str(response['name'])+") --> url = " + url
        print '-'*50

        if response:
            issues_list = []
            issues = fetch(url+"/issues?page="+str(1)+"&per_page=50&state=closed&sort=comments")

            if issues:
                totlIssues = fetch(url+"/issues?per_page=1&state=all")
                pprint.pprint(totlIssues[0]['number'])
                for issue in issues:
                    print "repo ("+str(response['name'])+") --> issue # "+str(issue['number'])
                    issue_author = extract_owner_info(issue['user'])

                    comments_list = []
                    if issue['comments'] > 0:
                        comments = fetch(issue['comments_url']+"?page="+str(1)+"&per_page=100")
                        if comments:
                            for com in comments:
                                if issue_author['id'] == com['user']['id']:
                                    comment_author = issue_author
                                    is_issue_author = True
                                else:
                                    if com['user']['id'] in auth_ids:
                                        ind = auth_ids.index(com['user']['id'])
                                        comment_author = auth_objs[ind]
                                    else:
                                        comment_author = extract_owner_info(com['user'])
                                    is_issue_author = False
                                comment_object = {
                                    "comment_id": com['id'],
                                    "comment_created_at": com['created_at'],
                                    "comment_body": com['body'],
                                    "comment_url": com['url'],
                                    "comment_author": comment_author,
                                    "is_issue_author": is_issue_author
                                }
                                comments_list.append(comment_object)
                                if com['user']['id'] not in auth_ids:
                                    auth_ids.append(com['user']['id'])
                                    auth_objs.append(comment_author)

                    issue_object = {
                        "issue_id": issue['id'],
                        "issue_number": issue['number'],
                        "issue_title": issue['title'],
                        "issue_created_at": issue['created_at'],
                        "issue_closed_at": issue['closed_at'],
                        "issue_comments_url": issue['comments_url'],
                        "issue_comments_count": issue['comments'],
                        "issue_author": issue_author,
                        "issue_comments": comments_list,
                        "issue_url": issue['url']
                    }
                    issues_list.append(issue_object)

                data_object = {
                    "repo_name": response['name'],
                    "repo_forks": response['forks_count'],
                    "repo_watchers": response['subscribers_count'],
                    "repo_stars": response['stargazers_count'],
                    "repo_langauge": response['language'],
                    "repo_created_at": response['created_at'],
                    "repo_issues_count": totlIssues[0]['number'],
                    "repo_repo_id": response['id'],
                    "repo_topics": response['topics'],
                    "repo_url": url,
                    "repo_issues_url": url+"/issues",
                    "repo_owner": extract_owner_info(response['owner']),
                    "repo_issues": issues_list
                }
                # pprint.pprint(data_object)

                print 'Done with repo '+str(response['name'])
                print '.'*100
                git_repos.insert(data_object)

    except Exception as er:
        print(er.message)


# The main function
if __name__ == "__main__":
    fetch_remaining()

    with open('url_final.txt') as f:
        lines = [line.rstrip() for line in f]

    for url in lines:
        extract_issue_data_from_repo(url)
