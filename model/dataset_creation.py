import pandas as pd
import numpy as np

all_players = pd.read_csv("/Users/sumeetkulkarni/Desktop/lstm-nba-hof-predictor/lstm_model/data/Player Totals.csv")
all_players = all_players.sort_values(by=['player_id', 'season'])

# for index, row in all_players.copy().iterrows():
#     if row["season"] > 2018:
#         all_players = all_players[all_players["player_id"] != row["player_id"]]
zeros = [0] * len(all_players)

all_players = all_players[all_players["tm"]!="TOT"]
all_players = all_players.drop(['seas_id', 'season', 'birth_year', 'age', 'experience', 'pos', 'lg', 'fg_percent', 'x2p', 'x2pa', 'x3p_percent', 'x2p_percent', 'e_fg_percent', 'ft_percent'], axis=1).fillna(0)
all_players = all_players.groupby(['player_id', 'player'], as_index=False).sum()

all_players["HOFer"] = [0] * len(all_players)

hof_stats = pd.read_csv("/Users/sumeetkulkarni/Desktop/lstm-nba-hof-predictor/lstm_model/data/NBA Hall of Famers 2021.csv")

for index, row in hof_stats.iterrows():
    if row["In_Hall_of_fame"] == 1:
        all_players.loc[all_players["player"]==row["Name"], "HOFer"] = 1

all_players.to_csv("nba_stats_dataset_all_players.csv")
