from flask import Flask, render_template, request
import pickle
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
import pandas

app = Flask(__name__)

model = pickle.load(open('model/final_model.pkl', 'rb'))
nba_players = players.get_players()

@app.route("/")
def home():
    """Returns the homepage"""
    return render_template('index.html')

@app.route("/predict", methods =['GET', 'POST'])
def predict():
    if request.method == "POST":
        player_name = request.form['player_name']
        player = [player for player in nba_players
                    if player['full_name'].lower() == player_name.lower()]
        if len(player)==0:
            return render_template('index.html')
        name = player[0]['full_name']
        id = player[0]['id']
        career = playercareerstats.PlayerCareerStats(player_id=id)
        df = career.get_data_frames()[0].drop(['PLAYER_ID', 'SEASON_ID', 'LEAGUE_ID', 'TEAM_ID', 'TEAM_ABBREVIATION', 'PLAYER_AGE', 'FG_PCT', 'FG3_PCT', 'FT_PCT'], axis=1).sum()

        input = df.to_numpy()

        proba = model.predict_proba(input.reshape(1, -1))[0][1] * 100

    return render_template('predict.html', name=name, proba=proba)
