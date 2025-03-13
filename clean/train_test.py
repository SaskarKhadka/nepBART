import codecs
import os
import math
import shutil
import random


def main():
    folders = os.listdir("./cleaned_data")

    for folder in folders:
        files = os.listdir(f"./cleaned_data/{folder}")

        random.shuffle(files)
        random.shuffle(files)
        random.shuffle(files)
        random.shuffle(files)

        split_index = math.floor(len(files) * 0.91)
        train = files[:split_index]
        test = files[split_index:]

        for train_file in train:
            source = f"./cleaned_data/{folder}/{train_file}"
            destination = f"./train_test/train/{folder}_{train_file}"

            shutil.copy(source, destination)

        for test_file in test:
            source = f"./cleaned_data/{folder}/{test_file}"
            destination = f"./train_test/test/{folder}_{test_file}"

            shutil.copy(source, destination)


if __name__ == "__main__":
    if not os.path.exists("./train_test"):
        os.mkdir("./train_test")
        os.mkdir("./train_test/train")
        os.mkdir("./train_test/test")
    main()
