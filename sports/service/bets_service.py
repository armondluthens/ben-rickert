
def get_payout(odds, wager):
    odds_int = int(odds)
    if odds_int < 0:
        wager_payout = wager * (100.0/(odds_int*-1))
        payout = round(wager_payout, 2)
    else:
        wager_payout = wager * (odds_int/100.0)
        payout = round(wager_payout, 2)
    return "$" + str(payout)
