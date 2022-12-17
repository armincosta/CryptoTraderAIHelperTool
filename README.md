####################################################

                   Software
                                      
           CryptoTraderAIHelperTool V1.0
                                        
   A tiny helpful Crypto Trading utility helper Tool
   

####################################################


 Software provided by SEESolutions.it
 
 copyright(c) 2022 - 2025

 
 Software License:

  Creative Commons Attribution-ShareAlike 4.0 International Public License (CC-SA)

  See LICENSE_CreativeCommons_CC-SA license and LICENSE_DISCLAIMER files for detailed terms

  CreativeCommons License ref: 
  https://creativecommons.org/licenses/by-sa/4.0/legalcode


Author: Armin Costa (admincostaAThotmail.com)


Contact: SEE Solutions e-mail: info@seesolutions.it


####################################################



# Intro

 Helper Tool software that aims to be helpful for aiding trading on Binance Crypto Exchange.

 It's particularly useful in case of small and big pumps or longer price increase time periods. If you

catch the momentum with the proper configurations you may lean back and see your $ growing without 

stressing yourself.
 

# Description
 
This small crypto trading helper Tool with a set of functionalities for improving and supporting your trading activity. It consists of a python code script that can be run in a commandd shell with a set of defined configurable parameters. The tool allows to make BUYs and SELLs in automatic way while constantly monitoring the token price being traded. Stop Limits for SELLs are automatically set and are incremental according to growing or downing price levels. It simplyfies buying and selling your favorite token. Especially helpful in cases of big and instant price increases or constant price increases over longer time periods.
 
 
# How it Works


 
# Prerequisites:



# How to Install
 
 
# Run Parameter Syntax

The following parameters can be set according to your strategy


MODE: 

Can be ONCE or in LOOP

BUYPARAM:

BUYNOW (buy coin immediately) or BUYLOW (buy at low price curve) or BUYFAST (faster and simpler execution, ideal for big pumps)

COIN_NAME_TO_TRADE:

Coin pair to trade, with the following syntax %TokenName%%TradingPair% (ex. SNMUSDT)

MAX_AMOUNT_BUY:

Amount you want to spend for the current trande (according to the token trading pair you choose (Ex. 1000 USDT)

STOP_LIMIT_SELL_THRESHOLD_PARAM:

STOP_LIMIT_INCREASE_PERC_PARAM:

TIME_INTERVAL_SLEEP:

GAIN_AMOUNT_THRESHOLD:

OPERATIONAL_MODE = True # True == real Trade  | False == Test mode
LOG_MODE = False # True == log to log files

 Example:
 ```
 python detectorTraderAIExecutor.py %MODE% %BUYPARAM% %COIN_NAME_TO_TRADE% %MAX_AMOUNT_BUY% %STOP_LIMIT_SELL_THRESHOLD_PARAM% %STOP_LIMIT_INCREASE_PERC_PARAM% %TIME_INTERVAL_SLEEP% %GAIN_AMOUNT_THRESHOLD%
```

 
# How to Run the software in different MODEs
 
Cases:

1)
Run a Trade ONCE in BUYFAST MODE on COIN_NAME_TO_TRADE SNMBUSD with the MAX_AMOUNT_BUY of 3000 BUSD with a initial STOP_LIMIT_SELL_THRESHOLD_PARAM set to 3.0 % below the buy price, the Trade monitoring iterates at 0 seconds TIME_INTERVAL_SLEEP (-1 are unused params)
 

Example:
 
```
python detectorTraderAIExecutor.py ONCE BUYFAST SNMBUSD 3000 3.0 -1 0 -1
```
 
Parameter syntax:

```
python detectorTraderAIExecutor.py %MODE% %BUYPARAM% %COIN_NAME_TO_TRADE% %MAX_AMOUNT_BUY% %STOP_LIMIT_SELL_THRESHOLD_PARAM% %STOP_LIMIT_INCREASE_PERC_PARAM% %TIME_INTERVAL_SLEEP% %GAIN_AMOUNT_THRESHOLD%
```

Contribution for new and enhanced functionalities:

Your free and precious contribution for further development of this Tool IF you like it and use it:
 

 If you find this trading utility Tool helpful to gain some nice $%$ profit$ while doing your trades and want to contribute to further development, improvements and fixes, please feel FREE to send some tiny amount of crypto you gained with this tool to one of these addresses:
 
 
 BUSD (BNB smart chain BEP20): 0x35372ea66892ed35109fb381caa88b7fed75e4b2
 
 BTC (Bitcoin):          1K1PHeqiUFoQ6Yp8mNP6u2sZR7R23QnffQ
 
 ETH (Ethereum ERC20):   0x35372ea66892ed35109fb381caa88b7fed75e4b2
 
 BNB (BNB smart chain BEP20):        0x35372ea66892ed35109fb381caa88b7fed75e4b2
 
 USDT (Ethereum ERC20): 0x35372ea66892ed35109fb381caa88b7fed75e4b2
 
 
 THANKS a LOT and God beless you, you will not regret for getting further improvements and functionalities for your Trades
 

 
    .'/  ,_   \'.
   |  \__( >__/  |
   \             /
    '-..__ __..-'
         /_\
 
 
Your Phoenix
A.C


