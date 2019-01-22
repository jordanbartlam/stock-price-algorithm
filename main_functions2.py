import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pandas_datareader.data as web
import random


# Define the variables. 
# start = dt.datetime(2000,1,1)
# stock_ticker = 'TSLA'
# number_of_days_before = 3
# number_of_days_after = 2
# type_of_price_data = 'Close'
list_of_returns = []

def run_analysis(year, month, day, stock_ticker, number_of_days_before, number_of_days_after, type_of_price_data, data_source='yahoo'):
    
    # Define the required variables.
    start = dt.datetime(year,month,day)
    end = dt.datetime.today()
    type_of_price_data_minus_days = type_of_price_data + ' (T-'+str(number_of_days_before)+')'
    type_of_price_data_plus_days = type_of_price_data + ' (T+'+str(number_of_days_after)+')'
    percent_change_before = '%change(T,T-'+str(number_of_days_before)+')'
    percent_change_after = '%change(T,T+'+str(number_of_days_after)+')'
    
    # Generate a datatable for Tesla's stock.
    df = web.DataReader(stock_ticker,data_source,start,end)
    
    
    # Make our new datatable for the chosen type of price data. 
    # Create the column for 'type_of_price_data' (T-3)
    df2 = df[type_of_price_data]
    df3 = df2.reset_index()
    df4 = df3[type_of_price_data].shift(-number_of_days_before)
    df5 = df3.assign((type_of_price_data) = df4)
    df5.rename(columns={'type_of_price_data': type_of_price_data_minus_days}, inplace=True)
    
    # Create the column for Close (T+2)
    df6 = df5[type_of_price_data].shift(number_of_days_after)
    df7 = df5.assign((type_of_price_data) = df6)
    df7.rename(columns={'type_of_price_data': type_of_price_data_plus_days}, inplace=True)
    
    # Create the column for %change(T,T-3)
    df7[percent_change_before] = (((df7[type_of_price_data]-df7[type_of_price_data_minus_days])/df7[type_of_price_data_minus_days])*100)
    
    # Create the column for %change(T,T+2)
    df7[percent_change_after] = (((df7[type_of_price_data_plus_days]-df7[type_of_price_data])/df7[type_of_price_data])*100)
    df7.set_index('Date',inplace=True)
    
    
    # Check if over the last 3 days there has been more than a 10% price drop.
    
    df8 = df7.loc[df7[percent_change_before] < -10]
    # print(df8.shape)
    # print(df8.head(10))
    # print(df8['%change(T,T+2)'])
    
    
    
    # Plot a histogram of the %change(T,T+2) vs the frequency. 
    global df8_list
    df8_list = df8[percent_change_after].tolist()
    
    # plt.hist(df8_list, bins=20) # Each bin represents 2.19%. 
    # plt.title("What is the change in share price "+str(number_of_days_after)+" days after the price has dropped >= 10%?")
    # plt.xlabel("%change in share price after "+str(number_of_days_after)+" days.",fontsize=14)
    # plt.ylabel("Frequency",fontsize=14)
    
    # plt.show()
    
    # Print the number of days before and after. 
    print("\nNumber of days before: "+str(number_of_days_before))
    print("Number of days after: "+str(number_of_days_after))
    
    # Calculate the mean and standard deviation. 
    print("\nThe mean is: "+str(round(np.mean(df8_list),2)))
    print("\nThe standard deviation is: "+str(round(np.std(df8_list),2)))
    
    
    # Calculate the amount we would have earned if we had followed this strategy.
    
    print("\nIf we had followed this strategy we would have earned: "+str(round(calc_return(),2))+"%")
    
    # Calculate the percentage of returns which are positive. 
    
    print("\nIn the days after the price drop, we found that "+str(round(percentage_positive(),2))+"% of results were positive.\n")



def percentage_positive():
    
    positive_nums = [r for r in df8_list if r>0]
    
    return ((len(positive_nums))/(len(df8_list))*100)


def calc_return():
    overall_return = 1
    for r in df8_list:
        overall_return *= (1+(r/100))
    percentage_return = (overall_return - 1)*100
    return percentage_return


