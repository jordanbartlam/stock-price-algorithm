import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pandas_datareader.data as web
import random


# Define the variables. 
list_of_returns = []

def find_num_days(year, month, day, stock_ticker, number_of_days_before, type_of_price_data, data_source='yahoo'):
    
    # Define the required variables.
    start = dt.datetime(year,month,day)
    end = dt.datetime.today()
    type_of_price_data_minus_days = type_of_price_data + ' (T-'+str(number_of_days_before)+')'
    percent_change_before = '%change(T,T-'+str(number_of_days_before)+')'
    price_after_number_days = str(type_of_price_data) + ' (T+#days)'
    
    
    # Generate a datatable for Tesla's stock.
    df = web.DataReader(stock_ticker,data_source,start,end)
    
    
    
    # Make our new datatable for the chosen type of price data. 
    # Create the column for 'type_of_price_data' (T-3)
    df2 = df[type_of_price_data]
    df3 = df2.reset_index()
    df4 = df3[type_of_price_data].shift(-number_of_days_before)
    df5 = df3.assign((type_of_price_data) = df4)
    df5.rename(columns={'type_of_price_data': type_of_price_data_minus_days}, inplace=True)

  
    # Create the column for %change(T,T-3)
    df5[percent_change_before] = (((df5[type_of_price_data]-df5[type_of_price_data_minus_days])/df5[type_of_price_data_minus_days])*100)
    df5.set_index('Date',inplace=True)
    
    # Create a column displaying the threshold level that price needs to reach to then sell. 
    df5['Threshold'] = (df5[type_of_price_data]*1.15)
    
    # Check if over the last 3 days there has been more than a 10% price drop.
    df6 = df5.loc[df5[percent_change_before] < -10]
    df7 = df6.copy()
    
    # Create columns showing how long it takes to rebound past the threshold value and the price it rebounds to. 
    
    days_til_threshold_list = []
    price_after_number_days_list = []
    date_of_exit_list = []
    for index, value in df6['Threshold'].items():
        for i, row in df5.iterrows():
            if (i>index) and (df6.loc[index,'Threshold'] <= df5.loc[i,type_of_price_data]):
                days_til_threshold_list.append((i-index).days)
                price_after_number_days_list.append(df5.loc[i,type_of_price_data])
                # date_of_exit_list.append(i.date())
                date_of_exit_list.append(i)
                break
    
    while len(days_til_threshold_list) < len(df6.index):
        days_til_threshold_list.append(0)
        
    while len(price_after_number_days_list) < len(df6.index):
        price_after_number_days_list.append(0)
        
    while len(date_of_exit_list) < len(df6.index):
        date_of_exit_list.append(0)
        
    df7['Number of Days'] = days_til_threshold_list
    df7[price_after_number_days] = price_after_number_days_list
    df7['Date of Exit'] = date_of_exit_list
    
    global df8
    
    df8 = df7.round(2)
    df8['Date of Exit'] = date_of_exit_list
    
    
    days_til_threshold_list.clear()
    price_after_number_days_list.clear()
    date_of_exit_list.clear()
    
    
    # Create a column showing the distance between dates. 
    
    df8.reset_index(inplace=True)
    df8['Days until next Date'] = ((df8['Date'].shift(-1)) - df8['Date']).dt.days
    df8.set_index('Date', inplace=True)
    df8['Days until next Date'].fillna(0, inplace=True)
    
    # Create a column showing the percentage increase in Close between Close (T+#days) and Close (T).
    
    df8['%change(T,T+days)'] = (((df8[price_after_number_days]-df8[type_of_price_data])/df8[type_of_price_data])*100)


    # print(df8)
      
      
      
      
    # Plot a histogram of distance between dates vs frequency. 
 
    # global df8_list
    # df8_list = df8['Days until next Date'].tolist()
        
    # plt.hist(df8_list) 
    # plt.title("Time between dates when share price drops by 10% or more.")
    # plt.xlabel("Number of days",fontsize=14)
    # plt.ylabel("Frequency",fontsize=14)
        
    # plt.show()
    
    
    # Mean return on each trade is 17%.
    # print(np.mean(df8["%change(T,T+days)"]))
    

    # Find the dates when you are able to invest. 
    find_burst_size_count(burst_size=2, burst_size_min=7)


    # Calculate the return using conditional probability. 
    compute_return(weight_1=0.3, weight_2=0.1, weight_3=0.3, weight_4=0.05, weight_5=0.05, weight_6=0.1, weight_rest=0.1)
    
    
    
    
