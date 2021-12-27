# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, render_template
import service.over_under as ou
import view.build_view as view


def over_under():
    results = ou.over_under()
    return results


# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)


@app.route('/')
def home():
    return render_template("test.html", message="Hello Flask!")


# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/sports/bets')
# ‘/’ URL is bound with hello_world() function.
def bets():
    result = over_under()
    page = view.get_page(result)
    return page


# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()
