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

M = loadStockData(STOCK_ROOT+'/2012/^GSPC.csv', "02/01/1995", "12/28/2007");

# Strategy 1 - Trading the S&P500

# Calculcate spreadbetting returns adjusted for transaction costs
pip = 0.1
prices = M['Close'] / pip # convert prices to pips
price_diff = diff(prices) - 1 # 1 pip is the typical spread on Indices
adj_return = price_diff / prices[:-1]

strategy_list = [ \
    SpreadsStrategy(net_return(prices), prices[:-1], name='Spreads', kelly=1.0), \
    SpreadsStrategy(adj_return, prices[:-1], name='Spreads + Tx Costs',kelly=0.5), \
    StocksStrategy(net_return(prices), prices[:-1], name='Spreads + Interest',kelly=1.0), \
    SpreadsStrategy(adj_return, prices[:-1], name='Spreads + Interest/TxCosts',kelly=0.5, creditRate=0.04) \
    ]

# ==================
# Display Statistics
# ==================

for strategy in strategy_list:
    strategy.display()

# ====
# Plot
# ====

fig, ax = plt.subplots(1)

# Set up plot
fig.autofmt_xdate()
minc = sys.maxsize
maxc = 0
for strategy in strategy_list:
    minc = min(minc, min(strategy.compound_return))
    maxc = max(maxc, max(strategy.compound_return))
ax.set_title('S&P500: The Impact of Transaction Costs');
ax.set_yscale('log', basey=e)
ax.set_yticks([.1,.2,.3,.4,.5,.6,.7,.8,.9,1,2,3,4,5,6,7,8,9,10,20,30,40,50,100,200,300,400,500])
ax.set_ylim([minc - abs(minc * .1),maxc + abs(maxc * .1)])
ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
ax.grid();

# Plot returns on log scale
colors = ['g','b','r','c','m','y'] # Allows for 6 plots

for i in range(0, len(strategy_list)):
    ret = strategy_list[i].compound_return
    ax.plot(M['Date'], ret, colors[i], label=strategy_list[i].name)

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels, loc=2)

# Add strategy statistics
ax1 = fig.add_axes([0,0,1,1])
ax1.set_axis_off()

for i in range(0,len(strategy_list)):
    
    textstr = \
    '%s\n' \
    '$\mathtt{APR}=%.2f$%%\n' \
    '$\mathtt{Sharpe}=%.2f$\n' \
    '$\mathtt{MaxDD}=%.2f$%%\n' \
    '$\mathtt{MaxDDD=%d\/days}$\n' \
    '$\mathtt{Leverage}=%.2f$' % ( \
        strategy_list[i].name, \
        (strategy_list[i].APR * 100), \
        strategy_list[i].sharpe, \
        (strategy_list[i].maxDD * 100), \
        strategy_list[i].maxDDD,
        strategy_list[i].leverage
        )
    
    ax1.text(1.0*(i+1)/(len(strategy_list)+1), -.1, 
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

