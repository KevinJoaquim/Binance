import ta
import stat_file

def ema(dfIterrows,df,lastIndex,btc,usdt,ema_fast,ema_slow,ema_fast_periode,ema_slow_periode,stop_loss_value):


    df[ema_fast] = ta.trend.ema_indicator(df['close'], ema_fast_periode)
    df[ema_slow] = ta.trend.ema_indicator(df['close'], ema_slow_periode)

    params_backtest=["ema_fast :"+ str(ema_fast),"ema_slow :"+ str(ema_slow),"ema_fast_periode :"+ str(ema_fast_periode),"ema_slow_periode :"+ str(ema_slow_periode),"stop_loss_value :"+ str(stop_loss_value),usdt]

    my_action = []

    #print(df)


    stop_loss_action = False

    for index, row in dfIterrows:


      if usdt > 10:
          if df[ema_fast][lastIndex] > df[ema_slow][lastIndex] and stop_loss_action== False :
              usdt = usdt - (usdt - usdt * 0.99)
              btc = usdt / df['close'][index]
              btc_position = df['close'][index]
              #btc = btc - 0.007 * btc
              usdt = 0
              #print("Buy BTC at",df['close'][index],'$ the',index," BTC account = ",btc)
              my_action.append((str(index),str(df['close'][index]),btc,usdt,"Buy","","",""))

          elif df[ema_fast][lastIndex] < df[ema_slow][lastIndex]:
              stop_loss_action= False




      elif btc > 0.000001 :

          #if stop_loss_active :
          low_tmp = df['low'][index]

          usdt_stoploss = btc * btc_position
          usdt_stoploss = stop_loss_value * usdt_stoploss


          usdt_low = btc * low_tmp

          if  usdt_low < usdt_stoploss and stop_loss_action == False:
              usdt = usdt_stoploss - (usdt_stoploss - usdt_stoploss * 0.99)
              #usdt = usdt - 0.007 * usdt
              btc = 0
              stop_loss_action = True
              #print("stop_loss => "+ str(stop_loss))
              #print("btc_position => "+ str(btc_position))
              #print("price close btc => "+str(df['close'][index]))
              #print("low => "+str(df['low'][index] ))
              #print("Sell BTC at",df['close'][index],'$ the',index, "usdt account = ",usdt)
              #stop_loss_action == True
              my_action.append((str(index),str(df['close'][index]),btc,usdt,"Sell",usdt_stoploss,btc_position,str(df['low'][index])))




          elif df[ema_fast][lastIndex] < df[ema_slow][lastIndex]:
              usdt = btc * df['close'][index]
              usdt = usdt - (usdt - usdt * 0.99)
              btc = 0
              stop_loss_action = False
              #print("Sell BTC at",df['close'][index],'$ the',index, "usdt account = ",usdt)
              my_action.append((str(index),str(df['close'][index]),btc,usdt,"Sell",usdt_stoploss,btc_position,str(df['low'][index])))

      # STOPLOSS

      lastIndex = index
    stat_file.excel(my_action,params_backtest)
    return btc, usdt, df
