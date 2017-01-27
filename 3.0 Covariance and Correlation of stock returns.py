# Section 3 : Covariance and Correlation of daily returns
#
# Demonstration of the calculation of covariance and correlation.
#
# Covariance is an indicator of how variables move in relation to each other. The formula is
#     E[(x - E[X])(y - E[Y])]
#
# Examining this formial, a residual in X is multiplied by its corresponding residual in Y. The result
# of each multiplication will be positive if both residuals move in the same direction, and negative if 
# they move in opposite directions. The larger the magnitude of the result, the more
# it contributes to the final value of the covariance (So larger moves could skew the result). The covariance tells us 
# nothing about the amount by which they move together, only if they tend to move in the same direction or not.
#
# To calculate a measure of how much they move together, we normalise the covariance by dividing by the std(X) * std(Y).
# This gives us the Correlation.
#
# When we calculate the covariance of X with X, we get the variance of X.
#
# The i,j elements of a Covariance Matrix give the cov(i,j). The diagnal is therefore always
# the values for the variances of the variables. This is why it is sometimes called the variance-covariance matrix. 
#
# The correlation of a variable with a time-lagged version of itself is called the Autocorrelation, i.e. AC(k) This gives an
# indication of the movement of X in relation to X - k. In other words, this is a formal description of phenomena such as
# momentum (AC = +ve) and mean reversion (AC = -ve).
# 

from numpy import *
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
from finance import *
from stockUtils import *

result = loadPair(STOCK_ROOT+'/2012/^DJI.csv', STOCK_ROOT+'/2012/^GSPC.csv', "01/05/2000", "01/05/2010");
      
prices1 = result['data1']
prices2 = result['data2']
dates = result['date']

prices1 = log(gross_return(prices1));
prices2 = log(gross_return(prices2));

# Manually calculate covariance for entire sample, then do it with numpy
meanX = mean(prices1);
meanY = mean(prices2);

residualX = prices1 - meanX;
residualY = prices2 - meanY;

manual_cov = sum(residualX * residualY) / (len(prices1) - 1)
var_x = sum(residualX * residualX) / (len(prices1) - 1)
var_y = sum(residualY * residualY) / (len(prices1) - 1)
std_x = sqrt(var_x)
std_y = sqrt(var_y)
manual_corr = manual_cov / (std_x * std_y)

# Now do it with numpy to check the values
M = vstack((prices1, prices2));
np_cov = cov(M)[0][1]
np_corr = corrcoef(M)[0][1]

print ("X: Mean = %.4f, StdDev = %.4f" % (meanX, std_x));
print ("Y: Mean = %.4f, StdDev = %.4f" % (meanY, std_y));
print ("Manual Covariance = %.4f" % manual_cov);
print ("Numpy Covariance = %.4f" % np_cov);
print ("Manual Correlation = %.4f" % manual_corr);
print ("Numpy Correlation = %.4f" % np_corr);
print ("Covariance Matrix = ")
print ("                          X        Y")
print ("                  X [ %.6f, %.6f ]" % (var_x,manual_cov))
print ("                  Y [ %.6f, %.6f ]" % (manual_cov,var_y))

