####################################################################################################
####################################################################################################
#
#                                   CryptoTraderAIHelperTool
#                                      Helper Tool utility
#
#
# Software provided by SEESolutions.it
# copyright(c) 2022 - 2025
#
# Author: 
# Armin Costa (armincostaAThotmail.com) 
# 
# SEE contact e-mail: 
# info@seesolutions.it
#
# Software License (Creative Commons Attribution-ShareAlike 4.0 International Public License)
# See LICENSE_CreativeCommons_CC-SA license file
#
# License ref: 
# https://creativecommons.org/licenses/by-sa/4.0/legalcode
#
####################################################################################################
#
# Python code file: detectorTraderAIExecutor.py
#
# Short Description:
# Helper Tool software that aims to be helpful for trading on Binance. Particularly useful for pumps
# 
# If you find this Tool helpful and want to contribute, feel free to send something to these crypto addresses:
# 
# BTC (Bitcoin): 1K1PHeqiUFoQ6Yp8mNP6u2sZR7R23QnffQ
# ETH (Ethereum ERC20): 0x35372ea66892ed35109fb381caa88b7fed75e4b2
# BNB (BSC chain): 0x35372ea66892ed35109fb381caa88b7fed75e4b2
# 
#
import sys
import threading
from threading import Thread
from datetime import datetime
import logging
import math
import os
import os.path
from os import path

import numpy as np
import collections

from binance.client import Client
from binance.enums import *
from binance.streams import BinanceSocketManager
from binance import ThreadedWebsocketManager
from binance import AsyncClient
from binance.enums import *
#from binance.websockets import BinanceSocketManager 
from pricechange import *
from Helper import *
from pricegroup import *


#######################################################################################
# User parameters that are passed when the code is executed (defaults are overwritten)
MODE = "LOOP" # ONCE or LOOP
BUY_NOW_PARAM = False # BUYNOW (buy coin immediately) or BUYLOW (buy at low price curve) or BUYFAST (faster and simpler execution, ideal for big pumps)
COIN_NAME_TO_TRADE = "Null"
MAX_AMOUNT_BUY = 101
STOP_LIMIT_SELL_THRESHOLD_PARAM = "1.0"
STOP_LIMIT_INCREASE_PERC_PARAM = "2.5"
TIME_INTERVAL_SLEEP = 1
GAIN_AMOUNT_THRESHOLD = 100.0 # 100 $
GAIN_AMOUNT_MIN_THRESHOLD = 3.0
COIN_PRICE_FLOAT_RESOLUTION = 2

OPERATIONAL_MODE = True # True == real Trade  | False == Test mode
LOG_MODE = False # True == log to log files

########################################################################################
# Stop limit thresholds and 
STOP_LIMIT_INITIAL_BUY_THRESHOLD = 0.99
STOP_LIMIT_SELL_THRESHOLD = 1.5
STOP_LIMIT_SLICE = 36.0
STOP_LIMIT_INCREASE_PERC = 2.5
AVG_PRICE_CORRECTION_THRESHOLD = 1.005
TRENDLINE_CURVE_THRESHOLD = 0.00003 # 0.003 #1.5e-06#

BUY_NOW = False

MAX_COIN_SCORE = 4
COIN_SCORE_BUY_LOW = -5
COIN_SCORE_BUY_HIGH = 2 
COIN_SCORE_INIT = -2
coin_score = COIN_SCORE_INIT

RUN = True

SELL_CMD_FILE = "./cmds/sell"
BUY_CMD_FILE = "./cmds/buy"

FAKE_ORDER_ID = "{'symbol': 'PONDBUSD', 'orderId': 98539824, 'orderListId': -1, 'clientOrderId': 'lvQ1BqSWKvF9JnUXnoxKc1', 'transactTime': 1655493012757, 'price': '0.00000000', 'origQty': '927.00000000', 'executedQty': '927.00000000', 'cummulativeQuoteQty': '11.02203000', 'status': 'FILLED', 'timeInForce': 'GTC', 'type': 'MARKET', 'side': 'BUY', 'fills': [{'price': '0.01189000', 'qty': '927.00000000', 'commission': '0.92700000', 'commissionAsset': 'POND', 'tradeId': 10492042}]}"


def exit_trade(code):
	printMsg("Exiting trade with code " + str(code))
	sys.exit(code)

def printMsg(msg):
	#print(msg)
	if(LOG_MODE == True and BUY_NOW_PARAM != "BUYFAST"):
		logger.info(msg)
	else:
		print(msg)

def writeGain(coin_pair, buy_value, sell_value, price_difference, price_diff_prercent, net_gain):
	dateTimeObj = datetime.now()
	print(dateTimeObj)
	print("")
	entry = "" + coin_pair + ";" + str(buy_value) + ";" + str(sell_value) + ";" + str(price_difference) + ";" + str(price_diff_prercent) + ";" + str(net_gain) + ""
	print(entry)
	logger2.info(entry)


