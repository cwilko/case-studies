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

result = loadStocks([ \
    STOCK_ROOT+'/2012/^DJI.csv', \
    #STOCK_ROOT+'/2012/^GSPC.csv', \
    #STOCK_ROOT+'/2012/^FTSE.csv', \
    #STOCK_ROOT+'/2012/^FTMC.csv', \
    ], "02/01/1993", "12/28/2007");

close_prices = result[0]['Close'] / 0.1
dates = result[0]['Date']

V0 = 10000.0
period = 252 # Annual
margin = 500.0 / V0 # Assume 500 pips margin

# Strategy 1 - Trading with Shares (X = Pn - Pn-1 / Pn-1)

X1 = net_return(close_prices)

m = (average(X1) * period) 
s = std(X1) * sqrt(period)



r = 0.00 # Assume a borrowing rate of 0.00
f1a = (m - r)/ (s * s)
strategy1a = (f1a * X1) + (1.0 - f1a) * ((1 + r) ** (1.0/period) - 1)
g = r + f1a * (m - r) - ((s ** 2) * (f1a ** 2) / 2.0) # e ^ (g1 * t) = Geometric Mean

# Half Kelly
strategy1b = ((f1a / 2.0) * X1) + (1.0 - (f1a / 2.0)) * ((1 + r) ** (1.0/period) - 1)

r = 0.04 # Now set borrowing rate to something realistic
f1c = (m - r)/ (s * s)
strategy1c = (f1c * X1) + (1.0 - f1c) * ((1 + r) ** (1.0/period) - 1)

# Now prevent any money mgmt (f1 = 1)
strategy1d = 1.0 * X1 

compound_return1a = cumprod(np.insert((1 + strategy1a),0,1)) # W(1+fr)
compound_return1b = cumprod(np.insert((1 + strategy1b),0,1))
compound_return1c = cumprod(np.insert((1 + strategy1c),0,1))
compound_return1d = cumprod(np.insert((1 + strategy1d),0,1))

# Strategy 2 - Trading with Spreadbetting (X = Pn - Pn-1)

X2 = diff(close_prices)



r = 0.00 # savings interest rate on excess cash
f2a = (m-r) / ( close_prices * s**2)
strategy2a = (f2a[:len(X2)] * X2) + (1.0 - f2a[:len(X2)] - margin) * ((1 + r) ** (1.0/period) - 1) 

# Half Kelly
strategy2b = ((f2a[:len(X2)] / 2) * X2) + (1.0 - (f2a[:len(X2)] / 2) - margin) * ((1 + r) ** (1.0/period) - 1)

r = 0.04 # Now set savings to a realistic amount
f2c = (m-r) / ( close_prices * s**2)
strategy2c = (f2c[:len(X2)] * X2) + (1.0 - f2c[:len(X2)] - margin) * ((1 + r) ** (1.0/period) - 1)

compound_return2a = cumprod(np.insert((1 + strategy2a),0,1)) # W(1+fr) 
compound_return2b = cumprod(np.insert((1 + strategy2b),0,1))
compound_return2c = cumprod(np.insert((1 + strategy2c),0,1))

# Strategy 3 - Expected Values of Trading with Spreadbetting (X = E]Pn] - E[Pn-1]) (See workbook)

P0 = close_prices[0] 

t = [1.0/period] * period * 20 # 20 yrs of daily t
t = np.insert(cumsum(t),0,0,0)

f3 = m  / (P0 * np.exp((m + s**2 ) * t) * s**2)

#dg = (P0 * m * f * np.exp(m * t)) - (P0**2 * s**2 * f**2 * np.exp(2 * m * t + s**2 * t) / 2.0)
#g = (P0 * f * (np.exp(m * t) - 1)) - (P0**2 * s**2 * f**2 * (np.exp(2 * m * t + s**2 * t) - 1)) / (2.0 * (2 * m  + s**2))
#GM = exp(g)
#AM = exp(P0 * f * (exp(m * t) - 1))
#V = V0 * AM;

#g2 = r + f2 * (m2 - r) - ((s2 ** 2) * (f2 ** 2) / 2.0)

strategy3 = (f3[:len(X2)] * X2) #+ (1.0 - f[:len(X2)]) * ((1 + r) ** (1.0/period) - 1)
strategy3 = np.insert(strategy3,0,0.0)

compound_return3 = cumprod(1 + strategy3) ;        
        

# ====
# Plot
# ====

fig, ax = plt.subplots(2)
fig.autofmt_xdate()
minc = min(min(compound_return1a), min(compound_return1b), min(compound_return1c), min(compound_return2a), min(compound_return2b), min(compound_return3))
maxc = max(max(compound_return1a), max(compound_return1b), max(compound_return1c), max(compound_return2a), max(compound_return2b), max(compound_return3))

# Plot Shares

ax[0].set_title('Kelly optimal fractional trading with Shares');
ax[0].set_yscale('log', basey=e)
ax[0].set_yticks([.1,.2,.3,.4,.5,.6,.7,.8,.9,1,2,3,4,5,6,7,8,9,10,20,30,40,50,100,200,300,400,500])
ax[0].set_ylim([minc - abs(minc * .1),maxc + abs(maxc * .1)])
ax[0].yaxis.set_major_formatter(ticker.ScalarFormatter())
ax[0].grid();

ax[0].plot(dates, compound_return1a, 'r', label='S&P500, f=%.2f, r=0%%'%f1a)
ax[0].plot(dates, compound_return1c, 'b', label='S&P500, f=%.2f, r=4%%'%f1c)
ax[0].plot(dates, compound_return1b, 'g', label='S&P500, f=%.2f/2 (Half Kelly)'%f1a)
ax[0].plot(dates, compound_return1d, 'c', label='S&P500, f=1 (No Mgmt)')

handles, labels = ax[0].get_legend_handles_labels()
ax[0].legend(handles, labels, loc=2)
ax[0].fmt_xdata = mdates.DateFormatter('%Y-%m-%d')

# Plot Spreads

ax[1].set_title('Kelly optimal fractional trading with SpreadBetting');
ax[1].set_yscale('log', basey=e)
ax[1].set_yticks([.1,.2,.3,.4,.5,.6,.7,.8,.9,1,2,3,4,5,6,7,8,9,10,20,30,40,50,100,200,300,400,500])
ax[1].set_ylim([minc - abs(minc * .1),maxc + abs(maxc * .1)])
ax[1].yaxis.set_major_formatter(ticker.ScalarFormatter())
ax[1].grid();

ax[1].plot(dates, compound_return2a, 'r', label='S&P500, f=%.2f/Pn, r=0%%' % f1a)
ax[1].plot(dates, compound_return2c, 'b', label='S&P500, f=%.2f/Pn, r=4%%' % f1c)
ax[1].plot(dates, compound_return2b, 'g', label='S&P500, f=%.2f/2Pn (Half Kelly)' % f1a)

handles, labels = ax[1].get_legend_handles_labels()
ax[1].legend(handles, labels, loc=2)
ax[1].fmt_xdata = mdates.DateFormatter('%Y-%m-%d')


# Display plot

mng = plt.get_current_fig_manager()
mng.resize(1280,960)

plt.show()

