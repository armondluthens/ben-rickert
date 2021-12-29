import nba_lib.team_stats as t
import constants.nba_teams as teams
import service.game_handler as gh
import database.dk_totals_table as dk_totals_t
import service.bets_service as bs
from database import team_stats_table

OVER = "O"
UNDER = "U"


def get_total(games):
    if not games:
        return
    game_totals = []
    for game in games:
        visiting_team = game[0]
        visiting_team_id = teams.get_team_id(visiting_team)
        home_team = game[1]
        home_team_id = teams.get_team_id(home_team)
        total = t.get_predicted_point_total(visiting_team_id, home_team_id)
        game_total = {
            "home_team_id": home_team_id,
            "visitor_team_id": visiting_team_id,
            "total": round(total)
        }
        game_totals.append(game_total)
    return game_totals


def analyze_bet(game):
    visitor = team_stats_table.get_team_by_team_id(game[0])
    home = team_stats_table.get_team_by_team_id(game[1])

    predicted_total = visitor[10] + home[10]

    total_line = dk_totals_t.get_total_by_team_ids(game[0], game[1])
    if total_line:
        matchup = "{} @ {}".format(total_line.visitor, total_line.home)
        line = total_line.over_line if predicted_total > total_line.over_line else total_line.under_line
        odds = total_line.over_odds if predicted_total > total_line.over_line else total_line.under_odds
        bet = OVER if predicted_total > total_line.over_line else UNDER

        result = (matchup, predicted_total, line, bet, odds, bs.get_payout(odds, 20), bs.get_payout(odds, 50),
                  bs.get_payout(odds, 100), visitor, home)

        return result


def over_under():
    results = []
    # Get the games for today
    games = gh.get_games_today()
    # Get the lines from DraftKings
    dk_totals_t.import_lines()

    if games:
        for game in games:
            bet = analyze_bet(game)
            if bet:
                results.append(bet)
        return results


def build_thick_response(results):
    result_list = []
    for result in results:
        visitor = result[8]
        home = result[9]

        visitor_score = round((visitor[10] + visitor[8] + home[9] + visitor[7]) / 4)
        home_score = round((home[10] + home[8] + visitor[9] + home[7]) / 4)
        predicted_score = str(visitor_score) + " - " + str(home_score)
        predicted_total = round(visitor_score + home_score)

        game = {
            "matchup": result[0],
            "bet": "OVER" if predicted_total > result[2] else "UNDER",
            "line": result[2],
            "predicted_total": predicted_total,
            "predicted_score": predicted_score,
            "visitor_score": visitor_score,
            "home_score": home_score,
            "odds": result[4],
            "payout": {
                "$20": result[5],
                "$50": result[6],
                "$100": result[7]
            },
            "visitor": {
                "team": visitor[2],
                "avg_5_game": visitor[3],
                "avg_10_game": visitor[4],
                "avg_15_game": visitor[5],
                "avg_20_game": visitor[6],
                "pace": visitor[7],
                "offensive_rating": visitor[8],
                "defensive_rating": visitor[9],
                "avg_points": visitor[10]
            },
            "home": {
                "team": home[2],
                "avg_5_game": home[3],
                "avg_10_game": home[4],
                "avg_15_game": home[5],
                "avg_20_game": home[6],
                "pace": home[7],
                "offensive_rating": home[8],
                "defensive_rating": home[9],
                "avg_points": home[10]
            }
        }
        result_list.append(game)

    return result_list


def build_response(results):
    result_list = []
    for result in results:
        visitor = result[8]
        home = result[9]

        visitor_score = round((visitor[10] + visitor[8] + home[9] + visitor[7]) / 4)
        home_score = round((home[10] + home[8] + visitor[9] + home[7]) / 4)
        predicted_score = str(visitor_score) + " - " + str(home_score)
        predicted_total = round(visitor_score + home_score)

        game = {
            "prediction": {
                "matchup": result[0],
                "line": result[2],
                "predicted_total": predicted_total,
                "bet": "OVER" if predicted_total > result[2] else "UNDER",
                "visitor_score": visitor_score,
                "home_score": home_score,
                "predicted_score": predicted_score,
                "odds": result[4]
            }
        }
        result_list.append(game)

    return result_list


def get_over_under(is_thick: bool):
    results = over_under()

    if not results:
        return {}
    if is_thick:
        return build_thick_response(results)
    return build_response(results)


if __name__ == '__main__':
    over_under()
