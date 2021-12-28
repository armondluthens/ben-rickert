from nba_api.stats.endpoints import leaguestandings as ls
from nba_api.stats.endpoints import teamyearbyyearstats as team_year_stats
from nba_api.stats.static import teams as team_stats
from nba_api.stats.endpoints import teamdashboardbylastngames as td
from database import nba_teams_table as nba_teams_t
import statistics

NBA_LEAGUE_ID = "00"
CURRENT_SEASON = 2021
PER_MODE = "Totals"
REGULAR_SEASON = "Regular Season"

GP_INDEX = 2
WIN_INDEX = 3
LOSS_INDEX = 4
POINTS_INDEX = 26

FIVE_GAME = "FIVE_GAME"
TEN_GAME = "TEN_GAME"
FIFTEEN_GAME = "FIFTEEN_GAME"
TWENTY_GAME = "TWENTY_GAME"


def get_team_dashboard(team_id):
    return td.TeamDashboardByLastNGames(team_id=team_id)


def get_predicted_point_total(team_1, team_2):
    team_1_dashboard = get_team_dashboard(team_1)
    team_2_dashboard = get_team_dashboard(team_2)

    point_avg = get_point_avg(team_1_dashboard, team_2_dashboard)
    return point_avg


def get_point_avg(team_1_dashboard, team_2_dashboard):
    avg_5_game = get_average_ppg_5_game(team_1_dashboard, team_2_dashboard)
    avg_10_game = get_average_ppg_10_game(team_1_dashboard, team_2_dashboard)
    avg_15_game = get_average_ppg_15_game(team_1_dashboard, team_2_dashboard)
    avg_20_game = get_average_ppg_20_game(team_1_dashboard, team_2_dashboard)

    return statistics.mean([avg_5_game, avg_10_game, avg_15_game, avg_20_game])


def get_average_ppg_5_game(team_1_dashboard, team_2_dashboard):
    team_1 = team_1_dashboard.last5_team_dashboard.data.get("data")[0]
    team_2 = team_2_dashboard.last5_team_dashboard.data.get("data")[0]
    return (team_1[POINTS_INDEX] / team_1[GP_INDEX]) + (team_2[POINTS_INDEX] / team_2[GP_INDEX])


def get_average_ppg_10_game(team_1_dashboard, team_2_dashboard):
    team_1 = team_1_dashboard.last10_team_dashboard.data.get("data")[0]
    team_2 = team_2_dashboard.last10_team_dashboard.data.get("data")[0]
    return (team_1[POINTS_INDEX] / team_1[GP_INDEX]) + (team_2[POINTS_INDEX] / team_2[GP_INDEX])


def get_average_ppg_15_game(team_1_dashboard, team_2_dashboard):
    team_1 = team_1_dashboard.last15_team_dashboard.data.get("data")[0]
    team_2 = team_2_dashboard.last15_team_dashboard.data.get("data")[0]
    return (team_1[POINTS_INDEX] / team_1[GP_INDEX]) + (team_2[POINTS_INDEX] / team_2[GP_INDEX])


def get_average_ppg_20_game(team_1_dashboard, team_2_dashboard):
    team_1 = team_1_dashboard.last20_team_dashboard.data.get("data")[0]
    team_2 = team_2_dashboard.last20_team_dashboard.data.get("data")[0]
    return (team_1[POINTS_INDEX] / team_1[GP_INDEX]) + (team_2[POINTS_INDEX] / team_2[GP_INDEX])


def get_league_standings():
    result = ls.LeagueStandings(league_id=NBA_LEAGUE_ID, season_nullable=CURRENT_SEASON, season_type=REGULAR_SEASON)
    print(result)


def get_team_year_stats(team_id):
    recent_season_stats = []
    stats = team_year_stats.TeamYearByYearStats(team_id=team_id, league_id=NBA_LEAGUE_ID,
                                                per_mode_simple=PER_MODE, season_type_all_star=REGULAR_SEASON)
    team = stats.data_sets[0].data
    seasons = team.get("data")

    for season in seasons:
        season_years = season[3]
        year = int(season_years[0:4])
        if year >= 2020:
            recent_season_stats.append(season)

    print(recent_season_stats)


def get_teams():
    nba_teams = team_stats.get_teams()
    for team in nba_teams:
        print(team['full_name'] + " " + str(team['id']))


def get_team_ids():
    ids = []
    nba_teams = team_stats.get_teams()
    for team in nba_teams:
        ids.append((team['id'], team['full_name']))
    return ids


def get_all_teams():
    team_tuple_list = []
    team_list = team_stats.get_teams()
    for team in team_list:
        team_id = team["id"]
        name = team["abbreviation"] + " " + team["nickname"]
        team_tuple_list.append((team_id, name))
    return team_tuple_list


def import_team_data():
    t = nba_teams_t.get_team_id_and_name()
    for team in t:
        tid = team[0]
        team_name = team[1]
        dashboard = get_team_dashboard(tid)


if __name__ == '__main__':
    print(get_all_teams())
