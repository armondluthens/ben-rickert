import csv
import util.date_util as du
import os.path
import database.nba_schedule as nba_schedule

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DECEMBER_SCHEDULE = os.path.join(BASE_DIR, "schedule/december.csv")
JANUARY_SCHEDULE = os.path.join(BASE_DIR, "schedule/january.csv")
FEBRUARY_SCHEDULE = os.path.join(BASE_DIR, "schedule/february.csv")
MARCH_SCHEDULE = os.path.join(BASE_DIR, "schedule/march.csv")
APRIL_SCHEDULE = os.path.join(BASE_DIR, "schedule/april.csv")


def get_schedule():
    schedule = open(DECEMBER_SCHEDULE)
    csv_reader = csv.reader(schedule)
    rows = []
    for row in csv_reader:
        rows.append(row)
    schedule.close()
    return rows


def get_games(day):
    games = []
    schedule = get_schedule()
    count = 0
    for game in schedule:
        if count > 0:
            if game[0] == du.get_day(day):
                games.append((game[2], game[4]))
        count += 1

    return games


def get_games_today():
    return nba_schedule.get_games(0)

