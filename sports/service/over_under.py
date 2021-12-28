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


# def analyze_bet(game):
#     predicted_total = game["total"]
#     total_line = dk_totals_t.get_total_by_team_ids(game['visitor_team_id'], game['home_team_id'])
#     if total_line:
#         matchup = "{} @ {}".format(total_line.visitor, total_line.home)
#         line = total_line.over_line if predicted_total > total_line.over_line else total_line.under_line
#         odds = total_line.over_odds if predicted_total > total_line.over_line else total_line.under_odds
#         bet = OVER if predicted_total > total_line.over_line else UNDER
#
#         return matchup, predicted_total, line, bet, odds, bs.get_payout(odds, 20), \
#                bs.get_payout(odds, 50), bs.get_payout(odds, 100)

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

        return matchup, predicted_total, line, bet, odds, bs.get_payout(odds, 20), \
               bs.get_payout(odds, 50), bs.get_payout(odds, 100), visitor, home


# def over_under2():
#     results = []
#     # Get the games for today
#     # Get the lines from DraftKings
#     dk_totals_t.import_lines()
#
#     games = get_total(gh.get_games(0))
#
#     if games:
#         for game in games:
#             bet = analyze_bet(game)
#             if bet:
#                 results.append(bet)
#         return results


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


if __name__ == '__main__':
    over_under()
