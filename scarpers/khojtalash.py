from bs4 import BeautifulSoup
import requests as req

from newspaper_info import *
import os
import json
import pandas as pd
import time

base_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_path, "data")
khojtalash_data_path = os.path.join(data_path, "khojtalash")

if not os.path.exists(data_path):
    os.mkdir(data_path)

if not os.path.exists(khojtalash_data_path):
    os.mkdir(khojtalash_data_path)

total_existsing_news = len(os.listdir(khojtalash_data_path))

news_count = total_existsing_news + 1

for category, category_details in KHOJTALASH_WEBSITES.items():
    for page in range(39, category_details[1]):
        res = req.get(category_details[0] + ("" if page == 1 else f"?page={page}"))
        with open("khojtalash_page.json", "w") as file:
            json.dump({"page": page, "category": category}, file)
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, "html5lib")
            titles_info = soup.select(
                "div.col-md-9 div.row div.col-md-4.mt-2.mb-3 a.small-title"
            )
            for title_info in titles_info:
                title = title_info.text.strip().replace("\xa0", " ").replace("\t", " ")
                res = req.get(title_info.get("href"))
                # res = req.get("https://khojtalashonline.com/news/136266")
                soup = BeautifulSoup(res.content, "html5lib")
                news_details = soup.select(
                    "div.single-detail div.col-md-12.col-sm-12 p"
                )
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
                    ).to_csv(os.path.join(khojtalash_data_path, f"{news_count}.csv"))
                    news_count += 1
                    time.sleep(4)
        elif res.status_code != 404:
            continue
        else:
            break
