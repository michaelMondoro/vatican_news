import requests
import bs4 as bs
from dateutil import parser
import uuid
from pytz import timezone
from transformers import pipeline

class VaticanNews():
    def __init__(self):
        self.articles = []
        self.daily_bulletin_url = "https://press.vatican.va/content/salastampa/en/bollettino.feedrss.xml"
        self.news_url = "https://www.vaticannews.va/en.rss.xml"
        self.dates = []
        self.summaries = []
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    def get_news(self):
        self.articles = []
        xml = requests.get(self.news_url)
        soup = bs.BeautifulSoup(xml.content, "xml")
        items = soup.find_all('item')
        for item in items:
            self.articles.append(Item(item.find('title').text, item.find('pubDate').text, desc=item.find('description').text, link=item.find("link").text))

        for a in self.articles:
            if a.pubDate.split(",")[0] not in self.dates:
                self.dates.append(a.pubDate.split(",")[0])
        
        return self.articles

    def get_summary(self, url):
        print("Getting article: " + url)
        res = requests.get(url)
        soup = bs.BeautifulSoup(res.content, "html.parser")
        text = soup.find("div", {"class": "article__text"}).text
        try:
            summary = self.summarizer(text, max_length=400, min_length=150, do_sample=False)
        except Exception:
            print("truncated...")
            summary = self.summarizer(text, max_length=400, min_length=150, do_sample=False, truncation=True)

        self.summaries.append({"name" : url,"summary" : summary[0]['summary_text']})
        return summary[0]['summary_text']
    
class Item:
    def __init__(self, title, pubDate, desc=None, link=None):
        self.id = str(uuid.uuid4())
        self.title = title.strip()
        self.link = link
        self.pubDate = parser.parse(pubDate.strip())
        self.pubDate = self.pubDate.astimezone(timezone('US/Eastern'))
        self.pubDate = self.pubDate.strftime("%b %d, %Y %I:%M%p")

        desc = desc.strip()
        start = desc.index('<p>')+3
        end = desc.index('</p>')
        self.desc = desc[start:end]

    def __str__(self):
        return f"Item(title={self.title}, pubDate={self.pubDate.ctime()}, desc=[ {self.desc} ], link={self.link})"
    def __repr__(self):
        return f"Item(title={self.title}, pubDate={self.pubDate.ctime()}, desc={self.desc}, link={self.link})"
