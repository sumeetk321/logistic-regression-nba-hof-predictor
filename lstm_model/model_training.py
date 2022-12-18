import pandas as pd
import numpy as np

all_players = pd.read_csv("/Users/sumeetkulkarni/Desktop/lstm-nba-hof-predictor/lstm_model/data/Player Per Game.csv")
all_players = all_players.sort_values(by=['player_id', 'season'])
all_players = all_players.drop(['seas_id', 'birth_year', 'age', 'experience', 'lg', 'gs'], axis=1).fillna(0)
advanced_stats = pd.read_csv("/Users/sumeetkulkarni/Desktop/lstm-nba-hof-predictor/lstm_model/data/Advanced.csv")
advanced_stats = advanced_stats.sort_values(by=['player_id', 'season']).fillna(0)
all_players[["ows","dws","ws","ws_48","obpm","dbpm","bpm","vorp", "per","ts_percent"]] = advanced_stats[["ows","dws","ws","ws_48","obpm","dbpm","bpm","vorp", "per","ts_percent"]]

#print(all_players)
zeros = [0] * 30933


all_players["all_star"] = zeros
all_players["roy"] = zeros
all_players["smoy"] = zeros
all_players["dpoy"] = zeros
all_players["mip"] = zeros
all_players["mvp"] = zeros
all_players["All-League"] = zeros
all_players["All-Defense"] = zeros
all_players["All-Rookie"] = zeros
all_players["Champion"] = zeros
all_players["Finals MVP"] = zeros

all_star_df = pd.read_csv("/Users/sumeetkulkarni/Desktop/lstm-nba-hof-predictor/lstm_model/data/All-Star Selections.csv")

for index, row in all_star_df.iterrows():
    name = row["player"]
    season = row["season"]
    all_players.loc[(all_players["player"]==name) & (all_players["season"]==season), "all_star"] = 1

award_shares_df = pd.read_csv("/Users/sumeetkulkarni/Desktop/lstm-nba-hof-predictor/lstm_model/data/Player Award Shares.csv")

for index, row in award_shares_df.iterrows():
    if row["winner"]:
        name = row["player"]
        award = row["award"]
        season = row["season"]
        if award == "nba mvp" or award == "aba mvp":
            award = "mvp"
        elif award == "nba roy" or award == "aba roy":
            award = "roy"
        all_players.loc[(all_players["player"]==name) & (all_players["season"]==season), award] = 1


eos_teams_df = pd.read_csv("/Users/sumeetkulkarni/Desktop/lstm-nba-hof-predictor/lstm_model/data/End of Season Teams.csv")

for index, row in eos_teams_df.iterrows():
    season = row["season"]
    name = row["player"]
    team = row["type"]
    if team == "All-NBA" or team == "All-ABA" or team == "All-BAA":
        team = "All-League"
    num = row["number_tm"][0]
    all_players.loc[(all_players["player"]==name) & (all_players["season"]==season), team] = num

finals_df = pd.read_csv("/Users/sumeetkulkarni/Desktop/lstm-nba-hof-predictor/lstm_model/data/Finals MVPs.csv")

for index, row in finals_df.iterrows():
    season = int(row["Season"][:4])+1
    name = row["Player"]
    team = row["Tm"]
    #print(season, name, team)
    all_players.loc[(all_players["player"]==name) & (all_players["season"]==season), "Finals MVP"] = 1
    all_players.loc[(all_players["tm"]==team) & (all_players["season"]==season), "Champion"] = 1

print(all_players.loc[(all_players["player"]=="Giannis Antetokounmpo")])

hof_stats = pd.read_csv("/Users/sumeetkulkarni/Desktop/lstm-nba-hof-predictor/lstm_model/data/NBA Hall of Famers 2021.csv")

hof_actual = np.zeros(shape=(5094,))

for i in range(5094):
    id = i+1
    name = all_players.loc[all_players["player_id"]==id]["player"].iloc[0]
    if not hof_stats.loc[hof_stats["Name"] == name]["In_Hall_of_fame"].empty and hof_stats.loc[hof_stats["Name"] == name]["In_Hall_of_fame"].iloc[0]==1:
        hof_actual[i] = 1
