from selenium import webdriver
import unittest

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class CurrencyToRial(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_successful_login(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8085/admin_login/")

        username = driver.find_element_by_name("username")
        password = driver.find_element_by_name("password")
        login_button = driver.find_element_by_name("loginButton")
        username.send_keys("karegar@gmail.com")
        password.send_keys("123456")
        login_button.click()

        try:
            WebDriverWait(driver, 2) \
                .until(expected_conditions.presence_of_element_located((By.NAME, "login_successful")))
            flag = True
        except TimeoutException:
            flag = False

        assert flag

    # def test_empty_field_login(self):
    #     driver = self.driver
    #     driver.get("http://127.0.0.1:8085/admin_login/")
    #     username = driver.find_element_by_name("username")
    #     password = driver.find_element_by_name("password")
    #     login_button = driver.find_element_by_name("loginButton")
    #     username.send_keys("karegar@gmail.com")
    #     password.send_keys("")
    #     login_button.click()
    #     assert driver.find_element_by_name("emptyField") is not None
    
    # def test_wrong_pattern_login(self):
    #     driver = self.driver
    #     driver.get("http://127.0.0.1:8085/admin_login/")
    #     username = driver.find_element_by_name("username")
    #     password = driver.find_element_by_name("password")
    #     login_button = driver.find_element_by_name("loginButton")
    #     username.send_keys("wrong.email@pattern")
    #     password.send_keys("123456")
    #     login_button.click()
    #     assert driver.find_element_by_name("wrongEmailPattern") is not None

    def test_wrong_username_login(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8085/admin_login/")
        username = driver.find_element_by_name("username")
        password = driver.find_element_by_name("password")
        login_button = driver.find_element_by_name("loginButton")
        username.send_keys("unregistered@gmail.com")
        password.send_keys("123456")
        login_button.click()

        try:
            WebDriverWait(driver, 2) \
                .until(expected_conditions.presence_of_element_located((By.NAME, "wrong_username")))
            flag = True
        except TimeoutException:
            flag = False

        assert flag

    def test_wrong_password_login(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8085/admin_login/")
        username = driver.find_element_by_name("username")
        password = driver.find_element_by_name("password")
        login_button = driver.find_element_by_name("loginButton")
        username.send_keys("karegar@gmail.com")
        password.send_keys("wrongPassword")
        login_button.click()

        try:
            WebDriverWait(driver, 2) \
                .until(expected_conditions.presence_of_element_located((By.NAME, "wrong_pass")))
            flag = True
        except TimeoutException:
            flag = False

        assert flag

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()