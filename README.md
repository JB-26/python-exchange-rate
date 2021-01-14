### Python Currency Exchange Rate

Welcome to the Python Currency Exchange Rate program!

This program uses the following API - https://exchangeratesapi.io

The API in turn retrieves it's data from the European Central Bank.

Feel free to clone this repo and have fun!

### Modules used

* [requests](https://pypi.org/project/requests/)
    * Used to make GET requests to the API
* json
    * Used to deserialise data from the response
* datetime
    * Used to get the current date
* os
    * Used to get the current working directory
* [pandas](https://pandas.pydata.org/)
    * Used for data analysis
* [plotly](https://plotly.com/)
    * Used for making interactive graphs
* [cufflinks](https://github.com/santosjorge/cufflinks)
    * Used to connect pandas and cufflinks

### What does this program do?

This program allows a user to make requests to the Exchange Rates API (which uses the European Central Bank as it's source). The user can:
* Fetch today's exchange rates.
* Fetch exchange rates from a day in history.
* Fetch exchange rates between two dates.
* Export the results to a CSV file
* Export the mean of the selected currencies (when using data of where there are exchange rates between two dates)
* Perform data analysis and make a scatter plot graph (when fetching exchange rates between two dates)

### Use of Pandas
* When fetching exchange rates the program will create a DataFrame with pandas using the dictionary response from the API. This is so that the results can be sorted and for a scatter graph or a table (which is created using Plotly)
* The DataFrame will be exported to a CSV file
    * If you have gathered data between two historical dates - you have the option to export a CSV file of the average rates for each currency

### Use of Plotly
Plotly is used to create interactive graphs. Each graph is saved as a HTML file.
* A table is created when current data or historical data for a specified day is used
* A scatter graph is created when retrieving historical data between two dates

**Warning!** If you request a large amount of historical data between two dates, this can result in long load times for the graph to be displayed.

