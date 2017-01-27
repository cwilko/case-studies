# Step 1 : Basic Strategy Architecture
#
# Demonstrates a number of concepts and performance measurements that are part of all strategies.
#
# Strategy Statistics
# ===================
#
# 1. Arithmetic Mean Return
# The Arithmetic Mean return is the average non-compounded return value that was made in each period, across the N periods. 
#
# 2. Geometric Mean Return / APR
# The Geometric Mean return is the average return that was made, if the returns were continuously compounded. This differs from the actual percentage
# rate of the strategy due to the fact that we are compounding daily rather than continuously.
#
# The value at the start of the period is always higher for compound returns, hence why the GMean is always a lower value than the AMean.
# Either mean can be used as the "Expected Value" of the return, depending on how you intend to implement the strategy (i.e compounded returns or arithmetic returns).
# If geometric mean is annualised, this value is called APR (Annual Percentage Rate)
#
# 3. Kelly Value
# The Kelly Criterion (or Geometric Criterion) states that one should compound returns and choose a leverage value such as to maximise the GMean. This results in
# an optimally efficient strategy for building maximum total return. Note that the trade-off is an increase in max drawdown, it is therefore often advisable
# to choose a half-kelly value for leverage.
#
# 4. Sharpe Ratio
# The Sharpe ratio is the average unit of return (in excess of the risk-free rate) per unit of volatility or risk. E.g.if this is greater than 1, you are
# earning more than 1% mean return for every 1% of standard deviation (risk).
# 
# The Sharpe Ratio can be obtained for various types of return. For example, we can obtain a Sharpe Ratio for a) all capital invested (f=1) into an underlying return, 
# b) a proportion of capital (f != 1) invested into an underlying return, c) a proportion of capital plus remaining capital earning/paying interest, d) a portfolio
# of returns plus remaining capital with interest. We need to be carefuil of making a distinction between a Sharpe ratio for the underlying return, vs the Sharpe Ratio 
# of the strategy based on this return (i.e. the deriviative).
#
# An increase in sharpe ratio of the underlying return will also see an increase in the optimal leverage (see kelly value), and therefore the maximum geometric mean return.
#
# Sharpe is used to compare strategies, and to compare the change in a portfolio's risk-return profile when a new asset is added. Portfolio Theory 
# states that adding assets to a diversified portfolio that have correlations of less than one with each other can decrease portfolio risk without 
# sacrificing return. Diversification will therefore serve to increase the Sharpe ratio of a portfolio. 
#
# 5. Maximum Drawdown
# The maximum percentage drop of capital during the lifetime of this strategy. Important as you may enter the strategy at a peak and you
# need to prepare for a potential immediate drop of capital of this magnitude.
#
# 6. Maximum Drawdown Duration 
# As above but the maximum duration (not necessarily the duration of the max drawdown). The max time which you may spend out of
# profit when entering the strategy.
#
# 7. Return over Maximum Drawdown (RoMaD)
# Sharpe ratio gives a leverage and compounding neutral indicator of the performance of the strategy. However, to compare across different 
# compounded strategies, we can use the gMean as a measure of return, and the max drawdown as a measure of risk, to form the RoMaD 
# measure of risk-adjusted return. The higher the value, the better the risk/reward ratio for a particular strategy.
#
# 8. Volatility (Risk)
# Used in the Sharpe Ratio calculation, this is the annualised standard deviation of returns. This indicates the size and likelihood of hitting
# a significant drawdown.
#
# Graphical Representation of Strategy Performance
# ================================================
# This study demonstrates the two appropriate graphical representations of a strategy. Both of these involve first calculating the compound
# returns rather than absolute values. This avoids dependence on an initial account balance and also avoids a negative balance. 
#
# Method 1 : Visualisation of compound returns on a log scale. The y-axis shows the multiples of the original capital, the mean of the strategy
# is a straight line through the return which makes easy judgement and comparisons of growth.
# 
# Method 2 : Convert compounded returns to "Percent Returns" (or "Cumulatively Compounded Returns"). This has the benefit of
# aiding in reading values off the y-axis, i.e. simple percentage increments/decrements. However, the curve of the chart can be misleading as
# return grows exponentially with time.


