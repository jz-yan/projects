import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from behave import given, when, then, step # pylint: disable=no-name-in-module

@step(u'I am subscribed to "{plan_type}" plan')
def step_impl(context, plan_type): # pylint: disable=function-redefined
    """
    Function to subscribe to desired plan

    Args:
        context
        plan_type (str): Plan to subscribe to
    """

    # Go to Pricing page
    context.execute_steps('given I am on the Pricing page')

    # Get buttons of plans
    activate_btns = context.browser.find_elements_by_xpath("//div[@class='billing-data-row-cell plan-control-cell']")
    # print('Length of activate_btns: ', len(activate_btns))
    plan_activated = []

    # Check to see if desired plan is subscribed already
    if plan_type == "Star":
        plan_activated = activate_btns[0].find_elements_by_xpath(".//div[@class='activated-plan-badge']")
    elif plan_type == "All Star":
        plan_activated = activate_btns[1].find_elements_by_xpath(".//div[@class='activated-plan-badge']")
    elif plan_type == "Superstar":
        plan_activated = activate_btns[2].find_elements_by_xpath(".//div[@class='activated-plan-badge']")

    # If not, subscribe to it
    if not plan_activated:
        context.execute_steps('''
            given I activate "''' + plan_type + '''" plan
            and I approve the subscription
            then I should see "''' + plan_type + '''" plan activated
        ''')   
    # else:
    #     print('Passed')

    time.sleep(1)

@step(u'I change to "{plan_type}" plan')
def step_impl(context, plan_type): # pylint: disable=function-redefined
    """
    Function to change plans

    Args:
        context
        plan_type (str): Plan to subscribe to
    """
    # Go to billing page
    context.execute_steps('given I am subscribed to "' + plan_type + '" plan')
