import pandas as pd, codecs, os, json, polars as pl


def main(limit: int):
    if not os.path.exists("./to_df_done.json"):
        with open("./to_df_done.json", "w") as f:
            completed_files = {}
            json.dump(completed_files, f)
    else:
        with open("./to_df_done.json", "r") as f:
            completed_files = json.load(f)

    # files = os.listdir("./tt/train/")
    files = pd.read_csv("./train_file_name.csv")["file_name"].to_list()

    # print(len(files))

    print("loaded")

    rows = []

    for idx, file in enumerate(files):

        if (idx + 1) % 10_000 == 0:
            print(f"{idx+1} Done")

        if completed_files.get(file):
            continue

        completed_files[file] = 1

        with codecs.open(f"./tt/train/{file}", "r", encoding="utf-8") as f:
            text = f.read().strip()

        rows.append(text)

        if len(rows) == limit:
            break

    if not os.path.exists("./train_dfs"):
        os.mkdir("./train_dfs")

    total_dfs = len(os.listdir("./train_dfs/"))

    print(completed_files)
    print(len(rows))

    pl.DataFrame(rows, columns=["news", pl.String], orient="row").write_csv(
        f"./train_dfs/df_{total_dfs}"
    )
    with open("./to_df_done.json", "w") as f:
        json.dump(completed_files, f)


if __name__ == "__main__":
    limit = 10
    main(limit)
