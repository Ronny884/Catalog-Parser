import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as e_x
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


class Waiter:
    def __init__(self, browser):
        self.browser = browser

    def wait(self, locator, value):
        """Ждать в соответствии с условием"""
        WebDriverWait(self.browser, 10).until(e_x.presence_of_element_located((locator, value)))

    def sleep(self, seconds):
        """Ждать определённое количество секунд"""
        time.sleep(seconds)