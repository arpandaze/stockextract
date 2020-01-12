import xlsxwriter

# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook('Expenses01.xlsx')
worksheet = workbook.add_worksheet()

# Some data we want to write to the worksheet.
expenses = (['S&P 500', 324628, '0.35', '0.50', '28.21'], ['Nasdaq Comp', 907147, '0.56', '1.12', '34.61'], ['Dow Jones 2870338', '0.24', '0.62', '22.49'], ['Russell2000', '166326', '0.14', '-0.30', '20.46'])

# Start from the first cell. Rows and columns are zero indexed.
row = 0
col = 0

# Iterate over the data and write it out row by row.
for item, cost, i, j, k in (expenses):
    worksheet.write(row, col,     item)
    worksheet.write(row, col + 1, cost)
    row += 1

# Write a total using a formula.
worksheet.write(row, 0, 'Total')
worksheet.write(row, 1, '=SUM(B1:B4)')

workbook.close()