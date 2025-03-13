import polars as pl
import regex as re
import os, sys, codecs
import json, traceback


def perform_preprocessing(text):
    text = (
        text.replace("\n", " ")
        .replace("\r", " ")
        .replace("\t", " ")
        .replace("–", "-")
        .replace(" ।", "। ")
        .replace("—", "-")
        .replace("ॽ", "? ")
        .replace(" ?", "? ")
        .replace("ঃ", "ः")
        .replace("“", '"')
        .replace("”", '"')
        .replace("‘", "'")
        .replace("’", "'")
        .replace("0", "०")
        .replace("1", "१")
        .replace("2", "२")
        .replace("3", "३")
        .replace("4", "४")
        .replace("5", "५")
        .replace("6", "६")
        .replace("7", "७")
        .replace("8", "८")
        .replace("9", "९")
    )

    # Remove emojis
    regrex_pattern = re.compile(
        pattern="["
        "\U0001f600-\U0001f64f"  # emoticons
        "\U0001f300-\U0001f5ff"  # symbols & pictographs
        "\U0001f680-\U0001f6ff"  # transport & map symbols
        "\U0001f1e0-\U0001f1ff"  # flags (iOS)
        "\U00002500-\U00002bef"  # chinese char
        "\U00002702-\U000027b0"
        "\U000024c2-\U0001f251"
        "\U0001f926-\U0001f937"
        "\U00010000-\U0010ffff"
        "\u2640-\u2642"
        "\u2600-\u2b55"
        "\u200d"
        "\u23cf"
        "\u23e9"
        "\u231a"
        "\ufe0f"  # dingbats
        "\u3030"
        "]+",
        flags=re.UNICODE,
    )
    text = regrex_pattern.sub(r"", text)

    # Handle comma (a whitespace after one and no whitespace before it)
    text = text.replace(",", ", ")
    text = re.sub(r"\s+,", ",", text)

    # Remove multiple white spaces
    text = re.sub(r"\s+", " ", text)

    return text


def main(folder_name: str):
    folder_exists = True

    if not os.path.exists(f"./cleaned_data"):
        os.mkdir("./cleaned_data")

    if not os.path.exists(f"./cleaned_data/{folder_name}"):
        folder_exists = False
        os.mkdir(f"./cleaned_data/{folder_name}")

    if not os.path.exists(f"./cleaned_data/{folder_name}/completed.json"):
        with open(f"./cleaned_data/{folder_name}/completed.json", "w") as file:
            completed_files = {}
            json.dump(completed_files, file)
    else:
        with open(f"./cleaned_data/{folder_name}/completed.json", "r") as file:
            completed_files = json.load(file)

    files = os.listdir(f"../data/{folder_name}")

    if folder_exists:
        completed_files_len = len(os.listdir(f"./cleaned_data/{folder_name}/"))
        if len(files) - completed_files_len >= 20_000:
            print(len(files), "Before")
            files = files[: completed_files_len + 20_000 - 1]
            print(len(files), "After")
    else:
        if len(files) >= 20_000:
            print(len(files), "First Before")
            files = files[:20_000]
            print(len(files), "First After")

    curr_file = None

    english = []

    try:
        for file in files:
            curr_file = file

            if completed_files.get(file):
                continue

            completed_files[curr_file] = 1

            df = pl.read_csv(f"../data/{folder_name}/{file}")

            if df["news"][0].strip() == "":
                continue

            text = perform_preprocessing(df["news"][0]).strip()

            text = text.split("।")

            if len(text) <= 1:
                continue

            if len(text[0].split()) <= 4:
                text = text[1:]

            if len(text[-1].split()) <= 4:
                text = text[:-1]

            text = "।".join(text).strip() + "।"

            if re.search("[a-zA-Z]", text):
                english.append(file)
                continue

            with codecs.open(
                f'./cleaned_data/{folder_name}/{file.split(".")[0]}.txt',
                "w",
                encoding="utf-8",
            ) as file:
                file.write(text)

    except Exception as e:
        print(traceback.format_exc())
        if completed_files.get(curr_file):
            del completed_files[curr_file]
    finally:
        with open(f"./cleaned_data/{folder_name}/completed.json", "w") as file:
            json.dump(completed_files, file)
        if not os.path.exists(f"./cleaned_data/{folder_name}_english.csv"):
            pl.DataFrame({"english_files": english}).write_csv(
                f"./cleaned_data/{folder_name}_english.csv"
            )
        else:
            data = pl.read_csv(f"./cleaned_data/{folder_name}_english.csv")
            pl.DataFrame(
                {"english_files": data["english_files"].to_list() + english}
            ).write_csv(f"./cleaned_data/{folder_name}_english.csv")


if __name__ == "__main__":
    folders = os.listdir("../data/")
    folder_name = sys.argv[1]
    if folder_name in folders:
        main(folder_name)
    else:
        print("Folder not found")
