import time
from lxml import etree
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as e_x
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


class ParsingOperations:
    """
    Нет ожиданий. Нет кликов
    """
    def __init__(self, browser):
        self.browser = browser

    def get_page_source(self):
        """Получаем актуальный html страницы в её текущем состоянии"""
        html = self.browser.page_source
        return html

    def make_actual_soup(self):
        """Получаем суп из текущего html"""
        html = self.get_page_source()
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    def get_actual_ng_binding_links(self):
        """
        Получем полный актуальный список всех ссылок ng_binging,
        по которым парсеру надлежит проходить на уровнях 1, 2 и 3
        """
        soup = self.make_actual_soup()
        ng_binding_links = soup.find_all('a', attrs={'class': 'ng-binding', 'target': '_self'})
        return ng_binding_links

    def get_links_for_level_4_and_5(self):
        """
        Получем полный актуальный список всех ссылок для нажатия. Для этого необходимо найти родительские
        элементы для элементов с классом 'icon-level-down'
        """
        soup = self.make_actual_soup()
        span_elements = soup.find_all('span', attrs={'class': 'icon-level-down'})
        links = []
        for span_element in span_elements:
            link = span_element.parent
            links.append(link)
        return links

    def get_xpath_with_lxml(self, link_text):
        """
        Если элемент не проскроллен и его невозможно отыскать по локатору LINK_NAME,
        то получаем его xpath с помощью lxml
        """
        html = self.get_page_source()
        root = etree.HTML(html)
        # element = root.xpath(f"//*[text()='{link_text}']")[0]
        try:
            element = root.xpath(f"//*[text()='{link_text}']")[-1]
        except:
            element = root.xpath(f"//*[text()='{link_text.strip()}']")[-1]
        xpath = etree.ElementTree(root).getpath(element)
        return xpath

    def find_element_by_link_name_or_xpath(self, link_text):
        """
        Ищем элемент по тексту ссылки, в случае ошибок - по xpath.
        Передаваемый link_text явл. полным и идёт с пробелом на конце
        """
        try:
            element = self.browser.find_elements(By.LINK_TEXT, link_text.strip())[-1]
        except:
            xpath = self.get_xpath_with_lxml(link_text)
            element = self.browser.find_element(By.XPATH, xpath)
        return element


