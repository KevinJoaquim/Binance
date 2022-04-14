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
    worksheet.write(row, 0 + 1, "values close")
    worksheet.write(row, 0 + 2, "btc")
    worksheet.write(row, 0 + 3, "usdt")
    worksheet.write(row, 0 + 4, "Position")

    col = 0
    row = 1
    # Iterate over the data and write it out row by row.
    for list_action in (my_action):
        worksheet.write(row, col, list_action[0])
        worksheet.write(row, col + 1, list_action[1])
        worksheet.write(row, col + 2, list_action[2])
        worksheet.write(row, col + 3, list_action[3])
        worksheet.write(row, col + 4, list_action[4])
        row += 1

    workbook.close()
