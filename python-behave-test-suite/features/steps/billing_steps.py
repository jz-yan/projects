import time

from behave import given, when, then, step # pylint: disable=no-name-in-module
# from testfixtures import Replace, test_date
# from testfixtures.tests.sample1 import str_today_1

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import steps.hooks as hk # pylint: disable=import-error

@step(u'I am on the Pricing page')
def step_impl(context): # pylint: disable=function-redefined
    """
    Function to navigate to Pricing

    Args:
        context
    """
    if context.browser.current_url != "https://webtest.servv.io/pricing":
        hk.click_xpath(context, "//li/a[@href='/pricing']")

@step(u'I activate "{plan_type}" plan')
def step_impl(context, plan_type): # pylint: disable=function-redefined
    """
    Function to activate a certain plan

    Args:
        context
        plan_type (str): Type of plan to activate
    """

    # Grab list of buttons corresponding to each plan
    activate_btns = context.browser.find_elements_by_xpath("//div[@class='billing-data-row-cell plan-control-cell']")

    # Clicking on appropriate button
    if plan_type == "Star":
        activate_btns[0].find_element_by_xpath(".//button").click()
    elif plan_type == "All Star":
        activate_btns[1].find_element_by_xpath(".//button").click()
    elif plan_type == "Superstar":
        activate_btns[2].find_element_by_xpath(".//button").click()

    time.sleep(1)

@step(u'I approve the {purchase_type}')
def step_impl(context, purchase_type): # pylint: disable=function-redefined
    """
    Function to approve subscription on Shopify page

    Args:
        context
        purchase_type (str): Purchase type
    """

    time.sleep(2)

    # If subscription, approve subscription
    if purchase_type == "subscription":
        hk.click_xpath(context, "//button[contains(text(), 'Approve subscription')]")
        # try:
        #     element = WebDriverWait(context.browser, 15).until(
        #         EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Approve subscription')]"))
        #     # EC.text_to_be_present_in_element((By.XPATH, "//div[@class='info-row']/div[@class='value']"), "servvteststore.myshopify.com")
        #     )
        # finally:
        #     pass
        # context.browser.find_element_by_xpath("//button[contains(text(), 'Approve subscription')]").click()
    # If free trial, approve free trial
    elif purchase_type == "free trial":
        hk.click_xpath(context, "//button[contains(text(), 'Start free trial')]")
        # context.browser.find_element_by_xpath("//button[contains(text(), 'Start free trial')]").click()

    time.sleep(2)

@then(u'I should see "{plan_type}" plan activated')
def step_impl(context, plan_type): # pylint: disable=function-redefined
    """
    Function to assert certain plan type is activated

    Args:
        context
        plan_type (str): Plan to assert
    """
    # if plan_type == "AllStar":
    #     plan_type = "All Star"

    # time.sleep(1)
    # context.browser.get("https://webtest.servv.io/pricing")
    # Go to the Pricing page
    context.execute_steps('given I am on the Pricing page')
    time.sleep(1)

    activate_btns = context.browser.find_elements_by_xpath("//div[@class='billing-data-row-cell plan-control-cell']")
    # print('Length of activate_btns: ', len(activate_btns))

    if plan_type == "Star":
        assert activate_btns[0].find_elements_by_xpath(".//div[@class='activated-plan-badge']")
    elif plan_type == "All Star":
        assert activate_btns[1].find_elements_by_xpath(".//div[@class='activated-plan-badge']")
    elif plan_type == "Superstar":
        assert activate_btns[2].find_elements_by_xpath(".//div[@class='activated-plan-badge']")

    time.sleep(1)
