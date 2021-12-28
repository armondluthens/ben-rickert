import database.db as db
import datetime
from service import stat_service


AVG_5 = "avg_5_game"
AVG_10 = "avg_10_game"
AVG_15 = "avg_15_game"
AVG_20 = "avg_20_game"
PACE = "pace"
OFFENSE = "offensive_rating"
DEFENSE = "defensive_rating"
PTS_AVG = "pts_avg"

TABLE = 'TEAM_STATS'
CREATE_STATEMENT = '''CREATE TABLE TEAM_STATS (
            [event_id] INTEGER PRIMARY KEY AUTOINCREMENT,
            [team_id] INTEGER,
            [team_name] TEXT,
            [avg_5_game] REAL,
            [avg_10_game] REAL,
            [avg_15_game] REAL,
            [avg_20_game] REAL,
            [pace] REAL,
            [offensive_rating] REAL,
            [defensive_rating] REAL,
            [pts_avg] REAL,
            [created] TEXT)'''


def create():
    db.execute_query(CREATE_STATEMENT)


def drop():
    db.drop(TABLE)


def clear():
    db.clear(TABLE)


def insert(team_id, team_name, team_stats):
    connection = db.get_database_connection()
    c = connection.cursor()

    insert_statement = '''
            INSERT OR REPLACE INTO TEAM_STATS (team_id, team_name, avg_5_game, avg_10_game, avg_15_game, 
            avg_20_game, pace, offensive_rating, defensive_rating, pts_avg, created) 
            VALUES ({}, '{}', {}, {}, {}, {}, {}, {}, {}, {}, '{}')
        '''.format(team_id, team_name, team_stats.get(AVG_5), team_stats.get(AVG_10), team_stats.get(AVG_15),
                   team_stats.get(AVG_20), team_stats.get(PACE), team_stats.get(OFFENSE), team_stats.get(DEFENSE),
                   team_stats.get(PTS_AVG), format_time())
    c.execute(insert_statement)
    connection.commit()


def format_time():
    t = datetime.datetime.now()
    s = t.strftime('%Y-%m-%d %H:%M:%S.%f')
    return s[:-3]


def get_all():
    return db.get_all(TABLE)


def print_all():
    print(get_all())


def get_team_by_team_id(team_id: int):
    return db.select_single_row("SELECT * FROM TEAM_STATS WHERE team_id={};".format(team_id))


def import_stats():
    stat_service.import_team_stats()


if __name__ == "__main__":
    import_stats()
    # drop()
    # create()
    # clear()
    # seed()
    # get_all()
    print_all()
