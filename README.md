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

 This source code repository provides some software tools that aim to be useful for supporting the trading of crypto tokens on the Binance Crypto Exchange.

 It's may be particularly useful in cases of small and big pumps or price increases over longer time periods. 

 If you catch the right momentum in a trade with the proper configuration parameters, you may stay more relaxed while the market rumbles.
 

# Description
 
This small crypto trading helper Tool comes with some functionalities for supporting your trading activity. It consists of some python code scripts that can be run in a commmon command shell available on Windows, MacOS and Linux. The program can be parameterized with configurable parameters and has different modes of operation. The tool allows to make BUYs and SELLs in semi-automatic way while constantly monitoring a token price. Stop Limits for SELLs are automatically set and are incremental according to growing or downing price levels. It simplyfies to some extend buying and selling your favorite crypto token. It is very useful in cases of big and instant price increases or constant slow price increases over longer time periods. Version 1.0 is just the first draft of this crypto trading utility, very interesting features will follow soon that will allow complex automatic AI decision trades. 
This software will at some point be able to automatically detect trading activities on the crypto markets and forcast possible trades that deliver gains. In particular this tool will also detect initial bit coin Pumps that can deliver significant gains.

 
# Features (MODEs of operation)

The software implements different modes of operation depending on the type of trade the user wants to make. More such modes will follow with future versions of the CryptoTraderAIHelperTool.

Currently the CryptoTraderAIHelperTool V1.0 supports the following modes:


**BUYNOW:**

Make an instant BUY and set a starting STOP LIMIT at a configurable threshold below the price level (expressed in percentage relative to buy price)
The software monitors constantly the price and as the price level increases or decreases it adjusts the configured STOP LIMIT thresholds.
When a SELL Command is executed, either by the user or automatically, the active stop limits orders are cancelled and a SELL at market price or desired price is executed.

A SELL can occur either automatically via executed stop limit orders, at a configurable amount (%) gained or at any moment by the user

This operations can be performed in two modes, ONCE or in a constant iterated LOOP


**NOTBUYNOW:** (experimental)

Calculate the price curve in a given time interval and detect the best BUY moment (ascending curve). STOP LIMIT orders are set and updated incrementally according to the 
configured thresholds (STOP_LIMIT_SELL_THRESHOLD_PARAM) expressed in percentage (%) relative to the buy price.


**BUYFAST:**

Similar to BUYNOW but with a faster execution. Sets only an initial Stop Limit order when a BUY is executed. In this mode there is NO automatic incremental STOP LIMIT orders)

This mode also allows also to make a fast BUY when a token is going to be listed for the first time. In this case the token availability is constantly monitored and as soon the token becomes available for trading the current price is shown. The user may than trigger a buy by issuing a BUY command (touch ./cmds/buy). NOTE: By default the ./cmds/buy command is active, so you have to remove this file if you want to poll the token price and you preffer to issue the BUY command manually.
 

# How it Works

When a trade is executed (BUY), the token price is monitored continuously at a given time interval defined by the user.
STOP LIMIT SELL orders are set (STOP_LIMIT_SELL_THRESHOLD_PARAM) and incremented or decremented automatically according to configurable thresholds (STOP_LIMIT_INCREASE_PERC_PARAM) expressed in percentage (%) relative to the price level.
 

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

2) The python code sofware is located in folder "src" that contains also auxiliary folders needed for execution. The scripts must be run from the command shell within the "src" folder.

The auxiliary folders are:
- logs: contain the log files of the trades)
- GAINS: contain a "GAINS.csv" file with the listed gains or losses of the trades executed
- cmds: commands can be executed by creating an empty file in this folder with the named command to be executed (ex. buy, sell, etc..). The program will detect these files and act accordingly.

 
# How to Run the software

1) Choose the MODE of execution for your trade (see MODE parameter)

2) Define the proper parameters for the crypto token you want to trade. 

NOTE: Each Token might have individual parameter settings according to market conditions (volume, speed, price jumps, etc....). 
For example if you set a too tight stop limit increase threshold, it's likely that your stop limit orders are executed immediately if the price makes instant jumps (this happens frequently in the initial momentum when a token starts to be traded actively, especially if the trade volume is low initially.

To run the software just open the command shell or terminal and execute the python script contained in the 'src' folder with the desired parameters.


Run a Trade Example:

Run a BUY trade with mode BUYFAST, on token %MyToken% with 730 BUSD . No initial STOP LIMIT setting (-1). The polling timing interval is set to 0 seconds (optimal for fast actions). Trigger an automatic SELL wehn the amount gained reaches 30 BUSD.

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


# Internal program parameters (to be edited in the scripts):


**OPERATIONAL_MODE** 

If True == real Trade 

If False == Test mode

**LOG_MODE** 

If False does only print the program output on the shell

If True the output is logged to log files (logs folder)

 
 
# How to Run the software in different MODEs
 
**Cases:**

1)
Run a Trade ONCE in BUYFAST MODE on COIN_NAME_TO_TRADE SNMBUSD with the MAX_AMOUNT_BUY of 3000 BUSD with a initial STOP_LIMIT_SELL_THRESHOLD_PARAM set to 3.0 % below the buy price, the Trade monitoring iterates at 0 seconds TIME_INTERVAL_SLEEP (-1 are unused params)
 

Example execution:
 
```
python detectorTraderAIExecutor.py ONCE BUYFAST SNMBUSD 3000 3.0 -1 0 -1
```
 
# HowTo

**Execute a SELL command manually**

Create an empty file named "sell" in the folder "cmds" (example: ./cmds/sell ). 
In linux/unix/MacOS environment you may use the following command:

```
touch ./cmds/sell
```

# Contribution and further developments


Your free and precious contribution for further development of this Tool IF you like it and use it:
 
 If you find this trading utility Tool helpful to gain some nice $%$ profit$ while doing your trades and want to contribute to further development, improvements and fixes, please feel FREE to send some tiny amount of crypto you gained with this tool to one of these addresses:
 
 
 BUSD (BNB smart chain BEP20): 0x35372ea66892ed35109fb381caa88b7fed75e4b2
 
 BTC (Bitcoin):          1K1PHeqiUFoQ6Yp8mNP6u2sZR7R23QnffQ
 
 ETH (Ethereum ERC20):   0x35372ea66892ed35109fb381caa88b7fed75e4b2
 
 BNB (BNB smart chain BEP20):        0x35372ea66892ed35109fb381caa88b7fed75e4b2
 
 USDT (Ethereum ERC20): 0x35372ea66892ed35109fb381caa88b7fed75e4b2
 
 
 THANKS a LOT, you will not regret for getting further improvements and functionalities for your Trades
 

 
    .'/  ,_   \'.
   |  \__( >__/  |
   \             /
    '-..__ __..-'
         /_\
 
 
A.C


