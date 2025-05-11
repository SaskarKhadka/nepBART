from bs4 import BeautifulSoup
import requests as req

from newspaper_info import *
import os
import json
import pandas as pd
import time

base_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_path, "data")
dcnepal_data_path = os.path.join(data_path, "dcnepal")

if not os.path.exists(data_path):
    os.mkdir(data_path)

if not os.path.exists(dcnepal_data_path):
    os.mkdir(dcnepal_data_path)

total_existsing_news = len(os.listdir(dcnepal_data_path))

news_count = total_existsing_news + 1

for category, category_details in DCNEPAL_WEBSITES.items():
    for page in range(517, category_details[1]):
        res = req.get(category_details[0] + ("" if page == 1 else f"page/{page}/"))
        with open("dcnepal_page.json", "w") as file:
            json.dump({"page": page, "category": category}, file)
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, "html5lib")
            titles_info = soup.select(
                "div.category__container div.grid div.column-3 div.row--news"
            )
            for title_info in titles_info:
                news = title_info.select("h3.news__title--small a.title")[0]
                title = news.text.strip().replace("\xa0", " ").replace("\t", " ")
                res = req.get(news.get("href"))
                soup = BeautifulSoup(res.content, "html5lib")
                news_details = soup.select("div.news-content-area p")
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
                    ).to_csv(os.path.join(dcnepal_data_path, f"{news_count}.csv"))
                    news_count += 1
                    time.sleep(4)
        elif res.status_code != 404:
            continue
        else:
            break
