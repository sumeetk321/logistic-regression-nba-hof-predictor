import pandas as pd
import numpy as np

all_players = pd.read_csv("/Users/sumeetkulkarni/Desktop/lstm-nba-hof-predictor/lstm_model/data/Player Totals.csv")
all_players = all_players.sort_values(by=['player_id', 'season'])

# for index, row in all_players.copy().iterrows():
#     if row["season"] > 2018:
#         all_players = all_players[all_players["player_id"] != row["player_id"]]
zeros = [0] * len(all_players)


all_players["all_star"] = zeros
all_players["roy"] = zeros
all_players["smoy"] = zeros
all_players["dpoy"] = zeros
all_players["mip"] = zeros
all_players["mvp"] = zeros
all_players["All-League"] = zeros
all_players["All-Defense"] = zeros
all_players["All-Rookie"] = zeros
all_players["Finals MVP"] = zeros
all_players["Champion"] = zeros
all_players["HOFer"] = zeros

finals_df = pd.read_csv("/Users/sumeetkulkarni/Desktop/lstm-nba-hof-predictor/lstm_model/data/Finals MVPs.csv")

for index, row in finals_df.iterrows():
    name = row["Player"]
    team = row["Tm"]
    season = int(row["Season"][:4])+1
    all_players.loc[(all_players["tm"]==team) & (all_players["season"]==season), "Champion"] = 1

all_players = all_players.drop(['seas_id', 'season', 'mp', 'g', 'birth_year', 'age', 'experience', 'pos', 'lg', 'gs', 'fg_percent', 'x3p_percent', 'x2p_percent', 'e_fg_percent', 'ft_percent'], axis=1).fillna(0)
all_players = all_players.groupby(['player_id', 'player'], as_index=False).sum()

all_star_df = pd.read_csv("/Users/sumeetkulkarni/Desktop/lstm-nba-hof-predictor/lstm_model/data/All-Star Selections.csv")

for index, row in all_star_df.iterrows():
    name = row["player"]
    all_players.loc[all_players["player"]==name, "all_star"] +=1


award_shares_df = pd.read_csv("/Users/sumeetkulkarni/Desktop/lstm-nba-hof-predictor/lstm_model/data/Player Award Shares.csv")

for index, row in award_shares_df.iterrows():
    if row["winner"]:
        name = row["player"]
        award = row["award"]
        if award == "nba mvp" or award == "aba mvp":
            award = "mvp"
        elif award == "nba roy" or award == "aba roy":
            award = "roy"
        all_players.loc[(all_players["player"]==name), award] += 1


eos_teams_df = pd.read_csv("/Users/sumeetkulkarni/Desktop/lstm-nba-hof-predictor/lstm_model/data/End of Season Teams.csv")

for index, row in eos_teams_df.iterrows():
    name = row["player"]
    team = row["type"]
    if team == "All-NBA" or team == "All-ABA" or team == "All-BAA":
        team = "All-League"
    num = row["number_tm"][0]
    if num=="1":
        all_players.loc[(all_players["player"]==name), team] += 5
    elif num=="2":
        all_players.loc[(all_players["player"]==name), team] += 3
    elif num=="3":
        all_players.loc[(all_players["player"]==name), team] += 1


finals_df = pd.read_csv("/Users/sumeetkulkarni/Desktop/lstm-nba-hof-predictor/lstm_model/data/Finals MVPs.csv")

for index, row in finals_df.iterrows():
    name = row["Player"]
    team = row["Tm"]
    all_players.loc[(all_players["player"]==name), "Finals MVP"] += 1

hof_stats = pd.read_csv("/Users/sumeetkulkarni/Desktop/lstm-nba-hof-predictor/lstm_model/data/NBA Hall of Famers 2021.csv")

for index, row in hof_stats.iterrows():
    if row["In_Hall_of_fame"] == 1:
        all_players.loc[all_players["player"]==row["Name"], "HOFer"] = 1
all_players.to_csv("nba_stats_dataset_all_players.csv")