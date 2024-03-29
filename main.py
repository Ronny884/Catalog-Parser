from selenium import webdriver
from wait import *
from automatic_actions import *
from parsing_operations import *


if __name__ == "__main__":
    browser = webdriver.Chrome()
    waiter = Waiter(browser)
    parser = ParsingOperations(browser)

    work = AutomaticActions(browser, waiter, parser)
    work()
    browser.quit()