find_num_days(2000, 1, 1,'TSLA', 5, 'Close')




def find_burst_size_count(burst_size, burst_size_min):
    
    df8.reset_index(inplace=True)
    number_of_times_can_invest = []
    
    for i, r in df8.iterrows():
        if i==0 or (df8.loc[(i-1), 'Date of Exit'] < (df8.loc[(i), 'Date'])):
            number_of_times_can_invest.append(i)
    
    # Find the number of days for each burst. 
    days_in_burst = [number_of_times_can_invest[i] - number_of_times_can_invest[i-1] for i in range(1,len(number_of_times_can_invest))]
    
    # Percent of times that the size of the burst is:
    # 1:
    print('The percentage of bursts of length '+str(burst_size)+' days was '+str((days_in_burst.count(burst_size)/len(days_in_burst))*100)+'%.')

    # More than 7 days:
    print('The percentage of bursts over length '+str(burst_size_min)+' days was '+str(((sum(i>7 for i in days_in_burst))/len(days_in_burst))*100)+'%.')
    
    df8.set_index('Date', inplace=True)



def compute_return(weight_1=0.3, weight_2=0.1, weight_3=0.3, weight_4=0.05, weight_5=0.05, weight_6=0.1, weight_rest=0.1):
    
    df8.reset_index(inplace=True)
    total_return = 1
    number_in_burst = 1
    mini_returns = []
    amount_invested = 0
    total_invested = 0
    
    for i, r in df8.iterrows():
        if i==0 or (df8.loc[(i-1), 'Date of Exit'] < (df8.loc[(i), 'Date'])):
            number_in_burst = 1
            number_in_burst += 1
            total_return += -total_invested + sum(mini_returns)
            mini_returns.clear()
            amount_invested = weight_1 * total_return
            mini_returns.append(amount_invested * (1+((df8.loc[i, '%change(T,T+days)'])/100)))
            total_invested = amount_invested
            
        elif number_in_burst == 2:
            amount_invested = weight_2 * total_return
            mini_returns.append(amount_invested * (1+((df8.loc[i, '%change(T,T+days)'])/100)))
            number_in_burst += 1
            total_invested += amount_invested
        
        elif number_in_burst == 3:
            amount_invested = weight_3 * total_return
            mini_returns.append(amount_invested * (1+((df8.loc[i, '%change(T,T+days)'])/100)))
            number_in_burst += 1
            total_invested += amount_invested
            
        elif number_in_burst == 4:
            amount_invested = weight_4 * total_return
            mini_returns.append(amount_invested * (1+((df8.loc[i, '%change(T,T+days)'])/100)))
            number_in_burst += 1
            total_invested += amount_invested
            
        elif number_in_burst == 5:
            amount_invested = weight_5 * total_return
            mini_returns.append(amount_invested * (1+((df8.loc[i, '%change(T,T+days)'])/100)))
            number_in_burst += 1
            total_invested += amount_invested
        
        elif number_in_burst == 6:
            amount_invested = weight_6 * total_return
            mini_returns.append(amount_invested * (1+((df8.loc[i, '%change(T,T+days)'])/100)))
            number_in_burst += 1
            total_invested += amount_invested
        
        elif number_in_burst == 7:
            amount_invested = weight_rest * total_return
            mini_returns.append(amount_invested * (1+((df8.loc[i, '%change(T,T+days)'])/100)))
            number_in_burst += 1
            total_invested += amount_invested
      
    # Convert this to the percentage return:
    overall_return = ((total_return - 1)/1)*100
    
    df8.set_index('Date', inplace=True)
    
    print("\nThe overall return was: "+str(round(overall_return,2))+"%.")
 