def buy_order_coin_fast(coin_symbol, amount, trigger_order):
    #printMsg("Placing BUY order for coin " + coin_symbol)
    if(trigger_order):
        try:
           coin_price = client.get_symbol_ticker(symbol=coin_symbol)
           buy_price_float = float(coin_price['price'])
           buy_quantity = math.floor(amount / buy_price_float)
           order = client.order_market_buy(
            symbol=coin_symbol,
            quantity=buy_quantity)

           order_dict = eval(str(order))
           order_fills_dict = eval(str(order_dict['fills']))
           order_fills_dict_str = str(order_fills_dict)
           order_fills_dict_str_sub = order_fills_dict_str[1:-1]
           index_s = order_fills_dict_str_sub.index("{")
           index_e = order_fills_dict_str_sub.index("}")
           order_fills_dict_str_sub = order_fills_dict_str_sub[index_s:index_e+1]

           order_fills_price_dict = eval(str(order_fills_dict_str_sub))

           buy_price_float = float(order_fills_price_dict['price'])

           Buy_Order_List_Executed.set_val(coin_symbol + "_buy", str(order))
           current_coin_balance_int = getCoinBalance(coin_symbol)
           buy_quantity_list.set_val(coin_symbol, current_coin_balance_int)
           buy_price_list.set_val(coin_symbol, buy_price_float)

           return True
        except Exception as e:
            print("Error in placing BUY order: ")
            print(e)
            return False
    else:
        coin_price = client.get_symbol_ticker(symbol=coin_symbol)
        buy_price_float = float(coin_price['price'])       
        buy_quantity = math.floor(amount / buy_price_float)

        Buy_Order_List_Executed.set_val(coin_symbol + "_buy", FAKE_ORDER_ID)
        buy_quantity_list.set_val(coin_symbol, buy_quantity)
        buy_price_list.set_val(coin_symbol, buy_price_float)
        return True   



def sell_order_coin_fast(coin_symbol, amount, trigger_order):
    if(trigger_order):
        try:
           order = client.order_market_sell(
            symbol=coin_symbol,
            quantity=amount)

           order_dict = eval(str(order))

           order_fills_dict = eval(str(order_dict['fills']))
           order_fills_dict_str = str(order_fills_dict)
           order_fills_dict_str_sub = order_fills_dict_str[1:-1]
           index_s = order_fills_dict_str_sub.index("{")
           index_e = order_fills_dict_str_sub.index("}")
           order_fills_dict_str_sub = order_fills_dict_str_sub[index_s:index_e+1]

           order_fills_price_dict = eval(str(order_fills_dict_str_sub))

           sell_price_float = float(order_fills_price_dict['price'])

           Buy_Order_List_Executed.set_val(coin_symbol + "_sell", str(order))
           sell_price_list.set_val(coin_symbol, sell_price_float)
           return True
        except Exception as e:
            print("Error in placing SELL order: ")
            print(e)
            return False
    else:
        coin_price = client.get_symbol_ticker(symbol=coin_symbol)
        sell_price_float = float(coin_price['price'])
        Buy_Order_List_Executed.set_val(coin_symbol + "_sell", FAKE_ORDER_ID)
        sell_price_list.set_val(coin_symbol, sell_price_float)
        #printMsg("fake sell")
        return True  



def buy_order_coin(coin_symbol, amount, trigger_order):
    #printMsg("Placing BUY order for coin " + coin_symbol)
    if(trigger_order):
        try:
           coin_price = client.get_symbol_ticker(symbol=coin_symbol)
           buy_price_float = float(coin_price['price'])
           buy_quantity = math.floor(amount / buy_price_float)
           order = client.order_market_buy(
            symbol=coin_symbol,
            quantity=buy_quantity)

           order_dict = eval(str(order))
           order_fills_dict = eval(str(order_dict['fills']))
           order_fills_dict_str = str(order_fills_dict)
           order_fills_dict_str_sub = order_fills_dict_str[1:-1]
           index_s = order_fills_dict_str_sub.index("{")
           index_e = order_fills_dict_str_sub.index("}")
           order_fills_dict_str_sub = order_fills_dict_str_sub[index_s:index_e+1]

           order_fills_price_dict = eval(str(order_fills_dict_str_sub))

           buy_price_float = float(order_fills_price_dict['price'])

           Buy_Order_List_Executed.set_val(coin_symbol + "_buy", str(order))
           #Buy_Order_List_Executed.set_val(coin_symbol + "_sell", str(order))
           buy_price_list.set_val(coin_symbol, buy_price_float)

           current_coin_balance_int = getCoinBalance(coin_symbol)
           buy_quantity_list.set_val(coin_symbol, current_coin_balance_int)

           return True
        except Exception as e:
            printMsg("Error in placing BUY order: ")
            printMsg(e)
            return False
    else:
        coin_price = client.get_symbol_ticker(symbol=coin_symbol)
        buy_price_float = float(coin_price['price'])       
        buy_quantity = math.floor(amount / buy_price_float)

        Buy_Order_List_Executed.set_val(coin_symbol + "_buy", FAKE_ORDER_ID)
        buy_quantity_list.set_val(coin_symbol, buy_quantity)
        buy_price_list.set_val(coin_symbol, buy_price_float)
        return True   


def sell_order_coin(coin_symbol, amount, trigger_order):
    if(trigger_order):
        try:
           order = client.order_market_sell(
            symbol=coin_symbol,
            quantity=amount)

           order_dict = eval(str(order))
           order_fills_dict = eval(str(order_dict['fills']))
           order_fills_dict_str = str(order_fills_dict)
           order_fills_dict_str_sub = order_fills_dict_str[1:-1]
           index_s = order_fills_dict_str_sub.index("{")
           index_e = order_fills_dict_str_sub.index("}")
           order_fills_dict_str_sub = order_fills_dict_str_sub[index_s:index_e+1]
           order_fills_price_dict = eval(str(order_fills_dict_str_sub))

           sell_price_float = float(order_fills_price_dict['price'])

           Buy_Order_List_Executed.set_val(coin_symbol + "_sell", str(order))
           sell_price_list.set_val(coin_symbol, sell_price_float)
           return True
        except Exception as e:
            printMsg("Error in placing SELL order: ")
            printMsg(e)
            return False
    else:
        coin_price = client.get_symbol_ticker(symbol=coin_symbol)
        sell_price_float = float(coin_price['price'])
        Buy_Order_List_Executed.set_val(coin_symbol + "_sell", FAKE_ORDER_ID)
        sell_price_list.set_val(coin_symbol, sell_price_float)
        #printMsg("fake sell")
        return True  


