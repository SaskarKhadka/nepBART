from bs4 import BeautifulSoup
import requests as req

from newspaper_info import *
import os
import pandas as pd
import time

base_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_path, "data")
gorkhapatra_data_path = os.path.join(data_path, "gorkhapatra")

if not os.path.exists(data_path):
    os.mkdir(data_path)

if not os.path.exists(gorkhapatra_data_path):
    os.mkdir(gorkhapatra_data_path)

total_existsing_news = len(os.listdir(gorkhapatra_data_path))

news_count = total_existsing_news + 1

for category, category_details in GORKHAPATRA_WEBSITES.items():
    for page in range(1, category_details[1]):
        res = req.get(category_details[0] + ("" if page == 1 else f"?page={page}"))
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, "html5lib")
            titles_info = soup.select(
                "div.container div.row.justify-content-center div.col-lg-9.category-left-layout div.row.justify-content-center div.col-lg-12.mb-5 div.slider-box-layout1 div.item-content"
            )
            titles_info += soup.select(
                "div.col-lg-12 div.blog-box-layout11.w-100.mb-5 div.item-content.d-flex.flex-column.align-items-start.justify-content-center"
            )
            for title_info in titles_info:
                news = title_info.select("h2.item-title a")[0]
                title = news.text
                res = req.get(news.get("href"))
                # res = req.get("https://gorkhapatraonline.com/news/136266")
                soup = BeautifulSoup(res.content, "html5lib")
                news_details = soup.select("div.single-blog-content div.blog-details p")
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
                    ).to_csv(os.path.join(gorkhapatra_data_path, f"{news_count}.csv"))
                    news_count += 1
                    time.sleep(3)
        elif res.status_code != 404:
            continue
        else:
            break
