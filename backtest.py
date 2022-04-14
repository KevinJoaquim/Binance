import pandas as pd
from binance.client import Client
import ta
import sys
import xlsxwriter
import ema

try:

    ## VARIABLE A MODIFIER

    date_test_depart = "01 January 2017"
    kline_interval = Client.KLINE_INTERVAL_1HOUR
    symbol = "BTCUSDT"
    # Courbe EMA
    ema_fast = 'EMA12'
    ema_slow = 'EMA32'
    ema_fast_periode=12
    ema_slow_periode=32

    usdt = 1000
    btc = 0

    print("date début du test : "+date_test_depart)
    print( "ema_fast => "+ ema_fast)
    print( "ema_fast_periode => "+ str(ema_fast_periode))
    print( "ema_slow => "+ ema_slow)
    print( "ema_slow_periode => "+ str(ema_slow_periode))


## Import, define Client and download data
    klinesT = Client().get_historical_klines(symbol,kline_interval, date_test_depart)
    df = pd.DataFrame(klinesT, columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_bases_av', 'tb_quote_av', 'ignore'])

    ## Clean Dataset

    del df[ 'tb_bases_av']
    del df[ 'ignore']
    del df[ 'close_time']
    del df[ 'quote_av']
    del df[ 'trades']
    del df[ 'tb_quote_av']

    df ['close'] = pd.to_numeric(df['close'])
    df ['high'] = pd.to_numeric(df['high'])
    df ['low'] = pd.to_numeric(df['low'])
    df ['open'] = pd.to_numeric(df['open'])
    #print(df)

    ## convert time
    df = df.set_index(df['timestamp'])
    df.index = pd.to_datetime(df.index, unit='ms')

    del df['timestamp']

    lastIndex = df.first_valid_index()

    btc,usdt,df= ema.ema(df.iterrows(),df,lastIndex,btc,usdt,ema_fast,ema_slow,ema_fast_periode,ema_slow_periode)

    print("final bitcoin", btc)
    finalResult = btc + usdt * int(float(df['close'].iloc[-1]))
    print("Final result",finalResult,'USDT')


except Exception as e:
    print('Failed to upload to ftp: '+ str(e))


exit(0)

