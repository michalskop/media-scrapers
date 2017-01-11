# scraper for articles and discussions in ihned.cz

import csv
import datapackage  # v0.8.3
import datetime
import git
import json
import os
import pytz
import requests
import sys

import settings
import disqus.disqus_utils as dutils
import scraper_utils as sutils

data_path = "data/"  # from this script to data

# repo settings
repo = git.Repo(settings.git_dir)
git_ssh_identity_file = settings.ssh_file
o = repo.remotes.origin
git_ssh_cmd = 'ssh -i %s' % git_ssh_identity_file
o.pull()

# load datapackage
dp = datapackage.DataPackage(settings.datapackage_path + "datapackage.json")
existing_articles = []
# older_articles = []
# existing_articles_with_posts = []
# existing_posts = []
for resource in dp.resources:
    if resource.descriptor['name'] == 'Articles':
        for row in resource.data:
            existing_articles.append(row['id'])
            # article_date = datetime.datetime.strptime(row['date'][:22] + row['date'][23:], '%Y-%m-%dT%H:%M:%S%z')
            # if (datetime.datetime.now(tz=datetime.timezone.utc) - article_date) > datetime.timedelta(settings.date_distance):
            #     older_articles.append(row['id'])
    # if resource.descriptor['name'] == 'Posts':
    #     for row in resource.data:
    #         existing_posts.append(row['id'])
    #         existing_articles_with_posts.append(row['article_id'])
new_articles = []
new_posts = []
new_likes = []
for category in settings.categories:
    date = datetime.datetime.now(tz=datetime.timezone.utc)
    arts = sutils.get_rss(category)
    for art in arts:
        art_id = int(sutils.extract_id(art['id']))
        art_date = datetime.datetime.strptime(art['published'], "%a, %d %b %Y %H:%M:%S %z")
        if art_id not in existing_articles and (date - art_date) > datetime.timedelta(settings.date_distance):
            # add to new articles
            try:
                article = {
                    "id": art_id,
                    "title": art['title'],
                    "date": art_date.isoformat(),
                    "summary": art['summary'],
                    "author": art["author"],
                    "link": art['link'],
                    "picture_link": art['media_content'][0]['url'],
                    "identifier": art['id'],
                    "category": category,
                    "scraped_date": date.isoformat()
                }

                ident = 'article_' + str(article['id'])
                thread = dutils.get_thread_details(api_code=settings.api_code, ident=ident, forum=settings.forum)
                try:
                    article['posts'] = thread['posts']
                except:
                    article['posts'] = 0
                posts = dutils.get_thread_posts(api_code=settings.api_code, ident=ident, forum=settings.forum)
                for p in posts:
                    post = {
                        'id': p['id'],
                        'article_id': article['id'],
                        'date': pytz.utc.localize(datetime.datetime.strptime(p['createdAt'], "%Y-%m-%dT%H:%M:%S")).isoformat(),
                        'message': p['raw_message'],
                        'likes': p['likes'],
                        'dislikes': p['dislikes'],
                        'user_id': p['author']['id'],
                        'user_name': p['author']['name'],
                        'user_username': p['author']['username'],
                        'user_location': p['author']['location'],
                        'user_reputation': p['author']['reputation'],
                        'scraped_date': date.isoformat()
                    }
                    new_posts.append(post)
                    if post['likes'] > 0:
                        likes = dutils.get_post_likes(api_code=settings.api_code, thread_id=thread['id'], post_id=post['id'])
                        for l in likes:
                            like = {
                                'article_id': article['id'],
                                'post_id': post['id'],
                                'poster_id': post['user_id'],
                                'liker_id': l['id'],
                                'like': 1
                            }
                            new_likes.append(like)
                new_articles.append(article)
                existing_articles.append(article['id'])
                print(category, article['title'], len(posts))
            except:
                nothing = None

            # raise(Exception)
f = settings.git_dir + settings.path + data_path + "articles.csv"
with open(f, "a") as fout:
    header = []
    for resource in dp.resources:
        if resource.descriptor['name'] == 'Articles':
            for field in resource.descriptor['schema']['fields']:
                header.append(field['name'])
    dw = csv.DictWriter(fout, header)
    for item in new_articles:
        dw.writerow(item)
    repo.git.add(f)

f = settings.git_dir + settings.path + data_path + "posts.csv"
with open(f, "a") as fout:
    header = []
    for resource in dp.resources:
        if resource.descriptor['name'] == 'Posts':
            for field in resource.descriptor['schema']['fields']:
                header.append(field['name'])
    dw = csv.DictWriter(fout, header)
    for item in new_posts:
        dw.writerow(item)
    repo.git.add(f)

f = settings.git_dir + settings.path + data_path + "likes.csv"
with open(f, "a") as fout:
    header = []
    for resource in dp.resources:
        if resource.descriptor['name'] == 'Likes':
            for field in resource.descriptor['schema']['fields']:
                header.append(field['name'])
    dw = csv.DictWriter(fout, header)
    for item in new_likes:
        dw.writerow(item)
    repo.git.add(f)

# commit to github
with repo.git.custom_environment(GIT_COMMITTER_NAME=settings.bot_name, GIT_COMMITTER_EMAIL=settings.bot_email):
    repo.git.commit(message="happily updating ihned %s articles, %s posts, %s likes" % (str(len(new_articles)), str(len(new_posts)), str(len(new_likes))), author="%s <%s>" % (settings.bot_name, settings.bot_email))
with repo.git.custom_environment(GIT_SSH_COMMAND=git_ssh_cmd):
    o.push()
