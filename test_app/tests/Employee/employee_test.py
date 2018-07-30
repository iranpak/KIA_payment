from selenium import webdriver
import unittest

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class UserTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    # def test_observe_all_transactions(self):
    #     driver = self.driver
    #     driver.get("http://127.0.0.1:8085/all_transactions")
    #
    #     transactions_list = driver.find_element_by_id("all_transactions_list")
    #
    #     try:
    #         WebDriverWait(driver, 2) \
    #             .until(expected_conditions.presence_of_element_located((By.NAME, "transaction_row")))
    #         flag = True
    #     except TimeoutException:
    #         flag = False
    #
    #     assert flag

    def test_select_transaction(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8085/all_transactions/1234")

        pick_button = driver.find_element_by_name("pick_button")
        pick_button.click()

        try:
            WebDriverWait(driver, 2) \
                .until(expected_conditions.presence_of_element_located((By.NAME, "transaction_picked")))
            flag = True
        except TimeoutException:
            flag = False

        assert flag

    # def test_report_transaction(self):
    #     driver = self.driver
    #     driver.get("http://127.0.0.1:8085/all_transactions/1234")
    #
    #     report_button = driver.find_element_by_name("report_button")
    #     report_button.click()
    #
    #     try:
    #         WebDriverWait(driver, 2) \
    #             .until(expected_conditions.presence_of_element_located((By.NAME, "transaction_reported")))
    #         flag = True
    #     except TimeoutException:
    #         flag = False
    #
    #     assert flag
    #
    # def test_finish_transaction(self):
    #     driver = self.driver
    #     driver.get("http://127.0.0.1:8085/all_transactions/1234")
    #
    #     finish_button = driver.find_element_by_name("finish_button")
    #     finish_button.click()
    #
    #     try:
    #         WebDriverWait(driver, 2) \
    #             .until(expected_conditions.presence_of_element_located((By.NAME, "transaction_finished")))
    #         flag = True
    #     except TimeoutException:
    #         flag = False
    #
    #     assert flag

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()
