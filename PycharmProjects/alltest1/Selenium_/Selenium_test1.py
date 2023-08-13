# bug = selenium版本需要换成3.11.0的版本
# 新版本的操作略微不同，这里用旧版本
# 自动操作网页基本
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select  # 使用 Select 對應下拉選單
from selenium.webdriver.chrome.webdriver import Service
import time

s = Service('chromedriver.exe')
driver = webdriver.Chrome(service=s)
driver.get('https://www.runoob.com/')  # 開啟範例網址
a = driver.find_element(By.CLASS_NAME, 'qrcode')  # 取得 id 為 a 的網頁元素 ( 按鈕 A )

action = ActionChains(driver)

action.click_and_hold(a)
print(a.text)  # 印出 a 元素的內容
time.sleep(1)
action.perform()  # 執行儲存的動作
