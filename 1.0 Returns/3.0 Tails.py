#  A study of the distribution tails for stock returns
#
#  This is a study of the structure of the distribution tails. 
#
#  We first overlay the left and right sides of the cdf (midpoint = delta) in 
#  order to compare them. The left tail values are plotted against the absolute 
#  values of the delta-shifted return, the right tail values are subtracted from 1, 
#  this aligns the tails and allows comparison. If beta=0, the tails align exactly.
#
#  This study demonstrates several things:
#
#  a) The exponent of the extent of the tails is equal to alpha. We can work this out
#  by calculating the gradient of the log-scaled data.
#
#  b) The actual CDF, calculated from the raw data, does not fit the stable distribution
#  in the extent of the tails. I.e. the actual alpha, as calculated in a), does not match 
#  the alpha value from the fitted stable distribution. The calculated alpha is larger
#  than the fitted alpha, and indeed, large enough to indicate that a combination of 
#  these distributions would converge to a normal distribution (alpha > 2). This result
#  is significant in that it indicates the data does  NOT follow a stable distribution.
#
#

import matplotlib.pyplot as plt
from finance import *
from stockUtils import *
import stable as stable
import matplotlib.ticker as ticker

def getLeftTail(x, delta):
    j=0;
    for i in x:
        if i > delta:
            break;
        j=j+1;
    return j;
    
def getRightTail(x, delta):
    j=0;
    for i in x:
        if i >= delta:
            break;
        j=j+1;
    return j;

M = loadStockData(STOCK_ROOT+'/2012/^GSPC.csv', "01/05/1995", "01/05/2010");

close_prices = M['Close']
open_prices = M['Open']
dates = M['Date']

log_returns = log(gross_return(close_prices));
n, bars = histogram(log_returns, 100, normed=True);
bars = bars[0:-1]
barWidth = bars[1] - bars[0]

cdf_steps = 8001
midpoint = int(cdf_steps / 2.0);
cdf_stepSize = 200.0 / midpoint

stable.init(log_returns);
fig, ax = plt.subplots(2)

# 1 : Fit to Normal Distribution

alpha,beta,gamma,delta = stable.fit(log_returns, alpha=2.0, beta=0.0); 

normal_cdf_x, normal_cdf_y = stable.cdf2(alpha, beta, gamma, delta, cdf_steps, cdf_stepSize * gamma);
normal_x = normal_cdf_x[midpoint+1:]

# 2 : Cauchy Distribution

alpha,beta,gamma,delta = stable.fit(log_returns, alpha=1.0, beta=0.0); 

cauchy_cdf_x, cauchy_cdf_y = stable.cdf2(alpha, beta, gamma, delta, cdf_steps, cdf_stepSize * gamma);
cauchy_x = cauchy_cdf_x[midpoint+1:]

# 3 : Levy Distribution

alpha,beta,gamma,delta = stable.fit(log_returns, alpha=0.5, beta=0.0); 

levy_cdf_x, levy_cdf_y = stable.cdf2(alpha, beta, gamma, delta, cdf_steps, cdf_stepSize * gamma);
levy_x = levy_cdf_x[midpoint+1:]

# 4 : Stable Distribution

alpha,beta,gamma,delta = stable.fit(log_returns); 

stable_cdf_x, stable_cdf_y = stable.cdf2(alpha, beta, gamma, delta, cdf_steps, cdf_stepSize * gamma);
stable_x = stable_cdf_x[midpoint+1:]
stable_delta = delta

# Actual CDF
actual_x = sort(log_returns)
actual_cdf = zeros(len(log_returns))
actual_cdf[:] = (1.0/(len(log_returns)+1))
actual_cdf = cumsum(actual_cdf)

leftStart = getLeftTail(actual_x, stable_delta)
rightStart = getRightTail(actual_x, stable_delta)

left_x = abs(actual_x[0:leftStart] - stable_delta) + stable_delta
left_cdf = actual_cdf[0:leftStart]

right_x = abs(actual_x[rightStart:] - stable_delta) + stable_delta
right_cdf = actual_cdf[rightStart:]

# Plot : CDF
chart = ax[0]
chart.set_title('Distribution of Returns');
chart.set_yscale('log', basey=e)
chart.set_xscale('log', basey=e)
chart.set_yticks([1e-05,0.0001,0.001,0.01,1])
chart.set_ylim(1e-05,1)
chart.plot(normal_x, normal_cdf_y[0:midpoint][::-1] , 'g', label='Normal');
chart.plot(normal_x, 1 - normal_cdf_y[midpoint+1:] , 'g');
chart.plot(cauchy_x, cauchy_cdf_y[0:midpoint][::-1] , 'cyan', label='Cauchy');
chart.plot(cauchy_x, 1 - cauchy_cdf_y[midpoint+1:] , 'cyan');
chart.plot(levy_x, levy_cdf_y[0:midpoint][::-1] , 'y', label='Levy');
chart.plot(levy_x, 1 - levy_cdf_y[midpoint+1:] , 'y');
chart.plot(stable_x, stable_cdf_y[0:midpoint][::-1] , 'b', label='Stable (Left)');
chart.plot(stable_x, 1 - stable_cdf_y[midpoint+1:] , 'r', label='Stable (Right)');
chart.scatter(left_x, left_cdf, color='blue')
chart.scatter(right_x, 1 - right_cdf, color='red')
chart.yaxis.set_major_formatter(ticker.ScalarFormatter())
handles, labels = chart.get_legend_handles_labels()
chart.legend(handles, labels)
chart.grid();

# Calculate the alpha of the stable distribution from the tail

stable_left = log(stable_cdf_y[:midpoint][::-1][-50:])
stable_right = log((1 - stable_cdf_y[midpoint:])[-50:])
stable_tail_x = log(stable_cdf_x[midpoint+1:][-50:])

left_stable_slope, left_stable_intercept = linalg.lstsq(array([stable_tail_x,ones(len(stable_tail_x))]).T,stable_left)[0]
right_stable_slope, right_stable_intercept = linalg.lstsq(array([stable_tail_x,ones(len(stable_tail_x))]).T,stable_right)[0]

# Extract least likely 5% data, fit a regression line to the log values
# in order to calculate the slope, i.e. the exponent
#
# QUESTION : The slope will change depending on gamma & delta, but alpha is supposed to stay constant!.
# ANSWER : Increase sample points (i.e. measure further out in the tail), will eventually converge to alpha.

left = log(left_cdf[:50])
left_x = log(left_x[:50])

right = log((1-right_cdf)[-50:])
right_x = log(right_x[-50:])

left_slope, left_intercept = linalg.lstsq(array([left_x,ones(len(left_x))]).T,left)[0]
right_slope, right_intercept = linalg.lstsq(array([right_x,ones(len(right_x))]).T,right)[0]

left_line = left_slope*left_x+left_intercept
right_line = right_slope*right_x+right_intercept

formula_left = "alpha = %.2f" % left_slope
formula_right = "alpha = %.2f" % right_slope

chart = ax[1]
chart.set_title('Tail Exponent');
chart.scatter(left_x, left, color='blue', label='Left Tail')
chart.scatter(right_x, right, color='red', label='Right Tail')
chart.plot([left_x[0], left_x[-1]],[left_line[0], left_line[-1]],'b-',label=formula_left)
chart.plot([right_x[0], right_x[-1]],[right_line[0], right_line[-1]],'r-',label=formula_right)
handles, labels = chart.get_legend_handles_labels()
chart.legend(handles, labels)
chart.grid();

mng = plt.get_current_fig_manager()
mng.resize(1280,960)

plt.show()
