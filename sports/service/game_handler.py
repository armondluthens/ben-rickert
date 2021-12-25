import csv
import util.date_util as du
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEDULE_PATH = os.path.join(BASE_DIR, "schedule/december.csv")


def get_schedule():
    schedule = open(SCHEDULE_PATH)
    csv_reader = csv.reader(schedule)
    rows = []
    for row in csv_reader:
        rows.append(row)
    schedule.close()
    return rows


def get_games(day):
    games = []
    schedule = get_schedule()
    for game in schedule:
        if game[0] == day:
            games.append((game[2], game[4]))
    return games


def get_games_today():
    return get_games(du.get_today())


def get_games_tomorrow():
    return get_games(du.get_tomorrow())

