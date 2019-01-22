import importlib
import main_functions2
import time
import matplotlib.pyplot as plt


# Reload external modules.
# importlib.reload(main_functions2)





# Run the main function.
main_functions2.run_analysis(2000, 1, 1,'TSLA', 5, 4, 'Close')





# Identify the actual return for each combination of years. 
def identify_years():
    for i in range(1,8):
        for j in range(1,8):
            main_functions2.run_analysis(2000,1,1,'TSLA',i,j,'Close')


# identify_years()


# Perform the first test (add noise)
def test1(iterations):
    our_days_before = 5
    our_days_after = 4
    start = time.time()
    for i in range(iterations):
        main_functions2.test1_analysis(2000, 1, 1,'TSLA', our_days_before, our_days_after, 'Close')
    
    print(main_functions2.list_of_returns)
    
    end = time.time()
    
    print("The time taken was: "+str(end-start))
    

    plt.hist(main_functions2.list_of_returns, bins='auto')  
    plt.title("What is the change in share price "+str(our_days_after)+" days after the price has dropped >= 10% in the last "+str(our_days_before)+" days.")
    plt.xlabel("%change in share price after "+str(our_days_after)+" days.",fontsize=14)
    plt.ylabel("Frequency",fontsize=14)
    # plt.xlim(xmin=0, xmax=40000)
    
    plt.show()

    main_functions2.list_of_returns.clear()

# test1(20)

# Perform the second test (resample the data)
def test2(iterations):
    our_days_before = 5
    our_days_after = 4
    start = time.time()
    for i in range(iterations):
        main_functions2.test2_analysis(2000, 1, 1,'TSLA', our_days_before, our_days_after, 'Close')
    
    print(main_functions2.list_of_returns)
    
    end = time.time()
    
    print("The time taken was: "+str(end-start))
    

    plt.hist(main_functions2.list_of_returns, bins='auto')  
    plt.title("What is the change in share price "+str(our_days_after)+" days after the price has dropped >= 10% in the last "+str(our_days_before)+" days.")
    plt.xlabel("%change in share price after "+str(our_days_after)+" days.",fontsize=14)
    plt.ylabel("Frequency",fontsize=14)
    # plt.xlim(xmin=0, xmax=40000)
    
    plt.show()

    main_functions2.list_of_returns.clear()

# test2(20)


# Perform the third test (gradually reduce the starting year)
def test3():
    our_days_before = 5
    our_days_after = 4
    
    years = [x for x in range(2010,2019)]

    for year in years:
        main_functions2.test3_analysis(year, 1, 1,'TSLA', our_days_before, our_days_after, 'Close')
    
    print(main_functions2.list_of_returns)
    

    plt.plot(years, main_functions2.list_of_returns, linewidth=5)  
    plt.title("What is the change in share price "+str(our_days_after)+" days after the price has dropped >= 10% in the last "+str(our_days_before)+" days.")
    plt.xlabel("Starting Year",fontsize=14)
    plt.ylabel("Actual Return",fontsize=14)
    plt.show()

    main_functions2.list_of_returns.clear()

# test3()





