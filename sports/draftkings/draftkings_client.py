import requests
import database.nba_teams_table as nba_teams_t


DK_NBA_API = "https://sportsbook-us-nj.draftkings.com//sites/US-NJ-SB/api/v4/eventgroups/88670846?format=json"


def draftkings_api():
    dk_api_result = requests.get(DK_NBA_API).json().get("eventGroup") \
        .get("offerCategories")[0] \
        .get("offerSubcategoryDescriptors")[0] \
        .get("offerSubcategory") \
        .get("offers")
    return dk_api_result


def get_spread(game):
    spread = game[0]
    if spread["isOpen"]:
        spread_outcomes = spread["outcomes"]
        visitor_spread = spread_outcomes[0]
        home_spread = spread_outcomes[1]
        spread_result = {
            "visitor": {
                "team": visitor_spread["label"],
                "odds": int(visitor_spread["oddsAmerican"]),
                "line": visitor_spread["line"]
            },
            "home": {
                "team": home_spread["label"],
                "odds": int(home_spread["oddsAmerican"]),
                "line": home_spread["line"]
            }

        }
        return spread_result


def get_total(game):
    total = game[1]
    if total["isOpen"]:
        total_outcomes = total["outcomes"]
        over = total_outcomes[0]
        under = total_outcomes[1]
        total_result = {
            "over": {
                "odds": int(over["oddsAmerican"]),
                "line": over["line"]
            },
            "under": {
                "odds": int(under["oddsAmerican"]),
                "line": under["line"]
            }

        }
        return total_result


def get_money_line(game):
    money_line = game[2]
    if money_line["isOpen"]:
        money_line_outcomes = money_line["outcomes"]
        visitor_money_line = money_line_outcomes[0]
        home_money_line = money_line_outcomes[1]

        money_line_result = {
            "visitor": {
                "team": visitor_money_line["label"],
                "odds": visitor_money_line["oddsAmerican"]
            },
            "home": {
                "team": home_money_line["label"],
                "odds": home_money_line["oddsAmerican"]
            }
        }
        return money_line_result


def get_game_id(game):
    return int(game[0]["providerEventId"])


def get_visitor_team_id(game):
    spread = game[0]
    if spread["isOpen"]:
        spread_outcomes = spread["outcomes"]
        visitor_spread = spread_outcomes[0]
        team_name = visitor_spread["label"]
        team = nba_teams_t.get_team_by_dk_name(team_name)
        return team[0]


def get_visitor_team_name(game):
    spread = game[0]
    if spread["isOpen"]:
        spread_outcomes = spread["outcomes"]
        home_spread = spread_outcomes[0]
        team_name = home_spread["label"]
        team = nba_teams_t.get_team_by_dk_name(team_name)
        return team[1]


def get_home_team_id(game):
    spread = game[0]
    if spread["isOpen"]:
        spread_outcomes = spread["outcomes"]
        home_spread = spread_outcomes[1]
        team_name = home_spread["label"]
        team = nba_teams_t.get_team_by_dk_name(team_name)
        return team[0]


def get_home_team_name(game):
    spread = game[0]
    if spread["isOpen"]:
        spread_outcomes = spread["outcomes"]
        home_spread = spread_outcomes[1]
        team_name = home_spread["label"]
        team = nba_teams_t.get_team_by_dk_name(team_name)
        return team[1]


def build_game_result(game):
    game_result = {
        "game_id": get_game_id(game),
        "visitor_team_id": get_visitor_team_id(game),
        "visitor": get_visitor_team_name(game),
        "home_team_id": get_home_team_id(game),
        "home": get_home_team_name(game),
        "spread": get_spread(game),
        "total": get_total(game),
        "money_line": get_money_line(game)
    }
    return game_result


def get_game_lines():
    game_results_list = []
    games_list = draftkings_api()

    for game in games_list:
        game_results_list.append(build_game_result(game))

    return {"draft_kings_result": game_results_list}


if __name__ == '__main__':
    print("Running DraftKings Client.")
