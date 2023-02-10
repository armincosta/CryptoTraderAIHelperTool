####################################################

                   Software
                                      
           CryptoTraderAIHelperTool V1.0
                                        
         A tiny Crypto Trading utility Tool
   

####################################################


 Software provided by SEESolutions.it
  copyright(c) 2022 - 2025


 **Author:**
  Armin Costa (admincostaAThotmail.com)



 
**Software License:**

  Creative Commons Attribution-ShareAlike 4.0 International Public License (CC-SA)

  See LICENSE_CreativeCommons_CC-SA license and LICENSE_DISCLAIMER files for detailed terms

  CreativeCommons License ref: 
  https://creativecommons.org/licenses/by-sa/4.0/legalcode



**Contact**
 SEESolutions
                    e-mail: info@seesolutions.it


####################################################



# Intro

 This source code repository provides some software tools that are useful for supporting the trading of crypto assets on the Binance Crypto Exchange.

 If you catch the right momentum in a trade with the proper configuration parameters, you may stay more relaxed while the market rumbles.
 

# Description
 
This tiny crypto trading helper Tool comes with some functionalities for supporting the crypto trading activity. It consists of python code scripts that can be run in a commmon command shell available on Windows, MacOS and Linux.

The program can be parameterized with configurable parameters and has different MODEs of operation. The tool allows to make BUYs and SELLs in semi-automatic way while constantly monitoring a token price. Stop Limit orders for SELLs are automatically set and are incremental according to growing or downing price levels. It simplyfies to some extend buying and selling your favorite crypto token.

It is very useful in cases of big and instant price increases or constant slow price increases over longer time periods. Version 1.0 is just the first release of this crypto trading utility, interesting features that will make complex automatic AI driven trades will follow.

This software will at some point be able to automatically detect the trading activities on the crypto market and forcast possible trades that deliver gains. In particular this tool will also detect early big price pumps that can deliver significant gains.


# How it Works

The Toolset allows to run a set of operations (MODEs) to trade crypto assets (BUYs and SELLs) in semi-automatic way by executing the program with user defined parameters.

When a trade operation is executed (i.e. BUYNOW), the token price is monitored continuously at a given time interval defined by the user (i.e each second). Immediately after the BUY operation is executed, a STOP LIMIT SELL orer is set and incremented or decremented automatically according to a configurable threshold value expressed in percentage (%) that is relative to the price level.

A SELL order can occur either automatically, via an executed stop limit order, at a desired amount gained (%) or at any moment by the user by executing a sell command.

One of the operation (MODE) allows also to poll (check continuously) the availability of a new crypto asset that is going to be listed on the Exchange and  perform a BUY operation as soon as the trading is open at a the lowest possible price level.

 
# Features (MODEs of operation)

The software has different modes (MODES) of operation depending on the type of trade the user wants to perform. More features (modes of operation) will follow in new release versions of the software.

Currently the CryptoTraderAIHelperTool (Version 1.0) supports the following operation MODEs:


**BUYNOW:**

Make an instant BUY and set a starting STOP LIMIT order at a configurable threshold below the price level (expressed in percent % relative to the price, see parameter STOP_LIMIT_SELL_THRESHOLD_PARAM). As the price increases, the active STOP LIMIT order is incremented according to a second threshold (expressed in %). When the token price increases by at least 2 times the increase threshold, the active STOP LIMIT orders are incremented by the defined threshold (STOP_LIMIT_INCREASE_PERC_PARAM) .    

The software monitors constantly the price and as the price level increases or decreases it adjusts the configured STOP LIMIT orders according to the threshold parameters.

When a SELL Command is executed, either by the user or automatically with an active order, the active stop limits orders are cancelled and a SELL at market price or at the desired price is executed.


This operations can be performed in different types of execution:
- only ONCE: program terminates with the SELL
or
- in a constant iterated LOOP: program iterates the operation until terminated by user.


**BUYLOW:** (experimental)

