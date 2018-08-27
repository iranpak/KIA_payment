import time
from selenium import webdriver
import unittest

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

ADMIN_USER = "admin"
ADMIN_PASS = "2=2=2=2="
SLEEP_TIME = 1


class CheckActivities(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def login_as_admin(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8085/login/")
        time.sleep(SLEEP_TIME)

        username = driver.find_element_by_name('username')
        username.send_keys(ADMIN_USER)
        password = driver.find_element_by_name('password')
        password.send_keys(ADMIN_PASS)
        button = driver.find_element_by_name('submit_button')
        button.click()

    def test_transaction_history(self):
        self.login_as_admin()

        driver = self.driver
        driver.get("http://127.0.0.1:8085/admin/activities")
        time.sleep(SLEEP_TIME)

        try:
            WebDriverWait(driver, SLEEP_TIME) \
                .until(expected_conditions.presence_of_element_located((By.ID, "transactions")))
            flag = True
        except TimeoutException:
            flag = False

        assert flag

    def test_admin_history(self):
        self.login_as_admin()

        driver = self.driver
        driver.get("http://127.0.0.1:8085/admin/my_history")
        time.sleep(SLEEP_TIME)

        try:
            WebDriverWait(driver, SLEEP_TIME) \
                .until(expected_conditions.presence_of_element_located((By.ID, "history")))
            flag = True
        except TimeoutException:
            flag = False

        assert flag

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()
