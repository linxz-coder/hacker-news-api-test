import requests
session = requests.Session()
from bs4 import BeautifulSoup as BS
import logging
logger = logging.getLogger(__name__)
from urllib.parse import urljoin, urlsplit
import re
from null import Null
from datetime import datetime, timedelta
# from news import News
from exception import ParseError

end_point = 'https://news.ycombinator.com/'

sites_for_users = ('github.com', 'medium.com', 'twitter.com')

def parse_comhead(url):
    # 也包含https，因为前四位是http
    if not url.startswith('http'):
        url = 'http://' + url
    us = urlsplit(url.lower())
    # print('us', us)
    comhead = us.hostname
    # print('comhead', comhead)
    hs = comhead.split('.')
    if len(hs) > 2 and hs[0] == 'www':
        comhead = comhead[4:]
    if comhead in sites_for_users:
        ps = us.path.split('/')
        # print('ps', ps)
        if len(ps) > 1 and ps[1]:
            comhead = '%s/%s' % (comhead, ps[1])
    return comhead

def human2datetime(text):
    """Convert human readable time strings to datetime
    >>> self.human2datetime('2 minutes ago')
    datetime.datetime(2015, 11, 1, 14, 42, 24, 910863)

    """
    day_ago = hour_ago = minute_ago = 0
    m = re.search(r'(?P<day>\d+) day', text, re.I)
    if m:
        day_ago = int(m.group('day'))
    m = re.search(r'(?P<hour>\d+) hour', text, re.I)
    if m:
        hour_ago = int(m.group('hour'))
    m = re.search(r'(?P<minute>\d+) minute', text, re.I)
    if m:
        minute_ago = int(m.group('minute'))
    return datetime.utcnow() - \
        timedelta(days=day_ago, hours=hour_ago, minutes=minute_ago)

# test_url = "https://github.com/linxz-coder/flask-blog"
# parse_comhead(test_url)

def get_comment_url(path):
    if not isinstance(path, str):
        return None
    return 'https://news.ycombinator.com/item?id=%s' % re.search(r'\d+', path).group()

def parse_news_list():
    resp = session.get(end_point)
    resp.raise_for_status() #如果发现错误如400/500，会抛出异常;如果没有错误，则会继续执行
    content = resp.text
    dom = BS(content, features="lxml")
    items = []
    for rank, item_line in enumerate(
            dom.select('table tr table tr.athing')):
        # previous_sibling won't work when there are spaces between them.
        subtext_dom = item_line.find_next_sibling('tr')
        title_dom = item_line.find('td', class_='title', align=False)
        title = title_dom.a.get_text(strip=True) #参数 strip=True 的作用是去除文本两端的空白字符，比如空格、换行符等。这通常用于清理和格式化提取出的文本。
        logger.info('Gotta %s', title)
        # url = urljoin(end_point, title_dom.a['href'])
        url = title_dom.a['href']
        # print('url', url)

        comhead = parse_comhead(url)
        # print('========================')
        # print('comhead', comhead)



        # pop up user first, so everything left has a pattern
        author_dom = (subtext_dom.find('a', href=re.compile(r'^user', re.I)) or Null).extract()
        # print('author_dom', author_dom)
        author = author_dom.text.strip() or None
        author_link = author_dom['href'] or None
        score_human = subtext_dom.find(string=re.compile(r'\d+.+point')) or '0'
        score = re.search(r'\d+', score_human).group() or None
        submit_time = subtext_dom.find(string=re.compile(r'\d+ \w+ ago')) or None
        if submit_time:
            submit_time = human2datetime(submit_time)
        # In case of no comments yet
        comment_dom = subtext_dom.find('a', string=re.compile(r'\d+.+comment')) or Null
        comment_cnt = re.search(r'\d+', comment_dom.get_text() or '0').group()
        comment_url = get_comment_url(comment_dom['href'])

        # items.append(News(
        #     rank=rank,
        #     title=title,
        #     url=url,
        #     comhead=comhead,
        #     score=score,
        #     author=author,
        #     author_link=urljoin(end_point, author_link) if author_link else None,
        #     submit_time=submit_time,
        #     comment_cnt=comment_cnt,
        #     comment_url=comment_url
        # ))

        items.append(dict(
            rank=rank,
            title=title,
            url=url,
            comhead=comhead,
            score=score,
            author=author,
            author_link=urljoin(end_point, author_link) if author_link else None,
            submit_time=submit_time,
            comment_cnt=comment_cnt,
            comment_url=comment_url
        ))
    if len(items) == 0:
        raise ParseError('failed to parse hacker news page, got 0 item, text %s' % content)
    print('items', items)
    return items

parse_news_list()