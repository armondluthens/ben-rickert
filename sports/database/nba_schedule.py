import database.db as db
import service.game_handler as gh
import constants.nba_teams as nba_teams
import util.date_util as du
# https://www.basketball-reference.com/leagues/NBA_2022_games.html

TABLE = 'NBA_SCHEDULE'
CREATE_STATEMENT = '''CREATE TABLE NBA_SCHEDULE (
            [event_id] INTEGER PRIMARY KEY AUTOINCREMENT,
            [date] TEXT,
            [start] TEXT,
            [visitor] TEXT,
            [visitor_team_id] INTEGER,
            [home] TEXT,
            [home_team_id] INTEGER)'''


def create():
    db.create(CREATE_STATEMENT)


def drop():
    db.drop(TABLE)


def clear():
    db.clear(TABLE)


def get_all():
    return db.get_all(TABLE)


def print_all():
    print(get_all())


def insert(date, start, visitor, visitor_team_id, home, home_team_id):
    connection = db.get_database_connection()
    c = connection.cursor()
    insert_statement = '''INSERT OR REPLACE INTO NBA_SCHEDULE (date, start, visitor, visitor_team_id, home, 
    home_team_id) VALUES ('{}', '{}', '{}', {}, '{}', {})
        '''.format(date, start, visitor, visitor_team_id, home, home_team_id)
    c.execute(insert_statement)
    connection.commit()


def import_schedule():
    schedule = gh.get_schedule()
    count = 0
    for game in schedule:
        if count > 0:
            insert(str(game[0]), str(game[1]), game[2], nba_teams.get_team_id(game[2]), game[4],
                   nba_teams.get_team_id(game[4]))
        count += 1


def get_games(offset):
    query = "SELECT visitor_team_id, home_team_id FROM NBA_SCHEDULE WHERE date = '{}';".format(du.get_day(offset))
    return db.select_multi_rows(query)
    # games = []
    # for game in results:
    #     games.append((game[0], game[1]))
    # return games


if __name__ == "__main__":
    print(get_games(1))
    # drop()
    # clear()
    # create()
    # import_schedule()
    # get_all()
    # print_all()
