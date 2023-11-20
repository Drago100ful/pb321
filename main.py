from datetime import datetime
from glob import glob

import pandas as pd


def generate_monthly_csv():
    dfs = []
    files = glob('./dataset/monthly/*.csv')

    for i, path in enumerate(files):
        dfs.append(pd.read_csv(path).head(200).set_index('Page'))
        dfs[i]["Date"] = datetime.strptime(path[len([files[0]]) - 12::].rstrip(".csv"), "%Y_%m").strftime("%B %Y")

    df = pd.concat(dfs)
    df = df.sort_values("Views", ascending=False)
    df.to_csv("./dataset/out/topviews_merged.csv")


if __name__ == '__main__':
    # generate_monthly_csv()

    dfMonthly = pd.read_csv("dataset/out/topviews_merged.csv")
    print(dfMonthly)
