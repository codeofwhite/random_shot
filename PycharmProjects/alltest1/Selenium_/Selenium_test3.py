# 爬取网页小测试：爬取的是tag最内的text
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import Service
from selenium.webdriver.common.by import By

url = 'file:///C:/Users/zhj20/PycharmProjects/alltest1/Selenium_/selenium_test3.html'
s = Service("C:/Users/zhj20/PycharmProjects/alltest1/Selenium_/chromedriver.exe")
driver = webdriver.Chrome(service=s)
driver.get(url)
text1 = driver.find_elements(By.TAG_NAME,'div')
print(text1[0].text)
