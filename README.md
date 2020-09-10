# Hit-And-Run-Trading

Instructions : Just run main.py

The ideas has been taken from the book : https://www.amazon.in/Hit-Run-Trading-Short-Term-Traders%E2%80%B2/dp/1592801986
____________________________________
HIT AND RUN TRADING IN PYTHON
____________________________________

The book has 11 short term strategies that give much better insights about the market. However, one can't monitor all these strategies on a variety of stocks.
This project is a small effort towards automating the whole process with the help of python. Out of these 11, 9 can easily be coded in any programming language.

The script takes daily OPEN-High-Low-Close from NSE website using the library NSEpy data of stocks in nifty500, runs the conditions of 4 major strategies against that data, and returns a buy, sell or do ignore signal.

NOTE: Whenever you see a signal on a stock, you should read about that strategy from the book and then you will have a higher probability of going right and then guessing blindly.

A. Expansion breakouts

Buy:
1) Today is a two month high
2) Today’s range must be the largest daily range in the last 9 days

B. 1–2–3 Pullbacks (very effective strategy)

Buy:
1) 14 day ADX less than 30 
2) +DI greater than -DI
3) Last 3 days should have 3 consecutive lower lows

C. Expansion pivots

Buy:
1) Today’s range is greater than the past 9 days range
2) Either yesterday or today the stock is at or below the 50-day moving average.

D. Boomer

Buy:
1) ADX greater than 30, +DI greater than -DI
2) Three consecutive inside candles

You can further read about the strategies from the book.

Note: Don't blindly jump into the trade using the signals given. Always backtest such strategies on the past data and then only take an educated decision.
