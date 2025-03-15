"""
Remove all the articles with less than or equal to 10 words
"""

import os
import pandas as pd


def main():
    df_5 = pd.read_csv("less_than_5.csv")
    df_10 = pd.read_csv("less_than_10.csv")

    for df in [df_5, df_10]:
        for _, each in df_5.iterrows():
            file_data = each["file_name"].split("_")
            if os.path.exists(f"./cleaned_data/{file_data[0]}/{file_data[1]}"):
                os.remove(f"./cleaned_data/{file_data[0]}/{file_data[1]}")


if __name__ == "__main__":
    main()
