import pandas as pd
if __name__ == '__main__':
    dfs = []

    df = pd.read_csv('dataset/monthly/topviews-2023_10.csv')
    df = df.head(200)
    df = df.set_index("Page")
    df["Date"] = "October 2023"
    dfs.append(df)

    df2 = pd.read_csv("dataset/monthly/topviews-2023_09.csv")
    df2 = df2.head(200)
    df2 = df2.set_index("Page")
    df2["Date"] = "September 2023"
    dfs.append(df2)

    df3 = pd.read_csv("dataset/monthly/topviews-2023_08.csv")
    df3 = df3.head(200)
    df3 = df3.set_index("Page")
    df3["Date"] = "August 2023"
    dfs.append(df3)

    df4 = pd.read_csv("dataset/monthly/topviews-2023_07.csv")
    df4 = df4.head(200)
    df4 = df4.set_index("Page")
    df4["Date"] = "July 2023"
    dfs.append(df4)

    df5 = pd.read_csv("dataset/monthly/topviews-2023_06.csv")
    df5 = df5.head(200)
    df5 = df5.set_index("Page")
    df5["Date"] = "June 2023"
    dfs.append(df5)

    df6 = pd.read_csv("dataset/monthly/topviews-2023_05.csv")
    df6 = df6.head(200)
    df6 = df6.set_index("Page")
    df6["Date"] = "May 2023"
    dfs.append(df6)

    df7 = pd.read_csv("dataset/monthly/topviews-2023_04.csv")
    df7 = df7.head(200)
    df7 = df7.set_index("Page")
    df7["Date"] = "April 2023"
    dfs.append(df7)

    df8 = pd.read_csv("dataset/monthly/topviews-2023_03.csv")
    df8 = df8.head(200)
    df8 = df8.set_index("Page")
    df8["Date"] = "March 2023"
    dfs.append(df8)

    df9 = pd.read_csv("dataset/monthly/topviews-2023_02.csv")
    df9 = df9.head(200)
    df9 = df9.set_index("Page")
    df9["Date"] = "February 2023"
    dfs.append(df9)

    df10 = pd.read_csv("dataset/monthly/topviews-2023_01.csv")
    df10 = df10.head(200)
    df10 = df10.set_index("Page")
    df10["Date"] = "January 2023"
    dfs.append(df10)

    dfBig = pd.concat(dfs)
    dfBig = dfBig.sort_values("Views", ascending=False)
    dfBig.to_csv('./dataset/monthly/monthly_merged.csv')
    print(dfBig)