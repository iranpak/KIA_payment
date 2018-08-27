import time
from selenium import webdriver
import unittest

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

USER_USER = "user"
USER_PASS = "3=3=3=3="
SLEEP_TIME = 1


class UserTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def login_as_user(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8085/login/")
        time.sleep(SLEEP_TIME)

        username = driver.find_element_by_name('username')
        username.send_keys(USER_USER)
        password = driver.find_element_by_name('password')
        password.send_keys(USER_PASS)
        button = driver.find_element_by_name('submit_button')
        button.click()

    # def test_user_wallet_valid(self):
    #     driver = self.driver
    #     driver.get("http://127.0.0.1:8085/user_wallet")
    #
    #     credit_increase = driver.find_element_by_name("credit")
    #     credit_increase.send_keys("50000")
    #
    #     submit_button = driver.find_element_by_name("registerButton")
    #     submit_button.click()
    #
    #     try:
    #         WebDriverWait(driver, 2)
    #     except:
    #         print("An error occurred during waiting")
    #
    #     assert driver.current_url == "http://127.0.0.1:8085/payment"
    #
    # def test_user_wallet_invalid(self):
    #     driver = self.driver
    #     driver.get("http://127.0.0.1:8085/user_wallet")
    #
    #     credit_increase = driver.find_element_by_name("credit")
    #     credit_increase.send_keys("99999999999999999999999")
    #
    #     submit_button = driver.find_element_by_name("registerButton")
    #     submit_button.click()
    #
    #     try:
    #         WebDriverWait(driver, 2) \
    #              .until(expected_conditions.presence_of_element_located((By.NAME, "invalid_credit")))
    #         flag = True
    #     except TimeoutException:
    #         flag = False
    #
    #     assert flag

    def test_user_service_successful(self):
        self.login_as_user()

        driver = self.driver
        driver.get("http://127.0.0.1:8085/services/test_service")
        time.sleep(SLEEP_TIME)

        price = driver.find_element_by_name("price")
        name = driver.find_element_by_name("name")
        submit = driver.find_element_by_name("submit")

        name.send_keys("test")
        price.send_keys("20")

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        submit.click()

        try:
            WebDriverWait(driver, 5) \
                .until(expected_conditions.url_contains("success"))
            flag = True
        except TimeoutException:
            flag = False

        assert flag

    # def test_user_service_fail_1(self):
    #     self.login_as_user()
    #
    #     driver = self.driver
    #     driver.get("http://127.0.0.1:8085/services/test_service")
    #     time.sleep(SLEEP_TIME)
    #
    #     price = driver.find_element_by_name("price")
    #     name = driver.find_element_by_name("name")
    #     submit = driver.find_element_by_name("submit")
    #
    #     name.send_keys("test")
    #     price.send_keys("1")
    #
    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #
    #     submit.click()
    #
    #     try:
    #         WebDriverWait(driver, SLEEP_TIME) \
    #             .until(expected_conditions.presence_of_element_located((By.NAME, "error")))
    #         flag = True
    #     except TimeoutException:
    #         flag = False
    #
    #     assert flag
    #
    # def test_user_service_fail_2(self):
    #     self.login_as_user()
    #
    #     driver = self.driver
    #     driver.get("http://127.0.0.1:8085/services/test_service")
    #     time.sleep(SLEEP_TIME)
    #
    #     price = driver.find_element_by_name("price")
    #     name = driver.find_element_by_name("name")
    #     submit = driver.find_element_by_name("submit")
    #
    #     name.send_keys("test")
    #     price.send_keys("1000")
    #
    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #
    #     submit.click()
    #
    #     try:
    #         WebDriverWait(driver, SLEEP_TIME) \
    #             .until(expected_conditions.presence_of_element_located((By.NAME, "error")))
    #         flag = True
    #     except TimeoutException:
    #         flag = False
    #
    #     assert flag

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()
