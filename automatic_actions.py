import os
import time
import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as e_x
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from dotenv import load_dotenv


class AutomaticActions:
    def __init__(self, browser, waiter, parser):
        self.browser = browser
        self.waiter = waiter
        self.parser = parser

    def __call__(self, *args, **kwargs):
        load_dotenv()
        self.authorize()
        self.open_catalog()
        self.start_a_reference_traversal_cycle()

    def authorize(self):
        """
        Авторизвция для открытия каталога
        """
        home_url = 'https://www.agroparts.com/agroparts/homepage'
        self.browser.get(home_url)
        self.waiter.wait(By.NAME, 'username')
        self.browser.find_element(By.NAME, 'username').send_keys(os.getenv('EMAIL'))
        self.browser.find_element(By.NAME, 'password').send_keys(os.getenv('PASSWORD'))
        self.waiter.wait(By.XPATH, "//input[@value='Вход']")
        self.browser.find_element(By.XPATH, "//input[@value='Вход']").click()
        self.waiter.sleep(2)
        self.browser.find_element(By.ID, 'login-override-session-button').click()
        self.waiter.sleep(2)

    def open_catalog(self):
        """
        Непосредственно открытие каталога
        """
        catalog_url = 'https://www.agroparts.com/ip40_lemken/#/filtergroup'
        self.browser.get(catalog_url)
        self.waiter.sleep(2)

    def start_a_reference_traversal_cycle(self):
        """
        Для удобства ссылки разделены на 5 условных уровней, где все уровни, кроме первого (категории),
        открываются динамически. Проход по ссылкам осуществляется поочерёдно через цикл
        """
        self.follow_the_links_level_1()

    def follow_the_links_level_1(self):
        """
        Проход по ссылкам 1 уровня
        """
        links_level_1 = self.parser.get_actual_ng_binding_links()
        for link in links_level_1:
            element = self.parser.find_element_by_link_name_or_xpath(link_text=link.text)
            element.click()
            self.waiter.sleep(1)
            self.follow_the_links_level_2(links_level_1)

    def follow_the_links_level_2(self, links_level_1):
        """
        Проход по ссыдкам 2 уровня. Для того, чтобы получить их список,
        необходимо из списка всех ссылок исключить ссылки, что соответствуют уровню 1
        """
        links_level_2 = [x for x in self.parser.get_actual_ng_binding_links() if x not in links_level_1]
        for link in links_level_2:
            element = self.parser.find_element_by_link_name_or_xpath(link_text=link.text)
            try:
                element.click()
            except:
                script = "arguments[0].scrollIntoView();"
                self.browser.execute_script(script, element)
                element.click()

            self.waiter.sleep(1)
            self.follow_the_links_level_3(links_level_1, links_level_2)

        self.browser.find_element(By.XPATH, '//*[@id="breadcrumb"]/ul[2]/li/a[1]').click()
        self.waiter.sleep(1)

    def follow_the_links_level_3(self, links_level_1, links_level_2):
        """
        Проход по ссылкам 3 уровня
        """
        links_level_1_2 = links_level_1 + links_level_2
        links_level_3 = [x for x in self.parser.get_actual_ng_binding_links() if x not in links_level_1_2]
        for link in links_level_3:
            element = self.parser.find_element_by_link_name_or_xpath(link_text=link.text)
            try:
                element.click()
            except:
                script = "arguments[0].scrollIntoView();"
                self.browser.execute_script(script, element)
                element.click()

            self.waiter.sleep(1)
            self.follow_the_links_level_4()
            self.browser.find_element(By.XPATH, '//*[@id="breadcrumb"]/ul[2]/li[2]/a[1]').click()
            self.waiter.sleep(1)

        self.browser.find_element(By.XPATH, '//*[@id="breadcrumb"]/ul[2]/li[2]/a[1]').click()
        self.waiter.sleep(1)

    def follow_the_links_level_4(self):
        """
        Проход по ссылкам 4 уровня
        """
        dirs = self.parser.get_links_for_level_4_and_5()
        for directory in dirs:
            element = self.browser.find_element(By.XPATH, f"//*[@title='{directory.attrs['title']}']")
            try:
                element.click()
            except:
                script = "arguments[0].scrollIntoView();"
                self.browser.execute_script(script, element)
                element.click()

            self.waiter.sleep(1)
            self.follow_the_links_level_5()

        self.browser.find_element(By.XPATH, '//*[@id="breadcrumb"]/ul[2]/li[3]/a[1]').click()
        self.waiter.sleep(1)

    def follow_the_links_level_5(self):
        """
        Проход по ссылкам 5 уровня
        """
        links = self.parser.get_links_for_level_4_and_5()
        for link in links:
            element = self.browser.find_element(By.XPATH, f"//*[@title='{link.attrs['title']}']")
            element.click()
            self.waiter.sleep(1)
            #
            self.browser.find_element(By.XPATH, '//*[@id="breadcrumb"]/ul[2]/li[4]/a[1]').click()
            self.waiter.sleep(1)
        self.waiter.sleep(1)