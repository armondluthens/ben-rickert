from flask import Flask, jsonify, request
import service.over_under as ou


# Flask constructor takes the name of current module (__name__) as argument.
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route('/sports/bets/spread')
def get_spread():
    return {"result": None}


@app.route('/sports/bets/over-under')
def get_over_under():
    is_thick = True if request.args.get('thick') == 'true' else False
    return jsonify(ou.get_over_under(is_thick))


@app.route('/sports/bets/moneyline')
def get_moneyline():
    return {"result": None}


@app.route('/sports/bets')
def bets():
    return {
        "over_under": get_over_under(),
        "spread": get_spread(),
        "moneyline": get_moneyline()
    }


if __name__ == '__main__':
    app.run()
