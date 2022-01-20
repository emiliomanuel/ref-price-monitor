__author__ = "Emilio Manuel"
__copyright__ = "Copyright (C) 2022 Emilio Manuel"
__license__ = "MIT License"
__version__ = "1.0"

from dataclasses import dataclass
import os
import re
import requests
import sys
import time

# class to store ticker data
@dataclass
class Ticker():
    symbol: str
    previous_price: float

    # function to update previous price
    def update_previous_price(self, price):
        self.previous_price = price

# store api url
api_url = "https://sodaki.com/api/last-tvl"
# store Ticker objects
ticker_list = []

# function to clear screen
def clear():
    os.system("cls")

# function to get current price
def get_current_price(response, symbol):
    price = -1
    # iterate through the json object from api
    for ticker_data in response:
        ftInfo = ticker_data["ftInfo"]
        current_symbol = ftInfo["symbol"]
        if current_symbol == symbol:
            price = float(ticker_data["price"])
            break
    return price

def main():
    # notify user what the script is for
    print("This is a script to display prices on Ref.finance by getting data from the Sodaki api.")
    
    # prompt user for tickers
    while True:
        # make sure that the latest data is used
        response = requests.get(api_url)
        json = response.json()
        
        # enter ticker data
        symbol = input("Enter token symbol or 0 if done: ").upper()
        if symbol == "0":
            # close the connection
            response.close()
            break

        # get the current price
        current_price = get_current_price(json, symbol)

        # create ticker object if current price is greater than -1
        if current_price > -1:
            new_ticker = Ticker(symbol, current_price)
            ticker_list.append(new_ticker)
        # if coin wasn't found, show message
        else:
            print(f"Ticker with symbol {symbol} was not found.")
            
        # close the connection before updating prices
        response.close()
        
    # clear the screen
    clear()
        
    print("Press CTRL-C to exit.")

    # update previous prices every 15 seconds
    while True:
        try:
            # make sure that the latest data is used
            response = requests.get(api_url)
            json = response.json()
            print()
            print("Prices:")
            
            for ticker in ticker_list:
                # get the current price
                current_price = get_current_price(json, ticker.symbol)
                
                # calculate difference
                price_diff = current_price - ticker.previous_price

                # update the previous price
                ticker.update_previous_price(current_price)
                
                # print the ticker information
                print(f"{ticker.symbol}: ${current_price} ({price_diff})")
                
            # close the connection
            response.close()
            
            # wait 15 seconds before updating
            time.sleep(15)
        except KeyboardInterrupt:
            # close the program
            print("Exiting...")
            time.sleep(2)
            sys.exit(0)

if __name__ == "__main__":
    main()