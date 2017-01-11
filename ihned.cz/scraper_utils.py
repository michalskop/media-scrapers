# scraper utils for ihned

import feedparser


# parse RSS
# [{"id": "https://domaci.ihned.cz/123456", "title": "Title ...", "summary": "Short summary ...", "media_content": {"url": "http://img.ihned.cz/attachment.php/730/66746730/Gqh9jIFikzpbP7M15DyfougvnwdKrCes/jarvis_586d469e498eab700899d5a5.jpeg"}, "link": "http://ihned.cz/xxx", "author": "Pepa z Blatna", "published": "Thu, 05 Jan 2017 00:00:00 +0100"}]
def get_rss(category):
    url = "https://" + category + ".ihned.cz/?m=rss"
    feed = feedparser.parse(url)
    return feed["items"]


# get id from item_id as https://domaci.ihned.cz/65577040"
def extract_id(item_id):
    return item_id.split('/')[-1]
