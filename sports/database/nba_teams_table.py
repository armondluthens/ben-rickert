import database.db as db

TABLE = 'NBA_TEAMS'
CREATE_NBA_TEAMS_TABLE_STATEMENT = '''
    CREATE TABLE NBA_TEAMS (
        [team_id] INTEGER PRIMARY KEY,
        [name] TEXT NOT NULL,
        [dk_name] TEXT,
        UNIQUE(team_id),
        UNIQUE(name),
        UNIQUE(dk_name)
    )
'''


def create():
    db.execute_query(CREATE_NBA_TEAMS_TABLE_STATEMENT)


def drop():
    db.drop(TABLE)


def clear():
    db.clear(TABLE)


def seed():
    insert(1610612737, 'ATL Hawks', 'ATL Hawks')
    insert(1610612738, 'BOS Celtics', 'BOS Celtics')
    insert(1610612739, 'CLE Cavaliers', 'CLE Cavaliers')
    insert(1610612740, 'NOP Pelicans', 'NOP Pelicans')
    insert(1610612741, 'CHI Bulls', 'CHI Bulls')
    insert(1610612742, 'DAL Mavericks', 'DAL Mavericks')
    insert(1610612743, 'DEN Nuggets', 'DEN Nuggets')
    insert(1610612744, 'GSW Warriors', 'GS Warriors')
    insert(1610612745, 'HOU Rockets', 'HOU Rockets')
    insert(1610612746, 'LAC Clippers', 'LA Clippers')
    insert(1610612747, 'LAL Lakers', 'LA Lakers')
    insert(1610612748, 'MIA Heat', 'MIA Heat')
    insert(1610612749, 'MIL Bucks', 'MIL Bucks')
    insert(1610612750, 'MIN Timberwolves', 'MIN Timberwolves')
    insert(1610612751, 'BKN Nets', 'BKN Nets')
    insert(1610612752, 'NYK Knicks', 'NY Knicks')
    insert(1610612753, 'ORL Magic', 'ORL Magic')
    insert(1610612754, 'IND Pacers', 'IND Pacers')
    insert(1610612755, 'PHI 76ers', 'PHI 76ers')
    insert(1610612756, 'PHX Suns', 'PHO Suns')
    insert(1610612757, 'POR Trail Blazers', 'POR Trail Blazers')
    insert(1610612758, 'SAC Kings', 'SA Kings')
    insert(1610612759, 'SAS Spurs', 'SA Spurs')
    insert(1610612760, 'OKC Thunder', 'OKC Thunder')
    insert(1610612761, 'TOR Raptors', 'TOR Raptors')
    insert(1610612762, 'UTA Jazz', 'UTA Jazz')
    insert(1610612763, 'MEM Grizzlies', 'MEM Grizzlies')
    insert(1610612764, 'WAS Wizards', 'WAS Wizards')
    insert(1610612765, 'DET Pistons', 'DET Pistons')
    insert(1610612766, 'CHA Hornets', 'CHA Hornets')


def insert(team_id, name, dk_name):
    connection = db.get_database_connection()
    c = connection.cursor()
    insert_statement = '''
            INSERT OR REPLACE INTO NBA_TEAMS (team_id, name, dk_name) 
            VALUES ('{}', '{}', '{}')
        '''.format(team_id, name, dk_name)
    c.execute(insert_statement)
    connection.commit()


def get_all():
    return db.get_all(TABLE)


def get_team_id_and_name():
    t = []
    teams = get_all()
    for team in teams:
        t.append((team[0], team[1]))
    return t


def get_team_ids():
    team_ids = []
    teams = get_all()
    for team in teams:
        team_ids.append(team[0])
    return team_ids


def print_all():
    print(get_all())


def get_team_by_name(name: str):
    return db.select_single_row("SELECT * FROM NBA_TEAMS WHERE name='{}';".format(name))


def get_team_by_dk_name(name: str):
    return db.select_single_row("SELECT * FROM NBA_TEAMS WHERE dk_name='{}';".format(name))


def get_team_by_team_id(team_id: int):
    return db.select_single_row("SELECT * FROM NBA_TEAMS WHERE team_id={};".format(team_id))


if __name__ == "__main__":
    # clear()
    # create()
    # seed()
    # get_all()
    print_all()
