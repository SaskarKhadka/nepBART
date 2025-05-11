from bs4 import BeautifulSoup
import requests as req

from newspaper_info import *
import os
import json
import pandas as pd
import time

base_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_path, "data")
ratopati_data_path = os.path.join(data_path, "ratopati")

if not os.path.exists(data_path):
    os.mkdir(data_path)

if not os.path.exists(ratopati_data_path):
    os.mkdir(ratopati_data_path)

total_existsing_news = len(os.listdir(ratopati_data_path))

news_count = total_existsing_news + 1

for category, category_details in RATOPATI_WEBSITES.items():
    for page in range(1, category_details[1]):
        res = req.get(category_details[0] + ("" if page == 1 else f"?page={page}"))
        with open("ratopati_page.json", "w") as file:
            json.dump({"page": page, "category": category}, file)
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, "html5lib")
            titles_info = soup.select("div.dn-grid div.columnnews.mbl-col.col3")
            for title_info in titles_info:
                news = title_info.select("a")[0]
                title = (
                    title_info.select("div.columnnews-wrap h3.news-title")[0]
                    .text.strip()
                    .replace("\xa0", " ")
                    .replace("\t", " ")
                )
                res = req.get(news.get("href"))
                # res = req.get("https://ratopationline.com/news/136266")
                soup = BeautifulSoup(res.content, "html5lib")
                news_details = soup.select("div.news-contentarea div.the-content p")
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
                    ).to_csv(os.path.join(ratopati_data_path, f"{news_count}.csv"))
                    news_count += 1
                    time.sleep(4)
        elif res.status_code != 404:
            continue
        else:
            break
