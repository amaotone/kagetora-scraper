from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


class Kagetora(object):
    def __init__(self, setting):
        self.setting = setting
        self.driver = webdriver.PhantomJS()
        self.login()

    def find(self, selector):
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector)))

    def finds(self, selector):
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))

    def login(self):
        self.driver.get('http://kagetora.bushidoo.com/')

        # shared
        self.find('#shared-pass input[type="password"]').send_keys(
            self.setting['shared_password'])
        self.find('#shared-pass').submit()

        # user
        Select(self.find('#initials')).select_by_visible_text(
            self.setting['user_initial'])
        Select(self.find('#user-names')).select_by_visible_text(
            self.setting['user_name'])
        self.find('#login input[type="password"]').send_keys(
            self.setting['user_password'])
        self.find('#login').submit()

        try:
            WebDriverWait(self.driver, 10).until(EC.title_contains('トップ'))
            print('login succeeded')
        except TimeoutException:
            print('login failed')
            raise TimeoutException
