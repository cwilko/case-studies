# Step 1.1 : A simple autocorrelation strategy
#
# Simple strategy of going long the next day if previous day was up vs going short the next day if previous day was down 
#
# Effectively, this is trading positive vs negative autocorrelation for a 1 day lag, i.e. AC(1). 
#
# Note that this is not Momentum vs Mean Reversion. Prices can autocorrelate but still follow a geometric random walk.
#
# Inverse strategies; Daily Follow Through; Autocorrelation

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from finance import *
from stockUtils import *

M = loadStockData(STOCK_ROOT+'/2012/^GSPC.csv', "01/05/2000", "01/05/2010");

close_prices = M['Close']
open_prices = M['Open']
dates = M['Date']

benchmark = compound_return(close_prices) 

# Strategy 1
N = len(close_prices);
strategy1 = range(0,N)
strategy1[0] = 1;
for n in range (1,N):
    if close_prices[n-1] > open_prices[n-1] :
        strategy1[n] = close_prices[n] / open_prices[n];
    else:
        strategy1[n] = open_prices[n] / close_prices[n];

compound_return1 = cumprod(strategy1);
log_return1 = cumsum(log(strategy1));

# ma200 = zeros(1,N);
# for n=200:N
#     ma200(n) = mean(returns(n-200+1:n));
# end;

# Strategy 2
N = len(close_prices);
strategy2 = range(0,N)
strategy2[0] = 1;
for n in range (1,N):
    if close_prices[n-1] < open_prices[n-1] :
        strategy2[n] = close_prices[n] / open_prices[n];
    else:
        strategy2[n] = open_prices[n] / close_prices[n];
        
compound_return2 = cumprod(strategy2);
log_return2 = cumsum(log(strategy2));
          
# Plot
fig, ax = plt.subplots(1)

# rotate and align the tick labels so they look better
fig.autofmt_xdate()

m = min(compound_return1)
n = max(compound_return2);
ax.set_title('Stock Prices (Log Scale)');
ax.set_yscale('log', basey=e)
ax.set_yticks([.1,.2,.3,.4,.5,.6,.7,.8,.9,1,2,3,4,5,6,7,8,9,10,11,12])
ax.set_ylim([m - abs(m * .1),n + abs(n * .1)])
ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
ax.grid();

# Plot returns on log scale
ax.plot(dates, benchmark, label='Benchmark : S&P 500')
ax.plot(dates, compound_return1, 'r', label='Strategy A : Momentum')
ax.plot(dates, compound_return2, 'g', label='Strategy B : Mean Reversion')
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels, loc=2)

# Plot log returns

#ax.plot(dates, log_return(benchmark) * 100)
#ax.plot(dates, log_return1 * 100, 'r')
#ax.plot(dates, log_return2 * 100, 'g')


ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')

mng = plt.get_current_fig_manager()
mng.resize(1280,960)

plt.show()