def sell_order_coin_stoplimit(coin_symbol, amount, stop_price, limit_price, trigger_order):
    #printMsg("Placing SELL STOP LIMIT order for coin " + coin_symbol)
    if(trigger_order):
        try:
           order = client.create_order(  # client.create_oco_order(
            symbol=coin_symbol,
            side='SELL',
            #type='STOP_LOSS_LIMIT',
            #stopLimitTimeInForce='FOK', #TIME_IN_FORCE_GTC
            type='STOP_LOSS_LIMIT',
            timeInForce="GTC",
            quantity=amount,
            stopPrice=stop_price,
            price=limit_price)
           Buy_Order_List_Executed.set_val(coin_symbol + "_sell", str(order))
           sell_price_list.set_val(coin_symbol, limit_price)
           stop_price_list.set_val(coin_symbol, stop_price)
           stoplimit_price_list.set_val(coin_symbol, limit_price)
           return True
        except Exception as e:
            printMsg("Error in placing SELL STOP LIMIT order: ")
            printMsg(e)
            return False
    else:
        Buy_Order_List_Executed.set_val(coin_symbol + "_sell", FAKE_ORDER_ID)
        sell_price_list.set_val(coin_symbol, limit_price)
        stop_price_list.set_val(coin_symbol, stop_price)
        stoplimit_price_list.set_val(coin_symbol, limit_price)
        #printMsg("fake sell Stop Limit"
        return True


def sell_order_coin_limit(coin_symbol, amount, limit_price, trigger_order):
    #printMsg("Placing SELL LIMIT order for coin " + coin_symbol)
	if(trigger_order):
		try:
			order = client.order_limit_sell(
			symbol=coin_symbol,
			quantity=amount,
			price=limit_price)
			Buy_Order_List_Executed.set_val(coin_symbol + "_sell", str(order))
			return True
		except Exception as e:
			printMsg("Error in placing SELL LIMIT order: ")
			printMsg(e)
		return False
	else:
		Buy_Order_List_Executed.set_val(coin_symbol + "_sell", FAKE_ORDER_ID)
		#printMsg("fake sell Limit")
		return True    


def cancelOrder(coin_symbol, order_id, order_type, trigger_order):
	printMsg("Placing CANCEL order for coin " + coin_symbol + " with OrderId: " + order_id)
	if(trigger_order):
		try:
			result = client.cancel_order(
				symbol=coin_symbol,
				orderId=order_id)
			Buy_Order_List_Executed.delete_val(coin_symbol + order_type)
			return True
		except Exception as e:
			printMsg("Error order cancel ")
			printMsg(e)
			exit_trade(-1)
			return False
	else:
		printMsg("Null")


def statusOrder(coin_symbol, order_id, trigger_order):
	#printMsg("Placing CANCEL order for coin " + coin_symbol + " with OrderId: " + order_id)
	if(trigger_order):
		try:
			result = client.get_order(
				symbol=coin_symbol,
				orderId=order_id)
			return result
		except Exception as e:
			printMsg("Error order cancel ")
			printMsg(e)
			return "Null"
	else:
		return "Null"


def getCoinBalance(coin_name_):
	current_coin_balance_int = -1
	if(OPERATIONAL_MODE == True):
		coin_name_abs = coin_name_[0:-4]
		current_coin_balance_json = client.get_asset_balance(asset=coin_name_abs)
		current_coin_balance_dict = eval(str(current_coin_balance_json))
		current_coin_balance = current_coin_balance_dict['free']
		current_coin_balance_float = float(current_coin_balance)
		current_coin_balance_float = math.floor(current_coin_balance_float)
		#current_coin_balance_float = round(current_coin_balance_float, 2) #math.floor(current_coin_balance_float)
		current_coin_balance_int = int(current_coin_balance_float)
	else:
		current_coin_balance_int = int(buy_quantity_list.get_val(coin_name_))

	return current_coin_balance_int


def getCoinLastPrice(coin_name_):
	coin_ticker =  client.get_symbol_ticker(symbol=coin_name_)
	buy_price = coin_ticker['price']
	buy_price_float = float(buy_price)
	return buy_price_float


def getCoinAvgPrice(coin_name_):
	avg_price_json = client.get_avg_price(symbol=coin_name_)
	coin_avg_price = avg_price_json['price']
	coin_avg_price_float = float(coin_avg_price)
	return coin_avg_price_float


def getCandleSticks(coin_name_):
	candles = client.get_klines(symbol=coin_name, interval=Client.KLINE_INTERVAL_30MINUTE)
	return candles


