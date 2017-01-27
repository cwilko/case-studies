# Section 3.1 : Covariance and Correlation of daily series
#
# Demonstration of the calculation of covariance and correlation.
#
# Covariance is an indicator of how variables move in relation to each other. The formula is
#     E[(x - E[X])(y - E[Y])]
#
# Examining this formial, a residual in X is multiplied by its corresponding residual in Y. The result
# of each multiplication will be positive if both residuals move in the same direction, and negative if 
# they move in opposite directions. The larger the magnitude of the result, the more
# it contributes to the final value of the covariance (So larger moves could skew the result). The covariance tells us 
# nothing about the amount by which they move together, only if they tend to move in the same direction or not.
#
# To calculate a measure of how much they move together, we normalise the covariance by dividing by the std(X) * std(Y).
# This gives us the Correlation.
#
# When we calculate the covariance of X with X, we get the variance of X.
#
# The i,j elements of a Covariance Matrix give the cov(i,j). The diagnal is therefore always
# the values for the variances of the variables. This is why it is sometimes called the variance-covariance matrix. 
#
# The correlation of a variable with a time-lagged version of itself is called the Autocorrelation, i.e. AC(k) This gives an
# indication of the movement of X in relation to X - k. In other words, this is a formal description of phenomena such as
# momentum (AC = +ve) and mean reversion (AC = -ve).
# 

from numpy import *
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
from finance import *
from stockUtils import *

result = loadStockData(STOCK_ROOT+'/2012/^GSPC.csv', "01/05/2000", "01/05/2010");

dates = result['Date']

returns = log(gross_return(result['Close']));
last = len(returns) - 1;
coefficients = zeros(500);

fig, ax = plt.subplots(2)

# Autocorrelation of log returns
for i in range(0,500):

    series1 = returns[last - 200:last]
    series2 = returns[last - 200 - i:last - i]


    # Now do it with numpy to check the values
    M = vstack((series1, series2));
    coefficients[i] = corrcoef(M)[0][1]

chart = ax[0]
chart.set_title('Autocorrelation function for S&P 500 returns');
chart.plot(range(0,500), coefficients , label='AC(k) of Log Returns');
chart.set_ylabel('Correlation')
handles, labels = chart.get_legend_handles_labels()
chart.legend(handles, labels)
chart.grid();

# Autocorrelation of absolute log returns (volatility)
returns = abs(returns);

for i in range(0,500):

    series1 = returns[last - 200:last]
    series2 = returns[last - 200 - i:last - i]


    # Now do it with numpy to check the values
    M = vstack((series1, series2));
    coefficients[i] = corrcoef(M)[0][1]

chart = ax[1]
chart.plot(range(0,500), coefficients , label='AC(k) of Absolute Log Returns');
chart.set_ylabel('Correlation')
chart.set_xlabel('lag (k)')
handles, labels = chart.get_legend_handles_labels()
chart.legend(handles, labels)
chart.grid();

mng = plt.get_current_fig_manager()
mng.resize(1280,960)

plt.show()