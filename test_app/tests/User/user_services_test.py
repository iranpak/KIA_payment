from selenium import webdriver
import unittest

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class UserTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    # def test_user_transactions(self):
    #     driver = self.driver
    #     driver.get("http://127.0.0.1:8085/user_transactions")
    #
    #     transactions_list = driver.find_element_by_id("transactions_list")
    #
    #     assert transactions_list.find_element_by_class_name("transaction_row") is not None

    def test_user_wallet_valid(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8085/user_wallet")

        credit_increase = driver.find_element_by_name("credit")
        credit_increase.send_keys("50000")

        submit_button = driver.find_element_by_name("registerButton")
        submit_button.click()

        try:
            WebDriverWait(driver, 2)
        except:
            print("An error occurred during waiting")

        assert driver.current_url == "http://127.0.0.1:8085/payment"

    def test_user_wallet_invalid(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8085/user_wallet")

        credit_increase = driver.find_element_by_name("credit")
        credit_increase.send_keys("99999999999999999999999")

        submit_button = driver.find_element_by_name("registerButton")
        submit_button.click()

        try:
            WebDriverWait(driver, 2) \
                 .until(expected_conditions.presence_of_element_located((By.NAME, "invalid_credit")))
            flag = True
        except TimeoutException:
            flag = False

        assert flag

    # def test_physical_mastercard_valid(self):
    #     driver = self.driver
    #     driver.get("http://127.0.0.1:8085/services/physical_mastercard")
    #
    #     credit = driver.find_element_by_name("credit")
    #     name = driver.find_element_by_name("name")
    #
    #     credit.send_keys("200")
    #     name.send_keys("Ali Alavi")
    #
    #     submit_button = driver.find_element_by_name("registerButton")
    #     submit_button.click()
    #
    #     try:
    #         WebDriverWait(driver, 2) \
    #              .until(expected_conditions.presence_of_element_located((By.NAME, "successful_request")))
    #         flag = True
    #     except TimeoutException:
    #         flag = False
    #
    #     assert flag
    #
    # def test_physical_mastercard_invalid(self):
    #     driver = self.driver
    #     driver.get("http://127.0.0.1:8085/services/physical_mastercard")
    #
    #     credit = driver.find_element_by_name("credit")
    #     name = driver.find_element_by_name("name")
    #
    #     credit.send_keys("1000000")
    #     name.send_keys("Ali Alavi")
    #
    #     submit_button = driver.find_element_by_name("registerButton")
    #     submit_button.click()
    #
    #     try:
    #         WebDriverWait(driver, 2) \
    #             .until(expected_conditions.presence_of_element_located((By.NAME, "not_enough_credit")))
    #         flag = True
    #     except TimeoutException:
    #         flag = False
    #
    #     assert flag
    #
    # def test_return_money_valid_and_invalid(self):
    #     driver = self.driver
    #     driver.get("http://127.0.0.1:8085/return_money")
    #
    #     credit = driver.find_element_by_name("return_credit")
    #     credit.send_keys("200000")
    #
    #     submit_button = driver.find_element_by_name("registerButton")
    #     submit_button.click()
    #
    #     try:
    #         WebDriverWait(driver, 2) \
    #             .until(expected_conditions.presence_of_element_located((By.NAME, "successful_return"))
    #                    or expected_conditions.presence_of_element_located((By.NAME, "not_enough_credit")))
    #         flag = True
    #     except TimeoutException:
    #         flag = False
    #
    #     assert flag
    #
    # def test_anonymous_money_invalid_account_number(self):
    #     driver = self.driver
    #     driver.get("http://127.0.0.1:8085/anonymous_money")
    #
    #     account_number = driver.find_element_by_name("account_number")
    #     money = driver.find_element_by_name("value")
    #     email = driver.find_element_by_name("email")
    #
    #     account_number.send_keys("12")
    #     money.send_keys("200000")
    #     email.send_keys("alialavi@gmail.com")
    #
    #     submit_button = driver.find_element_by_name("registerButton")
    #     submit_button.click()
    #
    #     try:
    #         WebDriverWait(driver, 2) \
    #             .until(expected_conditions.presence_of_element_located((By.NAME, "invalid_account")))
    #         flag = True
    #     except TimeoutException:
    #         flag = False
    #
    #     assert flag
    #
    # def test_anonymous_money(self):
    #     driver = self.driver
    #     driver.get("http://127.0.0.1:8085/anonymous_money")
    #
    #     account_number = driver.find_element_by_name("account_number")
    #     money = driver.find_element_by_name("value")
    #     email = driver.find_element_by_name("email")
    #
    #     account_number.send_keys("123456789101112131415161")
    #     money.send_keys("200000")
    #     email.send_keys("alialavi@gmail.com")
    #
    #     submit_button = driver.find_element_by_name("registerButton")
    #     submit_button.click()
    #
    #     try:
    #         WebDriverWait(driver, 2) \
    #             .until(expected_conditions.presence_of_element_located((By.NAME, "not_enough_credit"))
    #                    or expected_conditions.presence_of_element_located((By.NAME, "different_email"))
    #                    or expected_conditions.presence_of_element_located((By.NAME, "no_account"))
    #                    or expected_conditions.presence_of_element_located((By.NAME, "all_saved")))
    #         flag = True
    #     except TimeoutException:
    #         flag = False
    #
    #     assert flag

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()
