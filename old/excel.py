import xlsxwriter

sampleUSA = open('sampleUSA.txt','r').read().split('\n')
sampleEurope = open('sampleEuropa.txt','r').read().split('\n')
for i in sampleUSA:
    sampleUSA[sampleUSA.index(i)]=i.split(',')

for i in sampleEurope:
    sampleEurope[sampleEurope.index(i)]=i.split(',')

workbook = xlsxwriter.Workbook('example.xlsx')
worksheet = workbook.add_worksheet()

row = 0
col = 0
print(tuple(sampleUSA))
for item1,item2,item3,item4,item5 in tuple(sampleUSA):
    worksheet.write(row,col,item1)
    worksheet.write(row,col+1,item2)
    worksheet.write(row,col+2,item3)
    worksheet.write(row,col+3,item4)
    #worksheet.write(row,col+4,item5)
    row += 1

workbook.close()