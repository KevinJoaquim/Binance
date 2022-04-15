import xlsxwriter
import datetime


def excel(my_action):
    t = datetime.datetime.now()
    name_file = 'backtest-'+str(t)
    workbook = xlsxwriter.Workbook(name_file+'.xlsx')

    # By default worksheet names in the spreadsheet will be
    # Sheet1, Sheet2 etc., but we can also specify a name.
    worksheet = workbook.add_worksheet("My sheet")


    # Start from the first cell. Rows and
    # columns are zero indexed.
    row = 0
    worksheet.write(row, 0, "timestamp close")
    worksheet.write(row, 1, "values close")
    worksheet.write(row, 2, "btc")
    worksheet.write(row, 3, "usdt")
    worksheet.write(row, 4, "Position")
    worksheet.write(row, 10, "usdt_stoploss")
    worksheet.write(row, 11, "btc_position")
    worksheet.write(row, 12, "low")

    col = 0
    row = 1
    # Iterate over the data and write it out row by row.
    for list_action in (my_action):
        worksheet.write(row, col, list_action[0])
        worksheet.write(row, col + 1, list_action[1])
        worksheet.write(row, col + 2, list_action[2])
        worksheet.write(row, col + 3, list_action[3])
        worksheet.write(row, col + 4, list_action[4])


        worksheet.write(row, col + 10, list_action[5])
        worksheet.write(row, col + 11, list_action[6])
        worksheet.write(row, col + 12, list_action[7])
        row += 1

    workbook.close()
