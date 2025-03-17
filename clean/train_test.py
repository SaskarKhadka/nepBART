import codecs
import os
import math
import shutil
import random
import sys


def main(folder: str):
    folders = os.listdir("./cleaned_data")

    if folder in folders:
        # for folder in folders:
        print(f"Now running {folder}...")

        files = os.listdir(f"./cleaned_data/{folder}")

        # split_index =
        # test = list(random.sample(files, math.floor(len(files) * 0.09)))
        # train = files[:split_index]
        # test = files[split_index:]

        for train_file in files:
            if "train" in train_file:
                source = f"./cleaned_data/{folder}/{train_file}"
                # if folder == "agrakhanchi":
                destination = f"./train_test/train/{train_file}"
                # else:
                    # destination = f"./cleaned_data/{folder}/train_{folder}_{train_file}"

                shutil.copy(source, destination)

        # for test_file in test:
        #     source = f"./cleaned_data/{folder}/{test_file}"
        #     if folder == "agrakhanchi":
        #         destination = f"./cleaned_data/{folder}/test_{test_file}"
        #     else:
        #         destination = f"./cleaned_data/{folder}/test_{folder}_{test_file}"
        #     # destination = f"./train_test/{test}_{folder}_{test_file}"
        #     # destination = f"test_{folder}_{test_file}"

        #     os.rename(source, destination)

        print(folder, "completed")

    else:
        print(f"No such folder ({folder}) exists")


if __name__ == "__main__":
    if not os.path.exists("./train_test"):
        os.mkdir("./train_test")
        os.mkdir("./train_test/train")
        os.mkdir("./train_test/test")
    main(sys.argv[1])
