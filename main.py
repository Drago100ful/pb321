from datetime import datetime
from glob import glob

import matplotlib.dates as md
import matplotlib.pyplot as plt
import numpy
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

    query = ["Oppenheimer (film)"]
    log = True
    views = True
    editors = True
    edits = True

    dfMonthly = pd.read_csv("dataset/out/topviews_merged.csv", parse_dates=["Date"]).set_index("Date").sort_values("Date", ascending=True)

    dfs = []

    for param in query:
        dfs.append(dfMonthly[dfMonthly.Page.isin([param])])

    currentDf = dfs[0]

    for df in dfs:
        if currentDf.iloc[0].name >= df.iloc[0].name:
            currentDf = df

    for i, row in currentDf.iterrows():
        for df in dfs:
            if row.name not in df.index:
                df.loc[row.name] = numpy.NaN, numpy.NaN, numpy.NaN, numpy.NaN
            df.sort_values("Date", ascending=True, inplace=True)

    plt.figure()

    fig, ax = plt.subplots()

    ax.xaxis.set_major_locator(md.MonthLocator(interval=2))
    ax.xaxis.set_minor_locator(md.MonthLocator(interval=1))
    ax.xaxis.set_major_formatter(md.DateFormatter("%b %y"))

    for i, df in enumerate(dfs):
        if views:
            df["Views"].plot(ax=ax, title=query[0] if len(dfs) == 1 else ' / '.join(query), x="Date",
                             label="Views (" + query[i] + ")", legend=True)
            plt.yscale("log") if log else None
            plt.ylabel("Views")

        if edits:
            df["Edits"].plot(ax=ax, x="Date", title=query[0] if len(dfs) == 1 else ' / '.join(query),
                               secondary_y=True, label="Edits (" + query[i] + ")", legend=True)

        if editors:
            df["Editors"].plot(x="Date", y="Edits", ax=ax, title=query[0] if len(dfs) == 1 else ' / '.join(query),
                             secondary_y=True, label="Editors (" + query[i] + ")",
                             legend=True)

            plt.ylabel("Editors / Edits")

    fig.autofmt_xdate(rotation=90)

    plt.show()
