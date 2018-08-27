from selenium import webdriver
import unittest

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class UserRestriction(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_successfully_add_transaction(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8085/add_transaction")
        transaction_name = driver.find_element_by_name("transaction_name")
        amount = driver.find_element_by_name("pay_amount")
        submit_button = driver.find_element_by_name("submit_button")
        transaction_name.send_keys("IELTS")
        amount.send_keys(100000)
        submit_button.click()

        try:
            WebDriverWait(driver, 2) \
                .until(expected_conditions.presence_of_element_located((By.NAME, "successfully_done")))
            flag = True
        except TimeoutException:
            flag = False

        assert flag

    def test_valid_pay_amount(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8085/add_transaction")
        transaction_name = driver.find_element_by_name("transaction_name")
        amount = driver.find_element_by_name("pay_amount")
        submit_button = driver.find_element_by_name("submit_button")
        transaction_name.send_keys("IELTS")
        amount.send_keys("asd54df")
        submit_button.click()

        try:
            WebDriverWait(driver, 2) \
                .until(expected_conditions.presence_of_element_located((By.NAME, "invalid_input")))
            flag = True
        except TimeoutException:
            flag = False

        assert flag

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()
