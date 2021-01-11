#import modules
import requests as req
from json import loads
import datetime
import os
#Data Science modules
import pandas as pd
import plotly.express as px
import cufflinks as cf

#allows cufflinks to be used offline
cf.go_offline()

def setBase():
    '''
    Function for setting the base currency
    '''

    while True:
        print('Please enter the currency you wish to use as the base currency in the form of a three character string (i.e. GBP, JPY, USD)')

        base = input('Input base currency - ').upper()

        if len(base) > 3:
            print("That's too long! Please enter a three character string and try again!")
        elif len(base) < 3:
            print("That's too short! Please enter a three character string and try again!")
        elif len(base) == 3:
            print(f"You have selected - {base}")
            return base

def setCurrencyCompare():
    '''
    Function for setting the currencies to compare against
    '''

    while True:
        print('Please enter the currency you wish to compare against in the form of a three character string (i.e. GBP, JPY, USD)')
        print('You can enter multiple currencies using a comma after the first currency (i.e. JPY,GBP,USD)')
        print('Or you can leave this blank and hit enter to return ALL currencies')

        currency = input('Input currency - ').upper()

        return currency

def fetchRates():
    '''
    Function for deciding which rates to fetch from the API
    '''

    while True:
        print('Please enter which rates you would like to fetch')
        print('1 - latest rates')
        print('2 - historical rates (set date)')
        print('3 - historical rates (time period between two dates)')
        print('5 - return to main menu')

        choice = int(input('Enter your choice - '))

        if choice == 1:
            latestRates()
        elif choice == 2:
            historicalRatesSet()
        elif choice == 3:
            historicalRatesPeriod()
        elif choice == 5:
            print('Returning to main menu')
            break
        else:
            print(f'{choice} is invalid, please try again!')

def latestRates():
    '''
    Function for getting the latest rates from the API
    '''
    baseCurrency = setBase()
    compareCurrency = setCurrencyCompare()

    print(f'Now getting latest rates for {baseCurrency} as of {datetime.datetime.now()}')

    #Get data
    response = req.get(url=f'https://api.exchangeratesapi.io/latest?base={baseCurrency}&symbols={compareCurrency}')
    #Deserialise response into Python dictionary
    responseDict = loads(response.text)
    #the response has multiple dictionaries
    exchangeDict = responseDict['rates']
    print('Complete!')
    print('Current exchange rates')
    currencyList = []
    valueList = []
    for key,value in exchangeDict.items():
        #prints out the keys and values (up to 2 decimal places)
        #print(f'{key} - {value:.2f}')
        currencyList.append(key)
        valueList.append(f'{value:.2f}')
    completeDict = {'Currency Name':currencyList, 'Exchange Rate':valueList}
    #make a dataframe
    df = pd.DataFrame(completeDict)
    df = df.sort_values(by='Currency Name')
    print(df)
    print('Printing results to CSV file...')
    df.to_csv(f'latest-{datetime.datetime.now()}-{baseCurrency}.csv',index=False)
    print(f'CSV created! Written to {os.getcwd()}')
    print(f'File is called - latest-{datetime.datetime.now()}-{baseCurrency}')
    fig = px.bar(data_frame=df,x='Currency Name', y='Exchange Rate', title=f'Latest rates on {datetime.datetime.now()} for {baseCurrency}')
    fig.show()
    

def historicalRatesSet():
    '''
    Function for getting historical rates from the API (on a set date)
    '''
    while True:
        try:
            print('NOTE: The furthest you can go back to is 1999!')

            year = setYear()
            
            month = setMonth()

            day = setDay()
            break
        except ValueError:
            print('Incorrect value detected! Please try again!')
    
    baseCurrency = setBase()
    compareCurrency = setCurrencyCompare()

    currencyList = []
    valueList = []
    historicalDate = f'{day}-{month}-{year}'

    print(f'Now fetching exchange rates for {baseCurrency} on the following date: {day}-{month}-{year}')
    #Get data
    response = req.get(url=f'https://api.exchangeratesapi.io/{year}-{month}-{day}?base={baseCurrency}&symbols={compareCurrency}')
    #Deserialise response into Python dictionary
    responseDict = loads(response.text)
    #the response has multiple dictionaries
    exchangeDict = responseDict['rates']
    print('Complete!')
    print(f'Exchange rate for {baseCurrency} on {day}-{month}-{year}')
    for key,value in exchangeDict.items():
        currencyList.append(key)
        valueList.append(f'{value:.2f}')

    completeDict = {'Currency Name':currencyList, 'Exchange Rate':valueList}
    #make a dataframe
    df = pd.DataFrame(completeDict)
    df = df.sort_values(by='Currency Name')
    print(df)
    print('Printing results to CSV file...')
    df.to_csv(f'historical-{historicalDate}-{baseCurrency}.csv',index=False)
    print(f'CSV created! Written to {os.getcwd()}')
    print(f'File is called - historical-{historicalDate}-{baseCurrency}')
    fig = px.bar(data_frame=df,x='Currency Name', y='Exchange Rate')
    fig.show()

