import pandas as pd
from binance.client import Client
import ta
import sys
import xlsxwriter
import algo

date_test = sys.argv[1]
print("date début du test : "+date_test)
try:

    klinesT = Client().get_historical_klines("BTCUSDT",Client.KLINE_INTERVAL_1HOUR, date_test)
    df = pd.DataFrame(klinesT, columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_bases_av', 'tb_quote_av', 'ignore'])


    #print(df)


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


    df = df.set_index(df['timestamp'])
    df.index = pd.to_datetime(df.index, unit='ms')

    del df['timestamp']
    #print(df)


    #print(df)

    #usdt = 1000
    #btc = 0
    lastIndex = df.first_valid_index()
    ema_fast_periode=0
    ema_slow_periode=0

    btc,usdt,df= algo.algo(df.iterrows(),df,lastIndex)


    finalResult = btc + usdt * int(float(df['close'].iloc[-1]))
    print("Final result",finalResult,'USDT')

    finalResult = usdt +  df['close'].iloc[-1]
    print("final Result",finalResult,'USDT')

    print ("Buy and hold result", (1000 / df['close'].iloc[0]) * df['close'].iloc[-1],'USDT')

except Exception as e:
    print('Failed to upload to ftp: '+ str(e))


exit(0)

