# Telegram Signal Scrapper BOT
this is a project I made in 2021 to extract spot orders from a telegram channel (of crypto signals) and save and execute them in binance and send the notification 
to a private telegram channel. (although the bot fulfilled its functionality after a few months I realized that the signals from that channel that now no longer 
exists were not very profitable so I stopped using the bot.)

#FEATURES
-The bot could pull values such as pair, entries, exits, stop loss, and take profit from a signal message like this one:

![sginals](https://user-images.githubusercontent.com/34092193/232940479-39dc0d74-aee1-4727-bd62-2cbb02f73f10.png)

-saved in .json the pairs and the orders placed in binance when the orders were executed, to avoid placing more than one order per pair and to have a proper 
record of orders.

-send the buy/sell order at the same time as their respective SL/TP orders, if the sl or tp were cancelled manually so were the 
buy/sell orders or on the contrary avoiding to place orders without sl/tp.

-Finally, it has a notification system that sends each step performed to a private telegram channel.

![private](https://user-images.githubusercontent.com/34092193/232941962-34c8a408-10cd-478b-8a14-d501df3bb487.png)


## libraries required - Python 3.6 or later

- telethon.
- binance.

## can i use this repo freely?

of course you can, feel free to use this repo and learn how to develop a bot with similar features :).
