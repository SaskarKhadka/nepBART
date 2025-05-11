from bs4 import BeautifulSoup
import requests as req

from newspaper_info import *
import os
import json
import pandas as pd
import time

base_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_path, "data")
himalnews_data_path = os.path.join(data_path, "himalnews")

if not os.path.exists(data_path):
    os.mkdir(data_path)

if not os.path.exists(himalnews_data_path):
    os.mkdir(himalnews_data_path)

total_existsing_news = len(os.listdir(himalnews_data_path))

news_count = total_existsing_news + 1

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
}

for category, category_details in HIMALNEWS_WEBSITES.items():
    for page in range(527, category_details[1]):
        if page == 23:
            continue
        res = req.get(
            category_details[0] + ("" if page == 1 else f"?page={page}"),
            headers=headers,
        )
        with open("himalnews_page.json", "w") as file:
            json.dump({"page": page, "category": category}, file)
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, "html5lib", from_encoding="utf-8")
            # rows = soup.select()
            rows_location = "div#content div.container div.row.content-section section.section.section-news.big-news-list div.container div.row"
            titles_info = []

            titles_info += soup.select(
                rows_location
                + " "
                + "div.related-more.two-news.mt-4 div.container div.row div.col-sm-6.col-md-6.half-news-list.small-list div.item-news.media a"
            )
            titles_info += soup.select(
                rows_location
                + " "
                + "section.section.section-news.big-news-list div.container div.new-cat-box.border-0.pt-3 div.row div.left-side.main-news.bishesh-feat.cat-item div.samachar-box.mukhya-samachar div.items.big-news a"
            )
            for title_info in titles_info:
                title = (
                    title_info.select("span.main-title")[0]
                    .text.strip()
                    .replace("\xa0", " ")
                    .replace("\t", " ")
                )
                res = req.get(title_info.get("href"), headers=headers)
                soup = BeautifulSoup(res.content, "html5lib", from_encoding="utf-8")
                news_details = soup.select(
                    # "div.detail-box div.row div.editor-box.col-sm-11.col-md-11.fb-quotable.selectionShareable p"
                    "div.detail-box div.row div.editor-box.col-sm-11.col-md-11.fb-quotable p"
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
                    ).to_csv(os.path.join(himalnews_data_path, f"{news_count}.csv"))
                    news_count += 1
                    time.sleep(4)
        elif res.status_code != 404:
            print("hi")
            continue
        else:
            break
