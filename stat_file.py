import xlsxwriter
import datetime


def excel(my_action):



    t = datetime.datetime.now()
    name_file = 'backtest-'+str(t)
    workbook = xlsxwriter.Workbook(name_file+'.xlsx')

    # By default worksheet names in the spreadsheet will be
    # Sheet1, Sheet2 etc., but we can also specify a name.
    worksheet = workbook.add_worksheet("My sheet")

    cell_format = workbook.add_format()
    cell_format.set_bold()
    cell_format.set_font_color('blue')

    # Start from the first cell. Rows and
    # columns are zero indexed.
    row = 0
    worksheet.write(row, 0, "id timestamp",cell_format)
    worksheet.write(row, 1, "timestamp close",cell_format)
    worksheet.write(row, 2, "values close",cell_format)
    worksheet.write(row, 3, "btc",cell_format)
    worksheet.write(row, 4, "usdt",cell_format)
    worksheet.write(row, 5, "Position",cell_format)
    worksheet.write(row, 10, "usdt_stoploss",cell_format)
    worksheet.write(row, 11, "btc_position",cell_format)
    worksheet.write(row, 12, "low",cell_format)

    col = 1
    row = 1

    # Iterate over the data and write it out row by row.
    for list_action in (my_action):
        worksheet.write(row, 0, row-1)
        worksheet.write(row, col, list_action[0])
        worksheet.write(row, col + 1, list_action[1])
        worksheet.write(row, col + 2, list_action[2])
        worksheet.write(row, col + 3, list_action[3])
        worksheet.write(row, col + 4, list_action[4])


        worksheet.write(row, col + 10, list_action[6])
        worksheet.write(row, col + 11, list_action[7])
        worksheet.write(row, col + 12, list_action[8])
        row += 1

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