def test1_analysis(year, month, day, stock_ticker, number_of_days_before, number_of_days_after, type_of_price_data, data_source='yahoo'):
    
    # Define the required variables.
    start = dt.datetime(year,month,day)
    end = dt.datetime.today()
    noise_level = 0.01
    noise_level_limit = 0.05
    type_of_price_data_minus_days = type_of_price_data + ' (T-'+str(number_of_days_before)+')'
    type_of_price_data_plus_days = type_of_price_data + ' (T+'+str(number_of_days_after)+')'
    percent_change_before = '%change(T,T-'+str(number_of_days_before)+')'
    percent_change_after = '%change(T,T+'+str(number_of_days_after)+')'
    
    # Generate a datatable for Tesla's stock.
    df = web.DataReader(stock_ticker,data_source,start,end)
    
     
    
    # Add 5% noise to the chosen type of data. 
    
    # Uniform Distribution:
    # df[type_of_price_data] = df[type_of_price_data].apply(lambda x: x+(x*random.uniform(noise_level_negative, noise_level_positive)))
    
    # Normal Distribution:
    df[type_of_price_data] = df[type_of_price_data].apply(lambda x: x+(x*(max(min(np.random.normal(0,noise_level),noise_level_limit),-noise_level_limit))))

    # Changed Code for two parallel columns. 
    # df['Adjusted Close'] = df[type_of_price_data].apply(lambda x: x+(x*(max(min(np.random.normal(0,noise_level),noise_level_limit),-noise_level_limit))))
    # print(df.loc[:,['Close','Adjusted Close']])
    # test1_analysis(2000, 1, 1,'TSLA', 5, 4, 'Close')

    # Make our new datatable for the chosen type of price data. 
    # Create the column for 'type_of_price_data' (T-3)
    df2 = df[type_of_price_data]
    df3 = df2.reset_index()
    df4 = df3[type_of_price_data].shift(-number_of_days_before)
    df5 = df3.assign((type_of_price_data) = df4)
    df5.rename(columns={'type_of_price_data': type_of_price_data_minus_days}, inplace=True)
    
    # Create the column for Close (T+2)
    df6 = df5[type_of_price_data].shift(number_of_days_after)
    df7 = df5.assign((type_of_price_data) = df6)
    df7.rename(columns={'type_of_price_data': type_of_price_data_plus_days}, inplace=True)
    
    # Create the column for %change(T,T-3)
    df7[percent_change_before] = (((df7[type_of_price_data]-df7[type_of_price_data_minus_days])/df7[type_of_price_data_minus_days])*100)
    
    # Create the column for %change(T,T+2)
    df7[percent_change_after] = (((df7[type_of_price_data_plus_days]-df7[type_of_price_data])/df7[type_of_price_data])*100)
    df7.set_index('Date',inplace=True)
    
    
    # Check if over the last 3 days there has been more than a 10% price drop.
    
    df8 = df7.loc[df7[percent_change_before] < -10]
    
  
    # Plot a histogram of the %change(T,T+2) vs the frequency. 
    global df8_list
    df8_list = df8[percent_change_after].tolist()
    
    # Calculate the amount we would have earned if we had followed this strategy.
    
    global list_of_returns
    our_return = calc_return()
    list_of_returns.append(our_return)
    



