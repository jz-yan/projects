import xlrd
import pandas as pd
import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

wait_time = 0

def load_xls_data(predicate):
    """
    Function to load data from Excel spreadsheet

    Args:
        predicate (str): Row to retrieve from
    """
    
    # Read dataframe from Excel spreadsheet
    temp = pd.read_excel('features/data/test_data.xlsx', sheet_name='Meetings', header=None)

    # Set dictionary keys as column #1, or predicates
    temp_keys = temp.values.tolist()[0]
    # Set dictionary values as corresponding data
    new_list = temp.values.tolist()[1:]

    # Return the zipped dictionary containing appropriate predicate
    return dict(zip(temp_keys, [i for i in new_list if i[0] == predicate][0]))

def click_xpath(context, xpath, index=None):
    """
    Function to click on element located using xpath

    Args:
        context
        xpath (str): Xpath parameter
        index (int): Element number if multiple elements present
    """
    try:
        # Waiting for element to appear
        element = WebDriverWait(context.browser, 15).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )

        # Click on element
        if index:
            context.browser.find_elements_by_xpath(xpath)[index].click()
        else:
            context.browser.find_element_by_xpath(xpath).click()

        time.sleep(wait_time)
    except Exception as e:
        print('EXCEPTION: ', e)

def send_keys_id(context, id, message):
    """
    Function to send keys to element located using ID

    Args:
        context
        id      (str): ID parameter
        message (str): String message to input
    """
    try:
        # Wait for element to appear
        element = WebDriverWait(context.browser, 15).until(
            EC.element_to_be_clickable((By.ID, id))
        )

        # Clear field
        context.browser.find_element_by_id(id).clear()
        # Send message
        context.browser.find_element_by_id(id).send_keys(message)
        time.sleep(wait_time)
    except Exception as e:
        print('EXCEPTION: ', e)

def send_keys_xpath(context, xpath, message):
    """
    Function to send keys to element located using xpath

    Args:
        context
        xpath   (str): Xpath parameter
        message (str): String message to input
    """
    try:
        # Wait for element to appear
        element = WebDriverWait(context.browser, 15).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )

        # Send message
        context.browser.find_element_by_xpath(xpath).send_keys(message)
        time.sleep(wait_time)
    except Exception as e:
        print('EXCEPTION: ', e)

def click_id(context, id, index=None):
    """
    Function to click on element located using ID

    Args:
        context
        id    (str): ID parameter
        index (int): Element number if multiple elements present
    """
    try:
        # Wait for element to appear
        element = WebDriverWait(context.browser, 15).until(
            EC.element_to_be_clickable((By.ID, id))
        )

        # Click on element
        if index:
            context.browser.find_elements_by_id(id)[index].click()
        else:
            context.browser.find_element_by_id(id).click()

        time.sleep(wait_time)
    except Exception as e:
        print('EXCEPTION: ', e)

def wait_msg(context, xpath):
    """
    Function to wait for element to appear, located using xpath

    Args:
        context
        xpath (str): Xpath parameter
    """
    try:
        # Wait for element to appear
        element = WebDriverWait(context.browser, 15).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )

        time.sleep(wait_time)
    except Exception as e:
        print('EXCEPTION: ', e)

