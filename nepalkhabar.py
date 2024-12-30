from bs4 import BeautifulSoup
import requests as req

from newspaper_info import *
import os
import pandas as pd
import time

base_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_path, "data")
nepalkhabar_data_path = os.path.join(data_path, "nepalkhabar")

if not os.path.exists(data_path):
    os.mkdir(data_path)

if not os.path.exists(nepalkhabar_data_path):
    os.mkdir(nepalkhabar_data_path)

total_existsing_news = len(os.listdir(nepalkhabar_data_path))

news_count = total_existsing_news + 1

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15"
}

for category, category_details in NEPALKHABAR_WEBSITES.items():
    for page in range(113, category_details[1]):
        res = req.get(
            category_details[0] + ("" if page == 1 else f"?page={page}"),
            headers=headers,
        )
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, "html5lib")
            titles_info = soup.select(
                "ul.uk-list.uk-list-large.uk-list-divider li.nk-item-list-first-page div.uk-grid.uk-grid-medium"
            )
            for title_info in titles_info:
                news = title_info.select(
                    "div.uk-width-expand h3.uk-margin-remove a.uk-link-reset"
                )[0]
                title = news.text.strip().replace("\xa0", " ")
                res = req.get(NEPALKHABAR_BASE + news.get("href"), headers=headers)
                soup = BeautifulSoup(res.content, "html5lib")
                news_details = soup.select("div#body-content span p")
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
                    ).to_csv(os.path.join(nepalkhabar_data_path, f"{news_count}.csv"))
                    news_count += 1
                    time.sleep(4)
        elif res.status_code != 404:
            print(res)
            continue
        else:
            break
