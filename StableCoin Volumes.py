import urllib.parse
import requests
import json
import pandas
import numpy as np


# PART 1 ------------------------------------------------------------------

# Retrieve daily volumes for all Stablecoin exchanges from Coingecko API (in USD)
# Includes data from Ethfinex, Coinsuper, Kyber Network, Bancor Network, Coinchangex, Switcheo, and Ethex

dai_api = 'https://api.coingecko.com/api/v3/coins/dai/market_chart?vs_currency=usd&days=365'
dai_json = requests.get(dai_api).json()
len_dai = len(dai_json['total_volumes']) #Find length of array (how many days it's been active)
dai_json2 = [None]*(366-len_dai) #init array with today's latest entries added after empty values (total of 366 slots in array for each coin)

for i in range(len_dai):
    dai_json2.append(dai_json['total_volumes'][i][1]) #Make the array auto-adjust

# Get volume data for Gemini Dollar (GUSD)
gusd_api = 'https://api.coingecko.com/api/v3/coins/gemini-dollar/market_chart?vs_currency=usd&days=365'
gusd_json = requests.get(gusd_api).json()
len_gusd = len(gusd_json['total_volumes']) 
gusd_json2 = [None]*(366-len_gusd)

for i in range(len_gusd):
    gusd_json2.append(gusd_json['total_volumes'][i][1])

# Get volume data for Tether (USDT)
usdt_api = 'https://api.coingecko.com/api/v3/coins/tether/market_chart?vs_currency=usd&days=365'
usdt_json = requests.get(usdt_api).json()
usdt_json2 = []

for i in range(366):
    usdt_json2.append(usdt_json['total_volumes'][i][1])

# Get volume data for USD Coin (USDC)
usdc_api = 'https://api.coingecko.com/api/v3/coins/usd-coin/market_chart?vs_currency=usd&days=365'
usdc_json = requests.get(usdc_api).json()
len_usdc = len(usdc_json['total_volumes']) 
usdc_json2 = [None]*(366-len_usdc)

for i in range(len_usdc):
    usdc_json2.append(usdc_json['total_volumes'][i][1])

# Get volume data for True USD (TUSD)
tusd_api = 'https://api.coingecko.com/api/v3/coins/true-usd/market_chart?vs_currency=usd&days=365'
tusd_json = requests.get(tusd_api).json()
len_tusd = len(tusd_json['total_volumes']) 
tusd_json2 = [None]*(366-len_tusd)

for i in range(len_tusd):
    tusd_json2.append(tusd_json['total_volumes'][i][1])


'''
# Get volume data for Havven (HAV)
havven_api = 'https://api.coingecko.com/api/v3/coins/havven/market_chart?vs_currency=usd&days=365'
havven_json = requests.get(havven_api).json()

# Get volume data for Paxos Standard (PAX)
paxos_api = 'https://api.coingecko.com/api/v3/coins/paxos-standard/market_chart?vs_currency=usd&days=365'
paxos_json = requests.get(paxos_api).json()
'''


#PART 2 -----------------------------------------------------------------------------------
from sklearn import linear_model
from sklearn.linear_model import LinearRegression
from bokeh.plotting import figure, show, output_file
from sklearn.model_selection import train_test_split
from bokeh.models import Legend

#Compare date by volume for each coin and put into a graph using bokeh
date = list(range(0, 366)) # Make a list of days from 0 to 366

# Create a regression using scikit
'''
# Make a 2d array of days. For scikit regressions, the x-axis must be 2d.
dates = []
for i in range (366):
    dates.append([i])

x_train, x_test, y_train, y_test = train_test_split(dates, dai_json2, test_size = .2)
reg = LinearRegression()
reg.fit(x_train, y_train)
accuracy = reg.score(x_test, y_test)
print(accuracy)

reg = linear_model.LinearRegression()
reg.fit(dates, dai_json2)
m = reg.coef_[0] #slope
b = reg.intercept_ #y-intercept
predicted_values = [reg.coef_*i + reg.intercept_ for i in dai_json2] # how to make this an array of regression values?
'''

# Create the figure p
p = figure(title = 'StableCoin Volumes', x_axis_label = 'One Year (Days)', y_axis_label = 'Volume (USD)', y_axis_type= "log", y_range = (0, 10**10), plot_height = 425, plot_width=1200)

#Plot each arraay vs date
p.step(date, dai_json2, color = 'black', alpha = 0.6, legend = "DAI") # Plot all volumes with blue circles
#p.line(x_train, reg.predict(x_train), line_color = 'black', alpha = .15) # Plot best fit line for all volumes

p.step(date, usdt_json2, color='darkgreen', alpha=0.6, legend = "Tether (USDT)") 

p.step(date, gusd_json2, color='darkturquoise', alpha=0.6, legend = "Gemini Dollar (GUSD)") 

p.step(date, usdc_json2, color='coral', alpha=0.5, legend = "USDCoin (USDC)")

p.step(date, tusd_json2, color='navy', alpha=0.45, legend = "TrueUSD (TUSD)") 

''' 
p.step(date, havven_json, color='silver', alpha=0.5, legend = "Havven (HAV)")

p.step(date, paxos_json, color='khaki', alpha=0.5, legend = "Paxos (PAX)")
'''

p.legend.location = 'top_left' #legend orientation

# Specify the name of the output file and show the result
output_file("StableCoinVolumes.html", title="StableCoin Volumes")
show(p)
