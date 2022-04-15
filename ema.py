import ta
import stat_file

def ema(dfIterrows,df,lastIndex,btc,usdt,ema_fast,ema_slow,ema_fast_periode,ema_slow_periode,stop_loss_active,stop_loss_value):


    df[ema_fast] = ta.trend.ema_indicator(df['close'], ema_fast_periode)
    df[ema_slow] = ta.trend.ema_indicator(df['close'], ema_slow_periode)

    my_action = []

    #print(df)


    for index, row in dfIterrows:

      stop_loss_action=False

      if usdt > 10:
          if df[ema_fast][lastIndex] > df[ema_slow][lastIndex] :
              btc = usdt / df['close'][index]
              btc_position = df['close'][index]
              btc = btc - 0.007 * btc
              usdt = 0
              #print("Buy BTC at",df['close'][index],'$ the',index," BTC account = ",btc)
              my_action.append((str(index),str(df['close'][index]),btc,usdt,"Buy","","",""))




      elif btc > 0.000001 :

          if stop_loss_active :
              low_tmp = df['low'][index]
              #print(low_tmp)

              usdt_stoploss = btc * btc_position
              usdt_stoploss = stop_loss_value * usdt_stoploss
              #print(usdt_tmp)


              usdt_low = btc * low_tmp

              if  usdt_low < usdt_stoploss:
                  usdt = usdt_stoploss
                  usdt = usdt - 0.007 * usdt
                  btc = 0
                  #print("stop_loss => "+ str(stop_loss))
                  #print("btc_position => "+ str(btc_position))
                  #print("price close btc => "+str(df['close'][index]))
                  #print("low => "+str(df['low'][index] ))
                  #print("Sell BTC at",df['close'][index],'$ the',index, "usdt account = ",usdt)
                  stop_loss_action == True
                  my_action.append((str(index),str(df['close'][index]),btc,usdt,"Sell",usdt_stoploss,btc_position,str(df['low'][index])))




          if df[ema_fast][lastIndex] < df[ema_slow][lastIndex] and stop_loss_action == False:
              usdt = btc * df['close'][index]
              usdt = usdt - 0.007 * usdt
              btc = 0
              #print("Sell BTC at",df['close'][index],'$ the',index, "usdt account = ",usdt)
              my_action.append((str(index),str(df['close'][index]),btc,usdt,"Sell",usdt_stoploss,btc_position,str(df['low'][index])))

      # STOPLOSS

      lastIndex = index

    stat_file.excel(my_action)
    return btc, usdt, df
