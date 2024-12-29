from bs4 import BeautifulSoup
import requests as req

from newspaper_info import *
import os
import pandas as pd
import time

base_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_path, "data")
nagarik_data_path = os.path.join(data_path, "nagarik")

if not os.path.exists(data_path):
    os.mkdir(data_path)

if not os.path.exists(nagarik_data_path):
    os.mkdir(nagarik_data_path)

total_existsing_news = len(os.listdir(nagarik_data_path))

news_count = total_existsing_news + 1

for category, category_details in NAGARIK_WEBSITES.items():
    for page in range(101, category_details[1]):
        res = req.get(category_details[0] + f"/load-more?offset={page*24}&is_ajax=true")
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, "html5lib")
            titles_info = soup.select("div.articles article.list-group-item")
            for title_info in titles_info:
                news = title_info.select("div.text h1 a")[0]
                title = (
                    news.text.strip()
                    .replace("\xa0", " ")
                    .replace("\n", " ")
                    .replace("\t", " ")
                )
                res = req.get(NAGARIK_BASE + news.get("href"))
                # res = req.get("https://nagarikonline.com/news/136266")
                soup = BeautifulSoup(res.content, "html5lib")
                news_details = soup.select("div.content.text-justify article p")
                news_text = []
                for paragraph in news_details:
                    news_text.append(
                        paragraph.text.strip()
                        .replace("\xa0", " ")
                        .replace("\n", " ")
                        .replace("\t", " ")
                    )
                news_text = " ".join(news_text)
                if news_text.strip() != "":
                    pd.DataFrame(
                        data={
                            "title": [title],
                            "category": [category],
                            "news": [news_text],
                        }
                    ).to_csv(os.path.join(nagarik_data_path, f"{news_count}.csv"))
                    news_count += 1
                    time.sleep(3)
        elif res.status_code != 404:
            continue
        else:
            break
