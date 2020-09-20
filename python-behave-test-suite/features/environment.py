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
    # context.browser = webdriver.Chrome() if you have set chromedriver in your PATH
    context.browser.set_page_load_timeout(60)
    context.browser.implicitly_wait(5)
    context.browser.maximize_window()

    # context.browser.get("https://servvteststore.myshopify.com/admin/apps/servv_test")
    context.browser.get("https://webtest.servv.io")

    context.browser.find_element_by_id("account_email").send_keys("hjhutty@coderise.io")
    context.browser.find_element_by_name("commit").click()
    context.browser.find_element_by_id("account_password").send_keys("Servv@2020??")
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
        # expected_element = EC.presence_of_element_located()
        # wait.until(expected_element)
    except TimeoutError:
        raise

# def click_by_xpath(context, element_xpath):
#     try:
#         element = WebDriverWait(context.browser, 15).until(
#             EC.presence_of_element_located((By.XPATH, element_xpath))
#             # EC.text_to_be_present_in_element((By.XPATH, "//div[@class='info-row']/div[@class='value']"), "servvteststore.myshopify.com")
#         )
#     finally:
#         pass
    
#     context.browser.find_element_by_xpath(element_xpath).click()

# def wait_visible(context, element):
#     try:
#         wait = WebDriverWait(context.browser, 15)
#         expected_element = EC.presence_of_element_located(element)
#         wait.until(expected_element)
#     except TimeoutError:
#         raise

# def wait_clickable(context, element):
#     try:
#         wait = WebDriverWait(context.browser, 15)
#         expected_element = EC.element_to_be_clickable(element)
#         wait.until(expected_element)
#     except TimeoutError:
#         raise