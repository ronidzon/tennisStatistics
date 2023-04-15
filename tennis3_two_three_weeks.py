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

def get_draw_size_table(draw_size):
    if draw_size == 32:
        return ROUNDS32
    if draw_size == 64:
        return ROUNDS64
    if draw_size == 48:
        return ROUNDS48
    if draw_size == 128:
        return ROUNDS128

def two_week_strike(players_in_tourney_data, date, player_id):
    for game_index in range(players_in_tourney_data.shape[0]-1):
        # check player didn't play the week before
        if date - players_in_tourney_data.iloc[game_index]['tourney_date'] > 7:
            if players_in_tourney_data.iloc[game_index]['loser_id'] == player_id or players_in_tourney_data.iloc[game_index]['winner_id'] == player_id:
        if 0 < date - players_in_tourney_data.iloc[game_index]['tourney_date'] <= 7:
            if players_in_tourney_data.iloc[game_index]['loser_id'] == player_id or players_in_tourney_data.iloc[game_index]['winner_id'] == player_id:
                # player played a week ago
                return False
        for next_game_index in range(game_index + 1, players_in_tourney_data.shape[0]):
            if 0 < players_in_tourney_data.iloc[next_game_index]['tourney_date'] - date <= 7:
                if players_in_tourney_data.iloc[next_game_index]['loser_id'] == player_id or players_in_tourney_data.iloc[game_index]['winner_id'] == player_id:
                    # two weeks strike
                    return True

    return False


def three_week_strike(players_in_tourney_data, date, player_id):
    for game_index in range(players_in_tourney_data.shape[0]):
        if 7 < players_in_tourney_data.iloc[game_index]['tourney_date'] - date <= 14:
            if players_in_tourney_data.iloc[game_index]['loser_id'] == player_id or players_in_tourney_data.iloc[game_index]['winner_id'] == player_id:
                return True
        if players_in_tourney_data.iloc[game_index]['tourney_date'] - date > 14:
            return False
    return False


def calculate_sum_and_count(player_in_tourney_data, index, tourney_rounds_sum, tourney_rounds_count):
    if index > player_in_tourney_data.shape[0]:
        return tourney_rounds_sum, tourney_rounds_count
    rounds_for_draw_size = get_draw_size_table(int(player_in_tourney_data.iloc[index]["draw_size"]))
    if player_in_tourney_data.iloc[index]["round"] == "F":
        tourney_rounds_sum += rounds_for_draw_size.get("W")
    else:
        tourney_rounds_sum += rounds_for_draw_size.get(player_in_tourney_data.iloc[index]["round"])
    tourney_rounds_count += 1
    return tourney_rounds_sum, tourney_rounds_count


def print_conclusion(avg_2_weeks, avg_3_weeks, output):
    if (avg_2_weeks * 17.33) > (avg_3_weeks * 13):
        output.write("Better to play 2 weeks at a time\n\n\t")
    if (avg_2_weeks * 17.33) < (avg_3_weeks * 13):
        output.write("Better to play 3 weeks at a time\n\n\t")


def analyze_file(file_name1, file_name2, file_name3):
    df1 = pd.read_csv(file_name1, low_memory=False)
    df2 = pd.read_csv(file_name2, low_memory=False)
    df3 = pd.read_csv(file_name3, low_memory=False)
    df = pd.concat([df1, df2, df3])
    output = open("output3.txt", "w")

    for players_group_index in range(1, 11):
        output.write("\n")
        output.write("G" + str(players_group_index) + ":\n\t")
        tourneys = {15, 25, 60, 100, 80, "C", "P", "G", "W"}

        lower_b = 400 + 30 * (players_group_index - 1)
        upper_b = 400 + 30 * players_group_index - 1

        losers = df.loc[df['loser_rank'].isin(range(lower_b, upper_b))]
        winners = df.loc[df['winner_rank'].isin(range(lower_b, upper_b))]

        losers_and_winners = pd.concat([losers, winners])
        losers_and_winners.sort_values('tourney_date')

        players = pd.unique(losers_and_winners[['loser_id', 'winner_id']].values.ravel())

        for tourney in tourneys:

            tourney_losers_and_winners = losers_and_winners.loc[losers_and_winners['tourney_level'].isin({tourney})]
            tourney_losers_and_winners.sort_values('tourney_date')

            tourney_rounds_sum_2_weeks = 0
            tourney_rounds_count_2_weeks = 0
            tourney_rounds_sum_3_weeks = 0
            tourney_rounds_count_3_weeks = 0

            for j in range(tourney_losers_and_winners.shape[0] - 1):
                if two_week_strike(tourney_losers_and_winners, date=tourney_losers_and_winners.iloc[j]['tourney_date'], player_id=tourney_losers_and_winners.iloc[j]['loser_id']):
                    tourney_rounds_sum_2_weeks, tourney_rounds_count_2_weeks = calculate_sum_and_count(
                        tourney_losers_and_winners, j, tourney_rounds_sum_2_weeks, tourney_rounds_count_2_weeks)
                    if j + 1 < tourney_losers_and_winners.shape[0]:
                        tourney_rounds_sum_2_weeks, tourney_rounds_count_2_weeks = calculate_sum_and_count(
                            tourney_losers_and_winners, j+1, tourney_rounds_sum_2_weeks, tourney_rounds_count_2_weeks)

                    if three_week_strike(tourney_losers_and_winners, date=tourney_losers_and_winners.iloc[j]['tourney_date'], player_id=tourney_losers_and_winners.iloc[j]['loser_id']):
                        tourney_rounds_sum_3_weeks += tourney_rounds_sum_2_weeks
                        tourney_rounds_count_3_weeks += tourney_rounds_count_2_weeks
                        if j + 2 < tourney_losers_and_winners.shape[0]:
                            tourney_rounds_sum_3_weeks, tourney_rounds_count_3_weeks = calculate_sum_and_count(
                                tourney_losers_and_winners, j+2, tourney_rounds_sum_3_weeks, tourney_rounds_count_3_weeks)


            print("tourney_rounds_sum_2_weeks: ", tourney_rounds_sum_2_weeks)
            print("tourney_rounds_count_2_weeks", tourney_rounds_count_2_weeks)
            print("tourney_rounds_sum_3_weeks: ", tourney_rounds_sum_3_weeks)
            print("tourney_rounds_count_3_weeks", tourney_rounds_count_3_weeks)

            if tourney_rounds_sum_2_weeks != 0:
                avg_2_weeks = tourney_rounds_sum_2_weeks / tourney_rounds_count_2_weeks
                output.write(str(tourney) + " - [2 weeks] : " + str(avg_2_weeks) + "\n\t")
            else:
                output.write(str(tourney) + " : " + "n/a" + "\n\t")

            if tourney_rounds_sum_3_weeks != 0:
                avg_3_weeks = tourney_rounds_sum_3_weeks / tourney_rounds_count_3_weeks
                output.write(str(tourney) + " - [3 weeks] : " + str(avg_3_weeks) + "\n\t")
            else:
                output.write(str(tourney) + " : " + "n/a" + "\n\t")

            if tourney_rounds_sum_2_weeks > 0 and tourney_rounds_sum_3_weeks > 0:
                print_conclusion(avg_2_weeks, avg_3_weeks, output)

    output.close()




if __name__ == '__main__':
    analyze_file("wta_matches_qual_itf_2021.csv", "wta_matches_qual_itf_2022.csv", "wta_matches_qual_itf_2023.csv")
