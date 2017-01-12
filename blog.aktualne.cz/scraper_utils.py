# scraper utils for blog.aktualne.cz

import feedparser


# parse RSS
# [{'published_parsed': time.struct_time(tm_year=2017, tm_mon=1, tm_mday=11, tm_hour=21, tm_min=22, tm_sec=25, tm_wday=2, tm_yday=11, tm_isdst=0), 'summary': 'Nastal čas uvažovat vážně o tom, že pan prezident není schopen vykonávat funkci ze zdravotních důvodů.', 'links': [{'rel': 'alternate', 'type': 'text/html', 'href': 'http://blog.aktualne.cz/blogy/jan-payne.php?itemid=28674'}], 'image1': 'http://img.aktualne.centrum.cz/593/86/5938634-blog-jan-payne.jpg', 'image4': '346070', 'title_detail': {'value': 'Jan Payne: Nastal čas …', 'type': 'text/plain', 'language': None, 'base': 'http://blog.aktualne.cz/export-all.php'}, 'image3': 'http://img.aktualne.centrum.cz/593/86/5938646-blog-jan-payne.jpg', 'summary_detail': {'value': 'Nastal čas uvažovat vážně o tom, že pan prezident není schopen vykonávat funkci ze zdravotních důvodů.', 'type': 'text/html', 'language': None, 'base': 'http://blog.aktualne.cz/export-all.php'}, 'guidislink': False, 'link': 'http://blog.aktualne.cz/blogy/jan-payne.php?itemid=28674', 'published': 'Wed, 11 Jan 2017 22:22:25 +0100', 'id': 'http://blog.aktualne.cz/blogy/jan-payne.php?itemid=28674', 'title': 'Jan Payne: Nastal čas …'}]
def get_rss():
    url = "http://blog.aktualne.cz/export-all.php"
    feed = feedparser.parse(url)
    return feed["items"]


# get id from item_id as http://blog.aktualne.cz/blogy/jan-payne.php?itemid=28674"
def extract_id(item_id):
    return item_id.split('=')[-1]


# get author from blogpost's title
def extract_author(title):
    return title.split(':')[0]


# create Disqus identifier from id
def create_identifier(item_id):
    return "blogy-aktualne-" + str(item_id)
