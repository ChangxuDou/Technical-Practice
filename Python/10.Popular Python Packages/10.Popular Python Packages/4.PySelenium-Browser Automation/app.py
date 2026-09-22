# google python Selenium

from selenium import webdriver
from selenium.webdriver.common.by import By
import config
browser = webdriver.Chrome()
browser.get("http://github.com")


# we can find elements by their id, class, name, tag
signin_link = browser.find_element(By.LINK_TEXT, "Sign in")
signin_link.click()

username_box = browser.find_element(By.ID, "login_field")
username_box .send_keys(config.user_name)
password_box = browser.find_element(By.ID, "password")
password_box .send_keys(config.password)
password_box.submit()

input("等登录完成、打开头像菜单后，回到终端按回车检查……")

print("当前网址：", browser.current_url)
found = "Ryandou322" in browser.page_source
print("页面中是否包含用户名：", found)

assert found, "当前页面源码中没有找到 Ryandou322"

input("按回车关闭浏览器……")
browser.quit()
