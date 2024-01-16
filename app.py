from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

import requests 

def search_youtube_videos(topic, max_results=5):
    search_url = "https://www.googleapis.com/youtube/v3/search" 
    params = {"key": "AIzaSyDPsRTGq8vVCYJYYcBfBgPxxgVmtn983_o",
              "q": topic,
              "part": "snippet",
              "maxResults": max_results,
              "type": "video"}
    response = requests.get(search_url, params=params)
    if(response.status_code == 200):
        items = response.json()['items']
        video_links = []
        for item in items:
            title = item['snippet']['title']
            video_id = item['id']['videoId']
            link = "https://www.youtube.com/watch?v=" + video_id
            video_links.append({"title": title, "url": link, "video_id": video_id})
        return video_links
    base_url = "https://www.youtube.com/results"
    params = {"search_query": topic, "sp=EgIQAQ%253D%253D": ""}

    response = requests.get(base_url, params=params)
    soup = BeautifulSoup(response.content, "html.parser")

    video_links = []
    for link in soup.find_all("a", href=True, title=True, class_="yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink spf-link "):
        title = link.get("title")
        url = "https://www.youtube.com" + link.get("href")
        video_links.append({"title": title, "url": url})

        if len(video_links) >= max_results:
            break

    return video_links

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    topic_to_search = request.form['topic']
    results = search_youtube_videos(topic_to_search)

    return render_template('results.html', topic=topic_to_search, results=results)

if __name__ == "__main__":
    app.run(debug=True)