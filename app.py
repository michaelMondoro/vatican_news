from flask import Flask
from flask import render_template, request, jsonify
import requests 
import bs4 as bs
from vatican_news import VaticanNews
from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
news = VaticanNews()
app = Flask(__name__)

print("Initialized...")


@app.route("/summarize", methods=["POST"])
def summarize():
    url = request.args.get('url')
    print("Getting article: " + url)
    res = requests.get(url)
    soup = bs.BeautifulSoup(res.content, "html.parser")
    text = soup.find("div", {"class": "article__text"}).text
    try:
        summary = summarizer(text, max_length=400, min_length=150, do_sample=False)
    except Exception:
        print("truncated...")
        summary = summarizer(text, max_length=400, min_length=150, do_sample=False, truncation=True)

    print("SUMMARIZED")
    return {"summary" : summary[0]['summary_text']}

@app.route("/")
def home():
    print("addr: " + str(request.environ.get("REMOTE_ADDR")))
    articles = news.get_news()
    return render_template('index.html', articles=articles, dates=news.dates)

if __name__ == "__main__":
    app.run(debug=True)
