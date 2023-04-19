# Telegram Signal Scrapper BOT
this is a project I made in 2021 to extract spot orders from a telegram channel (of crypto signals) and save and execute them in binance and send the notification 
to a private telegram channel. (although the bot fulfilled its functionality after a few months I realized that the signals from that channel that now no longer 
exists were not very profitable so I stopped using the bot.)

#FEATURES
-Extracts values such as pair, entries, exits, stop loss, and take profit from a signal message like this one:

![sginals](https://user-images.githubusercontent.com/34092193/232940479-39dc0d74-aee1-4727-bd62-2cbb02f73f10.png)

-Saves the pairs and orders placed in Binance as .json files when the orders are executed. This prevents placing more than one order per pair and provides a proper record of orders.

-Sends the buy/sell order at the same time as their respective SL/TP orders. If the SL or TP orders are manually cancelled, the buy/sell orders are cancelled as well. Conversely, it avoids placing orders without SL/TP.

-Has a notification system that sends updates on each step performed to a private Telegram channel.

![private](https://user-images.githubusercontent.com/34092193/232941962-34c8a408-10cd-478b-8a14-d501df3bb487.png)


## libraries required - Python 3.6 or later

To run the bot, you need the following Python libraries:

-telethon
-binance

## Can I Use This Repo Freely?

Absolutely! Feel free to use this repo and learn how to develop a bot with similar features.
