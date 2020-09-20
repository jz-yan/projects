# Servv.ai Automated Test Suite Documentation

Jason Yan

This documentation details how to use, maintain and add onto the automated regression test suites for Servv.ai web application. A regression test suite is an organized collection of test cases that is regularly run to ensure software functionality after changes. These test cases are automated, meaning all test actions (e.g. clicking on buttons, filling in fields, looking for an element), are automatically performed in a standalone browser.

The main languages used are Python and Gherkin supported by the Behave framework and Selenium webdriver. This documentation is up to date as of August 21st, 2020.

# Servv.ai

[https://webtest.servv.io/](https://webtest.servv.io/)

Servv.ai is a web application built on the Shopify platform that allows clients to create virtual events (video conferences or meetings), organized using Google Calendar, to be purchased by customers. Attendance for these events are done via Zoom.

Clients have two choices of Zoom events to create: one-time events and recurring events. One-time events, as its name suggests, occur and are purchasable only once. Recurring events may be scheduled more than once, up to 20 times. Events may be edited and deleted after creation (after events are completed, they are automatically deleted).

Clients can choose three different plans: Star, All Star and Superstar. While all plans offer unlimited one-time events, Star plan has a recurring event limit of one, All Star ten and Superstar unlimited.

# Test Suites

Servv.ai has two separate test suites. One tests its Postman APIs while the other tests the web application itself. Almost all automation maintenance will be done of the web application test suite.

# Suite Logic

The automated regression test suite is coded in Python and Gherkin using Selenium webdriver and Behave framework. The IDE of choice is Visual Studio Code.

The main building blocks of the test suite are test cases, each designed to test something different. For example, if recurring event creation stops at 10 events for All Star plan or creating an event without a topic name produces an error. Behave framework organizes the test cases such that each one has one part in a Gherkin file (scenario) and another in a Python file (step definitions), just like Cucumber.

## Scenarios

The part coded in Gherkin, or scenario, is the first section processed. Basically, it tells the compiler which Python functions (step definitions) to execute to successfully run the test case. But first, what is Gherkin? Gherkin is a plain-text language that uses special keywords and plain English text to make understanding and contextualising test cases easier. An example scenario is as follows:

![0IcADa.png](https://i1.lensdump.com/i/0IcADa.png)

In VS Code, all words in blue are Gherkin keywords. Everything else are free text, or predicates. Scenario keyword outlines the name/description of the test case, while Given, When, And and Then lines are the actual steps that will be executed in the test browser. This example test case tests the validity of the given credentials by entering them on Servv.ai&#39;s login page and seeing if it successfully logs in.

A Gherkin file essentially is a collection of scenarios headed by a Feature keyword that usually describes the overall functionality or webpage being tested. As these files have the .feature extension, they are called feature files.

![0IciWe.png](https://i1.lensdump.com/i/0IciWe.png)

## Step Definitions

Step definitions are essentially Python functions defined by the scenarios, contained in Python files ending in \__steps.py_. For example, _homepage\_steps.py_ corresponds to _homepage.feature_. These step definitions extensively use Selenium webdriver&#39;s library to interact with the test browser.

The predicate identified in the feature file is used to search for a Python step definition with a matching decorator. For example:

Given I go to Servv.ai

@step(u&#39;I go to Servv.ai&#39;)

def step\_impl(context): # pylint: disable=function-redefined

    context.browser.get(&quot;https://webtest.servv.io&quot;)

Here, we can see &quot;I go to Servv.ai&quot; is present in both the feature predicate and Python decorator. Therefore, every occurrence of that predicate will execute the matching step definition.

## Selenium Webdriver

Selenium webdriver is a collection of APIs that allows test cases to be automatically executed in a browser setting. Its library is mainly used to interact with the browser elements and assert test conditions.

## Following URL

context.browser.get(&quot;https://webtest.servv.io&quot;)

## Find Element

context.browser.find\_element\_by\_id(&quot;account\_email&quot;)

context.browser.find\_element\_by\_xpath(&quot;//li/a[@href=&#39;/events&#39;]&quot;)

## Find All Elements

context.browser.find\_elements\_by\_xpath(&quot;//li/a[@href=&#39;/events&#39;]&quot;)

## Interact with Element

context.browser.find\_element\_by\_xpath(&quot;//li/a[@href=&#39;/events&#39;]&quot;).click()

context.browser.find\_element\_by\_id(&quot;account\_email&quot;).send\_keys(&quot;coderise.io&quot;)

## Assert Element is Present

assert context.browser.find\_elements\_by\_xpath(&quot;//li/a[@href=&#39;/events&#39;]&quot;)

Execute Step

context.execute\_steps(&#39;when I navigate to Events&#39;)

# File Structure

The file structure of the test suites are relatively straight forward. Everything is contained within the _features_ folder. Inside, there are _environment_._py_, all feature files and subfolders. Python step files and _hooks.py_ are contained in the _steps_ subfolder while test data files are in the _data_ subfolder.

## environment.py

_environment.py_ sets up the test suite and outlines any steps to take before and after the test suite, feature or scenario.

## hooks.py

_hooks.py_ contains common-used, shared Python functions to be used in the step definitions.

# Running Tests

Start execution of test suite by opening a command prompt window in the root folder.

![](RackMultipart20200919-4-8mc9fv_html_7b1ddcd764481ff6.png)

To run all feature files (and effectively all test cases), enter the command _behave_.

To run a single feature file, enter the command: _behave -i [feature file name].feature_

To run a single scenario, enter the command: _behave__-n &quot;[name of scenario]&quot;_

# Installation

## Installing VS Code

The preferred IDE is Visual Studio Code. Download from [https://code.visualstudio.com/](https://code.visualstudio.com/). When downloaded, install Python, Behave Test Explorer and Cucumber (Gherkin) Full Support extensions.

## Installing Python

Down the latest stable version of Python from [https://www.python.org/downloads/](https://www.python.org/downloads/). When running the downloaded executable, ensure the option &quot;Add Python to PATH&quot; on the first page of the installer is selected. This allows you to run the Python interpreter and package installer Pip.

## Installing Chrome Webdriver

The preferred test browser is Google Chrome. To allow Selenium webdriver to interact with it, Chrome webdriver must be downloaded from [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads). When downloaded, add it to the system path.

## Installing Python Libraries

Open a command prompt window in the repository&#39;s root folder. Enter the following commands to install necessary libraries:

- _pip install behave_ to install Behave
- _pip install selenium_ to install Selenium
- _pip install xlrd_

## Cloning Repository

Clone the Servv.ai test suite repository from [https://github.com/dev-coderise/servv-automation](https://github.com/dev-coderise/servv-automation). As mentioned earlier, there are two test suites included. API-test-suite is the test suite for APIs while servv-test-suite is the test suite for the web application.

![](RackMultipart20200919-4-8mc9fv_html_6c06b56453012a01.png)
