# Section 2 : Linear combinations of stocks
#
# Illustrates the formation of a "basket" of stocks. I.e. a linear combination of stocks. The resulting linear equation
# gives the proportions of each stock to trade. 
# 
# The residual term is the value of the basket. 
#
# i.e. : r = y - ax - c 
# 
# You can "buy" or "sell" the basket and hence trade the residual. 
# 
# If the relationship parameters continued to hold, i.e. the residuals were "stationary",
# the basket value would oscillate around a mean value of 0.
#
# This property of some linear combination of non-stationary series to produce a stationary series is called cointegration.
# If a combination of securities cointegrated, the resulting stationary basket could be traded profitably.
#
# To "buy" the basket, buy 1 unit of y, sell a units of x.
#
# This opens up an infinite world of synthetic securities over the finite set of stock, indices, FX, etc.
#
# pair trading; linear regression; OLS; residuals; cointegration; stationarity

from numpy import *
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
from finance import *
from stockUtils import *

result = loadPair(STOCK_ROOT+'/2012/^DJI.csv', STOCK_ROOT+'/2012/^GSPC.csv', "01/02/2008", "01/05/2010");
      
prices1 = result['data1']
prices2 = result['data2']
dates = result['date']

# Make use of numpy OLS function
slope, intercept = linalg.lstsq(array([prices1,ones(len(prices1))]).T,prices2)[0]

line = slope*prices1+intercept

formula = "y = %.2fx + %.2f" % (slope, intercept)

fig, ax = plt.subplots(2)

# Scatter Plot with Regression line

ax[0].set_title("Stock Prices Scatter plot")
ax[0].plot(prices1,line,'r-', label=formula )
ax[0].plot(prices1,prices2,'o')
handles, labels = ax[0].get_legend_handles_labels()
ax[0].legend(handles, labels, loc=4)

# Residual plot (Basket value over time)

ax[1].set_title("Basket Value")
ax[1].plot(dates, prices2-line, label='Basket Value')
ax[1].plot(dates, zeros(len(dates)), 'r', label='Mean');
ax[1].fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
handles, labels = ax[1].get_legend_handles_labels()
ax[1].legend(handles, labels, loc=4)
plt.setp( ax[1].xaxis.get_majorticklabels(), rotation=30 )

mng = plt.get_current_fig_manager()
mng.resize(1280,960)
plt.show()

