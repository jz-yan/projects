import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException

from behave import given, when, then, step # pylint: disable=no-name-in-module

import steps.hooks as hk # pylint: disable=import-error

test_event_counter = 0

@given(u'I am on the Dashboard')
def step_impl(context): # pylint: disable=function-redefined
    """
    Function to navigate to Dashboard

    Args:
        context
    """
    if context.browser.current_url != "https://webtest.servv.io/":
        hk.click_xpath(context, "//li/a[@href='/']")

@given(u'I am on the Events page')
def step_impl(context): # pylint: disable=function-redefined
    """
    Function to navigate to Events

    Args:
        context
    """
    if context.browser.current_url != "https://webtest.servv.io/events":
        hk.click_xpath(context, "//li/a[@href='/events']")

@step(u'I navigate to Events')
def step_impl(context): # pylint: disable=function-redefined
    """
    Function to navigate to Events

    Args:
        context
    """
    context.execute_steps('given I am on the Events page')

@when(u'I click on Create Event')
def step_impl(context): # pylint: disable=function-redefined
    """
    Function to click "Create Event" button

    Args:
        context
    """
    hk.click_xpath(context, "//button[@class='svv-circle-btn']")

@step(u'I click on Create Meeting')
def step_impl(context): # pylint: disable=function-redefined
    """
    Function to click "Create Meeting" button

    Args:
        context
    """
    hk.click_xpath(context, "//button[@class='svv-circle-btn']")

@step(u'I delete {delete_num} recurring meetings, {predicate}')
def step_impl(context, delete_num, predicate): # pylint: disable=function-redefined
    """
    Function to create then delete a number of recurring meetings

    Args:
        context
        delete_num (int): Number of times to create, then delete, recurring meeting
        predicate  (str): Type of recurring meeting to create
    """

    # Looping through number of recurring events
    for i in range(int(delete_num)):
        context.execute_steps('''
            given I click on Create Meeting
            when given I fill in recurring meeting data, ''' + predicate + '''
            then I should see success dialogue alert
        ''')

    # Delete all meetings
    context.execute_steps(u'given I delete all meetings')  
    global test_event_counter
    test_event_counter = 0

@when(u'I create {meeting_num} one-time meetings')
def step_impl(context, meeting_num): # pylint: disable=function-redefined
    """
    Function to create a number of one-time meetings

    Args:
        context
        meeting_num (int): Number of times to create one-time meeting
    """

    # Loop through number of one-time meetings
    for i in range(int(meeting_num)):
        context.execute_steps('when I click on Create Meeting')

        create_step = u'given I fill in meeting data, test number ' + str(i + 1)
        context.execute_steps(create_step)

        context.execute_steps(u'then I should see success dialogue alert')

    global test_event_counter
    test_event_counter = 0

@when(u'I create {meeting_num} recurring meetings, {predicate}')
def step_impl(context, meeting_num, predicate): # pylint: disable=function-redefined
    """
    Function to create a number of recurring meetings

    Args:
        context
        meeting_num (int): Number of times to create recurring meeting
        predicate   (str): Type of recurring meeting to create
    """

    # Loop through number of recurring meetings
    for i in range(int(meeting_num)):
        context.execute_steps('when I click on Create Meeting')

        context.execute_steps(u'given I fill in recurring meeting data, ' + predicate)
    global test_event_counter
    test_event_counter = 0

@step(u'I delete all meetings')
def step_impl(context): # pylint: disable=function-redefined
    """
    Function to delete all meetings in Events

    Args:
        context
    """

    # Go to Events
    context.execute_steps('given I navigate to Events')

    # Get number of meetings in total
    meeting_div = context.browser.find_element_by_xpath("//div[@class='upcoming-meetings-grid-container']")
    meeting_num = int(meeting_div.get_attribute("data-records-number").strip())

    # Loop through all meetings
    while meeting_num > 0:
        # Click on Remove button
        hk.click_xpath(context, "//button[contains(text(), 'Remove')]")
        # time.sleep(1)

        # If meeting is Recurring, subtract number of reccurences from total meetings amount
        if context.browser.find_elements_by_xpath("//div[@class='removed-items-number']"):
            recur_num = int(context.browser.find_element_by_xpath("//div[@class='removed-items-number']").text.split()[0])
            meeting_num -= recur_num
        else:
            meeting_num -= 1

        hk.click_xpath(context, "//button[contains(text(), 'Yes')]")
        
        time.sleep(1)
    time.sleep(1)

