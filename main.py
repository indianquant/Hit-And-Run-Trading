import os
import pandas as pd
import numpy as np
from nsepy import get_history
from datetime import date
from datetime import timedelta
import sys
import csv
import time


class jeffCooper:

	def __init__(self):
		print("Object Created")
		pass

	def getData(self,ticker):
		s =  date.today()-timedelta(days=170)
		e =  date.today()
		data = get_history(symbol=ticker, start=s, end=e)
		data100 = pd.DataFrame(data[-100:])
		return data100

	def adx(self, ohlc):
	
		n=14 # book emphasises on 14 day ADX as higher as possible
		df2 = ohlc.copy()
		df2['H-L']=abs(df2['High']-df2['Low'])
		df2['H-PC']=abs(df2['High']-df2['Close'].shift(1))
		df2['L-PC']=abs(df2['Low']-df2['Close'].shift(1))
		df2['TR']=df2[['H-L','H-PC','L-PC']].max(axis=1,skipna=False)
		df2['DMplus']=np.where((df2['High']-df2['High'].shift(1))>(df2['Low'].shift(1)-df2['Low']),df2['High']-df2['High'].shift(1),0)
		df2['DMplus']=np.where(df2['DMplus']<0,0,df2['DMplus'])
		df2['DMminus']=np.where((df2['Low'].shift(1)-df2['Low'])>(df2['High']-df2['High'].shift(1)),df2['Low'].shift(1)-df2['Low'],0)
		df2['DMminus']=np.where(df2['DMminus']<0,0,df2['DMminus'])
		TRn = []
		DMplusN = []
		DMminusN = []
		TR = df2['TR'].tolist()
		DMplus = df2['DMplus'].tolist()
		DMminus = df2['DMminus'].tolist()
		for i in range(len(df2)):
			if i < n:
				TRn.append(np.NaN)
				DMplusN.append(np.NaN)
				DMminusN.append(np.NaN)
			elif i == n:
				TRn.append(df2['TR'].rolling(n).sum().tolist()[n])
				DMplusN.append(df2['DMplus'].rolling(n).sum().tolist()[n])
				DMminusN.append(df2['DMminus'].rolling(n).sum().tolist()[n])
			elif i > n:
				TRn.append(TRn[i-1] - (TRn[i-1]/n) + TR[i])
				DMplusN.append(DMplusN[i-1] - (DMplusN[i-1]/n) + DMplus[i])
				DMminusN.append(DMminusN[i-1] - (DMminusN[i-1]/n) + DMminus[i])
		df2['TRn'] = np.array(TRn)
		df2['DMplusN'] = np.array(DMplusN)
		df2['DMminusN'] = np.array(DMminusN)
		df2['DIplusN']=100*(df2['DMplusN']/df2['TRn'])
		df2['DIminusN']=100*(df2['DMminusN']/df2['TRn'])
		df2['DIdiff']=abs(df2['DIplusN']-df2['DIminusN'])
		df2['DIsum']=df2['DIplusN']+df2['DIminusN']
		df2['DX']=100*(df2['DIdiff']/df2['DIsum'])
		ADX = []
		DX = df2['DX'].tolist()
		for j in range(len(df2)):
			if j < 2*n-1:
				ADX.append(np.NaN)
			elif j == 2*n-1:
				ADX.append(df2['DX'][j-n+1:j+1].mean())
			elif j > 2*n-1:
				ADX.append(((n-1)*ADX[j-1] + DX[j])/n)
		df2['ADX']=np.array(ADX)
		df3 = df2.loc[:,'DIdiff':'DX']
		return df3

	def OTT_Pullback(self,ohlc_1day,ticker):
		adx1=self.adx(ohlc_1day)
		if adx1['DX'][-3]>40:
			if adx1['DIsum'][-3]>adx1['DIdiff'][-3]:
				if (ohlc_1day['Low'][-3]>ohlc_1day['Low'][-2] and ohlc_1day['Low'][-2]>ohlc_1day['Low'][-1]) or (ohlc_1day['Low'][-3]>ohlc_1day['Low'][-2] and ohlc_1day['Low'][-2]<ohlc_1day['Low'][-1]):
					print("1-2-3 pullback = buy:",ticker)
					return "b"
				
		if adx1['DX'][-3]>40:
			if adx1['DIdiff'][-3]>adx1['DIsum'][-3]:
				if (ohlc_1day['High'][-3]<ohlc_1day['High'][-2] and ohlc_1day['High'][-2]<ohlc_1day['High'][-1]) or (ohlc_1day['High'][-3]<ohlc_1day['High'][-2] and ohlc_1day['High'][-2]>ohlc_1day['High'][-1]):
					print("1-2-3 pullback = sell:",ticker)
					return "s"
		else:
			print("1-2-3 pullback = ignore:",ticker)


	def Expansion_Breakouts(self,ohlc_1day,ticker):
	
		if ohlc_1day["High"][-1]>=ohlc_1day["High"][-59:-1].max():
			if ohlc_1day["High"][-1]-ohlc_1day["Low"][-1]>=(ohlc_1day["High"][-10:-1]-ohlc_1day["Low"][-10:-1]).max():
				print("Expansion Breakout = buy:",ticker)
				return "b"
				
		if ohlc_1day["Low"][-1]<=ohlc_1day["Low"][-59:-1].min():
			if ohlc_1day["High"][-1]-ohlc_1day["Low"][-1]>=(ohlc_1day["High"][-10:-1]-ohlc_1day["Low"][-10:-1]).max():
				print("Expansion Breakout = sell:",ticker)
				return "s"
		else:
			print("Expansion Breakout = ignore:",ticker)

	def Expansion_pivots(self,ohlc_1day,ticker):
		ma = ohlc_1day["Close"].rolling(50).mean()
		if ohlc_1day["High"][-1]-ohlc_1day["Low"][-1]>=(ohlc_1day["High"][-10:-1]-ohlc_1day["Low"][-10:-1]).max():
			if ohlc_1day["High"][-2]<=ma[-2] and ohlc_1day["Low"][-1]>ma[-1]:
				print("expansion pivots = buy:",ticker)
				return "b"
			
		if ohlc_1day["High"][-1]-ohlc_1day["Low"][-1]>=(ohlc_1day["High"][-10:-1]-ohlc_1day["Low"][-10:-1]).max():
			if ohlc_1day["Low"][-2]>=ma[-2] and ohlc_1day["High"][-1]<ma[-1]:
				print("expansion pivots = sell:",ticker)
				return "s"
			
		else:
			print("expansion pivots = ignore:",ticker)

	def Boomer(self,ohlc_1day,ticker):
		adx2=self.adx(ohlc_1day)
		if adx2['DX'][-3]>30:
			if adx2['DIsum'][-3]>adx2['DIdiff'][-3]:
				if ohlc_1day["High"][-3]>ohlc_1day["High"][-2] and ohlc_1day["High"][-2]>ohlc_1day["High"][-1]:
					if ohlc_1day["Low"][-3]<ohlc_1day["Low"][-2] and ohlc_1day["Low"][-2]<ohlc_1day["Low"][-1]:
						print("Boomer = buy:",ticker)
						return "b"
						
			if adx2['DIdiff'][-3]>adx2['DIsum'][-3]:
				if ohlc_1day["High"][-3]>ohlc_1day["High"][-2] and ohlc_1day["High"][-2]>ohlc_1day["High"][-1]:
					if ohlc_1day["Low"][-3]<ohlc_1day["Low"][-2] and ohlc_1day["Low"][-2]<ohlc_1day["Low"][-1]:
						print("Boomer = sell:",ticker)
						return "s"
			else:
				print("boomer = ignore:",ticker)
		else:
			print("boomer = ignore:",ticker)




if __name__ == "__main__":
	jc = jeffCooper()

	nifty500list = pd.read_csv("nifty500list.csv")
	sample = ["AFFLE","HDFC"]
	tickerNifty500 = []
	for i in range(500):
		print(nifty500list["Symbol"][i])
		tickerNifty500.append(nifty500list["Symbol"][i])

	original_stdout = sys.stdout
	timestr = time.strftime("%Y%m%d-%H%M%S")
	i = 0
	with open('output-'+ timestr +'.txt', 'w') as f:
		for ticker in tickerNifty500:
			try:
				ohlcData = jc.getData(ticker)
				sys.stdout = f
				jc.OTT_Pullback(ohlcData,ticker)
				jc.Expansion_Breakouts(ohlcData,ticker)
				jc.Expansion_pivots(ohlcData,ticker)
				jc.Boomer(ohlcData,ticker)
				print("---------------------XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX----------------------------")
				sys.stdout = original_stdout
				print(i)
				i = i + 1
			except Exception as e: print("")