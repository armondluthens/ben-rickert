# First we will import our packages
import pandas as pd
import numpy as np
from sklearn import linear_model
import requests
from nba_api.stats import endpoints
from matplotlib import pyplot as plt


def lg():
    # Here we access the leagueleaders module through endpoints & assign the class to "data"
    data = endpoints.leagueleaders.LeagueLeaders()

    # Our "data" variable now has built in functions such as creating a dataframe for our data
    df = data.league_leaders.get_data_frame()
    # take a sneak peak at the first 5 rows
    df.head()

    # First we need to get per game stats.
    # We divide each variable by games played (GP) to get per game average
    x, y = df.FGA/df.GP, df.PTS/df.GP

    x = np.array(x).reshape(-1,1)     # we have to reshape our array from 1d to 2d.
    y = np.array(y).reshape(-1,1)     # The proper shaped array is an input requirement for the linear model
                                      # reshaping is usually an issue when using 1 x variable

    model = linear_model.LinearRegression()    # create an object that contains the linear model class
    model.fit(x,y)                             # Fit our modeling using FGA (x) and PPG (y)

    # Get our r2 value and round it to 2 decimals. How much variance is exaplained?
    r2 = round(model.score(x,y), 2)
    # Get our predicted y values for x
    predicted_y = model.predict(x)

    # Scatterplot:  Specfiy size(s) and transparency(alpha) of dots
    plt.scatter(x, y, s=15, alpha=.5)
    # line: Add line for regression line w/ predicted values
    plt.plot(x, predicted_y, color='black')

    plt.title('NBA - Relationship Between FGA and PPG')  # Give it a title
    plt.xlabel('FGA per Game')  # Label x-axis
    plt.ylabel('Points Per Game')  # Label y-axis
    plt.text(10, 25, f'R2={r2}')  # 10, 25 are the coordinates for our text. Adjust accordingly

    """ It looks like one player is far from the pack on offense. We should annotate that point! 
        We know that the first x-value in our dataset ( the first row ) is the highest scoring player
        because of the .head() that we used earlier. So we can use x[0] and y[0] since this refers to the first row
    """
    plt.annotate(df.PLAYER[0],  # This the name of the top scoring player. Refer to the .head() from earlier
                 (x[0], y[0]),  # This is the point we want to annotate.
                 (x[0] - 7, y[0] - 2),  # These are coords for the text
                 arrowprops=dict(arrowstyle='-'))  # Here we use a flat line for the arrow '-'

    # Finally, let's save an image called 'graph.png'. We'll set the dpi (dots per inch) to 300, so we have a nice
    # looking picture.
    plt.savefig('graph.png', dpi=300)


if __name__ == '__main__':
    lg()