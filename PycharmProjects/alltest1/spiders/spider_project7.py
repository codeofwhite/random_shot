# 这个干不过验证

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.webdriver import Service
from selenium.webdriver.chrome.webdriver import Service

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15"
opt = webdriver.ChromeOptions()
opt.add_argument('--user-agent=%s' % user_agent)
s = Service('C:/Users/zhj20/PycharmProjects/alltest1/Selenium_/chromedriver.exe')
driver = webdriver.Chrome(service=s)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
})
driver.get('https://www.mobile01.com/')
# checkbox = driver.find_element(By.CSS_SELECTOR, 'input[type = "checkbox"]')
# checkbox.click()

# loginBtn = driver.find_element(By.CSS_SELECTOR, 'a.c-login')
# loginBtn.click()
