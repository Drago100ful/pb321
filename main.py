from datetime import datetime
from glob import glob

import matplotlib.pyplot as plt
import pandas as pd


def generate_monthly_csv():
    dfs = []
    files = glob('./dataset/monthly/*.csv')

    for i, path in enumerate(files):
        dfs.append(pd.read_csv(path).head(200).set_index('Page'))
        dfs[i]["Date"] = datetime.strptime(path[len([files[0]]) - 12::].rstrip(".csv"), "%Y_%m").strftime("%Y-%m-%d")

    dfGen = pd.concat(dfs)
    dfGen = dfGen.sort_values("Date", ascending=False)
    dfGen.to_csv("./dataset/out/topviews_merged.csv")


if __name__ == '__main__':
    # generate_monthly_csv()
    plt.rcParams[("figure.figsize")] = [10, 5]
    query = "Taylor Swift"

    dfMonthly = pd.read_csv("dataset/out/topviews_merged.csv").set_index("Date").sort_values("Date", ascending=True)
    df = dfMonthly[dfMonthly.Page.isin([query])]

    df["Views"].plot(title=query, label="Views", legend=True)
    plt.ylabel("Views in millions")

    mask = df["Edits"] == "?"
    df[~mask]["Edits"].astype(int).plot(secondary_y=True, label="Edits", legend=True)
    plt.ylabel("Edits")

    mask = df["Editors"] == "?"
    df[~mask]["Editors"].astype(int).plot(secondary_y=True, label="Editors", legend=True)

    plt.gcf().autofmt_xdate(rotation=45)
    plt.show()
