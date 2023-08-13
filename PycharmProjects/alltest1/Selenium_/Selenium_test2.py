# 点击网页事件
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.webdriver import Service

chrome_options = Options()
chrome_options.page_load_strategy = 'eager'
s = Service('./chromedriver')
driver = webdriver.Chrome(service=s, options=chrome_options)
driver.get('https://example.oxxostudio.tw/python/selenium/demo.html')
a = driver.find_element(By.ID, 'a')
show = driver.find_element(By.ID, 'show')
actions = ActionChains(driver)
actions.click(show).send_keys(['1', '2', '3', '4', '5'])
actions.pause(1)
actions.double_click(a)
actions.pause(1)
actions.click(show)
actions.send_keys_to_element(show, ['A', 'B', 'C', 'D', 'E'])  # # 輸入 A～E 的鍵盤值
actions.perform()
