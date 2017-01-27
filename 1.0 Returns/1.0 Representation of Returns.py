# Step 1 : A study of the representation of stock returns
# 
# Stock prices and returns inherently feature compounding effects. Any models include an 
# exponential term, which is hard to work with. This makes it difficult to work with and 
# calculate distribution properties such as the mean.
#
# We can elminiate the exponential terms by using a log transformation. This can be done
# by either a) Charting the stock prices/returns on log scale, or b) Calculating log
# prices and returns.
#
# Using log returns gives us very simple linear methods of combining returns and calculating
# mean returns.
#
# Where : log (r) = log (p2) - log (p1)


import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
from finance import *
from stockUtils import *

M = loadStockData(STOCK_ROOT+'/2012/^GSPC.csv', "01/05/2000", "01/05/2010");

close_prices = M['Close']
open_prices = M['Open']
dates = M['Date']

# 1 : Stock Prices

series1 = close_prices;

# 2 : Stock Prices (Log Scale)

series2 = close_prices;

# 3 : Compound Returns

series3 = compound_return(close_prices)

# 4 : Compound Retuns (Log Scale)

series4 = compound_return(close_prices)

# 5 : Percent returns 

series5 = percent_return(close_prices)

# 6 : Percent Log Returns

series6 = log_return(close_prices) * 100;

# 7 : Daily Percent Returns

series7 = net_return(close_prices, False) * 100;

# 8 : Daily Log Returns
series8 = log(gross_return(close_prices)) * 100;

# Plot
fig, ax = plt.subplots(4,2)

# rotate and align the tick labels so they look better
fig.autofmt_xdate()

ax[0][0].set_title('Stock Prices');
ax[0][0].plot(dates, series1)
ax[0][0].fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
ax[0][0].grid();

m = min(series2);
n = max(series2);
ax[0][1].set_title('Stock Prices (Log Scale)');
ax[0][1].set_yscale('log', basey=e)
ax[0][1].set_yticks(range(200,10000,200))
ax[0][1].set_ylim([m - abs(m * .1),n + abs(n * .1)])
ax[0][1].plot(dates, series2)
ax[0][1].yaxis.set_major_formatter(ticker.ScalarFormatter())
ax[0][1].fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
ax[0][1].grid();

ax[1][0].set_title('Compound Returns');
ax[1][0].plot(dates, series3)
ax[1][0].fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
ax[1][0].grid();

m = min(series4);
n = max(series4);
ax[1][1].set_title('Compound Returns (Log Scale)');
ax[1][1].set_yscale('log', basey=e)
ax[1][1].set_yticks(linspace(-2,2,41))
ax[1][1].set_ylim([m - abs(m * .1),n + abs(n * .1)])
ax[1][1].plot(dates, series4)
ax[1][1].yaxis.set_major_formatter(ticker.ScalarFormatter())
ax[1][1].fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
ax[1][1].grid();

ax[2][0].set_title('Percent Returns');
ax[2][0].plot(dates, series5)
ax[2][0].fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
ax[2][0].grid();

ax[2][1].set_title('Percent Log Returns');
ax[2][1].plot(dates, series6)
ax[2][1].fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
ax[2][1].grid();

ax[3][0].set_title('Daily Returns');
ax[3][0].plot(dates, series7)
ax[3][0].fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
ax[3][0].grid();

ax[3][1].set_title('Daily Log Returns');
ax[3][1].plot(dates, series8)
ax[3][1].fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
ax[3][1].grid();

mng = plt.get_current_fig_manager()
mng.resize(1280,960)


plt.show()