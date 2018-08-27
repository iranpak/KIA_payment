import time
from selenium import webdriver
import unittest

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

ADMIN_USER = "admin"
ADMIN_PASS = "2=2=2=2="
SLEEP_TIME = 1


class UserRestriction(unittest.TestCase):

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

    def test_successfully_add_transaction(self):
        self.login_as_admin()

        driver = self.driver
        driver.get("http://127.0.0.1:8085/create_service/")
        time.sleep(SLEEP_TIME)

        name = driver.find_element_by_name("name")
        label = driver.find_element_by_name("label")
        select = Select(driver.find_element_by_name('currency'))
        checkbox = driver.find_element_by_name("variable_price")
        commission = driver.find_element_by_name("commission")
        details = driver.find_element_by_name("details")
        image_url = driver.find_element_by_name("image_url")

        submit_button = driver.find_element_by_name("submit")

        name.send_keys("test_service")
        label.send_keys("خدمت آزمایشی")
        select.select_by_value('1')
        checkbox.click()
        commission.send_keys("20")
        details.send_keys("توضیحات")
        image_url.send_keys("http://127.0.0.1:8085/create_service/")

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        submit_button.click()

        try:
            WebDriverWait(driver, SLEEP_TIME) \
                .until(expected_conditions.url_contains("test_service"))
            flag = True
        except TimeoutException:
            flag = False

        assert flag

        name = driver.find_element_by_name("name")
        label = driver.find_element_by_name("label")
        select_type = Select(driver.find_element_by_name('type'))

        submit_button = driver.find_element_by_name("cont")

        name.send_keys("name")
        label.send_keys("اسم")
        select_type.select_by_value("2")

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        submit_button.click()

        try:
            WebDriverWait(driver, SLEEP_TIME) \
                .until(expected_conditions.url_contains("test_service"))
            flag = True
        except TimeoutException:
            flag = False

        assert flag

        submit_button = driver.find_element_by_name("finish")

        submit_button.click()

        try:
            WebDriverWait(driver, 5) \
                .until(expected_conditions.url_contains("success"))
            flag = True
        except TimeoutException:
            flag = False

        assert flag

    def test_transaction_history(self):
        self.login_as_admin()

        driver = self.driver
        driver.get("http://127.0.0.1:8085/admin/activities/")
        time.sleep(SLEEP_TIME)

        try:
            WebDriverWait(driver, SLEEP_TIME) \
                .until(expected_conditions.presence_of_element_located((By.ID, "transactions")))
            flag = True
        except TimeoutException:
            flag = False

        assert flag


if __name__ == '__main__':
    unittest.main()
