import pandas as pd

############################################################################
#
# The following code calculates and outputs for each group of players,
# given a tournament type and a draw size,
# the round in which the player will probably lose.
#
# Players are devided to groups based on their rank as follows:
#
#   G1: 400-429
#   G2: 430-459
#   G3: 460-489
#   G4: 490-519
#   G5: 520-549
#   G6: 550-579
#   G7: 580-609
#   G8: 610-639
#   G9: 640-669
#   G10: 670-699
#
###########################################################################

ROUNDS32 = {
    "Q1": 1,
    "Q2": 2,
    "Q3": 3,
    "R32": 4,
    "R16": 5,
    "QF": 6,
    "SF": 7,
    "F": 8,
    "W": 9
}

ROUNDS64 = {
    "Q1": 1,
    "Q2": 2,
    "Q3": 3,
    "R64": 4,
    "R32": 5,
    "R16": 6,
    "QF": 7,
    "SF": 8,
    "F": 9,
    "W": 10
}

ROUNDS48 = {
    "Q1": 1,
    "Q2": 2,
    "Q3": 3,
    "R64": 4,
    "R32": 5,
    "R16": 6,
    "QF": 7,
    "SF": 8,
    "F": 9,
    "W": 10
}

ROUNDS128 = {
    "Q1": 1,
    "Q2": 2,
    "Q3": 3,
    "R128": 4,
    "R64": 5,
    "R32": 6,
    "R16": 7,
    "QF": 8,
    "SF": 9,
    "F": 10,
    "W": 11
}


def analyze_file(file_name):
    df = pd.read_csv(file_name, low_memory=False)
    output = open("output1.txt", "w")

    for i in range(1, 11):
        output.write("\n")
        output.write("G" + str(i) + ":\n\t")
        tourneys = {"15", "25", "60", "100", "80", "C", "P", "G"}

        lower_b = 400 + 30 * (i - 1)
        upper_b = 400 + 30 * i - 1

        losers = df.loc[df['loser_rank'].isin(range(lower_b, upper_b))]
        winners = df.loc[df['winner_rank'].isin(range(lower_b, upper_b))]

        for tourney in tourneys:
            losers_in_tourney = losers.loc[losers['tourney_level'].isin({tourney})]
            winners_in_tourney = winners.loc[winners['tourney_level'].isin({tourney})]
            tourney_rounds_sum = 0
            tourney_rounds_count = 0
            for j in range(losers_in_tourney.shape[0]):
                if int(losers_in_tourney.iloc[j]["draw_size"]) == 32:
                    tourney_rounds_sum += ROUNDS32.get(losers_in_tourney.iloc[j]["round"])
                    tourney_rounds_count += 1
                elif int(losers_in_tourney.iloc[j]["draw_size"]) == 64:
                    tourney_rounds_sum += ROUNDS64.get(losers_in_tourney.iloc[j]["round"])
                    tourney_rounds_count += 1
                elif int(losers_in_tourney.iloc[j]["draw_size"]) == 48:
                    tourney_rounds_sum += ROUNDS48.get(losers_in_tourney.iloc[j]["round"])
                    tourney_rounds_count += 1
                elif int(losers_in_tourney.iloc[j]["draw_size"]) == 128:
                    tourney_rounds_sum += ROUNDS128.get(losers_in_tourney.iloc[j]["round"])
                    tourney_rounds_count += 1

            for j in range(winners_in_tourney.shape[0]):
                if int(winners_in_tourney.iloc[j]["draw_size"]) == 32 and winners_in_tourney.iloc[j]["round"] == "F":
                    tourney_rounds_sum += ROUNDS32.get("W")
                    tourney_rounds_count += 1
                if int(winners_in_tourney.iloc[j]["draw_size"]) == 64 and winners_in_tourney.iloc[j]["round"] == "F":
                    tourney_rounds_sum += ROUNDS64.get("W")
                    tourney_rounds_count += 1
                if int(winners_in_tourney.iloc[j]["draw_size"]) == 48 and winners_in_tourney.iloc[j]["round"] == "F":
                    tourney_rounds_sum += ROUNDS48.get("W")
                    tourney_rounds_count += 1
                if int(winners_in_tourney.iloc[j]["draw_size"]) == 128 and winners_in_tourney.iloc[j]["round"] == "F":
                    tourney_rounds_sum += ROUNDS128.get("W")
                    tourney_rounds_count += 1

            print("tourney_rounds_sum: ", tourney_rounds_sum)
            print("tourney_rounds_count", tourney_rounds_count)
            if tourney_rounds_count != 0:
                output.write(tourney + " : " + str(tourney_rounds_sum / tourney_rounds_count) + "\n\t")
                print("zero")
            else:
                output.write(tourney + " : " + "n/a" + "\n\t")

    output.close()


if __name__ == '__main__':
    analyze_file("wta_matches_qual_itf_2022.csv")
