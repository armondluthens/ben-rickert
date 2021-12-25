import database.db as db
import draftkings.draftkings_client as dk
import model.OverUnder as overUnder

TABLE = 'DK_TOTALS'
CREATE_STATEMENT = '''
        CREATE TABLE DK_TOTALS (
            [game_id] INTEGER PRIMARY KEY,
            [visitor] TEXT,
            [visitor_team_id] INTEGER,
            [home] TEXT,
            [home_team_id] INTEGER,
            [over_odds] INTEGER,
            [over_line] INTEGER,
            [under_odds] INTEGER,
            [under_lines] INTEGER,
            UNIQUE(game_id)
        )
    '''


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


def insert(game_id, visitor, visitor_team_id, home, home_team_id, over_odds, over_line, under_odds, under_lines):
    connection = db.get_database_connection()
    c = connection.cursor()
    insert_statement = '''
            INSERT OR REPLACE INTO DK_TOTALS (game_id, visitor, visitor_team_id, home, home_team_id, over_odds, over_line, under_odds, under_lines) 
            VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')
        '''.format(game_id, visitor, visitor_team_id, home, home_team_id, over_odds, over_line, under_odds, under_lines)
    c.execute(insert_statement)
    connection.commit()


def import_data():
    dk_lines = dk.get_game_lines()
    results = dk_lines["draft_kings_result"]
    for result in results:
        total = result["total"]
        insert(result["game_id"], result["visitor"], result["visitor_team_id"], result["home"], result["home_team_id"],
               total["over"]["odds"], total["over"]["line"], total["under"]["line"], total["under"]["line"])


def get_total_by_team_ids(visitor_team_id, home_team_id):
    query = "SELECT * FROM {} WHERE visitor_team_id={} AND home_team_id={} LIMIT 1;"\
        .format(TABLE, visitor_team_id, home_team_id)
    result = db.select_single_row(query)
    return build_over_under(result)


def build_over_under(result):
    if not result:
        return None
    return overUnder.OverUnder(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8])


if __name__ == "__main__":
    drop()
    # clear()
    create()
    import_data()
    # get_all()
    print_all()


