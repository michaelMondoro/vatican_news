import requests
import bs4 as bs
from dateutil import parser

daily_bulletin_url = "https://press.vatican.va/content/salastampa/en/bollettino.feedrss.xml"
news_url = "https://www.vaticannews.va/en.rss.xml"

xml = requests.get(news_url)
soup = bs.BeautifulSoup(xml.content, "xml")
items = soup.find_all('item')

class Item:
    def __init__(self, title, pubDate, desc=None, link=None):
        self.title = title.strip()
        self.link = link
        self.pubDate = parser.parse(pubDate.strip())

        desc = desc.strip()
        start = desc.index('<p>')+3
        end = desc.index('</p>')
        self.desc = desc[start:end]
    
    def __str__(self):
        return f"Item(title={self.title}, pubDate={self.pubDate.ctime()}, desc=[ {self.desc} ], link={self.link})"
    def __repr__(self):
        return f"Item(title={self.title}, pubDate={self.pubDate.ctime()}, desc={self.desc}, link={self.link})"

articles = []
for item in items:
    articles.append(Item(item.find('title').text, item.find('pubDate').text, desc=item.find('description').text, link=item.find("link").text))

articles.sort(key=lambda x: x.pubDate, reverse=True)

for item in articles:
    print(item)
    print("----")
    print()