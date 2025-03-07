from bs4 import BeautifulSoup
import requests as req

from newspaper_info import *
import os
import json
import pandas as pd
import time

base_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_path, "data")
agrakhanchi_data_path = os.path.join(data_path, "agrakhanchi")

if not os.path.exists(data_path):
    os.mkdir(data_path)

if not os.path.exists(agrakhanchi_data_path):
    os.mkdir(agrakhanchi_data_path)

total_existsing_news = len(os.listdir(agrakhanchi_data_path))

news_count = total_existsing_news + 1

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

for category, category_details in AGRAKHANCHI_WEBSITES.items():
    for page in range(1, category_details[1]):
        res = req.get(
            category_details[0] + ("" if page == 1 else f"/page/{page}"),
            headers=headers,
        )
        with open("agrakhanchi_page.json", "w") as file:
            json.dump({"page": page, "category": category}, file)
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, "html5lib")
            titles_info = soup.select(
                "div.col.s12.m12 div.row div.col.s12.m3 div.news-list div.news-l-single h3"
            )
            for title_info in titles_info:
                news = title_info.select("a")[0]
                title = news.text.strip().replace("\xa0", " ").replace("\t", " ")
                res = req.get(news.get("href"), headers=headers)
                soup = BeautifulSoup(res.content, "html5lib")
                news_details = soup.select("div.news-bodyDetail div.news-body p")
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
                    ).to_csv(os.path.join(agrakhanchi_data_path, f"{news_count}.csv"))
                    news_count += 1
                    time.sleep(4)
        elif res.status_code != 404:
            print("hi")
            continue
        else:
            break