def updateSell_STOP_LIMIT(coin_name, price_level, stop_limit_threshold):
	printMsg("getting preview sell order id...")
	prev_sell_order = Buy_Order_List_Executed.get_val(coin_name + "_sell")

	if(prev_sell_order == "No record found"):
		printMsg("No record found")
	else:
		printMsg("order found: ") # + prev_sell_order)
		printMsg("cancelling preview order...")
		prev_sell_order_dict = eval(prev_sell_order)
		prev_sell_order_order_id = prev_sell_order_dict['orderId']

		if(cancelOrder(coin_name, str(prev_sell_order_order_id), "_sell", OPERATIONAL_MODE) == True):
			Buy_Order_List_Executed.delete_val(coin_name + "_sell")
			printMsg("order cancelled")
			
	printMsg("getting coin balance...")
	quantity_buy_int = buy_quantity_list.get_val(coin_name)
	printMsg("coin sell amount: " + str(quantity_buy_int))


	printMsg("getting preview stoplimit price...")
	stoplimit_price = stoplimit_price_list.get_val(coin_name)
	printMsg("stoplimit price " + str(stoplimit_price))

	if(stoplimit_price == "No record found"):
		printMsg("NO Current stop limit set...using prove default")
		affordable_loss_amount_price_buy = (price_level * stop_limit_threshold) / 100
		printMsg("affordable loss amount: " + str(affordable_loss_amount_price_buy)) 
		stop_price = price_level - affordable_loss_amount_price_buy
		limit_price_slice = (affordable_loss_amount_price_buy * STOP_LIMIT_SLICE) / 100 
		limit_price = stop_price - limit_price_slice
	else:
		stoplimit_price = stoplimit_price_list.get_val(coin_name)
		stoplimit_price_float = float(stoplimit_price)
		price_level = stoplimit_price_float 
		affordable_loss_amount_price_buy = (price_level * stop_limit_threshold) / 100
		printMsg("affordable loss amount: " + str(affordable_loss_amount_price_buy)) 
		stop_price = price_level + affordable_loss_amount_price_buy
		limit_price_slice = (affordable_loss_amount_price_buy * STOP_LIMIT_SLICE) / 100 
		limit_price = stop_price - limit_price_slice

	stop_price = round(stop_price, COIN_PRICE_FLOAT_RESOLUTION)
	limit_price = round(limit_price, COIN_PRICE_FLOAT_RESOLUTION)

	printMsg("STOP: " + str(stop_price))
	printMsg("LIMIT:" + str(limit_price))

	if(sell_order_coin_stoplimit(coin_name, quantity_buy_int, stop_price, limit_price, OPERATIONAL_MODE)): #current_coin_balance_int
			printMsg("SELL Stop Limit set executed sucessfully")



def forceSellCoin(coin_name):
	printMsg("Forcing SELL coin...")
	printMsg("SELL command detected...")
	prev_sell_order = Buy_Order_List_Executed.get_val(coin_name + "_sell")

	printMsg("getting previews stop limit order...")
	if(prev_sell_order == "No record found"):
		printMsg("No record found")
	else:
		printMsg("order found: ") # + prev_sell_order)
		printMsg("cancelling preview order...")
		prev_sell_order_dict = eval(prev_sell_order)
		prev_sell_order_order_id = prev_sell_order_dict['orderId']
		if(cancelOrder(coin_name, str(prev_sell_order_order_id), "_sell", OPERATIONAL_MODE) == True):
			Buy_Order_List_Executed.delete_val(coin_name + "_sell")
			printMsg("order cancelled")

	quantity_to_sell = buy_quantity_list.get_val(coin_name)

	printMsg("selling quantity: " + str(quantity_to_sell))
	if(sell_order_coin(coin_name, quantity_to_sell, OPERATIONAL_MODE)):
		printMsg("Sell issued successfully...")
		printMsg("")
		printMsg("removing cmds...")

		printMsg("calculating gains...")

		calculateGains(coin_name)

		printMsg("removing order...")

		removingOrder(coin_name)

		printMsg("done")

		if(MODE == "ONCE"):
			printMsg("exiting Trade...")
			RUN = False
			exit_trade(0)


def calculateGains(coin_name_):
	buy_price_last =  buy_price_list.get_val(coin_name_)
	sell_price_last = sell_price_list.get_val(coin_name_)
	sell_last_price_float = float(sell_price_last)
	coin_price_diff = sell_last_price_float - float(buy_price_last)
	coin_price_diff_perc = (coin_price_diff / sell_last_price_float) * 100  #current_price_float
	net_gain_amount = coin_price_diff * (MAX_AMOUNT_BUY / buy_price_last)
	writeGain(coin_name_, buy_price_last, sell_last_price_float, coin_price_diff, coin_price_diff_perc, net_gain_amount)


def removingOrder(coin_name_):
	buy_order_list.remove(coin_name_)
	buy_price_list.delete_val(coin_name_)
	sell_price_list.delete_val(coin_name_)
	stoplimit_price_list.delete_val(coin_name_)
	Buy_Order_List_Executed.delete_val(coin_name_ + "_buy")
	Buy_Order_List_Executed.delete_val(coin_name_ + "_sell")
	coin_score = COIN_SCORE_INIT
	prev_estimated_gain_amount = 65000
	accumulated_GAINS = 0.0
	BUY_NOW = False
	print("----------------------------------------------------") # we just want to delimitate gains in console output


def getTrendline(index,data, order=1):
    coeffs = np.polyfit(index, list(data), order)
    slope = coeffs[-2]
    return float(slope)


def price_for_curve_not_equal(a, b): 
	diff_ = abs(a - b)
	val_ = abs(a - b) > 0.003
	return val_