def historicalRatesPeriod():
    '''
    Function for getting historical rates from the API (on a time period)
    '''

    while True:
        try:
            print('NOTE: Creating start date')
            print('NOTE: The furthest you can go back to is 1999!')

            year = setYear()
            
            month = setMonth()

            day = setDay()

            startDate = f'{year}-{month}-{day}'
            break
        except ValueError:
            print('Incorrect value detected! Please try again!')
    
    while True:
        try:
            print('NOTE: Creating end date')
            print('NOTE: The furthest you can go back to is 1999!')

            year = setYear()
            
            month = setMonth()

            day = setDay()

            endDate = f'{year}-{month}-{day}'
            break
        except ValueError:
            print('Incorrect value detected! Please try again!')
    
    baseCurrency = setBase()
    compareCurrency = setCurrencyCompare()

    print(f'Now fetching exchange rates for {baseCurrency} between the following dates: {startDate} - {endDate}')
    #Get data
    response = req.get(url=f'https://api.exchangeratesapi.io/history?start_at={startDate}&end_at={endDate}&base={baseCurrency}&symbols={compareCurrency}')
    #Deserialise response into Python dictionary
    responseDict = loads(response.text)
    #the response has multiple dictionaries
    exchangeDict = responseDict['rates']
    print('Complete!')
    
    df = pd.DataFrame(exchangeDict)
    df = df.reindex(sorted(df.columns), axis=1)
    print(df)
    print('Printing results to CSV file...')
    df.to_csv(f'historical-{startDate}-{endDate}-{baseCurrency}.csv',index=True)
    print(f'CSV created! Written to {os.getcwd()}')
    print(f'File is called - historical-{startDate}-{endDate}-{baseCurrency}')

    fig = px.line(data_frame=df, title=f'Historical rates between {startDate} - {endDate} for {baseCurrency}')
    fig.show()

def setYear():
    '''
    Function for setting the year from user
    '''
    while True:
        try:
            print('Please enter the year (as a numerical value)')
            year = int(input('Enter the year - '))

            if year < 1999:
                print('Please enter a valid year!')
            else:
                return year
        except ValueError:
            print('Incorrect value detected! Please try again!')

def setMonth():
    '''
    Function for setting the month from user
    '''
    while True:
        try:
            print('Please enter the month (as a numerical value)')
            month = int(input('Enter the month - '))

            if month < 1 or month > 12:
                print('Please enter a valid month!')
            else:
                return month
        except ValueError:
            print('Incorrect value detected! Please try again!')

def setDay():
    '''
    Function for setting the day from user
    '''
    while True:
        try:
            print('Please enter the day (as a numerical value)')
            day = int(input('Enter the day - '))

            if day < 1 or day > 31:
                print('Please enter a valid day!')
            else:
                return day
        except ValueError:
            print('Incorrect value detected! Please try again!')

def main():
    '''
    The main function for running the program
    '''

    while True:
        print('Welcome to the Currency Exchange Program!')
        print('Enter the character inbetween the parentheses')

        print('(F)etch rates')
        print('(V)iew configuration')
        print('(A)bout')
        print('(Q)uit')


        choice = input('Enter your choice - ').upper()

        if choice == 'F':
            fetchRates()
        elif choice == 'A':
            print('The currency exchange program uses the foreign exchange rates API (https://exchangeratesapi.io/) which gets data from the European Central Bank.')
        elif choice == 'Q':
            print('Goodbye!')
            break
        else:
            print(f"{choice} is invalid! Please try again!")

main()