@step(u'I fill in meeting data, {predicate}')
def step_impl(context, predicate): # pylint: disable=function-redefined
    """
    Function to fill in meeting data for a particular meeting type, defined in the Excel spreadsheet

    Args:
        context
        predicate (str): Type of meeting to fill out, from Excel spreadsheet
    """

    # Get data from Excel spreadsheet
    params = hk.load_xls_data(predicate)
    time.sleep(2)

    # Topic field
    if params["Topic"]:
        hk.send_keys_id(context, "topic", params["Topic"])
    
    # Time Zone
    # if params["Time Zone"]:
    #     hk.send_keys_xpath(context, "//label[contains(text(), 'Time Zone')]/../div", params["Time Zone"])

    # Schedule
    if params["Schedule"]:
        if params["Schedule"] == "First Day Next Month":
            # Click field first
            hk.click_xpath(context, "//label[contains(text(), 'Schedule')]/../div/input")
            # Click button for next month
            hk.click_xpath(context, "/html/body/div[3]/div[3]/div/div[1]/div/div[3]/div[1]/div[1]/button[2]")
            # Click first day
            hk.click_xpath(context, "//button[@class='MuiButtonBase-root MuiIconButton-root MuiPickersDay-day']")

            # Click OK to exit menu
            hk.click_xpath(context, "//span[contains(text(), 'OK')]")

    # Price
    if params["Price"]:
        hk.send_keys_xpath(context, "//label[contains(text(), 'Price')]/../input", params["Price"])

    # Duration
    if params["Duration"]:
        hk.send_keys_xpath(context, "//label[contains(text(), 'Duration (minutes)')]/../input", params["Duration"])

    # Password
    if params["Password"]:
        hk.send_keys_xpath(context, "//label[contains(text(), 'Password')]/../input", params["Password"])

    # Description
    if params["Description"]:
        hk.send_keys_xpath(context, "//label[contains(text(), 'Description')]/../textarea", params["Description"])

    time.sleep(2)

@step(u'I fill in one-time meeting data, {predicate}')
def step_impl(context, predicate): # pylint: disable=function-redefined
    """
    Function to fill in data for one-time meeting of a particular type defined in Excel spreadsheet

    Args:
        context
        prediate (str): Type of meeting to create
    """
    context.execute_steps('given I fill in meeting data, ' + predicate)

    # Create Meeting
    hk.click_xpath(context, "//button[contains(text(), 'Create event')]")

# @step(u'k')

# @step(u'I fill in meeting data, test number {test_num}')
# def step_impl(context, test_num): # pylint: disable=function-redefined
#     time.sleep(1)
#     meeting_name = "Test Meeting #" + test_num
#     context.browser.find_element_by_id("topic").send_keys(meeting_name)
#     time.sleep(1)
#     context.browser.find_element_by_xpath("//button[contains(text(), 'Create meeting')]").click()
#     time.sleep(1)

@step(u'I fill in recurring meeting data, {predicate}')
def step_impl(context, predicate): # pylint: disable=function-redefined
    """
    Function to fill in data for recurring meeting of a particular type defined in Excel spreadsheet

    Args:
        context
        predicate (str): Type of meeting to create
    """

    global test_event_counter

    context.execute_steps('given I fill in meeting data, ' + predicate)
    
    # Click to open recurring meeting options
    hk.click_xpath(context, "//div[@class='toggle-section-title']", 1)
    # Scroll to bottom of popup menu
    context.browser.find_element_by_xpath('//body').send_keys(Keys.CONTROL + Keys.END)

    # Select recurring meeting
    hk.click_xpath(context, '//span[@class="checkmark"]', 1)

    # Select and confirm number of recurring meetings
    input_element = context.browser.find_element_by_xpath('/html/body/div/div/div/div[6]/div/div[2]/div/form/div[7]/div[3]/div[3]/div/div/div/div[1]')
    input_element.click()
    
    # Create the event
    hk.click_xpath(context, "//button[contains(text(), 'Create event')]")
    # context.browser.find_element_by_xpath("//button[contains(text(), 'Create event')]").click()
    time.sleep(1)

@then(u'I should see successful dialogue alert')
def step_impl(context): # pylint: disable=function-redefined    
    """
    Function to assert successful meeting creation message is present and visible

    Args:
        context
    """
    # hk.wait_msg(context, "//div[contains(text(), 'Meeting has been created successfully.')][@role='alert']")
    context.execute_steps('given I should see dialogue alert "Meeting has been created successfully."')

