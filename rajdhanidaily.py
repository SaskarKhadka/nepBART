from bs4 import BeautifulSoup
import requests as req

from newspaper_info import *
import os
import json
import pandas as pd
import time

base_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_path, "data")
rajdhanidaily_data_path = os.path.join(data_path, "rajdhanidaily")

if not os.path.exists(data_path):
    os.mkdir(data_path)

if not os.path.exists(rajdhanidaily_data_path):
    os.mkdir(rajdhanidaily_data_path)

total_existsing_news = len(os.listdir(rajdhanidaily_data_path))

news_count = total_existsing_news + 1

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

for category, category_details in RAJDHANIDAILY_WEBSITES.items():
    for page in range(1851, category_details[1]):
        res = req.get(
            category_details[0] + ("" if page == 1 else f"/page/{page}"),
            headers=headers,
        )
        with open("rajdhanidaily_page.json", "w") as file:
            json.dump({"page": page, "category": category}, file)
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, "html5lib")
            titles_info = soup.select(
                # "div.elementor-posts-container.elementor-posts.elementor-posts--skin-cards.elementor-grid.elementor-has-item-ratio article.elementor-post.elementor-grid-item.post.type-post.status-publish.format-standard.hentry.entry div.elementor-post__card div.elementor-post__text h3.elementor-post__title"
                "article div.elementor-post__card div.elementor-post__text h3.elementor-post__title"
            )
            for title_info in titles_info:
                news = title_info.select("a")[0]
                title = news.text.strip().replace("\xa0", " ").replace("\t", " ")
                res = req.get(news.get("href"), headers=headers)
                soup = BeautifulSoup(res.content, "html5lib")
                news_details = soup.select(
                    "div.elementor-widget-theme-post-content div.elementor-widget-container p"
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
                    ).to_csv(os.path.join(rajdhanidaily_data_path, f"{news_count}.csv"))
                    news_count += 1
                    time.sleep(4)
        elif res.status_code != 404:
            print("hi")
            continue
        else:
            break
