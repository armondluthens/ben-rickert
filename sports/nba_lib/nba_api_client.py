from nba_api.stats.endpoints import leaguestandings as ls
from nba_api.stats.endpoints import teamyearbyyearstats as team_year_stats
from nba_api.stats.static import teams as team_stats
from nba_api.stats.endpoints import teamdashboardbylastngames as td
import nba_lib.league_team_dash as ltd
from database import nba_teams_table as nba_teams_t
import statistics

NBA_LEAGUE_ID = "00"
CURRENT_SEASON = 2021
PER_MODE = "Totals"
REGULAR_SEASON = "Regular Season"


def get_team_dashboard(team_id):
    return td.TeamDashboardByLastNGames(team_id=team_id)


def get_advanced_team_stats():
    team_stats_dict = {}
    league_team_dash_stats = ltd.LeagueTeamDashStats()
    advanced_stats = league_team_dash_stats.data_sets[0].data['data']
    if advanced_stats:
        for team in advanced_stats:
            team_stats_dict[team[0]] = team
    return team_stats_dict


if __name__ == '__main__':
    print(get_advanced_team_stats())
