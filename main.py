from datetime import datetime
from glob import glob

import matplotlib.dates as md
import matplotlib.pyplot as plt
import numpy
import pandas as pd


def generate_monthly_csv():
    dfs = []
    files = glob('./dataset/monthly/*.csv')

    # Reads csvs and strips date from filename
    # Replace "?" with None in order to allow Pandas to interpret the data correctly
    for i, path in enumerate(files):
        dfs.append(pd.read_csv(path).set_index('Page'))
        dfs[i].loc[dfs[i]["Edits"] == "?", "Edits"] = "None"
        dfs[i].loc[dfs[i]["Editors"] == "?", "Editors"] = "None"
        dfs[i]["Date"] = datetime.strptime(path[len([files[0]]) - 12::].rstrip(".csv"), "%Y_%m").strftime("%Y-%m-%d")

    # Concat all dataframes and sort their data by date
    dfGen = pd.concat(dfs)
    dfGen = dfGen.sort_values("Date", ascending=False)
    # Generate output csv
    dfGen.to_csv("./dataset/out/topviews_merged.csv")


if __name__ == '__main__':
    # Regenerate source dataset, if needed
    # generate_monthly_csv()

    # Plot size which translates into resolution
    plt.rcParams[("figure.figsize")] = [15, 7.5]

    # Add query parameters here. Supports multi-article plots
    query = ["Vladimir Putin", "Russo-Ukrainian War", "Volodymyr Zelenskyy", "Ukraine"]

    # Visualization parameters
    # Log: Plots y-axis logarithmically
    # Views: Plots views
    # Editors: Plots editors
    # Edits: Plots edits
    log = True
    views = True
    editors = False
    edits = False
    # Adds and plots derivative data
    # Veq: Plots Views / Edits
    # Eed: Plots Edits - Editors
    veq = False
    eed = False

    # Reads csv and parses dates as datetime
    dfMonthly = pd.read_csv("dataset/out/topviews_merged.csv", parse_dates=["Date"]).set_index("Date").sort_values(
        "Date", ascending=True)

    dfs = []

    # Gets and appends subset dataframes which contain query data
    for param in query:
        dfs.append(dfMonthly[dfMonthly.Page.isin([param])])

    currentDf = dfs[0]

    # Pandas does not plot dataframes with differing lengths properly.
    # Iterate through all dataframes, determine the longest and add NaN rows to
    # the shorter dataframes in order to align their data in plotting
    if len(dfs) > 1:
        for df in dfs:
            if currentDf.iloc[0].name >= df.iloc[0].name:
                currentDf = df

        for i, row in currentDf.iterrows():
            for df in dfs:
                if row.name not in df.index:
                    df.loc[row.name] = numpy.NaN, numpy.NaN, numpy.NaN, numpy.NaN
                df.sort_values("Date", ascending=True, inplace=True)

    # Adds veq column and data; See Visualization parameters
    if veq:
        for df in dfs:
            df.insert(len(df.columns), "Veq", numpy.NaN)
            for i, row in df.iterrows():
                crow = df.loc[i]
                if (crow.Views != numpy.NaN) & (crow.Edits != numpy.NaN):
                    df.loc[i, "Veq"] = (crow.Views / crow.Edits)

    # Adds eed column and data; See Visualization parameters
    if eed:
        for df in dfs:
            df.insert(len(df.columns), "Eed", numpy.NaN)
            for i, row in df.iterrows():
                crow = df.loc[i]
                if (crow.Editors != numpy.NaN) & (crow.Edits != numpy.NaN):
                    df.loc[i, "Eed"] = (crow.Edits - crow.Editors)

    plt.figure()

    fig, ax = plt.subplots()

    # Set custom major and minor mark locator and formatter
    # Results in labels like "Dec 23"
    ax.xaxis.set_major_locator(md.MonthLocator(interval=2))
    ax.xaxis.set_major_formatter(md.DateFormatter("%b %y"))
    ax.xaxis.set_minor_locator(md.MonthLocator(interval=1))

    # Iterate through all dataframes and plot their data based on previous parameters
    for i, df in enumerate(dfs):
        if views:
            df["Views"].plot(ax=ax, x_compat=True, title=query[0] if len(dfs) == 1 else ' / '.join(query), x="Date",
                             label="Views (" + query[i] + ")", legend=True)
            plt.yscale("log") if log else None
            plt.ylabel("Views")

        if veq:
            df["Veq"].plot(ax=ax, x_compat=True, title=query[0] if len(dfs) == 1 else ' / '.join(query), x="Date",
                           label="V/E (" + query[i] + ")", legend=True)

        if edits:
            df["Edits"].plot(ax=ax, x_compat=True, x="Date", title=query[0] if len(dfs) == 1 else ' / '.join(query),
                             secondary_y=True, label="Edits (" + query[i] + ")", legend=True)

        if eed:
            df["Eed"].plot(ax=ax, x_compat=True, x="Date", title=query[0] if len(dfs) == 1 else ' / '.join(query),
                           secondary_y=True, label="E/E (" + query[i] + ")", legend=True)

        if editors:
            df["Editors"].plot(x="Date", x_compat=True, y="Edits", ax=ax,
                               title=query[0] if len(dfs) == 1 else ' / '.join(query),
                               secondary_y=True, label="Editors (" + query[i] + ")",
                               legend=True)

            plt.ylabel("Editors / Edits")

    # Rotate X-tick-labels
    fig.autofmt_xdate(rotation=90)

    plt.show()
