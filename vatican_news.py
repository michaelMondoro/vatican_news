import requests
import bs4 as bs
from dateutil import parser

class VaticanNews():
    def __init__(self):
        self.articles = []
        self.daily_bulletin_url = "https://press.vatican.va/content/salastampa/en/bollettino.feedrss.xml"
        self.news_url = "https://www.vaticannews.va/en.rss.xml"


    def get_news(self):
        xml = requests.get(self.news_url)
        soup = bs.BeautifulSoup(xml.content, "xml")
        items = soup.find_all('item')
        for item in items:
            self.articles.append(Item(item.find('title').text, item.find('pubDate').text, desc=item.find('description').text, link=item.find("link").text))

        self.articles.sort(key=lambda x: x.pubDate, reverse=True)

        return self.articles


class Item:
    def __init__(self, title, pubDate, desc=None, link=None):
        self.title = title.strip()
        self.link = link
        self.pubDate = parser.parse(pubDate.strip())
        self.pubDate = self.pubDate.strftime("%b %d, %Y")

        desc = desc.strip()
        start = desc.index('<p>')+3
        end = desc.index('</p>')
        self.desc = desc[start:end]
    
    def __str__(self):
        return f"Item(title={self.title}, pubDate={self.pubDate.ctime()}, desc=[ {self.desc} ], link={self.link})"
    def __repr__(self):
        return f"Item(title={self.title}, pubDate={self.pubDate.ctime()}, desc={self.desc}, link={self.link})"
