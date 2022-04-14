import asyncio
import pandas as pd
import xlsxwriter
import logging
from binance.client import Client
from binance import ThreadedWebsocketManager
import pprint
from time import sleep

TEST_NET = True



# Get the BTC value in the last 24 hrs
def btc_values_received(msg):
    ''' Process the btc values received in the last 24 hrs '''

    if msg['e'] != 'error':
        print(msg['e'] + "/////////////////////////////////////////////////////////// price BTCUSDT = " + str(float(msg['c'])))
        btc_price['BTCUSDT'] = float(msg['c'])


    else:
        btc_price['error'] = True


# Buy or sell ETHUSDT when BTC reaches a particular value
def buy_and_sell_ETH_at_BTC():

    while True:
        # error check to make sure WebSocket is working
        if btc_price['error']:
            # stop and restart socket (cleanup)
            twm.stop()
            sleep(2)
            twm.start()
            btc_price['error'] = False
        else:
            if 1000 < btc_price['BTCUSDT'] < 40000:  # bitcoin price
                try:
                    print("Buying when BTCUSDTprice:", btc_price['BTCUSDT'])
                    order = client.order_market_buy(symbol='ETHUSDT', quantity=1)
                    pprint.pprint(order)
                    f = open("history-transaction.txt", "a")
                    timestamp = pd.to_datetime(order["transactTime"], unit='ms')

                    f.write(timestamp + " ; "+order["side"]+ ' , ' + str(order) + '\n')
                    f.close()


#curl -X POST --data-urlencode "payload={\"channel\": \"#trade\", \"username\": \"webhookbot\", \"text\": \"Ceci est publié dans #trade et provient d'un robot nommé webhookbot.\", \"icon_emoji\": \":ghost:\"}" https://hooks.slack.com/services/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


                    break
                except Exception as e:
                    print(e)
                    break
            else:
                try:
                    print("Selling when BTCUSDT price:", btc_price['BTCUSDT'])
                    order = client.order_market_sell(symbol='ETHUSDT', quantity=1)
                    pprint.pprint(order)

                    f = open("history-transaction.txt", "a")
                    timestamp = pd.to_datetime(order["transactTime"], unit='ms')

                    f.write(str(timestamp) + " ; "+order["side"] + ' , ' + str(order) + '\n')
                    f.close()
                    break
                except Exception as e:
                    print(e)
                    break
            sleep(0.1)



def main():


    pprint.pprint(client.get_account())
    #print(client.get_asset_balance(asset='BNB'))
    eth_price = client.get_symbol_ticker(symbol="ETHUSDT")
    #print(eth_price)
    # Start the websocket manager and register
    # callback for the bitcoin price
    twm.start()
    twm.start_symbol_ticker_socket(callback=btc_values_received, symbol='BTCUSDT')
    # wait here to receive some btc value initially through websocket callback
    while not btc_price['BTCUSDT']:
        sleep(0.1)
    # call buy ETH function with a while loop to keep a track on btc price
    buy_and_sell_ETH_at_BTC()
    #twm.join() # to stop main thread exit.
    #twm.stop()


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
    #logging.getLogger("asyncio").setLevel(logging.WARNING)

    if TEST_NET:
        # passkey (saved in bashrc for linux)
        api_key = 'bAQbSugYEBgYVBu89joIflmRPRovcThZK29PqRUjEOQ2LaRXOPMPhxCAoOCkRWGI'

        # secret (saved in bashrc for linux)
        api_secret = 'rerlKK4JbkPydfThevFNYT7gUZfwSoxNvsQd5kkFbSzIj5eygfSsR8ng287Smmxh'

        client = Client(api_key, api_secret, testnet=True)
        print("Using Binance TestNet server")

    # Add btc price and instantiate ThreadedWebsocketManager()
    btc_price = {'BTCUSDT': None, 'error': False}
    twm = ThreadedWebsocketManager()

    #loop = asyncio.get_event_loop()
    #asyncio.run(main(), debug=True)
    main()