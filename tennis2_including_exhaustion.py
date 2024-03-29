import pandas as pd
import datetime

# Rounds per draw size

EXHAUSTION_DATA_FILE = "data_with_exhaustion_groups.csv"

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


def calculate_players_exhaustion_severity(player_id, df):
    loser_player_data = df.loc[df['loser_id'].isin({player_id})]
    winner_player_data = df.loc[df['winner_id'].isin({player_id})]

    calculate_players_exhaustion_severity_helper(loser_player_data, df)
    calculate_players_exhaustion_severity_helper(winner_player_data, df)


def calculate_players_exhaustion_severity_helper(player_data, df):
    player_data = player_data.sort_values('tourney_date', ascending=False)

    for i, row_a in player_data.iterrows():
        if not (get_related_map(int(row_a['draw_size'])) is None):
            rounds_played = get_related_map(int(row_a['draw_size'])).get(row_a['round'])
            for j, row_b in player_data.iterrows():
                days_passed = (parse_date(row_a['tourney_date']) - parse_date(row_b['tourney_date'])).days
                if 0 < days_passed < 21:
                    new_exhaustion_index = (21 - days_passed) * rounds_played
                    prev_exhaustion_index = df.at[j, 'exhaustion_index']
                    t = type(df)
                    if not isinstance(df, pd.DataFrame):
                        print(t)
                    player_data.at[j, 'exhaustion_index'] = prev_exhaustion_index + new_exhaustion_index
                    df.at[j, 'exhaustion_index'] = prev_exhaustion_index + new_exhaustion_index


def analyze_data(output):
    df = pd.read_csv("data_with_exhaustion_groups.csv")
    for severity_level in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
        output.write("\n*** Exhaustion Severity Level " + severity_level + " ***\n")
        severity_level_data = df.loc[df['exhaustion_severity_group'].isin({severity_level})]

        analyze_severity_level_data(severity_level_data, output)


def get_draw_size_table(draw_size):
    if draw_size == 32:
        return ROUNDS32
    if draw_size == 64:
        return ROUNDS64
    if draw_size == 48:
        return ROUNDS48
    if draw_size == 128:
        return ROUNDS128


def analyze_severity_level_data(df, output):
    for i in range(1, 11):
        output.write("\n")
        output.write("G" + str(i) + ":\n\t")
        tourneys = {"15", "25", "60", "100", "80", "C", "P", "G"}

        lower_b = 400 + 30 * (i - 1)
        upper_b = 400 + 30 * i - 1

        losers_rank = df.loc[(df['loser_rank'].isin(range(lower_b, upper_b)))]

        winners = df.loc[(df['winner_rank'].isin(range(lower_b, upper_b)))]

        for tourney in tourneys:
            losers_in_tourney = losers_rank.loc[losers_rank['tourney_level'].isin({tourney})]
            winners_in_tourney = winners.loc[winners['tourney_level'].isin({tourney})]
            tourney_rounds_sum = 0
            tourney_rounds_count = 0
            for j in range(losers_in_tourney.shape[0]):

                rounds_for_draw_size = get_draw_size_table(int(losers_in_tourney.iloc[j]["draw_size"]))
                tourney_rounds_sum += rounds_for_draw_size.get(losers_in_tourney.iloc[j]["round"])
                tourney_rounds_count += 1

            for j in range(winners_in_tourney.shape[0]):

                rounds_for_draw_size = get_draw_size_table(int(losers_in_tourney.iloc[j]["draw_size"]))
                if winners_in_tourney.iloc[j]["round"] == "F":
                    tourney_rounds_sum += rounds_for_draw_size.get("W")
                    tourney_rounds_count += 1

            if tourney_rounds_count != 0:
                output.write(tourney + " : " + str(tourney_rounds_sum / tourney_rounds_count) + "\n\t")
            else:
                output.write(tourney + " : " + "n/a" + "\n\t")


# assuming date is string
def parse_date(date):
    date = str(date)
    year = date[0:4]
    month = date[4:6]
    day = date[6:8]

    if month[0] == 0:
        month = month[1]
    if day[0] == 0:
        day = day[1]

    return datetime.datetime(int(year), int(month), int(day))


def get_related_map(draw_size):
    if draw_size == 32:
        return ROUNDS32
    elif draw_size == 64:
        return ROUNDS64
    elif draw_size == 48:
        return ROUNDS48
    elif draw_size == 128:
        return ROUNDS128
    else:
        print("Error in draw size")


#
# A is best
# G is worst
#
def get_exhaustion_severity_group(exhaustion_index):
    if exhaustion_index <= 330:
        return 'A'
    elif 331 <= exhaustion_index <= 660:
        return 'B'
    elif 661 <= exhaustion_index <= 990:
        return 'C'
    elif 991 <= exhaustion_index <= 1320:
        return 'D'
    elif 1321 <= exhaustion_index <= 1650:
        return 'E'
    elif 1651 <= exhaustion_index <= 1980:
        return 'F'
    elif 1981 <= exhaustion_index <= 2310:
        return 'G'
    else:
        print("Error: Severity group")

# Given a file with players data prepare for data analysis by finding the players exhaustion group at a given match
def analyze_file(file_name):
    df = pd.read_csv(file_name, low_memory=False)

    df.insert(df.shape[1], "exhaustion_index", ([0]*df.shape[0]))
    df.insert(df.shape[1], 'exhaustion_severity_group', ([0] * df.shape[0]))

    output = open("output.txt", "w")
    players_ids = set(df['winner_id'])
    players_ids.union(set(df['loser_id']))

    # calculating exhaustion level
    for player_id in players_ids:
        calculate_players_exhaustion_severity(player_id, df)

    for i, row in df.iterrows():
        try:
            df.at[i, 'exhaustion_severity_group'] = get_exhaustion_severity_group(row["exhaustion_index"])
        except:
            print("exception")

    df.to_csv(EXHAUSTION_DATA_FILE)

    # analyze data
    analyze_data(output)

    output.close()



if __name__ == '__main__':
    analyze_file("wta_matches_qual_itf_2022.csv")
    output = open("output.txt", "w")
    analyze_data(output)
