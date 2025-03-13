import codecs
import os


def main():
    folders = os.listdir("./cleaned_data")

    folders = ["annapurna"]

    for folder in folders:
        files = os.listdir(f"./cleaned_data/{folder}")
        files = list(range(15, 20))
        for file in files:
            with codecs.open(
                f"./cleaned_data/{folder}/{file}", "r", encoding="utf-8"
            ) as file:
                text = file.read().split("।'")
                # text_temp = text[:]
                sentences = []
                for each in text:
                    each.split()
                # for text in text.split("।'")


if __name__ == "__main__":
    main()
