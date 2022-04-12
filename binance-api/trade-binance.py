import os
from binance.client import Client
from binance import ThreadedWebsocketManager
import pprint
from time import sleep

TEST_NET = True


# Get the BTC value in the last 24 hrs
def btc_values_received(msg):
    ''' Process the btc values received in the last 24 hrs '''

    pprint.pprint(msg)

    if msg['e'] != 'error':
        print(msg['e'])
        btc_price['BTCUSDT'] = float(msg['c'])
    else:
        btc_price['error'] = True


def main():
    pprint.pprint(client.get_account())
    print(client.get_asset_balance(asset='BNB'))  # BTC, USDT, ETH

    # get latest price from Binance API
    eth_price = client.get_symbol_ticker(symbol="ETHUSDT")
    print(eth_price)

    # Start the websocket manager and register
    # callback for the bitcoin price
    twm.start()
    twm.start_symbol_ticker_socket(callback=btc_values_received,
                                   symbol='BTCUSDT')
    # To keep the ThreadedWebsocketManager running using join()
    # to join it to the main thread.
    twm.join()


if __name__ == "__main__":
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
    main()

    main()
