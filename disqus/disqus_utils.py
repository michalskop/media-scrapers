# Utils for getting likes/dislikes from disqus
# note: pagination not taken into account (limit 100) TODO

import json
import requests


# Thread details
# {"response": {"id": "5447027452", "link": "https://...", "title": "Article ...", "posts": 48}}
def get_thread_details(api_code, ident, forum):
    url = "http://disqus.com/api/3.0/threads/details.json"
    params = {
        'api_key': api_code,
        'thread:ident': ident,
        'forum': forum
    }
    r = requests.get(url, params=params)
    if r.status_code == 200:
        return r.json()['response']
    else:
        return {}


# Thread posts
# {"response": [{"id": "3091110048", "raw_message": "bla bla bla", "likes": 2, "dislikes": 1, "createdAt": "2017-01-09T12:10:44", "author": {id": "194584300", "username": "some_user_name", "name": "somename", "location": "", "reputation": 1.61}]}
def get_thread_posts(api_code, ident, forum):
    url = "http://disqus.com/api/3.0/threads/listPosts.json"
    params = {
        'api_key': api_code,
        'thread:ident': ident,
        'forum': forum,
        'limit': 100
    }
    r = requests.get(url, params=params)
    if r.status_code == 200:
        return r.json()['response']
    else:
        return []


# Thread likes
# {"response": [{"id": "194584300", "username": "some_user_name", "name": "somename"}]}
def get_post_likes(api_code, thread_id, post_id):
    url = "http://disqus.com/api/3.0/posts/listUsersVotedPost"
    params = {
        'api_key': api_code,
        'thread': thread_id,
        'post': post_id,
        'limit': 100,
        'vote': 1
    }
    r = requests.get(url, params=params)
    if r.status_code == 200:
        return r.json()['response']
    else:
        return []


# Thread dislikes
# {"response": [{"id": "194584300", "username": "some_user_name", "name": "somename"}]}
# note: dislikes may not me working
def get_post_dislikes(api_code, thread_id, post_id):
    url = "http://disqus.com/api/3.0/posts/listUsersVotedPost"
    params = {
        'api_key': api_code,
        'thread': thread_id,
        'post': post_id,
        'limit': 100,
        'vote': -1
    }
    r = requests.get(url, params=params)
    if r.status_code == 200:
        return r.json()['response']
    else:
        return []
