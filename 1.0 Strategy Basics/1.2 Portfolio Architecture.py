# Transaction Costs
#
# Demonstrates the effect of transaction costs on a strategy

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import sys as sys
from finance import *
from stockUtils import *
from strategy import *

# ======================
# Instance of a Strategy
#=======================

result = loadStocks([ \
    STOCK_ROOT+'/2012/^DJI.csv', \
    #STOCK_ROOT+'/2012/^GSPC.csv'
    ], "02/01/1993", "12/28/2007");
    

pip = 0.1
dates = result[0]['Date']
prices1 = result[0]['Close'] 
#prices2 = result[1]['Close'] / pip

return1 = net_return(prices1)
#return2 = net_return(prices2)

strategy_list = [ \
    StocksStrategy(return1,txCost=0), \
    #StocksStrategy(return2,txCost=0), \
    ]

portfolio_list = [ \
    #Portfolio([strategy_list[0]], name='Dow Jones', kelly=1.0), \
    #Portfolio([strategy_list[1]], name='FTMC', kelly=1.0), \
    Portfolio(strategy_list, name='Portfolio', kelly=1.0) \
    ]

# ==================
# Display Statistics
# ==================

for strategy in portfolio_list:
    strategy.display()

# ====
# Plot
# ====

fig, ax = plt.subplots(1)

# Set up plot
fig.autofmt_xdate()
minc = sys.maxsize
maxc = 0
for strategy in portfolio_list:
    minc = min(minc, min(strategy.compound_return))
    maxc = max(maxc, max(strategy.compound_return))
ax.set_title('Portfolio Architecture');
ax.set_yscale('log', basey=e)
ax.set_yticks([.1,.2,.3,.4,.5,.6,.7,.8,.9,1,2,3,4,5,6,7,8,9,10,20,30,40,50,100,200,300,400,500])
ax.set_ylim([minc - abs(minc * .1),maxc + abs(maxc * .1)])
ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
ax.grid();

# Plot returns on log scale
colors = ['g','b','r','c','m','y'] # Allows for 6 plots

for i in range(0, len(portfolio_list)):
    ret = portfolio_list[i].compound_return
    ax.plot(dates, ret, colors[i], label=portfolio_list[i].name)

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels, loc=2)

# Add strategy statistics
ax1 = fig.add_axes([0,0,1,1])
ax1.set_axis_off()

for i in range(0,len(portfolio_list)):
    
    textstr = \
    '%s\n' \
    '$\mathtt{APR}=%.2f$%%\n' \
    '$\mathtt{Sharpe}=%.2f$\n' \
    '$\mathtt{MaxDD}=%.2f$%%\n' \
    '$\mathtt{MaxDDD=%d\/days}$\n' \
    '$\mathtt{Leverage}=%.2f$' % ( \
        portfolio_list[i].name, \
        (portfolio_list[i].APR * 100), \
        portfolio_list[i].sharpe, \
        (portfolio_list[i].maxDD * 100), \
        portfolio_list[i].maxDDD,
        portfolio_list[i].leverage
        )
    
    ax1.text(1.0*(i+1)/(len(portfolio_list)+1), -.1, 
            textstr, 
            horizontalalignment='center',
            verticalalignment='top',
            bbox = dict(boxstyle='round', facecolor=colors[i], alpha=0.5), 
            transform=ax.transAxes)
            
# Display plot
ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
mng = plt.get_current_fig_manager()
mng.resize(1280,860)

plt.show()

