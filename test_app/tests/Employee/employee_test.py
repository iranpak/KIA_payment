import time
from selenium import webdriver
import unittest

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

EMP_USER = "emp"
EMP_PASS = "1=1=1=1="
SLEEP_TIME = 1


class UserTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def login_as_emp(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8085/login/")
        time.sleep(SLEEP_TIME)

        username = driver.find_element_by_name('username')
        username.send_keys(EMP_USER)
        password = driver.find_element_by_name('password')
        password.send_keys(EMP_PASS)
        button = driver.find_element_by_name('submit_button')
        button.click()

    def test_observe_all_transactions(self):
        self.login_as_emp()

        driver = self.driver
        driver.get("http://127.0.0.1:8085/emp/transactions/")

        try:
            WebDriverWait(driver, SLEEP_TIME) \
                .until(expected_conditions.presence_of_element_located((By.ID, "transactions")))
            flag = True
        except TimeoutException:
            flag = False

        assert flag

    def test_select_transaction(self):
        self.login_as_emp()

        driver = self.driver
        driver.get("http://127.0.0.1:8085/emp/transactions/")

        link = driver.find_element_by_id("select_transaction")

        link.click()

        try:
            WebDriverWait(driver, 2) \
                .until(expected_conditions.presence_of_element_located((By.NAME, "take")))
            flag = True
        except TimeoutException:
            flag = False

        assert flag

        take_button = driver.find_element_by_name("take")

        take_button.click()

        try:
            WebDriverWait(driver, SLEEP_TIME) \
                .until(expected_conditions.url_contains("success"))
            flag = True
        except TimeoutException:
            flag = False

        assert flag

    def test_finish_transaction(self):
        self.login_as_emp()

        driver = self.driver
        driver.get("http://127.0.0.1:8085/emp/taken_transactions")

        link = driver.find_element_by_id("select_transaction")

        link.click()

        try:
            WebDriverWait(driver, 2) \
                .until(expected_conditions.presence_of_element_located((By.NAME, "finish")))
            flag = True
        except TimeoutException:
            flag = False

        assert flag

        take_button = driver.find_element_by_name("finish")

        take_button.click()

        try:
            WebDriverWait(driver, SLEEP_TIME) \
                .until(expected_conditions.url_contains("success"))
            flag = True
        except TimeoutException:
            flag = False

        assert flag

    def test_fail_transaction(self):
        self.login_as_emp()

        driver = self.driver
        driver.get("http://127.0.0.1:8085/emp/taken_transactions")

        link = driver.find_element_by_id("select_transaction")

        link.click()

        try:
            WebDriverWait(driver, 2) \
                .until(expected_conditions.presence_of_element_located((By.NAME, "fail")))
            flag = True
        except TimeoutException:
            flag = False

        assert flag

        take_button = driver.find_element_by_name("fail")

        take_button.click()

        try:
            WebDriverWait(driver, SLEEP_TIME) \
                .until(expected_conditions.url_contains("success"))
            flag = True
        except TimeoutException:
            flag = False

        assert flag

    def test_report_transaction(self):
            self.login_as_emp()

            driver = self.driver
            driver.get("http://127.0.0.1:8085/emp/taken_transactions")

            link = driver.find_element_by_id("select_transaction")

            link.click()

            try:
                WebDriverWait(driver, 2) \
                    .until(expected_conditions.presence_of_element_located((By.NAME, "report")))
                flag = True
            except TimeoutException:
                flag = False

            assert flag

            take_button = driver.find_element_by_name("report")

            take_button.click()

            try:
                WebDriverWait(driver, SLEEP_TIME) \
                    .until(expected_conditions.url_contains("success"))
                flag = True
            except TimeoutException:
                flag = False

            assert flag

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()