def trade_execution():
	printMsg("trade execution...")
	coin_name = COIN_NAME_TO_TRADE

	update_stop_limit_counter = 0
	cumulative_price_increase = 0

	# we set the STOP_LIMIT_SLICE dynamically
	STOP_LIMIT_SLICE = 36.0
	STOP_LIMIT_SLICE = STOP_LIMIT_SLICE * STOP_LIMIT_SELL_THRESHOLD

	curr_price_float = getCoinLastPrice(coin_name)

	RUN = True
	BUY_NOW = False

	coin_score = COIN_SCORE_INIT

	prev_estimated_gain_amount = 65000

	if(BUY_NOW_PARAM == "BUYNOW"):
		BUY_NOW = True

	#index_curve=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]#,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
	#Price_Curve=[999,999,999,999,999,999,999,999,999,999,999,999,999,999,999]#,999,999,999,999,999,999,999,999,999,999,999,999,999,999,999]
	price_curve_index = 10 #5 #19 #49 #14
	index_curve = list(range(0, price_curve_index + 1))
	Price_Curve = [999] * (price_curve_index +1)

	accumulated_GAINS = 0.0

	prev_price_float = float(0.0)
	prev_price_float_stoplimit = float(0.0)

	CURVE_UPDATE_INTERVAL = 3
	counter_curve_update = 0

	while RUN :

		curr_price_float = getCoinLastPrice(coin_name)
		#prev_price = coin_prev_price_list.get_val(coin_name)
		#if(prev_price != "No record found"):
		#	prev_price_float =  float(prev_price)

		if(curr_price_float > prev_price_float):
			coin_score += 1
		elif(curr_price_float == prev_price_float):
			#nop
			coin_score = coin_score
		else:
			coin_score -= 1

		#coin_prev_price_list.set_val(coin_name, curr_price_float)

		if(abs(coin_score) >= MAX_COIN_SCORE):
			coin_score = COIN_SCORE_INIT

		# rounding might be an option, but not used currently
		curr_price_float_round = round(curr_price_float, COIN_PRICE_FLOAT_RESOLUTION)
		prev_price_float_round = round(prev_price_float, COIN_PRICE_FLOAT_RESOLUTION)

		if(counter_curve_update % CURVE_UPDATE_INTERVAL == 0):
			if(curr_price_float_round != prev_price_float_round):   ##curr_price_float != prev_price_float)  # price_for_curve_not_equal(curr_price_float, prev_price_float) == True #not math.isclose(curr_price_float, prev_price_float, rel_tol=0.50)
				a_list = collections.deque(Price_Curve)
				a_list.rotate(-1)
				Price_Curve = list(a_list)
				Price_Curve[price_curve_index] = curr_price_float
		counter_curve_update += 1

		trend_list_result = getTrendline(index_curve,Price_Curve)
		trend_list_result = round(trend_list_result, 8)


		coin_avg_price_float = getCoinAvgPrice(coin_name)
		coin_avg_price_float_corrected = coin_avg_price_float * AVG_PRICE_CORRECTION_THRESHOLD

		printMsg("#################")
		printMsg("")
		printMsg("current price: " + str(curr_price_float))
		printMsg("preview price: " + str(prev_price_float))
		printMsg("avg. price: " + str(coin_avg_price_float))
		printMsg("avg. price corr: " + str(coin_avg_price_float_corrected))
		printMsg("")
		printMsg("coin score: " + str(coin_score))
		printMsg("")
		printMsg("Trend: " + str(trend_list_result))
		printMsg("curve: " + str(Price_Curve))
		#candles_sticks_coin = getCandleSticks(coin_name)
		#printMsg("candles: " + str(candles_sticks_coin))
		#and (curr_price_float < coin_avg_price_float_corrected) and (coin_score > 0)

		if(BUY_NOW):
			#we force the first buy
			coin_avg_price_float_corrected = curr_price_float
			trend_list_result = float(TRENDLINE_CURVE_THRESHOLD)
			coin_score = COIN_SCORE_BUY_HIGH + 1
			BUY_NOW = False

		#(curr_price_float <= coin_avg_price_float_corrected) and (coin_score > COIN_SCORE_BUY_HIGH)
		#
		# and ((trend_list_result >= float(TRENDLINE_CURVE_THRESHOLD)) 
		if(coin_name not in buy_order_list and ((trend_list_result >= float(TRENDLINE_CURVE_THRESHOLD)) )): # and (coin_score >= COIN_SCORE_BUY_HIGH) #and (coin_score >= COIN_SCORE_BUY_HIGH)#or (coin_score == 0) coin_score >= COIN_SCORE_BUY_HIGH coin_score <= COIN_SCORE_BUY_LOW or 
		    printMsg("------------------------------------------------")
		    printMsg("EXECUTING Order BUY") 
		    printMsg("")
		    printMsg("coin: " + coin_name)
		    printMsg("")
		    printMsg("getting last price...")

		    buy_price_float = getCoinLastPrice(coin_name)

		    printMsg("price: " + str(buy_price_float))
		    printMsg("")

		    #quantity_to_buy = ((float(MAX_AMOUNT_BUY) * 1.0) / BUY_THRESHOLD)
		    #printMsg("optimal quantity to buy: " + str(quantity_to_buy))
		    printMsg("executing order...")
		    if(buy_order_coin(coin_name, MAX_AMOUNT_BUY, OPERATIONAL_MODE)):
		        printMsg("Order executed successfully")
		        order_json = Buy_Order_List_Executed.get_val(coin_name + "_buy")
		        if(order_json == "No record found"):
		        	printMsg("No record found")
		        else:
		        	printMsg("order_id json: " + order_json)
		        	order_dict = eval(order_json)
		        	order_id = order_dict['orderId']
		        	#commission = order_dict['commission']
		        	printMsg("order_id: " + str(order_id))
		        	#printMsg("commission: " + str(commission))
		        	printMsg("order_id: " + order_json) #order_json_dict['order_id']
		        	printMsg("UPDATING Order with new STOP LIMIT")
		        	updateSell_STOP_LIMIT(coin_name, buy_price_float, STOP_LIMIT_SELL_THRESHOLD)  # * STOP_LIMIT_INITIAL_BUY_THRESHOLD

		        printMsg("adding order to list...")
		        buy_order_list.add(coin_name)

		        printMsg("order added...")
		    else:
		        printMsg("Error in executing order")

		    printMsg("------------------------------------------------")


		buy_price_last =  buy_price_list.get_val(coin_name)
		quantity_buy_int = buy_quantity_list.get_val(coin_name)

		current_price_float = getCoinLastPrice(coin_name)
		buy_last_price_float = current_price_float
		if(buy_price_last != "No record found"):
			buy_last_price_float = float(buy_price_last)

		stoplimit_price_last_float = buy_last_price_float
		stoplimit_price_last = stoplimit_price_list.get_val(coin_name)
		if(stoplimit_price_last != "No record found"):
			stoplimit_price_last_float = float(stoplimit_price_last)

		stop_price_last_float = buy_last_price_float
		stop_price_last = stop_price_list.get_val(coin_name)
		if(stop_price_last != "No record found"):
			stop_price_last_float = float(stop_price_last)

		coin_price_diff = current_price_float - buy_last_price_float
		coin_price_diff_perc = (coin_price_diff / current_price_float) * 100

		coin_price_diff_stoplimit = current_price_float - stoplimit_price_last_float 
		coin_price_diff_perc_stoplimit = (coin_price_diff_stoplimit / current_price_float) * 100

		cumulative_price_increase = coin_price_diff_perc_stoplimit ##round(coin_price_diff_perc_stoplimit)
		net_gain_amount = coin_price_diff * (MAX_AMOUNT_BUY / buy_last_price_float)
		
		if(coin_name in buy_order_list):
			dateTimeObj = datetime.now()
			printMsg("------------------------------------------------------")
			printMsg(dateTimeObj)
			printMsg("")
			printMsg("MONITORING: " + coin_name)
			printMsg("coin score: " + str(coin_score))
			printMsg("")
			printMsg("BUY price: " + str(buy_price_last))
			printMsg("quantity: " + str(quantity_buy_int))
			printMsg("")
			printMsg("STOP price: " + str(stop_price_last_float))
			printMsg("LIMIT price: " + str(stoplimit_price_last_float))
			printMsg("")
			printMsg("CURRENT price: " + str(current_price_float))
			printMsg("coin avg price: " + str(coin_avg_price_float))
			printMsg("coin avg. price corr.: " + str(coin_avg_price_float_corrected))
			printMsg("")
			printMsg("relative increase (percent): " + str(coin_price_diff_perc))
			printMsg("stoplimit increase (percent): " + str(coin_price_diff_perc_stoplimit))
			printMsg("cumulative_price_increase (percent): " + str(cumulative_price_increase))
			printMsg("absulute increase: " + str(coin_price_diff))
			printMsg("coin price diff: " + str(coin_price_diff))
			printMsg("")
			printMsg("stop limit price: " + str(stoplimit_price_last_float))
			printMsg("")
			printMsg("Trend: " + str(trend_list_result))
			printMsg("")

			# real gaicumulative_price_increasen with current price
			coin_price_diff_real = current_price_float - buy_last_price_float
			absolute_gain_amount = coin_price_diff_real * (MAX_AMOUNT_BUY / buy_last_price_float)

			# estimated gain considering stoplimit
			coin_price_diff = stoplimit_price_last_float - buy_last_price_float
			estimated_gain_amount = coin_price_diff * (MAX_AMOUNT_BUY / buy_last_price_float)
			printMsg("#########################")
			printMsg("")
			printMsg("CURRENT price: " + str(current_price_float))
			printMsg("")
			printMsg("stoplimit GAIN: " + str(estimated_gain_amount))
			printMsg("")
			printMsg("absolute GAIN: " + str(absolute_gain_amount))
			printMsg("")
			printMsg("#########################")
			

			if((GAIN_AMOUNT_THRESHOLD != -1) and ((absolute_gain_amount >= GAIN_AMOUNT_THRESHOLD) or (absolute_gain_amount <= GAIN_AMOUNT_MIN_THRESHOLD))): #and trend_list_result <= 0
				printMsg("++++++++++++++++++++++++")
				printMsg("FORCE SELL")
				printMsg("")
				printMsg("Accumulated GAINS is >= than GAIN_AMOUNT_THRESHOLD and tredline is falling, selling...")
				printMsg("")
				printMsg("Trend line: " + str(trend_list_result))
				printMsg("")
				printMsg("Accumulated GAINS: " + str(accumulated_GAINS))
				printMsg("")
				printMsg("selling coin...")
				forceSellCoin(coin_name)
				time.sleep(15)


			prev_estimated_gain_amount = estimated_gain_amount

			printMsg("")
			printMsg("------------------------------------------------------")

			cumulative_price_increase = round(cumulative_price_increase, 2)
			coin_price_diff = round(coin_price_diff, 2)
			printMsg("")
			printMsg("coin price diff: " + str(coin_price_diff))
			printMsg("cumulative price increase: " + str(cumulative_price_increase))
			if(current_price_float > prev_price_float_stoplimit and cumulative_price_increase >= (STOP_LIMIT_INCREASE_PERC*2) and STOP_LIMIT_INCREASE_PERC != -1): # coin_price_diff >= 0.0 and  # cumul_mod_price_increase == 0
				printMsg("")
				printMsg("UPDATING Order with new STOP LIMIT (gain)")
				current_price_float = getCoinLastPrice(coin_name)
				updateSell_STOP_LIMIT(coin_name, current_price_float, STOP_LIMIT_INCREASE_PERC)
				prev_price_float_stoplimit = current_price_float
			

			printMsg("")

			# check Order Status
			sell_order_status = Buy_Order_List_Executed.get_val(coin_name + "_sell")

			if(sell_order_status == "No record found"):
				printMsg("No record found")
			else:
				#printMsg("order found: ")# + sell_order_status)
				#printMsg("getting order status...")
				prev_sell_order_dict = eval(sell_order_status)
				prev_sell_order_order_id = prev_sell_order_dict['orderId']

				status_order_json = statusOrder(coin_name, str(prev_sell_order_order_id), OPERATIONAL_MODE)
				status_order = "NA"

				if(status_order_json != "Null"):
					status_order_dict = eval(str(status_order_json))
					status_order = status_order_dict['status']
				else:
					if(current_price_float <= stoplimit_price_last_float):
						status_order = "FILLED"
					else:
						status_order = "NEW"

				printMsg("Order STATUS: " + status_order)

				if(status_order == "FILLED"):
					try:
						printMsg("calculating gains...")

						calculateGains(coin_name)

						printMsg("removing order...")

						removingOrder(coin_name)

						printMsg("done")

					except:
						printMsg("error in removing order")

					if(MODE == "ONCE"):
						RUN = False
						exit_trade(0)

				else:
					printMsg("Pending SELL order STOP LIMIT")

			printMsg("checking for CMDs...")
			if(path.exists(SELL_CMD_FILE)):
				printMsg("SELL command detected...")
				prev_sell_order = Buy_Order_List_Executed.get_val(coin_name + "_sell")

				printMsg("getting previews stop limit order...")
				if(prev_sell_order == "No record found"):
					printMsg("No record found")
				else:
					printMsg("order found: ") # + prev_sell_order)
					printMsg("cancelling preview order...")
					prev_sell_order_dict = eval(prev_sell_order)
					prev_sell_order_order_id = prev_sell_order_dict['orderId']
					if(cancelOrder(coin_name, str(prev_sell_order_order_id), "_sell", OPERATIONAL_MODE) == True):
						Buy_Order_List_Executed.delete_val(coin_name + "_sell")
						printMsg("order cancelled")

				quantity_to_sell = buy_quantity_list.get_val(coin_name)

				printMsg("selling quantity: " + str(quantity_to_sell))
				if(sell_order_coin(coin_name, quantity_to_sell, OPERATIONAL_MODE)):
					printMsg("Sell issued successfully...")
					printMsg("")
					printMsg("removing cmds...")

					try:
						os.remove(SELL_CMD_FILE)
					except:
						printMsg("Error in removing command")

					printMsg("calculating gains...")

					calculateGains(coin_name)

					printMsg("removing order...")

					removingOrder(coin_name)

					printMsg("done")

					if(MODE == "ONCE"):
						printMsg("exiting Trade...")
						RUN = False
						exit_trade(0)
			else:
				printMsg("No command detected...")

		#coin_prev_price_list.set_val(current_price_float)
		prev_price_float = current_price_float

		time.sleep(TIME_INTERVAL_SLEEP)
		update_stop_limit_counter += 1




