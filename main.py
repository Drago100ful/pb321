from datetime import datetime
from glob import glob

import pandas as pd
import matplotlib.pyplot as plt


def generate_monthly_csv():
    dfs = []
    files = glob('./dataset/monthly/*.csv')

    for i, path in enumerate(files):
        dfs.append(pd.read_csv(path).head(200).set_index('Page'))
        dfs[i]["Date"] = datetime.strptime(path[len([files[0]]) - 12::].rstrip(".csv"), "%Y_%m").strftime("%Y-%m-%d")

    df = pd.concat(dfs)
    df = df.sort_values("Date", ascending=False)
    df.to_csv("./dataset/out/topviews_merged.csv")


if __name__ == '__main__':
    # generate_monthly_csv()

    dfMonthly = pd.read_csv("dataset/out/topviews_merged.csv")
    dfMonthly = dfMonthly.head(3600)
    dfMonthlyChatGPT = dfMonthly[dfMonthly.Page.isin(["ChatGPT"])]
    dfMonthly2 = dfMonthly[dfMonthly.Page.isin(["YouTube"])]
    dfMonthly3 = dfMonthly[dfMonthly.Page.isin(["Donald Trump"])]
    plt.plot(dfMonthlyChatGPT["Date"], dfMonthlyChatGPT["Views"], label='ChatGPT')
    plt.plot(dfMonthly2["Date"], dfMonthly2["Views"], label='YouTube')
    plt.plot(dfMonthly3["Date"], dfMonthly3["Views"], label='Donald Trump')
    plt.legend()
    plt.show()
    print(dfMonthly)
