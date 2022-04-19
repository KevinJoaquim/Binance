import xlsxwriter
import datetime
import statistics

def excel(my_action,params_backtest):



    t = datetime.datetime.now()
    name_file = 'backtest-'+str(t)
    workbook = xlsxwriter.Workbook(name_file+'.xlsx')

    # By default worksheet names in the spreadsheet will be
    # Sheet1, Sheet2 etc., but we can also specify a name.
    worksheet = workbook.add_worksheet("My sheet")

    cell_format = workbook.add_format()
    cell_format.set_bold()
    cell_format.set_font_color('blue')

    cell_format_pourcentage = workbook.add_format()

    cell_format_pourcentage.set_num_format(3)

# Start from the first cell. Rows and
    # columns are zero indexed.
    row = 0
    worksheet.write(row, 0, "id timestamp",cell_format)
    worksheet.write(row, 1, "timestamp close",cell_format)
    worksheet.write(row, 2, "values close",cell_format)
    worksheet.write(row, 3, "btc",cell_format)
    worksheet.write(row, 4, "usdt",cell_format)
    worksheet.write(row, 5, "Position",cell_format)
    worksheet.write(row, 6, "result win/lost",cell_format)
    worksheet.write(row, 11, "usdt_stoploss",cell_format)
    worksheet.write(row, 12, "btc_position",cell_format)
    worksheet.write(row, 13, "low",cell_format)

    col = 7
    row = 1

    list_trade_lost = []
    list_trade_win = []

    for params_backtest_result in (params_backtest):

        worksheet.write(row, col, params_backtest_result)
        row = row +1


    col = 1
    row = 1

    #stat trade
    trade_win = 0
    trade_lost = 0


    # Iterate over the data and write it out row by row.
    for list_action in (my_action):
        worksheet.write(row, 0, row-1)
        worksheet.write(row, col, list_action[0])
        worksheet.write(row, col + 1, list_action[1])
        worksheet.write(row, col + 2, list_action[2])
        worksheet.write(row, col + 3, list_action[3])
        worksheet.write(row, col + 4, list_action[4])

        usdt = list_action[3]
        if row == 2 :
            if usdt < params_backtest[5]:
                trade_lost=trade_lost+1
                trade_lost_pourcentate = usdt / params_backtest[5] * 100

                list_trade_lost.append(trade_lost_pourcentate)
            else:
                trade_win=trade_win+1
                trade_win_pourcentate = usdt / params_backtest[5] * 100
                list_trade_win.append(trade_win_pourcentate)

            worksheet.write(row, col + 5, usdt / params_backtest[5] * 100 )
            usdt_tmp = usdt
        else:
            if usdt != 0:
                if usdt_tmp > list_action[3]:
                    trade_lost=trade_lost+1

                    list_trade_lost.append(usdt / usdt_tmp * 100)
                else:
                    trade_win=trade_win+1
                    list_trade_win.append(usdt / usdt_tmp * 100)

                worksheet.write(row, col + 5, usdt / usdt_tmp * 100 )

                usdt_tmp = list_action[3]



        worksheet.write(row, col + 10, list_action[5])
        worksheet.write(row, col + 11, list_action[6])
        worksheet.write(row, col + 12, list_action[7])
        row += 1



    number_trade_total= trade_win + trade_lost
    worksheet.write(9, 8, "nb")
    worksheet.write(9, 9, "%")
    worksheet.write(10, 7, "win")
    worksheet.write(10, 8, trade_win)
    worksheet.write(10, 9, trade_win / number_trade_total * 100,cell_format_pourcentage)
    worksheet.write(11, 7, "lost")
    worksheet.write(11, 8, trade_lost)
    worksheet.write(11, 9, trade_lost / number_trade_total * 100,cell_format_pourcentage)


    moyen_trade_lost = statistics.mean(list_trade_lost)
    moyen_trade_win = statistics.mean(list_trade_win)

    worksheet.write(12, 7, "moyen win")
    worksheet.write(12, 8, str(moyen_trade_win))
    worksheet.write(13, 7, "moyen lost")
    worksheet.write(13, 8, str(moyen_trade_lost))

# Charts are independent of worksheets
    chart = workbook.add_chart({'type': 'line'})
    chart.set_y_axis({'name': 'USDT values'})
    chart.set_x_axis({'name': 'id timestamp'})
    chart.set_title({'name': 'Sell Bitcoin to USDT$'})

    data_start_loc = [1, 4] # xlsxwriter rquires list, no tuple
    data_end_loc = [data_start_loc[1] + len(my_action), 4]

    chart.add_series({
        'values': [worksheet.name] + data_start_loc + data_end_loc,
        'name': "USDT $",
    })
    chart.set_size({'width': 720, 'height':720})
    worksheet.insert_chart('O1', chart)


    workbook.close()
