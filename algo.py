import ta

def algo(dfIterrows,df,lastIndex):

    # Capital de départ
    usdt = 1000
    btc = 0

    #declaration variable (pas touché)

    # Courbe EMA
    ema_fast = 'EMA12'
    ema_slow = 'EMA26'
    ema_fast_periode=int(ema_fast[-2:])
    ema_slow_periode=int(ema_slow[-2:])

    # affichage variable
    print( "ema_fast => "+ ema_fast)
    print( "ema_fast_periode => "+ str(ema_fast_periode))
    print( "ema_slow => "+ ema_slow)
    print( "ema_slow_periode => "+ str(ema_slow_periode))


    df[ema_fast] = ta.trend.ema_indicator(df['close'], ema_fast_periode)
    df[ema_slow] = ta.trend.ema_indicator(df['close'], ema_slow_periode)

    for index, row in dfIterrows:
      if df[ema_fast][lastIndex] > df[ema_slow][lastIndex] and usdt > 10:
       btc = usdt / df['close'][index]
       btc = btc - 0.007 * btc
       usdt = 0
      #print("Buy BTC at",df['close'][index],'$ the',index)


      if df[ema_fast][lastIndex] < df[ema_slow][lastIndex] and btc < 0.000001:
       usdt = btc * df['close'][index]
       usdt = usdt - 0.007 * usdt
       btc = 0
      #print("Sell BTC at",df['close'][index],'$ the',index)


      lastindex = index

    return btc, usdt, df
