import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import pandas as pd
import pandas_datareader.data as web
import finance_functions as ff



# Change the style of the plots.
style.use('ggplot')



# Define the variables. 
start = dt.datetime(2000,1,1)
end = dt.datetime.today()
stock_ticker = 'TSLA'
data_source = 'yahoo'
type_of_price_data = 'Close'
close_minus_three = 'Close (T-3)'



# Generate a datatable for Tesla's stock.
df = web.DataReader(stock_ticker,data_source,start,end)



# Make our new datatable for the chosen type of price data. 
# Create the column for Close (T-3)
df2 = df[type_of_price_data]
df3 = df2.reset_index()
df4 = df3['Close'].shift(-3)
df5 = df3.assign((close_minus_three) = df4)
df5.rename(columns={'close_minus_three': 'Close (T-3)'}, inplace=True)

# Create the column for Close (T+2)
df6 = df5['Close'].shift(2)
df7 = df5.assign((close_plus_two) = df6)
df7.rename(columns={'close_plus_two': 'Close (T+2)'}, inplace=True)

# Create the column for %change(T,T-3)
df7['%change(T,T-3)'] = (((df7['Close']-df7['Close (T-3)'])/df7['Close (T-3)'])*100)

# Create the column for %change(T,T+2)
df7['%change(T,T+2)'] = (((df7['Close (T+2)']-df7['Close'])/df7['Close'])*100)
df7.set_index('Date',inplace=True)


# Check if over the last 3 days there has been more than a 10% price drop.

# for index, value in df7['%change(T,T-3)'].head(100).items():
#     if value < -10:
        # print(df7.loc[[index]])
        # print('\nOn the '+str(index)+' the share price had fallen '+str(value)+'% from what it was 3 days before.')
        # print('In the succeeding 2 days, the share price had a % change of: '+str(df7['%change(T,T+2)'].loc[index])+'%.')




df8 = df7.loc[df7['%change(T,T-3)'] < -10]
# print(df8.shape)
# print(df8.head(10))
# print(df8['%change(T,T+2)'])



# Plot a histogram of the %change(T,T+2) vs the frequency. 

df8_list = df8['%change(T,T+2)'].tolist()

plt.hist(df8_list, bins=20) # Each bin represents 2.19%. 
plt.title("What is the change in share price 2 days after the price has dropped >= 10%?")
plt.xlabel("%change in share price after 2 days.",fontsize=14)
plt.ylabel("Frequency",fontsize=14)

plt.show()

# Calculate the mean and standard deviation. 
print(np.mean(df8_list))
print(np.std(df8_list))


# Calculate the amount we would have earned if we had followed this strategy.

# ff.calc_return()

# Calculate the percentage of returns which are positive. 

ff.percentage_positive()




