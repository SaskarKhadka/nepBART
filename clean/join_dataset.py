import polars as pl
import os

files = os.listdir("./cleaned")

df = pl.DataFrame()

for file in files:
    if ".csv" in file:
        if df.is_empty():
            df = pl.read_csv(f"./cleaned/{file}")
        else:
            df.extend(pl.read_csv(f"./cleaned/{file}"))

print(df.height)
df.write_csv("./cleaned/full_dataset.csv")
