import ta
import stat_file

def ema(dfIterrows,df,lastIndex,btc,usdt,ema_fast,ema_slow,ema_fast_periode,ema_slow_periode):


    df[ema_fast] = ta.trend.ema_indicator(df['close'], ema_fast_periode)
    df[ema_slow] = ta.trend.ema_indicator(df['close'], ema_slow_periode)

    my_action = []


    for index, row in dfIterrows:
      if df[ema_fast][lastIndex] > df[ema_slow][lastIndex] and usdt > 10:
          btc = usdt / df['close'][index]
          btc = btc - 0.007 * btc
          usdt = 0
          #print("Buy BTC at",df['close'][index],'$ the',index," BTC account = ",btc)
          my_action.append((str(index),str(df['close'][index]),btc,usdt,"Buy"))


      if df[ema_fast][lastIndex] < df[ema_slow][lastIndex] and btc > 0.000001:
          usdt = btc * df['close'][index]
          usdt = usdt - 0.007 * usdt
          btc = 0
          #print("Sell BTC at",df['close'][index],'$ the',index, "usdt account = ",usdt)
          my_action.append((str(index),str(df['close'][index]),btc,usdt,"Sell"))


      lastIndex = index

    stat_file.excel(my_action)
    return btc, usdt, df
