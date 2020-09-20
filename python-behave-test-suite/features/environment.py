import xlrd

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

shop_name = "servvteststore.myshopify.com"
username = "hjhutty@coderise.io"

def before_all(context):
    context.browser = webdriver.Chrome()
    context.wait = WebDriverWait(context.browser, 10)

    context.browser.set_page_load_timeout(60)
    context.browser.implicitly_wait(5)
    context.browser.maximize_window()

    context.browser.get("https://webtest.servv.io")

    context.browser.find_element_by_id("account_email").send_keys("Email") # Please contact me privately for test email
    context.browser.find_element_by_name("commit").click()
    context.browser.find_element_by_id("account_password").send_keys("Password") # Please contact me privately for test password
    context.browser.implicitly_wait(2)
    context.browser.find_element_by_name("commit").click()

    try:
        element = WebDriverWait(context.browser, 15).until(
            EC.text_to_be_present_in_element((By.XPATH, "//div[@class='info-row']/div[@class='value']"), "servvteststore.myshopify.com")
        )
    finally:
        pass

    context.xlsx_data = xlrd.open_workbook('features/data/test_data.xlsx')

def after_all(context):
    context.browser.quit()  

def before_feature(context, feature):
    try:
        wait = WebDriverWait(context.browser, 15)
    except TimeoutError:
        raise
