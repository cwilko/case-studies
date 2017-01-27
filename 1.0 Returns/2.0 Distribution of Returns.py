#  A study of the distribution of stock returns
#
#  As can be seen in this study, stock returns do not fit well to a normal distribution.
#  The actual distribution appears to contain more data points in the tails and less in the 
#  body than the normal distribution.
#
#  This study shows the fit of stock returns to the class of stable distributions. This class
#  of distributions has paramters : 
#
#  alpha : Describes the shape of the distribution
#  beta  : Describes the skewness of the distributions
#  gamma : The scale 
#  delta : The shift
#
#  Any stable distribution, X, can be standardised by : X_Standard = (X - delta) / gamma.
#
#  The PDF & CDF of stable distributions have no closed form (i.e. no formula). They can only
#  be calculated using numerical methods.
#

import matplotlib.pyplot as plt
from finance import *
from stockUtils import *
import stable as stable

M = loadStockData(STOCK_ROOT+'/2012/^GSPC.csv', "01/05/2000", "01/05/2010");

close_prices = M['Close']
open_prices = M['Open']
dates = M['Date']

log_returns = log(gross_return(close_prices));

x_standard = linspace(-40,40,2001);
x_standard_diff = (x_standard[1] - x_standard[0]);

# Actual PDF
n, bars = histogram(log_returns, 100, normed=True);
bars = bars[0:len(bars)-1]
barWidth = bars[1] - bars[0]

# Actual CDF
actual_x = sort(log_returns)
actual_cdf = zeros(len(log_returns))
actual_cdf[:] = (1.0/len(log_returns))
actual_cdf = cumsum(actual_cdf)

# 1 : Fit to Normal Distribution

alpha,beta,gamma,delta = stable.fit(log_returns, alpha=2.0, beta=0.0); 

# Transform the x-scale to standardised form (i.e. gamma = 1) to get the relevant pdf values.
# Plot scaled pdf values at original x values to scale out the pdf.

normal_x = (x_standard * gamma) + delta;
x_diff = normal_x[1] - normal_x[0];

pdf = stable.pdf(x_standard, alpha, beta);
normal_pdf = pdf * x_standard_diff / x_diff

normal_cdf = stable.cdf(x_standard, alpha, beta);

# 2 : Fit to Cauchy Distribution

alpha,beta,gamma,delta = stable.fit(log_returns, alpha=1.0, beta=0.0); 

cauchy_x = (x_standard * gamma) + delta;
x_diff = cauchy_x[1] - cauchy_x[0];

pdf = stable.pdf(x_standard, alpha, beta);
cauchy_pdf = pdf * x_standard_diff / x_diff

cauchy_cdf = stable.cdf(x_standard, alpha, beta);

# 3 : Fit to Levy Distribution

alpha,beta,gamma,delta = stable.fit(log_returns, alpha=0.5, beta=0.0); 

levy_x = (x_standard * gamma) + delta;
x_diff = levy_x[1] - levy_x[0];

pdf = stable.pdf(x_standard, alpha, beta);
levy_pdf = pdf * x_standard_diff / x_diff

levy_cdf = stable.cdf(x_standard, alpha, beta);

# 4 : Fit to Stable Distribution

alpha,beta,gamma,delta = stable.fit(log_returns); 

stable_x = (x_standard * gamma) + delta;
x_diff = stable_x[1] - stable_x[0];

pdf = stable.pdf(x_standard, alpha, beta);
stable_pdf = pdf * x_standard_diff / x_diff

stable_cdf = stable.cdf(x_standard, alpha, beta);


# Plot
fig, ax = plt.subplots(2)

chart = ax[0]
chart.set_title('Probability Density of Returns');
chart.bar(bars, n, width=barWidth);
chart.plot(normal_x, normal_pdf , 'g', label='Normal');
chart.plot(cauchy_x, cauchy_pdf , 'cyan', label='Cauchy');
chart.plot(levy_x, levy_pdf , 'y', label='Levy');
chart.plot(stable_x, stable_pdf , 'r', label='Stable');
chart.set_xlim([-0.1, 0.1])
chart.set_ylim([0, 80])
handles, labels = chart.get_legend_handles_labels()
chart.legend(handles, labels)
chart.grid();

# Plot : CDF
chart = ax[1]
chart.set_title('Cumulative Distribution of Returns');
chart.scatter(actual_x, actual_cdf)
chart.plot(normal_x, normal_cdf , 'g', label='Normal');
chart.plot(cauchy_x, cauchy_cdf , 'cyan', label='Cauchy');
chart.plot(levy_x, levy_cdf , 'y', label='Levy');
chart.plot(stable_x, stable_cdf , 'r', label='Stable');
chart.set_xlim([-0.1, 0.1])
chart.set_ylim([0, 1])
handles, labels = chart.get_legend_handles_labels()
chart.legend(handles, labels)
chart.grid();

mng = plt.get_current_fig_manager()
mng.resize(1280,960)

plt.show()