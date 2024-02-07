from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import yfinance as yf
import pandas as pd 
import pandas_ta as ta 

import backtrader as bt
import matplotlib.pyplot as plt


def graficar(data, chart1, chart2, name):
        #chosen = data[]
        data = data[:]
        
        axis = []
        for i in range(len(data)):
            plt.vlines(x = i, ymin=float(data['Low'][i]), ymax = float(data['High'][i]), color= 'black', linewidth=1)
            if float(data['Close'][i])  > float(data['Open'][i]):
                plt.vlines(x = i, ymin=float(data['Open'][i]), ymax = float(data['Close'][i]), color= 'green', linewidth=4)
            if float(data['Close'][i]) < float(data['Open'][i]):
                plt.vlines(x = i, ymin=float(data['Close'][i]), ymax = float(data['Open'][i]), color= 'red', linewidth=4)
            axis.append(i)
        axis_buy =[]
        data_buy = []
        for x, a in enumerate(data["Signal_buy"]):
             if a != 0:
                  axis_buy.append(x)
                  data_buy.append(a)
        axis_sell =[]
        data_sell = []
        for x, a in enumerate(data["Signal_sell"]):
             if a != 0:
                  axis_sell.append(x)
                  data_sell.append(a + 60)
        plt.plot(axis_sell, data_sell, marker='v', color='red', markersize=10)
        plt.plot(axis_buy, data_buy, marker='^', color='blue', markersize=10)
        plt.plot(axis, chart1["sma"], color="green")
        plt.plot(axis, chart2["sma"], color="red")
        #print(data.head())
        
        plt.grid()
        plt.title(name)
        plt.show()

# Create a Stratey
class TestStrategy(bt.Strategy):
    params = (
        ('maperiod', 50),
        ('maperiod2', 200)
    )

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # Add a MovingAverageSimple indicator
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.maperiod)
        self.sma2 = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.maperiod2)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        # Simply log the closing price of the series from the reference
        #self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            if self.sma[0] > self.sma2[0]:

                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log('BUY CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()

        else:

            if self.sma[0] < self.sma2[0]:
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()

        


stock_symbols = [
    "FL",
]

stock_data = yf.download(stock_symbols, period="1y", interval='60m')
sma_50 = pd.DataFrame()
sma_200 = pd.DataFrame()
print(stock_data)
ticket = pd.DataFrame(index = ["Close", "Open", "High", "Low"], columns = stock_symbols)

sma_50["sma"] = ta.sma(stock_data["Close"], length=50)
sma_200["sma"] = ta.sma(stock_data["Close"], length= 200)

stock_data["Signal_buy"] = ta.cross(sma_50["sma"], sma_200["sma"])
stock_data["Signal_sell"] = ta.cross(sma_200["sma"], sma_50["sma"])       
          
current_sma_50 = sma_50.iloc[-1]
current_sma_200 = sma_200.iloc[-1]

graficar(stock_data, sma_50, sma_200, "FL")

################ backtesting #################
cerebro = bt.Cerebro()
cerebro.addstrategy(TestStrategy)

data = bt.feeds.PandasData(dataname=stock_data, name=stock_symbols[0])
cerebro.adddata(data)

cerebro.broker.setcash(1000.0)

# Add a FixedSize sizer according to the stake
cerebro.addsizer(bt.sizers.FixedSize, stake=10)
 # Set the commission
cerebro.broker.setcommission(commission=0.0)
# Normalizando data


print("Starting Portfolio Value: %.2f" %cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
stock_data.to_csv("stock_data.csv")
