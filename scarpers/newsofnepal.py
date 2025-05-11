from bs4 import BeautifulSoup
import requests as req

from newspaper_info import *
import os
import json
import pandas as pd
import time

base_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_path, "data")
newsofnepal_data_path = os.path.join(data_path, "newsofnepal")

if not os.path.exists(data_path):
    os.mkdir(data_path)

if not os.path.exists(newsofnepal_data_path):
    os.mkdir(newsofnepal_data_path)

total_existsing_news = len(os.listdir(newsofnepal_data_path))

news_count = total_existsing_news + 1

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

for category, category_details in NEWSOFNEPAL_WEBSITES.items():
    for page in range(1, category_details[1]):
        res = req.get(
            category_details[0] + ("" if page == 1 else f"/page/{page}/"),
            headers=headers,
        )
        with open("newsofnepal_page.json", "w") as file:
            json.dump({"page": page, "category": category}, file)
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, "html5lib")
            titles_info = soup.select(
                # "div.uk-grid.uk-grid-stack div.uk-grid.uk-grid-small.uk-margin-medium-top.uk-grid-margin.uk-first-column div div.card.uk-card.uk-card-small div.uk-padding-small h4"
                # "div div.card.uk-card.uk-card-small div.uk-padding-small h4"
                "div div.card.uk-card.uk-card-small div.uk-margin-small-top h4"
            )
            for title_info in titles_info:
                news = title_info.select("a.ah")[0]
                title = news.text.strip().replace("\xa0", " ").replace("\t", " ")
                res = req.get(news.get("href"), headers=headers)
                soup = BeautifulSoup(res.content, "html5lib")
                news_details = soup.select("article.uk-card div.post-entry p")
                news_text = []
                for paragraph in news_details:
                    news_text.append(
                        paragraph.text.strip().replace("\xa0", " ").replace("\t", " ")
                    )
                news_text = "\n".join(news_text)
                if news_text.strip() != "":
                    pd.DataFrame(
                        data={
                            "title": [title],
                            "category": [category],
                            "news": [news_text],
                        }
                    ).to_csv(os.path.join(newsofnepal_data_path, f"{news_count}.csv"))
                    news_count += 1
                    time.sleep(4)
        elif res.status_code != 404:
            print(res)
            continue
        else:
            break
