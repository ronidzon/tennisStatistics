# This is a sample Python script.
import pandas as pd
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # df = pd.read_csv('wta_matches_2019.csv')
    # winnerRank = df.loc[df['winner_rank'].isin(range(400,701))]
    # loserRank = df.loc[df['loser_rank'].isin(range(400, 701))]
    # result = pd.concat([winnerRank, loserRank])
    # # print(df.head(1000).to_string())
    # print(result.to_string())

    df = pd.read_csv('wta_matches_qual_itf_2022.csv', low_memory=False)

    # winnerRank = df.loc[df['winner_rank'].isin(range(400,701))]
    # loserRank = df.loc[df['loser_rank'].isin(range(400, 701))]
    # result = pd.concat([winnerRank, loserRank])

    print(df.head(100).to_string())
    # print(result.to_string())
    # print(df["tourney_level"].unique())











# See PyCharm help at https://www.jetbrains.com/help/pycharm/
