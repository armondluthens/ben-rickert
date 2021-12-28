from database import nba_teams_table
from nba_lib import nba_api_client
from database import team_stats_table
import time
import statistics

GP_INDEX = 2
WIN_INDEX = 3
LOSS_INDEX = 4
POINTS_INDEX = 26
OFFENSIVE_RATING = 8
DEFENSIVE_RATING = 10
'''
['TEAM_ID', 'TEAM_NAME', 'GP', 'W', '4L', '5W_PCT', 'MIN', 'E_OFF_RATING', 'OFF_RATING', 'E_DEF_RATING', '10DEF_RATING', 'E_NET_RATING', 'NET_RATING', 'AST_PCT', 'AST_TO', 'AST_RATIO', 'OREB_PCT', 'DREB_PCT', 'REB_PCT', 'TM_TOV_PCT', '20EFG_PCT', 'TS_PCT', 'E_PACE', '23PACE', 'PACE_PER40', 'POSS', 'PIE', 'GP_RANK', 'W_RANK', 'L_RANK', 'W_PCT_RANK', 'MIN_RANK', 'OFF_RATING_RANK', 'DEF_RATING_RANK', 'NET_RATING_RANK', 'AST_PCT_RANK', 'AST_TO_RANK', 'AST_RATIO_RANK', 'OREB_PCT_RANK', 'DREB_PCT_RANK', 'REB_PCT_RANK', 'TM_TOV_PCT_RANK', 'EFG_PCT_RANK', 'TS_PCT_RANK', 'PACE_RANK', 'PIE_RANK', 'CFID', 'CFPARAMS']
'''
ADV_STATS_PACE = 23

AVG_5 = "avg_5_game"
AVG_10 = "avg_10_game"
AVG_15 = "avg_15_game"
AVG_20 = "avg_20_game"
PACE = "pace"
OFFENSE = "offensive_rating"
DEFENSE = "defensive_rating"
PTS_AVG = "pts_avg"


def get_average_ppg_5_game(team_dashboard):
    team = team_dashboard.last5_team_dashboard.data.get("data")[0]
    return team[POINTS_INDEX] / team[GP_INDEX]


def get_average_ppg_10_game(team_dashboard):
    team = team_dashboard.last10_team_dashboard.data.get("data")[0]
    return team[POINTS_INDEX] / team[GP_INDEX]


def get_average_ppg_15_game(team_dashboard):
    team = team_dashboard.last15_team_dashboard.data.get("data")[0]
    return team[POINTS_INDEX] / team[GP_INDEX]


def get_average_ppg_20_game(team_dashboard):
    team = team_dashboard.last20_team_dashboard.data.get("data")[0]
    return team[POINTS_INDEX] / team[GP_INDEX]


def fetch_team_stats(team_id, advanced_stats):
    team_dashboard = nba_api_client.get_team_dashboard(team_id)
    avg_5_game = round(get_average_ppg_5_game(team_dashboard), 2)
    avg_10_game = round(get_average_ppg_10_game(team_dashboard), 2)
    avg_15_game = round(get_average_ppg_15_game(team_dashboard), 2)
    avg_20_game = round(get_average_ppg_20_game(team_dashboard), 2)
    pace = advanced_stats[ADV_STATS_PACE]
    offensive_rating = advanced_stats[OFFENSIVE_RATING]
    defensive_rating = advanced_stats[DEFENSIVE_RATING]

    return {
        AVG_5: avg_5_game,
        AVG_10: avg_10_game,
        AVG_15: avg_15_game,
        AVG_20: avg_20_game,
        PACE: pace,
        OFFENSE: offensive_rating,
        DEFENSE: defensive_rating,
        PTS_AVG: statistics.mean([avg_5_game, avg_10_game, avg_15_game, avg_20_game])
    }


def import_team_stats():
    advanced_team_stats = nba_api_client.get_advanced_team_stats()
    teams = nba_teams_table.get_team_id_and_name()
    for team in teams:
        time.sleep(1)
        team_id = team[0]
        team_name = team[1]
        team_stats = fetch_team_stats(team_id, advanced_team_stats.get(team_id))
        team_stats_table.insert(team_id, team_name, team_stats)
        print(team_stats)