A price curve is calculated in a given time interval and the program tries to detect the best BUY moment (ascending curve). STOP LIMIT orders are set (STOP_LIMIT_SELL_THRESHOLD_PARAM) and incremented according to the configured thresholds (STOP_LIMIT_SELL_THRESHOLD_PARAM) expressed in percentage (%) relative to the price.


**BUYFAST:**

Similar to the mode BUYNOW but with a faster execution. Sets only an initial Stop Limit order, if configured, when a BUY is executed. In this mode there are NO automatic incremental STOP LIMIT orders.

This mode also allows also to make a fast BUY when a token is going to be listed for the first time. In this case the token availability is constantly monitored and as soon the token becomes available for trading the current price is shown. The user may than trigger a buy by issuing a BUY command (touch ./cmds/buy). NOTE: By default the ./cmds/buy command is active, so you have to remove this file if you want to poll the token price and you preffer to issue the BUY command manually.
 
 
# Prerequisites:

Python Version > 3

**Python Library Dependencies:**
- numpy
- Python Binance API (ttps://github.com/sammchardy/python-binance)


# How to Install the software
 
1) Install Python (version > 3) and the following python packages:

```
pip install numpy
pip install python-binance
```

2) The python code sofware is located in folder "src" that contains also auxiliary folders needed for execution. The scripts must be run from the a command shell within the "src" folder.

The auxiliary folders are:
- logs: contain the log files of the trades
- GAINS: contain a "GAINS.csv" file with the listed gains or losses of the trades executed
- cmds: commands can be executed by creating an empty file in this folder with the named command to be executed (ex. buy, sell, etc..). The program will detect these files and act accordingly.

 
# How to Run the software

1) Choose the MODE of execution for your trade (see MODE parameter)

2) Define the proper parameters for the crypto token you want to trade (, i.e. TokenPair, Amount, initial stop limit order threshold, etc...)

NOTE: Each Token might have individual parameter settings according to market conditions (volume, speed, price jumps, etc....).

For example if you set a too tight stop limit increase threshold, it's likely that your stop limit orders are executed immediately if the price makes instant jumps (this happens frequently in the initial momentum when a token starts to be traded actively, especially if the trade volume is low initially. Try to trade with small amounts at the beginning. This version supports only one STOP LIMIT order at time, in coming releases the orders will be splitted in many orders according to the amount traded.

To run the software just open the command shell or terminal and execute the python script contained in the 'src' folder with the desired parameters.


Run a Trade with MODE(BUYFAST) Example:

Run a BUY trade with mode BUYFAST, on token %MyToken% with an amount of 730 BUSD . No initial STOP LIMIT setting (-1). The polling timing interval is set to 0 seconds (optimal for fast actions). Trigger a SELL automatically when the amount gained reaches 30 BUSD.

```
python3.6 detectorTraderAIExecutor.py ONCE BUYFAST %MyToken%BUSD 730 -1 -1 0 30
```

# Configuration Parameters

The following parameters can be set according to your trading strategy or MODE of operation.

**Parameter Syntax:**
 
 python detectorTraderAIExecutor.py **MODE BUYPARAM COIN_NAME_TO_TRADE MAX_AMOUNT_BUY STOP_LIMIT_SELL_THRESHOLD_PARAM STOP_LIMIT_INCREASE_PERC_PARAM TIME_INTERVAL_SLEEP GAIN_AMOUNT_THRESHOLD**


**Parameters:**


**MODE:** 

Can be ONCE or in LOOP

ONCE -> The trade iteration is executed only once and finishes when the trade exits

LOOP -> The trade iteration is reiterated and starts a new trade when the starting trade finishes


**BUYPARAM:**

BUYNOW (buy coin immediately) or NOTBUYNOW (buy at low price curve) or BUYFAST (faster and simpler execution, ideal for big pumps)


**COIN_NAME_TO_TRADE:**

Coin pair to trade, with the following syntax %TokenName%%TradingPair% (ex. SNMUSDT)


**MAX_AMOUNT_BUY:**

