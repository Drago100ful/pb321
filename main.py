from datetime import datetime
from glob import glob

import matplotlib.pyplot as plt
import pandas as pd


def generate_monthly_csv():
    dfs = []
    files = glob('./dataset/monthly/*.csv')

    for i, path in enumerate(files):
        dfs.append(pd.read_csv(path).set_index('Page'))
        dfs[i].loc[dfs[i]["Edits"] == "?", "Edits"] = "None"
        dfs[i].loc[dfs[i]["Editors"] == "?", "Editors"] = "None"
        dfs[i]["Date"] = datetime.strptime(path[len([files[0]]) - 12::].rstrip(".csv"), "%Y_%m").strftime("%Y-%m-%d")

    dfGen = pd.concat(dfs)
    dfGen = dfGen.sort_values("Date", ascending=False)
    dfGen.to_csv("./dataset/out/topviews_merged.csv")


if __name__ == '__main__':
    # generate_monthly_csv()

    plt.rcParams[("figure.figsize")] = [10, 5]
    query = "Oppenheimer (film)"

    dfMonthly = pd.read_csv("dataset/out/topviews_merged.csv").set_index("Date").sort_values("Date", ascending=True)
    df = dfMonthly[dfMonthly.Page.isin([query])]

    plt.figure()
    fig, ax = plt.subplots()

    df["Views"].plot(ax=ax, title=query, x="Date", label="Views", legend=True)
    plt.ylabel("Views in millions")

    mask = df["Edits"] == "?"
    df[~mask]["Edits"].plot(x="Date", y="Edits", ax=ax, secondary_y=True, label="Edits", legend=True)
    plt.ylabel("Edits")

    mask2 = df["Editors"] == "?"
    df[~mask2]["Editors"].plot(ax=ax, x="Date", secondary_y=True, label="Editors", legend=True)

    plt.gcf().autofmt_xdate(rotation=45)
    plt.show()
