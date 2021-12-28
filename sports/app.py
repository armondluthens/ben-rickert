from flask import Flask
import service.over_under as ou
import statistics
import json


# Flask constructor takes the name of current module (__name__) as argument.
app = Flask(__name__)


@app.route('/sports/bets/spread')
def get_spread():
    return {"result": None}


@app.route('/sports/bets/over-under')
def get_over_under():
    results = ou.over_under()

    if not results:
        return {}

    json_result_list = []
    for result in results:
        visitor = result[8]
        home = result[9]

        visitor_score = round((visitor[10] + visitor[8] + home[9] + visitor[7])/4)
        home_score = round((home[10] + home[8] + visitor[9] + home[7])/4)
        predicted_score = str(visitor_score) + " - " + str(home_score)
        predicted_total = round(visitor_score + home_score)

        # game = {
        #     "prediction": {
        #         "matchup": result[0],
        #         "line": result[2],
        #         "visitor_score": visitor_score,
        #         "home_score": home_score,
        #         "predicted_score": predicted_score,
        #         "predicted_total": predicted_total,
        #         "odds": result[4],
        #         "bet": "OVER" if predicted_total > result[2] else "UNDER"
        #     },
        #     "matchup": result[0],
        #     "predicted": result[1],
        #     "line": result[2],
        #     "bet": result[3],
        #     "odds": result[4],
        #     "payout": {
        #         "20": result[5],
        #         "50": result[6],
        #         "100": result[7]
        #     },
        #     "visitor": {
        #         "team": visitor[2],
        #         "avg_5_game": visitor[3],
        #         "avg_10_game": visitor[4],
        #         "avg_15_game": visitor[5],
        #         "avg_20_game": visitor[6],
        #         "pace": visitor[7],
        #         "offensive_rating": visitor[8],
        #         "defensive_rating": visitor[9],
        #         "avg_points": visitor[10]
        #     },
        #     "home": {
        #         "team": home[2],
        #         "avg_5_game": home[3],
        #         "avg_10_game": home[4],
        #         "avg_15_game": home[5],
        #         "avg_20_game": home[6],
        #         "pace": home[7],
        #         "offensive_rating": home[8],
        #         "defensive_rating": home[9],
        #         "avg_points": home[10]
        #     }
        # }
        game = {
            "prediction": {
                "matchup": result[0],
                "line": result[2],
                "visitor_score": visitor_score,
                "home_score": home_score,
                "predicted_score": predicted_score,
                "predicted_total": predicted_total,
                "odds": result[4],
                "bet": "OVER" if predicted_total > result[2] else "UNDER"
            }
        }
        json_result_list.append(game)

    return {"result": json_result_list}


@app.route('/sports/bets/moneyline')
def get_moneyline():
    return {"result": None}


@app.route('/sports/bets')
def bets():
    return {
        "over_under": get_over_under(),
        "spread": get_spread(),
        "moneyline": get_moneyline()
    }


if __name__ == '__main__':
    app.run()