def test2_analysis(year, month, day, stock_ticker, number_of_days_before, number_of_days_after, type_of_price_data, data_source='yahoo'):
    
    # Define the required variables.
    start = dt.datetime(year,month,day)
    end = dt.datetime.today()
    type_of_price_data_minus_days = type_of_price_data + ' (T-'+str(number_of_days_before)+')'
    type_of_price_data_plus_days = type_of_price_data + ' (T+'+str(number_of_days_after)+')'
    percent_change_before = '%change(T,T-'+str(number_of_days_before)+')'
    percent_change_after = '%change(T,T+'+str(number_of_days_after)+')'
    
    # Generate a datatable for Tesla's stock.
    df = web.DataReader(stock_ticker,data_source,start,end)
    
    

    # Make our new datatable for the chosen type of price data. 
    # Create the column for 'type_of_price_data' (T-3)
    df2 = df[type_of_price_data]
    df3 = df2.reset_index()
    df4 = df3[type_of_price_data].shift(-number_of_days_before)
    df5 = df3.assign((type_of_price_data) = df4)
    df5.rename(columns={'type_of_price_data': type_of_price_data_minus_days}, inplace=True)
    
    # Create the column for Close (T+2)
    df6 = df5[type_of_price_data].shift(number_of_days_after)
    df7 = df5.assign((type_of_price_data) = df6)
    df7.rename(columns={'type_of_price_data': type_of_price_data_plus_days}, inplace=True)
    
    # Create the column for %change(T,T-3)
    df7[percent_change_before] = (((df7[type_of_price_data]-df7[type_of_price_data_minus_days])/df7[type_of_price_data_minus_days])*100)
    
    # Create the column for %change(T,T+2)
    df7[percent_change_after] = (((df7[type_of_price_data_plus_days]-df7[type_of_price_data])/df7[type_of_price_data])*100)
    df7.set_index('Date',inplace=True)
    
    # Select a random sample out of this dataframe to perform the analysis on. 
    
    df8 = df7.sample(frac=0.667)
    
    # Check if over the last 3 days there has been more than a 10% price drop.
    
    df9 = df8.loc[df8[percent_change_before] < -10]
    
    
    global df9_list
    df9_list = df9[percent_change_after].tolist()
    
    # Calculate the amount we would have earned if we had followed this strategy.
    
    global list_of_returns
    our_return = calc_return_test2()
    list_of_returns.append(our_return)

def calc_return_test2():
    overall_return = 1
    for r in df9_list:
        overall_return *= (1+(r/100))
    percentage_return = (overall_return - 1)*100
    return percentage_return




def test3_analysis(year, month, day, stock_ticker, number_of_days_before, number_of_days_after, type_of_price_data, data_source='yahoo'):
    
    # Define the required variables.
    start = dt.datetime(year,month,day)
    end = dt.datetime.today()
    type_of_price_data_minus_days = type_of_price_data + ' (T-'+str(number_of_days_before)+')'
    type_of_price_data_plus_days = type_of_price_data + ' (T+'+str(number_of_days_after)+')'
    percent_change_before = '%change(T,T-'+str(number_of_days_before)+')'
    percent_change_after = '%change(T,T+'+str(number_of_days_after)+')'
    
    # Generate a datatable for Tesla's stock.
    df = web.DataReader(stock_ticker,data_source,start,end)
    
    

    # Make our new datatable for the chosen type of price data. 
    # Create the column for 'type_of_price_data' (T-3)
    df2 = df[type_of_price_data]
    df3 = df2.reset_index()
    df4 = df3[type_of_price_data].shift(-number_of_days_before)
    df5 = df3.assign((type_of_price_data) = df4)
    df5.rename(columns={'type_of_price_data': type_of_price_data_minus_days}, inplace=True)
    
    # Create the column for Close (T+2)
    df6 = df5[type_of_price_data].shift(number_of_days_after)
    df7 = df5.assign((type_of_price_data) = df6)
    df7.rename(columns={'type_of_price_data': type_of_price_data_plus_days}, inplace=True)
    
    # Create the column for %change(T,T-3)
    df7[percent_change_before] = (((df7[type_of_price_data]-df7[type_of_price_data_minus_days])/df7[type_of_price_data_minus_days])*100)
    
    # Create the column for %change(T,T+2)
    df7[percent_change_after] = (((df7[type_of_price_data_plus_days]-df7[type_of_price_data])/df7[type_of_price_data])*100)
    df7.set_index('Date',inplace=True)
    
    
    # Check if over the last 3 days there has been more than a 10% price drop.
    
    df8 = df7.loc[df7[percent_change_before] < -10]
    
    
    global df8_list
    df8_list = df8[percent_change_after].tolist()
    
    # Calculate the amount we would have earned if we had followed this strategy.
    
    global list_of_returns
    our_return = calc_return()
    list_of_returns.append(our_return)




    