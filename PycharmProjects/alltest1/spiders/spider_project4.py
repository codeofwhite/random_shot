# 爬空气指数
import requests
import csv

csvfile = open('csv-aqi.csv', 'w', encoding='utf-8')
csv_write = csv.writer(csvfile)

url = 'https://data.epa.gov.tw/api/v2/aqx_p_432?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=ImportDate%20desc&format=JSON'
data = requests.get(url)
data_json = data.json()
print(data_json)
print(type(data_json))
print(data_json['records'])
print('\n')
for i in data_json['records']:
    print(i['county'] + '' + i['sitename'], end=',')
    print('AQI:' + i['aqi'], end=',')
    print('空气品质' + i['status'])
# 存入csv
output = [['county', 'sitename', 'aqi', '空气品质']]
for i in data_json['records']:
    output.append([i['county'], i['sitename'], i['aqi'], i['status']])
print(output)
csv_write.writerows(output)
