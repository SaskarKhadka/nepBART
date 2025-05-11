from bs4 import BeautifulSoup
import requests as req

from newspaper_info import *
import os
import json
import pandas as pd
import time

base_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_path, "data")
jaanastha_data_path = os.path.join(data_path, "jaanastha")

if not os.path.exists(data_path):
    os.mkdir(data_path)

if not os.path.exists(jaanastha_data_path):
    os.mkdir(jaanastha_data_path)

total_existsing_news = len(os.listdir(jaanastha_data_path))

news_count = total_existsing_news + 1

for category, category_details in JAANASTHA_WEBSITES.items():
    for page in range(93, category_details[1]):
        res = req.get(category_details[0] + ("" if page == 1 else f"?page={page}"))
        if res.status_code == 200:
            with open("jaanastha_page.json", "w") as file:
                json.dump({"page": page, "category": category}, file)
            soup = BeautifulSoup(res.content, "html5lib")
            titles_info = soup.select(
                "div.category__list-wrapper div.category__list-grid div.grid__card div.card__details h3.card__title"
            )
            for title_info in titles_info:
                news = title_info.select("a")[0]
                title = news.text.strip().replace("\xa0", " ").replace("\t", " ")
                res = req.get(JAANASTHA_BASE + news.get("href"))
                # res = req.get("https://jaanasthaonline.com/news/136266")
                soup = BeautifulSoup(res.content, "html5lib")
                news_details = soup.select("div.para__text p")
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
                    ).to_csv(os.path.join(jaanastha_data_path, f"{news_count}.csv"))
                    news_count += 1
                    time.sleep(4)
        elif res.status_code != 404:
            continue
        else:
            break
