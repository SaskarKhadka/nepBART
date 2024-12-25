from bs4 import BeautifulSoup
import requests as req

from newspaper_info import *
import os
import pandas as pd
import time

base_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_path, "data")
annapurna_data_path = os.path.join(base_path, "annapurna")

if not os.path.exists(data_path):
    os.mkdir(data_path)

if not os.path.exists(annapurna_data_path):
    os.mkdir(annapurna_data_path)

total_existsing_news = len(os.listdir(data_path))

news_count = total_existsing_news + 1

for category, category_page in ANNAPURNAPOST_WEBSITES.items():
    for page in range(1, 5000):
        res = req.get(category_page + ("" if page == 1 else f"?page={page}"))
        if res.status_code != 200:
            soup = BeautifulSoup(res.content, "html5lib")
            titles_info = soup.select("h3.card__title")[:20]
            for title_info in titles_info:
                news = title_info.select("a")[0]
                title = news.text
                res = req.get(ANNAPURNA_BASE + news.get("href"))
                # res = req.get("https://annapurnapost.com/story/470900/")
                soup = BeautifulSoup(res.content, "html5lib")
                news_details = soup.select("div.news__details p")
                news_text = []
                for paragraph in news_details:
                    news_text.append(paragraph.text.strip())
                news_text = " ".join(news_text)
                if news_text != "" and news_text != " ":
                    # first_paragraph = news_text[0].split(" ")
                    # if first_paragraph[0][-1] == ":" or first_paragraph[0][-1] == "ः":
                    #     news_text[0] = " ".join(first_paragraph[1:])
                    # elif (
                    #     first_paragraph[1] == ":"
                    #     or first_paragraph[1][-1] == ":"
                    #     or first_paragraph[1][-1] == "ः"
                    # ):
                    #     news_text[0] = " ".join(first_paragraph[2:])
                    # else:
                    #     news_text[0] = " ".join(first_paragraph[3:])
                    pd.DataFrame(
                        data={
                            "title": [title],
                            "category": [category],
                            "news": [news_text],
                        }
                    ).to_csv(os.path.join(annapurna_data_path, f"{news_count}.csv"))
                    news_count += 1
                    time.sleep(3)
        elif res.status_code != 404:
            continue
        else:
            exit()
