class OverUnder:
    def __init__(self, event_id, game_id, visitor, visitor_id, home, home_id, over_odds, over_line, under_odds, under_line, created):
        self.game_id = game_id
        self.visitor = visitor
        self.visitor_id = visitor_id
        self.home = home
        self.home_id = home_id
        self.over_odds = over_odds
        self.over_line = over_line
        self.under_odds = under_odds
        self.under_line = under_line

    def print(self):
        print(f"Game: {self.game_id}\n"
              f"Visitor: {self.visitor}\n"
              f"Home: {self.home}\n"
              f"Over: {self.over_odds}\n"
              f"Over Line: {self.over_line}\n"
              f"Under: {self.under_odds}\n"
              f"Under Line: {self.under_line}\n")
