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
'''
result = loadStocks([ \
    'E:/stock/2012/^DJI.csv', \
    'E:/stock/2012/^GSPC.csv', \
    'E:/stock/2012/^FTSE.csv', \
    'E:/stock/2012/^IXIC.csv', \
    'E:/stock/2012/^NDX.csv', \
    'E:/stock/2012/^FTMC.csv', \
    ], "02/01/1993", "12/28/2007");
'''

result = loadPair(STOCK_ROOT+'/2012/^DJI.csv', STOCK_ROOT+'/2012/^GSPC.csv', "02/01/1993", "12/28/2007");

pip = 0.1
prices1 = result['data1'] 
prices2 = result['data2'] / pip
dates = result['date']

'''
pip = 0.1
prices1 = result[0]['Close'] 
prices2 = result[1]['Close'] / pip
prices3 = result[2]['Close'] 
prices4 = result[3]['Close'] / pip
prices5 = result[4]['Close'] / pip
prices6 = result[5]['Close'] 

dates = result[0]['Date']
'''

strategy_list = [ \
#    SpreadsStrategy(net_return(prices1), prices1[:-1], txCost=0.5), \
#    SpreadsStrategy(net_return(prices2), prices2[:-1], txCost=1.5), \
    SpreadsStrategy(net_return(prices1), prices1[:-1]), \
    SpreadsStrategy(net_return(prices2), prices2[:-1]), \
    #SpreadsStrategy(net_return(prices3), prices3[:-1], txCost=0.5), \
    #SpreadsStrategy(net_return(prices4), prices4[:-1], txCost=2), \
    #SpreadsStrategy(net_return(prices5), prices5[:-1], txCost=2), \
    #SpreadsStrategy(net_return(prices6), prices6[:-1], txCost=15), \
    ]

portfolio_list = [ \
    #SpreadsPortfolio([strategy_list[0]], name='Dow Jones', kelly=1.0, creditRate=0.04), \
    #SpreadsPortfolio([strategy_list[1]], name='S&P 500', kelly=1.0, creditRate=0.04), \
    #SpreadsPortfolio([strategy_list[2]], name='FTSE 100', kelly=1.0, creditRate=0.04), \
    #SpreadsPortfolio([strategy_list[3]], name='Nasdaq', kelly=1.0, creditRate=0.04), \
    #SpreadsPortfolio([strategy_list[4]], name='Nasdaq-100', kelly=1.0, creditRate=0.04), \
    #SpreadsPortfolio([strategy_list[5]], name='FTSE-250', kelly=1.0, creditRate=0.04), \
    SpreadsPortfolio(strategy_list[:2], name='Portfolio', kelly=1.0, creditRate=0.04) \
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
colors = ['g','b','r','c','m','y','orange','purple','brown'] # Allows for 9 plots

for i in range(0, len(portfolio_list)):
    ret = portfolio_list[i].compound_return
    ax.plot_date(dates, ret, colors[i], label=portfolio_list[i].name)

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

