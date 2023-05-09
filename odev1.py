import numpy as np
import matplotlib.pyplot as plt

def calculate_option_value(option_type, is_long, strike_price, stock_price):
    if option_type == "Call":
        option_value = max(stock_price - strike_price, 0)
    else:
        option_value = max(strike_price - stock_price, 0)
    
    if not is_long:
        option_value *= -1
    
    return option_value

def calculate_stock_profit(initial_price, is_long ,stock_price, stock_quantity):
    profit = (stock_price - initial_price) * stock_quantity
    if not is_long:
        profit *= -1
    return profit    
    

def calculate_portfolio_value(option_details, stock_details, stock_price, stock_quantity):
    portfolio_value = 0
    for option in option_details:
        option_type, is_long, strike_price, option_value = option
        if is_long:
            portfolio_value += (calculate_option_value(option_type, is_long, strike_price, stock_price)-option_value)
        else:
            portfolio_value += -1*(calculate_option_value(option_type, is_long, strike_price, stock_price)-option_value)  
    for stock in stock_details:
        stock_type, initial_price = stock
        if stock_type == "Long":
            portfolio_value += calculate_stock_profit(initial_price, True, stock_price, 1)
        else:
            portfolio_value += calculate_stock_profit(initial_price, False, stock_price, 1)           

    return portfolio_value



def is_there_artbitrage(option_details, spot_price):
    count = 0
    for option in option_details:
        option_type, is_long, strike_price, option_value = option
        if option_type == "Call" and is_long == True and strike_price+option_value < spot_price:
            print("{0} tipindeki {1}. opsiyon arbitraj firsati sunuyor.".format(option_type, count+1))
        if option_type == "Put" and is_long == True and strike_price-option_value > spot_price:
            print("{0} tipindeki {1}. opsiyon arbitraj firsati sunuyor.".format(option_type, count+1))
        if option_type == "Call" and is_long == False and strike_price+option_value > spot_price:
            print("{0} tipindeki {1}. opsiyon arbitraj firsati sunuyor.".format(option_type, count+1))
        if option_type == "Put" and is_long == False and strike_price-option_value < spot_price:
            print("{0} tipindeki {1}. opsiyon arbitraj firsati sunuyor.".format(option_type, count+1))    
        count += 1 
    call_options = [option for option in option_details if option[0] == "Call"]
    call_options2 = [option for option in option_details if option[0] == "Call"]
    call_options.sort(key=lambda x: x[2])
    call_options2.sort(key=lambda x: x[3],reverse=True)
    if not call_options == call_options2:
        print("Call Option fiyatinda anormallik vardir.")
    put_options = [option for option in option_details if option[0] == "Put"]
    put_options2 = [option for option in option_details if option[0] == "Put"]
    put_options.sort(key=lambda x: x[2])
    put_options2.sort(key=lambda x: x[3])
    if not put_options == put_options2:
        print("Put Option fiyatinda anormallik vardir.")

def main():
    option_details = []
    stock_details = []

    option_count = int(input("Kaç adet opsiyon bulunuyor? "))
    stock_quantity = int(input("Kaç adet hisse senedi bulunuyor? "))
    stock_price = float(input("Hisse senedi spot fiyatini girin: "))

    for i in range(stock_quantity):
        stock_type = input("{0}. Hisse senedinin tipini girin (Long/Short): ".format(i+1))
        stock_details.append((stock_type, stock_price))


    for i in range(option_count):
        option_type = input("{0}. Opsiyonun tipini girin (Call/Put): ".format(i+1))
        is_long = input("Alim mi, satim mi (Alim için 'A', Satim için 'S'): ")
        strike_price = float(input("Strike fiyatini girin: "))
        option_value = float(input("Opsiyonun değerini girin: "))
        
        if is_long == "S":
            option_value *= -1
        
        option_details.append((option_type, is_long == "A", strike_price, option_value))


    is_there_artbitrage(option_details, stock_price)    
    
  
    stock_prices = np.linspace(0, stock_price*2, 100)
    portfolio_values = [calculate_portfolio_value(option_details,stock_details ,p, stock_quantity) for p in stock_prices]


    plt.plot(stock_prices, portfolio_values, color="red",label="Portföy Profiti")

    for option in option_details:
        option_type, is_long, strike_price, option_value = option
        if is_long:
            plt.plot(strike_price, calculate_portfolio_value(option_details,stock_details, strike_price, stock_quantity), "ro")
        else:
            plt.plot(strike_price, calculate_portfolio_value(option_details,stock_details, strike_price, stock_quantity), "bo")
        plt.annotate(strike_price, (strike_price, calculate_portfolio_value(option_details, stock_details ,strike_price, stock_quantity)))
    
    for option in option_details:
        option_type, is_long, strike_price, option_value = option 
        if is_long:
            plt.plot(stock_prices, [(calculate_option_value(option_type, is_long, strike_price, p)-option_value) for p in stock_prices],label="Option Profit", color="black")
        else:
            plt.plot(stock_prices, [-1*(calculate_option_value(option_type, is_long, strike_price, p)-option_value)   for p in stock_prices], label="Option Profit",color="black")

    for stock in stock_details:
        stock_type, stock_price = stock
        if stock_type == "Long":
            plt.plot(stock_prices, [calculate_stock_profit(stock_price, True, p, 1) for p in stock_prices], label="Stock Profit",color="green")
        else:
            plt.plot(stock_prices, [calculate_stock_profit(stock_price, False, p, 1) for p in stock_prices],label="Stock Profit" ,color="green")           
        
    plt.xlabel("Hisse Senedi Fiyati")
    plt.ylabel("Portföy Değeri")
    plt.title("Hisse Senedi Fiyatina Göre Portföy Değeri Grafiği")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()