Amount you want to spend for the current trande (according to the token trading pair you choose (Ex. 1000 USDT)


**STOP_LIMIT_SELL_THRESHOLD_PARAM:**

Initial Stop Limit threshold (expressed in percent % relative to the buy price) you want to set immediately after a BUY is executed. This might depend from the trading activity and of course from the amount you can afford to loose. NOTE: be aware not to choose a too small threshold, to avoid having a SELL when the price jumps a bit. 

**STOP_LIMIT_INCREASE_PERC_PARAM:**

The Stop Limit increase threshold (expressed in percent % and is relative to the initial STOP_LIMIT_SELL_THRESHOLD_PARAM  threshold). Iff the price of the token increases by the set Stop Limit increase threshold X 2, the preview stop limit order is cancelled and incremented by the STOP_LIMIT_INCREASE_PERC_PARAM threshold relative to the preview stop limit order.

**TIME_INTERVAL_SLEEP:**

This parameter allows to set the time interval (in seconds) between one monitoring iteration and subsequent ones. For a fast operation choose (set 0), in most cases having a time interval of 1 second is appropriate (set 1) 

**GAIN_AMOUNT_THRESHOLD:**

Amount of gain relative to your investment, where you want to force a SELL. If positive (+) it's a gain $, if negative (-) it's the affordable loss you want to take if the price dumps fast.

**A NULL parameter (not used):**

To pass a NULL parameter use the value -1


# Internal program parameters (to be edited in the code):


**OPERATIONAL_MODE** 

If True == real Trade 

If False == Test mode


**LOG_MODE** 

If False does only print the program output on the shell

If True the output is logged to log files (logs folder)

 
 
# How to Run the software in different MODEs
 

**Cases:**

1) MODE (BUYFAST)

Run a Trade ONCE in MODE BUYFAST on the coin pair  SNMBUSD with the amount of 3000 BUSD and set a initial STOP_LIMIT_SELL_THRESHOLD_PARAM set to 3.0 % below the buy price, the Trade monitors the price level in iterations of 0 seconds (-1 are unused params).
 

Example execution:
 
```
python detectorTraderAIExecutor.py ONCE BUYFAST SNMBUSD 3000 3.0 -1 0 -1
```

 
# User COMMANDS

User commands are available for executing given operations for example to BUY, SELL or set STOPLIMIT orders.

A command can be issued by the user anytime by creating a command named file in the "cmds" folder (i.e Sell command: ./cmds/sell). This is simply an empty file with the filename that corresponds to the command name. Whenever the commands is excuted the file is removed automatically.

In linux/unix/MacOS environment you may use the following sintax:

```
touch ./cmds/name_of_command
```


**Execute a SELL command**

A SELL operation can be triggered anytime by the user by executing the following command.

```
./cmds/sell
```

**Set a STOPLIMIT command**

A new STOPLIMIT order can be re-set anytime by executing thie following command. The preview STOPLIMIT order is cancelled and reset to a new STOPLIMIT order with a threshold (parameter: STOP_LIMIT_SELL_THRESHOLD_PARAM) expressed in % below the current price level

Create an empty file named "sell" in the folder "cmds" (example: ./cmds/stoplimit ). 

In linux/unix/MacOS environment you may use the following command:

```
touch ./cmds/sell
```


# Free Contribution and further developments


Your free and precious contribution for further development of this Tool IF you like it and use it is very appreciated:
 
 If you find this trading utility Tool helpful to gain some nice $%$ profit$ while doing your trades and want to contribute to further development, improvements and fixes, please feel FREE to send some tiny amount of crypto you gained with this tool to one of these addresses:
 
 
 BTC (Bitcoin):          bc1q7fpjscwe3la7790nwfjw2z723zr8zg0mxu6w0e

 BUSD (BNB smart chain BEP20): 0x1D6047820F00dE49a7Eb7B57E8cd58EF034324D5

 
 
 Thank you for using and supporting the CryptoTraderAIHelperTool
 

 
    .'/  ,_   \'.
   |  \__( >__/  |
   \             /
    '-..__ __..-'
         /_\
 
 
A.C
SEESolutions.it


