# 爬汇率
import requests
import csv

csvfile = open('trade.csv', 'w', encoding='utf-8')
csv_write = csv.writer(csvfile)

url = 'https://rate.bot.com.tw/xrt/flcsv/0/day'
rate = requests.get(url)
rate.encoding = 'utf-8'
rt = rate.text
rts = rt.split('\n')
output = []
for i in rts:
    try:
        a = i.split(',')
        print(a[0] + ':' + a[12])
        output.append([a[0], a[12]])
    except:
        break
csv_write.writerows(output)