@step(u'I should see dialogue alert "{alert_msg}"')
def step_impl(context, alert_msg): # pylint: disable=function-redefined
    """
    Function to assert successful inputted message is present and visible

    Args:
        context
        alert_msg (str): Inputted message to check
    """

    time.sleep(1)
    # Wait for message to appear, then confirm its visibility
    hk.wait_msg(context, "//div[contains(text(), '" + alert_msg + "')][@role='alert']")

@then(u'I should see "{error_msg}" on screen')
def step_impl(context, error_msg): # pylint: disable=function-redefined
    """
    Function to assert error meeting is present and visible, usually during creating a meeting

    Args:
        context
        error_msg (str): Inputted error message to check
    """

    # Wait for error message to appear
    hk.wait_msg(context, "//span[@class='input-error-msg'][contains(text(), '" + error_msg + "')]")
    time.sleep(3)
    # Press Cancel button to exit meeting creation window
    hk.click_xpath(context, "//button[contains(text(), 'Cancel')]")

@then(u'I should see error on the last meeting')
def step_impl(context): # pylint: disable=function-redefined
    time.sleep(1)
    """
    Function to assert error message present, usually after last recurring meeting creation

    Args:
        context
    """
    # if context.browser.find_element_by_xpath("//div[contains(text(), 'You need update your billing plan for this action. (Error 402)')][@role='alert']").is_displayed():
    #     print('Dialogue is displayed')
    # else:
    #     print('Dialogue is not displayed')
    
    # Assert error message is present and visible
    context.execute_steps('given I should see dialogue alert "You need update your billing plan for this action. (Error 402)"')
    # Click on cancel
    hk.click_xpath(context, "//button[contains(text(), 'Cancel')]")
    time.sleep(1)

@then(u'I should see no error on the last meeting')
def step_impl(context): # pylint: disable=function-redefined
    """
    Function to assert no error message present after last recurring meeting creation

    Args:
        context
    """
    time.sleep(1)
    # if context.browser.find_element_by_xpath("//div[contains(text(), 'Meeting has been created successfully.')][@role='alert']").is_displayed():
    #     print('Dialogue is displayed')
    # else:
    #     print('Dialogue is not displayed')
    # time.sleep(1)

    context.execute_steps('given I should see successful dialogue alert')

# @then(u'I should see meeting, all valid')
# def step_impl(context): # pylint: disable=function-redefined
#     """
#     Function to assert successful meeting creation message is present and visible

#     Args:
#         context
#     """

#     if context.browser.find_element_by_xpath("//div[contains(text(), 'Test Topic 15')]").is_displayed():
#         print('Element is displayed')
#     else:
#         print('Element is not displayed')
#     time.sleep(2)

# @then(u'I should see limit of {event_lim} events')
# def step_impl(context, event_lim): # pylint: disable=function-redefined
#     time.sleep(3)
#     context.browser.find_element_by_xpath("//li/a[@href='/events']").click()
#     time.sleep(1)

#     event_num = len(context.browser.find_elements_by_xpath("//div[@class='single-meeting-card-container grid-item']"))
#     page_btns = len(context.browser.find_elements_by_xpath("//button[@class='pagination-btn']"))

#     print('event_num: ', event_num)
#     print('page_btns: ', page_btns)

#     assert event_num <= int(event_lim) and page_btns == 1

# @then(u'I should see limit of 50 meetings')
# def step_impl(context, event_lim): # pylint: disable=function-redefined
#     time.sleep(3)
#     context.browser.find_element_by_xpath("//li/a[@href='/events']").click()
#     time.sleep(1)

#     event_num = len(context.browser.find_elements_by_xpath("//div[@class='single-meeting-card-container grid-item']"))
#     page_btns = len(context.browser.find_elements_by_xpath("//button[@class='pagination-btn']"))

#     print('event_num: ', event_num)
#     print('page_btns: ', page_btns)

#     assert event_num <= int(event_lim) and page_btns == 1

# @then(u'I should see {meeting_limit} meetings')
# def step_impl(context, meeting_limit): # pylint: disable=function-redefined
#     time.sleep(1)
#     context.execute_steps('when I navigate to Events')
#     time.sleep(1)

#     meeting_div = context.browser.find_element_by_xpath("//div[@class='upcoming-meetings-grid-container']")
#     meeting_num = int(meeting_div.get_attribute("data-records-number").strip())

#     print('Meeting num: ', meeting_num)



