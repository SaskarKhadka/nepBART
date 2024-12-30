from bs4 import BeautifulSoup
import requests as req

from newspaper_info import *
import os
import pandas as pd
import time

base_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_path, "data")
ujyaaloonline_data_path = os.path.join(data_path, "ujyaaloonline")

if not os.path.exists(data_path):
    os.mkdir(data_path)

if not os.path.exists(ujyaaloonline_data_path):
    os.mkdir(ujyaaloonline_data_path)

total_existsing_news = len(os.listdir(ujyaaloonline_data_path))

news_count = total_existsing_news + 1

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15"
}

for category, category_details in UJYAALOONLINE_WEBSITES.items():
    for page in range(204, category_details[1]):
        res = req.get(
            category_details[0] + ("" if page == 1 else f"?page={page}"),
            headers=headers,
        )
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, "html5lib")
            titles_info = soup.select(
                "div.grid-posts div.col-md-4.padding-10 div.grid-post"
            )
            for title_info in titles_info:
                news = title_info.select(
                    "div.post-info.padding-15.ptb-20.bd-grey.match-height.text-center h3.mb-15.fw-6.fz-20 a.text-dark"
                )[0]
                title = news.text.strip().replace("\xa0", " ").replace("\t", " ")
                res = req.get(UJYAALOONLINE_BASE + news.get("href"), headers=headers)
                soup = BeautifulSoup(res.content, "html5lib")
                news_details = soup.select("div#body-content p")
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
                    ).to_csv(os.path.join(ujyaaloonline_data_path, f"{news_count}.csv"))
                    news_count += 1
                    time.sleep(4)
        elif res.status_code != 404:
            print(res.status_code)
            continue
        else:
            print("HIqq")
            break