import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import sys as sys
from finance import *
from stockUtils import *
from trading import maxDD
from uuid import uuid4
    
# ======================          
# Strategy Class
# ======================

class Strategy:
    def __init__(self, net_return, name=uuid4().hex, period=252.0, kelly=0, r=0):
        
        ''' Unleveraged Returns & Statistics '''
        self.name = name
        self.net_return = net_return   
        self.r = r    
        self.mean = mean(self.net_return) 
        self.var = var(self.net_return)
        self.std = std(self.net_return)
        self.amean = self.mean * period
        self.kelly = (self.mean - (self.r / period)) / self.var
        self.sharpe = sqrt(period) * (self.mean - (self.r / period)) / self.std
        
        ''' Leveraged Returns & Statistics '''
        self.leverage = 1
        if kelly>0:
            self.leverage = kelly * self.kelly
        
        compound_return = cumprod(1 + (self.leverage * net_return + (1.0 - self.leverage) * ((1 + self.r) ** (1.0/period) - 1)))
        self.compound_return = np.insert(compound_return,0,1)
        
        # Difference between gmean and APR due to daily compounded returns (APR) rather than continuously compounded returns (gmean)
        self.gmean = exp(r + self.leverage * ((self.mean * period) - r) - ((self.var * period * (self.leverage ** 2)) / 2.0))-1
        self.APR = self.compound_return[-1] ** (1.0 * period/float(len(self.compound_return))) - 1 # Nth root of the final capital
        self.APR = exp(log(self.compound_return[-1]) / (len(self.compound_return) / period)) - 1 # exp(log of final capital / T)
        
        self.maxDD, self.maxDDD = maxDD(self.compound_return)
        self.romad = self.APR / self.maxDD
    
    def display(self):
        
        # Strategy Statistics
        print
        print "=" * (len(self.name) + 14)
        print "Strategy ID : %s " % self.name
        print "Aritmetic Mean = %.2f" % (self.amean * 100)
        print "Sharpe Ratio = %.2f" % self.sharpe
        print "Kelly Optimal Leverage = %.2f" % self.kelly
        
        # Execution Statistics
        print "Geometric Mean Annual Return (APR) = %.2f%%" % (self.gmean * 100)
        print "Max Drawdown = %.2f%%" % (self.maxDD * 100)
        print "Max Drawdown Duration = %d days" % self.maxDDD
        print "Return over Maximum Drawdown (RoMaD) = %.2f" % self.romad
        print "Strategy Leverage = %.2f" % self.leverage
        print "APR = %.2f" % (self.APR * 100)
        print "=" * (len(self.name) + 14)
            

# ======================
# Instance of a Strategy
#=======================

M = loadStockData(STOCK_ROOT+'/2012/^GSPC.csv', "02/01/1993", "12/28/2007");

# Strategy 1 - Trading the S&P500
strategy_list = [ \
    Strategy(net_return(M['Close']), name='S&P500 Unlevered', r=0.04), \
    Strategy(net_return(M['Close']), name='S&P500 Full-Kelly', kelly=1, r=0.04), \
    Strategy(net_return(M['Close']), name='S&P500 3/4-Kelly', kelly=0.75, r=0.04), \
    Strategy(net_return(M['Close']), name='S&P500 1/2-Kelly', kelly=0.5, r=0.04), \
    Strategy(net_return(M['Close']), name='S&P500 1/4-Kelly', kelly=0.25) \
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
ax.set_title('Strategy Architecture');
ax.set_yscale('log', basey=e)
ax.set_yticks([.1,.2,.3,.4,.5,.6,.7,.8,.9,1,2,3,4,5,6,7,8,9,10,20,30,40,50,100,200,300,400,500])
ax.set_ylim([minc - abs(minc * .1),maxc + abs(maxc * .1)])
ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
ax.grid();

# Plot returns on log scale
colors = ['g','b','r','c','m','y'] # Allows for 6 plots

for i in range(0, len(strategy_list)):
    ax.plot(M['Date'], strategy_list[i].compound_return, colors[i], label=strategy_list[i].name)

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

