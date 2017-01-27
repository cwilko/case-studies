# Step 1.2 : Money Management
#
# Demonstrates use of the kelly criterion. Shows how Shares and Spreads can be used to achieve the same optimal strategy, and how the leverage 
# implicit in spreads can be used to an advantage.
#
#
# # Shares vs Spreads
# =================
# The study shows two simple strategies : Spread trading vs Shares trading the S&P using the Kelly Criterion.
#
# An investment in shares is the traditional method of trading, and this equates to returns of the form (Pn - Pn-1) / Pn. 
# This gives the multiple of f which is gained/lost during a trade (note that the loss cannot be less than -1, i.e. it is not
# possible to lose more than the original stake.
#
# An investment in spreadbets equates to a return of the form Pn - Pn-1. There is no normalisation by the original price,
# therefore it is possible to lose (and win) far more than the original stake. 
#
#
# Kelly Criterion
# ===============
# Kelly Criterion aims to trade a fixed fraction (f) of capital such that the expected growth rate (g) of the compounded
# returns is maximised.

# Where :
#   m = mean return of underlying normally distributed random variable (i.e. stock return)
#   s = standard deviation of variable
#   r = interest rate for any borrowed/saved capital
#   f = proportion of capital to trade
#   g = Expected growth rate of compounded returns from trading
# 
#   g = r + f(m-r) - s^2f^2 / 2
#
#   Optimal f1 = f1* = (m-r)/s^2          (Shares)
#
#   Optimal f2 = f2* = Pn(m-r)/Pn^2s^2    (Spreads)
#
# Also see workbook for application of these equations where Pn is unknown.
# 
# Conclusions
# ===========
#
# The risk associated with spreads (i.e. unlimited downside) comes with an implicit leverage benefit. Notice the difference in returns 
# of spreads vs shares when the portfolio includes a cash element, which earns interest at a rate > 0%.
# The small kelly leverage portion of capital used for spreads leaves a large amount to be invested in the risk-free rate. The effect is a reduced risk,
# higher return strategy.
# However, for shares we need to BORROW money to achieve the kelly leverage! This means we have to pay out interest at at the risk-free rate 
# (in reality this would be higher than the risk-free rate). The result is a reduced risk ANDreduced return strategy.
#

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from finance import *
from stockUtils import *

M = loadStockData(STOCK_ROOT+'/2012/^GSPC.csv', "02/01/1993", "12/28/2007");

close_prices = M['Close'] / 0.1
dates = M['Date']

r=0.0
V0 = 10000.0
period = 252 # Annual
margin = 500.0 / V0 # Assume 500 pips margin

# Strategy 1 - Trading with Shares (X = Pn - Pn-1 / Pn-1)

r1 = net_return(close_prices)

m = (average(r1) * period) 
s = std(r1) * sqrt(period)

f1 = (m - r)/ (s * s)
strategy1a = 1 + (f1 * r1)                  # 1 + fr
strategy1a = np.insert(strategy1a,0,1)
W1a = cumprod(strategy1a)                                 # W(1+fr)

# TxCosts

a1 = 0.01 # txCost is 10% of rebalance amount
X1 = ( f1 * r1 * (1 - f1) )  / (1 - a1 * f1) # rebalance amount

strategy1b = 1 + f1 * r1 - sign(X1) * a1 * X1                  # 1 + fr
strategy1b = np.insert(strategy1b,0,1)

W1b = cumprod(strategy1b)                                 # W(1+fr) - aX

# Strategy 2 - Trading with Spreadbetting (X = Pn - Pn-1)

r2 = diff(close_prices)

f2 = (m-r) / ( close_prices[:len(r2)] * s**2)
strategy2a = 1 + (f2 * r2)
strategy2a = np.insert(strategy2a,0,1)
W2a = cumprod(strategy2a) # W(1+ fr) 

# TxCosts

a2 = 1 # txCost is 50% of rebalance amount
X2 = ( f2 * r2 * f2 )  / (1 + (a2 * f2)) # rebalance amount   

strategy2b = 1 + f2 * r2 - sign(X2) * a2 * X2
strategy2b = np.insert(strategy2b,0,1)

W2b = cumprod(strategy2b) # W(1+fr) - aX

# ====
# Plot
# ====

fig, ax = plt.subplots(2)
fig.autofmt_xdate()
minc = min(min(W1a), min(W1b), min(W2a), min(W2b))
maxc = max(max(W1a), max(W1b), max(W2a), max(W2b))

# Plot Shares

ax[0].set_title('S&P500 Shares under Transaction Costs');
ax[0].set_yscale('log', basey=e)
ax[0].set_yticks([.1,.2,.3,.4,.5,.6,.7,.8,.9,1,2,3,4,5,6,7,8,9,10,20,30,40,50,100,200,300,400,500])
ax[0].set_ylim([minc - abs(minc * .1),maxc + abs(maxc * .1)])
ax[0].yaxis.set_major_formatter(ticker.ScalarFormatter())
ax[0].grid();

ax[0].plot(dates, W1a, 'r', label='No TxCosts')
ax[0].plot(dates, W1b, 'b', label='TxCosts = %.1f%%' % (a1*100))

handles, labels = ax[0].get_legend_handles_labels()
ax[0].legend(handles, labels, loc=2)
ax[0].fmt_xdata = mdates.DateFormatter('%Y-%m-%d')

# Plot Spreads

ax[1].set_title('S&P500 Spreadbetting under Transaction Costs');
ax[1].set_yscale('log', basey=e)
ax[1].set_yticks([.1,.2,.3,.4,.5,.6,.7,.8,.9,1,2,3,4,5,6,7,8,9,10,20,30,40,50,100,200,300,400,500])
ax[1].set_ylim([minc - abs(minc * .1),maxc + abs(maxc * .1)])
ax[1].yaxis.set_major_formatter(ticker.ScalarFormatter())
ax[1].grid();

ax[1].plot(dates, W2a, 'r', label='No TxCosts')
ax[1].plot(dates, W2b, 'b', label='TxCosts = %d pip(s)' % (a2*2))

handles, labels = ax[1].get_legend_handles_labels()
ax[1].legend(handles, labels, loc=2)
ax[1].fmt_xdata = mdates.DateFormatter('%Y-%m-%d')


# Display plot

mng = plt.get_current_fig_manager()
mng.resize(1280,960)

plt.show()

