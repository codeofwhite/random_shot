# 自动发送twitter推文
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from time import sleep
from selenium.webdriver import ActionChains

# 加入headers资讯
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15'
opt = webdriver.ChromeOptions()
s = Service("C:/Users/zhj20/PycharmProjects/alltest1/Selenium_/chromedriver.exe")
driver = webdriver.Chrome(service=s)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {  # 清空 window.navigator
    "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
})

driver.get('https://twitter.com/')
driver.execute_script(f'window.scrollTo(0,200)')
# 点击登录按钮
login = driver.find_element(By.CSS_SELECTOR, 'a[href="/login"]')  # tag是a，href是/login
login.click()
sleep(2)

# 输入账号
username = driver.find_element(By.CSS_SELECTOR, 'input[autocomplete="username"]')
username.send_keys('99gelanjingling@gmail.com')
print('enter email')
# 点击下一步
buttons = driver.find_elements(By.CSS_SELECTOR, 'div[role="button"]')  # 返回一个序列
for i in buttons:  # 判断那个是‘下一步’的按钮
    if i.text == 'Next' or i.text == '下一步':
        i.click()
        print('tap btn')
        break
sleep(2)

# 这边会弹个视窗叫输入用户名验证，也可能会没有
try:
    check = driver.find_element(By.CSS_SELECTOR, 'input[autocomplete="on"]')  # 这玩意on就是要验证
    check.send_keys('KokaLjl')
    buttons = driver.find_elements(By.CSS_SELECTOR, 'div[role="button"]')
    for i in buttons:  # 判断那个是‘下一步’的按钮
        if i.text == 'Next' or i.text == '下一步':
            i.click()
            print('tap check btn')
            break
    sleep(2)
except:
    print('no check')
    sleep(2)

# 输入密码
password = driver.find_element(By.CSS_SELECTOR, 'input[autocomplete="current-password"]')
password.send_keys('Jason20040903')
sleep(2)
# 点击按钮
buttons = driver.find_elements(By.CSS_SELECTOR, 'div[role="button"]')
for i in buttons:  # 判断那个是‘下一步’的按钮
    if i.text == '登录' or i.text == 'Log in':
        i.click()
        print('login')
        break
sleep(2)

# 发推文
textbox = driver.find_element(By.CSS_SELECTOR, 'div[role="textbox"]')
textbox.send_keys('Hello World!I am Robot~ ^_^')  # 在輸入框輸入文字
print('輸入文字')
sleep(1)
imgInput = driver.find_element(By.CSS_SELECTOR, 'input[data-testid="fileInput"]')
imgInput.send_keys('C:/Users/zhj20/PycharmProjects/alltest1/images/201936.jpg')  # 提供圖片絕對路徑，上傳圖片
print('上傳圖片')
sleep(1)
buttons = driver.find_elements(By.CSS_SELECTOR, 'div[role="button"]')
for i in buttons:
    if i.text == 'Everyone can reply' or i.text == '所有人可见':
        i.click()  # 點擊推文按鈕
        print('点击发送设置')
        break
sleep(1)
menuItems = driver.find_elements(By.CSS_SELECTOR, 'div[role="menuitem"]')
for i in menuItems:
    if i.text == 'Only people you mention':
        i.click()  # 點擊推文按鈕
        print('设定隐私')
        break
sleep(1)
buttons = driver.find_elements(By.CSS_SELECTOR, 'div[role="button"]')
for i in buttons:
    if i.text == '推文' or i.text == 'Tweet':
        i.click()  # 點擊推文按鈕
        print('推文完成')
        break
sleep(1)
