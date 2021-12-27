import nba_lib.team_stats as t
import constants.nba_teams as teams
import service.game_handler as gh
import database.dk_totals_table as dk_totals_t


def get_total(games):
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


def tomorrow_over_under():
    get_total(gh.get_games_tomorrow())


def analyze_bet(game):
    predicted_total = game["total"]
    total_line = dk_totals_t.get_total_by_team_ids(game['visitor_team_id'], game['home_team_id'])
    if total_line:
        matchup = "{} @ {}".format(total_line.visitor, total_line.home)

        if predicted_total > total_line.over_line:
            comparison = "{}/{}".format(predicted_total, total_line.over_line)
            bet = "OVER"
            odds = total_line.over_odds
            return matchup, comparison, bet, odds
            # print(f'{predicted_total}/{total_line.over_line} ---------- TAKE OVER @ {total_line.over_odds}')

        elif predicted_total < total_line.under_line:
            comparison = "{}/{}".format(predicted_total, total_line.under_line)
            bet = "UNDER"
            odds = total_line.under_odds
            return matchup, comparison, bet, odds
            # print(f'{predicted_total}/{total_line.under_line} ---------- TAKE UNDER @ {total_line.under_odds}')


def over_under():
    dk_totals_t.import_data()
    games = get_total(gh.get_games_today())

    bets = []
    for game in games:
        bet = analyze_bet(game)
        if bet:
            bets.append(bet)
    return bets


if __name__ == '__main__':
    print("")
