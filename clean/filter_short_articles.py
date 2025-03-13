import codecs
import pandas as pd


def main():
    folders = os.listdir("./cleaned_data")

    less_than_20 = []
    less_than_15 = []
    less_than_10 = []
    less_than_5 = []

    for folder in folders:
        files = os.listdir(f"./cleaned_data/{folder}")
        for file in files:
            with codecs.open(
                f"./cleaned_data/{folder}/{file}", "r", encoding="utf-8"
            ) as file:
                text = file.read()
            if len(text.split()) <= 5:
                less_than_5.append(f"{folder}_{file}")
            elif len(text.split()) <= 10:
                less_than_10.append(f"{folder}_{file}")
            elif len(text.split()) <= 15:
                less_than_15.append(f"{folder}_{file}")
            elif len(text.split()) <= 20:
                less_than_20.append(f"{folder}_{file}")

    pd.Series(less_than_5, name="file_name").to_csv("less_than_5.csv", index=None)
    pd.Series(less_than_10, name="file_name").to_csv("less_than_10.csv", index=None)
    pd.Series(less_than_15, name="file_name").to_csv("less_than_15.csv", index=None)
    pd.Series(less_than_20, name="file_name").to_csv("less_than_20.csv", index=None)


if __name__ == "__main__":
    main()