if __name__ == '__main__':
    #main()
    # global var
    buy_order_list = set();

    coin_prev_price_list = HashTable(1000)
    buy_price_list = HashTable(1000)
    buy_quantity_list = HashTable(1000)
    sell_price_list = HashTable(1000)
    stop_price_list = HashTable(1000)
    stoplimit_price_list = HashTable(1000)
    # Order Hash set list
    Buy_Order_List_Executed = HashTable(100)

    COIN_NAME_TO_TRADE = "null"

    log_name = "trading_" + COIN_NAME_TO_TRADE + ".txt"
    log_name_gains = "GAINS"

    logger = logging.getLogger(log_name)
    hdlr = logging.FileHandler('./logs/' + log_name + ".log")
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.INFO)

    logger2 = logging.getLogger(log_name_gains)
    hdlr2 = logging.FileHandler('./GAINS/' + log_name_gains + ".csv")
    formatter2 = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr2.setFormatter(formatter2)
    logger2.addHandler(hdlr2) 
    logger2.setLevel(logging.INFO)

    if(len(sys.argv)) > 7:
        MODE = sys.argv[1]
        BUY_NOW_PARAM = sys.argv[2]
        COIN_NAME_TO_TRADE = sys.argv[3]
        MAX_AMOUNT_BUY = float(sys.argv[4])
        STOP_LIMIT_SELL_THRESHOLD = float(sys.argv[5])
        STOP_LIMIT_INCREASE_PERC = float(sys.argv[6])
        TIME_INTERVAL_SLEEP = int(sys.argv[7])
        GAIN_AMOUNT_THRESHOLD = float(sys.argv[8])

        print("###################################################")
        print("")
        print("          CryptoTraderAIHelperTool                ")
        print("")
        print(" provided by SEESolutions.it                      ")
        print(" copyright(c) 2022 - 2025                         ")       
        print("")
        print(" License License (CC BY-SA Attribution-ShareAlike ")
        print("")
        print(" Author: A.Costa                                  ")
        print("")
        print("##################################################")
        print("")
        print("init() client...")

        #READ API CONFIG
        api_config = {}
        with open('api_config.json') as json_data:
            api_config = json.load(json_data)
            json_data.close()

        # create the client
        client = Client(api_config['api_key'], api_config['api_secret'])
        print("client inited successuflly")

        # read coin price to get number of decimals
        coin_price = getCoinLastPrice(COIN_NAME_TO_TRADE)

        coin_price_str = str(coin_price)
        coin_decimals = coin_price_str[::-1].find('.')
        COIN_PRICE_FLOAT_RESOLUTION = int(coin_decimals)

        coin_price = 0.0
        if(BUY_NOW_PARAM == "BUYFAST"):
        	coinAvailable = False
        	while not coinAvailable:
        		try:
        			coin_price = getCoinLastPrice(COIN_NAME_TO_TRADE)
        			printMsg(".")
        			if(path.exists(BUY_CMD_FILE)):
        				printMsg("bying coin at price " + str(coin_price))
        				buy_order_coin_fast(COIN_NAME_TO_TRADE, MAX_AMOUNT_BUY, OPERATIONAL_MODE)
        				printMsg("buy successuflly")
        				if(STOP_LIMIT_SELL_THRESHOLD != -1):
        					updateSell_STOP_LIMIT(COIN_NAME_TO_TRADE, coin_price, STOP_LIMIT_SELL_THRESHOLD)
        				coinAvailable = True
        		except Exception as e:
        				printMsg("coin not available yet...")
        				printMsg(e)
        				now = datetime.now()
        				printMsg(now)
        				coinAvailable = False


        	coinSell = False
        	sleep_pause_interval = 7
        	cnt_sleep = 0
        	while  not coinSell:
        			try:
        				current_coin_balance_int = -1
        				coin_price = getCoinLastPrice(COIN_NAME_TO_TRADE)

        				if(STOP_LIMIT_SELL_THRESHOLD != -1):
        					current_coin_balance_int = buy_quantity_list.get_val(COIN_NAME_TO_TRADE)
        				else:
        					current_coin_balance_int = getCoinBalance(COIN_NAME_TO_TRADE)

        				buy_price_list_str = buy_price_list.get_val(COIN_NAME_TO_TRADE)
        				buy_trade = buy_price_list_str * current_coin_balance_int
        				current_trade = coin_price * current_coin_balance_int
        				gain_trade_prec = (buy_price_list_str * coin_price) / 100
        				coin_gain =  current_trade - buy_trade
        				now = datetime.now()
        				printMsg("###########################################################################")
        				printMsg("Date:           " + str(now))
        				printMsg("")
        				printMsg("Price:          " + str(coin_price))
        				printMsg("Buy price:      " + str(buy_price_list_str))
        				printMsg("Balance:        " +  str(current_coin_balance_int))
        				printMsg("")
        				printMsg("Buy trade:      " + str(buy_trade))
        				printMsg("Current trade:  " + str(current_trade))
        				printMsg("Gain(%):        " + str(gain_trade_prec))
        				printMsg("")
        				printMsg("GAIN ($):       " + str(coin_gain))

        				if(path.exists(SELL_CMD_FILE)):
        					coinSell = True
        					printMsg("---------------------------------------------------------------------------")
        					printMsg("Sell CMD detected...selling coin...")
        					printMsg("getting previews stop limit order...")
        					prev_sell_order = Buy_Order_List_Executed.get_val(COIN_NAME_TO_TRADE + "_sell")
        					if(prev_sell_order == "No record found"):
        						printMsg("No record found")
        					else:
        						printMsg("order found: ") # + prev_sell_order)
        						printMsg("cancelling preview order...")
        						prev_sell_order_dict = eval(prev_sell_order)
        						prev_sell_order_order_id = prev_sell_order_dict['orderId']
        						if(cancelOrder(COIN_NAME_TO_TRADE, str(prev_sell_order_order_id), "_sell", OPERATIONAL_MODE) == True):
        							Buy_Order_List_Executed.delete_val(COIN_NAME_TO_TRADE + "_sell")
        							printMsg("order cancelled")
        					sell_order_coin_fast(COIN_NAME_TO_TRADE, current_coin_balance_int, OPERATIONAL_MODE)
        					sell_price_list_str = sell_price_list.get_val(COIN_NAME_TO_TRADE)
        					coin_price_diff = float(sell_price_list_str) - float(buy_price_list_str)
        					coind_gain = coin_price_diff * (MAX_AMOUNT_BUY / buy_price_list_str)
        					printMsg("******************************************************************************")
        					printMsg("SELL successuflly " + str(current_coin_balance_int) + " at Price " + str(sell_price_list_str) + "  GAIN: " + str(coin_gain))
        					printMsg("writing gains...")
        					calculateGains(COIN_NAME_TO_TRADE)
        					printMsg("-----------------------------------------------------------------------------")
        					try:
        						os.remove(SELL_CMD_FILE)
        					except:
        						printMsg("Error in removing command")
        			except Exception as e:        					
        					printMsg("error in selling coin")
        					printMsg(e)
        					now = datetime.now()
        					printMsg(now)
        					coinSell = False
        			if((cnt_sleep % sleep_pause_interval) != 0):
        				time.sleep(TIME_INTERVAL_SLEEP)
        			else:
        				time.sleep(TIME_INTERVAL_SLEEP+1)
        			cnt_sleep = cnt_sleep + 1

        	sys.exit(0)

        # read coin price to get number of decimals
        coin_price = getCoinLastPrice(COIN_NAME_TO_TRADE)

        # getting coin info
        coin_info = client.get_symbol_info(COIN_NAME_TO_TRADE)
        print("coin_info: " + str(coin_info))

        coin_price_str = str(coin_price)
        coin_decimals = coin_price_str[::-1].find('.')
        COIN_PRICE_FLOAT_RESOLUTION = int(coin_decimals)

        print("coin price: " + str(coin_price))
        print("coin decimals: " + str(coin_decimals))
        print("")
        print("Parameters->")
        print("")
        print("MODE: " + MODE)
        print("BUY_NOW_PARAM: " + BUY_NOW_PARAM)
        print("COIN_NAME_TO_TRADE: " + COIN_NAME_TO_TRADE)
        print("MAX_AMOUNT_BUY: " + str(MAX_AMOUNT_BUY))
        print("STOP_LIMIT_SELL_THRESHOLD: " + str(STOP_LIMIT_SELL_THRESHOLD))
        print("STOP_LIMIT_INCREASE_PERC: " + str(STOP_LIMIT_INCREASE_PERC))
        print("TIME_INTERVAL_SLEEP: " + str(TIME_INTERVAL_SLEEP))
        print("COIN_PRICE_FLOAT_RESOLUTION: " + str(COIN_PRICE_FLOAT_RESOLUTION))
        print("")
        print("------------------------------------------------")
        print("")
        print("GAINS:")
        print("->")

    else:
    	print("Parameters: MODE, BUY_NOW_PARAM, COIN_NAME_TO_TRADE, MAX_AMOUNT_BUY, STOP_LIMIT_SELL_THRESHOLD, STOP_LIMIT_INCREASE_PERC, TIME_INTERVAL_SLEEP, GAIN_AMOUNT_THRESHOLD")
    	exit()

    lock = threading.Lock()

    RUN = True

    thread_ = Thread(target = trade_execution).start()

    

