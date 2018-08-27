from selenium import webdriver
import unittest
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


### DONE

class Login(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_successful_login(self):
        driver = self.driver

        driver.get("http://127.0.0.1:8085/login")
        username = driver.find_element_by_name('username')
        username.send_keys('admin')
        password = driver.find_element_by_name('password')
        password.send_keys('1q1q1q1q')
        button = driver.find_element_by_name('submit_button')
        button.click()
        time.sleep(1)

        try:
            WebDriverWait(driver, 1) \
                .until(expected_conditions.url_matches("http://127.0.0.1:8085"))
            flag = True
        except TimeoutException:
            flag = False

        assert flag

    def test_empty_field_login(self):
        driver = self.driver

        driver.get("http://127.0.0.1:8085/login")
        username = driver.find_element_by_name('username')
        username.send_keys('admin')
        password = driver.find_element_by_name('password')
        password.send_keys('')
        button = driver.find_element_by_name('submit_button')
        button.click()
        time.sleep(1)

        try:
            WebDriverWait(driver, 1) \
                .until(expected_conditions.url_matches("http://127.0.0.1:8085/login"))
            flag = True
        except TimeoutException:
            flag = False

        assert flag

    def test_wrong_username_login(self):
        driver = self.driver

        driver.get("http://127.0.0.1:8085/login")
        username = driver.find_element_by_name('username')
        username.send_keys('wrong_username')
        password = driver.find_element_by_name('password')
        password.send_keys('1q1q1q1q')
        button = driver.find_element_by_name('submit_button')
        button.click()
        time.sleep(1)

        try:
            WebDriverWait(driver, 1) \
                .until(expected_conditions.url_matches("http://127.0.0.1:8085/login"))
            flag = True
        except TimeoutException:
            flag = False

        assert flag

    def test_wrong_password_login(self):
        driver = self.driver

        driver.get("http://127.0.0.1:8085/login")
        username = driver.find_element_by_name('username')
        username.send_keys('admin')
        password = driver.find_element_by_name('password')
        password.send_keys('wrong_password')
        button = driver.find_element_by_name('submit_button')
        button.click()
        time.sleep(1)

        try:
            WebDriverWait(driver, 1) \
                .until(expected_conditions.url_matches("http://127.0.0.1:8085/login"))
            flag = True
        except TimeoutException:
            flag = False

        assert flag


if __name__ == '__main__':
    unittest.main()