from flask import Flask
from flask import render_template, request, jsonify
import bs4 as bs
from vatican_news import VaticanNews

print("Initializing . . .")
news = VaticanNews()
app = Flask(__name__)
@app.route("/hi")
def hi():
    return jsonify({'hi':'hi'})
@app.route("/summarize", methods=["POST"])
def summarize():
    url = request.args.get('url')
    summary = news.get_summary(url)
    return jsonify({"summary" : summary})

@app.route("/")
def home():
    print("addr: " + str(request.environ.get("REMOTE_ADDR")))
    articles = news.get_news()
    return render_template('index.html', articles=articles, dates=news.dates)

if __name__ == "__main__":
    app.run(debug=False)
