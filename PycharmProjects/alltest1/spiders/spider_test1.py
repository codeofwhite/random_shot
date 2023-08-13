import requests
import json

web = requests.get('https://water.taiwanstat.com/')
web.encoding = 'utf-8'
print(web.text)
web2 = requests.get('https://data.kcg.gov.tw/dataset/6f29'
                    'f6f4-2549-4473-aa90-bf60d10895dc/resource/30dfc2cf-17b'
                    '5-4a40-8bb7-c511ea166bd3/download/lightrailtraffic.json')
web2.encoding = 'utf-8-sig'  # 注意要使用 utf-8-sig 解码
print(web2.json())

with open('data.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(web2.json(), ensure_ascii=False))  # 要加ensure_ascii = False 转码才成功
