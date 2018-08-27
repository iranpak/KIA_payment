from selenium import webdriver
import unittest
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

USER_USERNAME = 'user'
USER_PASSWORD = '1q1q1q1q'


class UserTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.close()

    def login_as_user(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8085/login")
        username = driver.find_element_by_name('username')
        username.send_keys(USER_USERNAME)
        password = driver.find_element_by_name('password')
        password.send_keys(USER_PASSWORD)
        button = driver.find_element_by_name('submit_button')
        button.click()
        time.sleep(1)

    def test_user_observe_profile_data(self):
        global element_existence, value_existence
        driver = self.driver

        self.login_as_user()

        driver.get("http://127.0.0.1:8085/edit_profile/")
        elements = [driver.find_element_by_name("first_name"),
                    driver.find_element_by_name("last_name"),
                    driver.find_element_by_name("email"),
                    driver.find_element_by_name("phone_number"),
                    driver.find_element_by_name("account_number"),
                    driver.find_element_by_name("username")
                    ]

        for element in elements:
            element_existence = element is not None

        essential_elements = list(elements)
        essential_elements.pop()
        essential_elements.pop()

        for element in essential_elements:
            value_existence = element.get_property("value") != ""

        assert element_existence & value_existence

    def test_user_change_profile_data_valid(self):
        driver = self.driver

        self.login_as_user()

        driver.get("http://127.0.0.1:8085/edit_profile")
        first_name = driver.find_element_by_name("first_name")
        last_name = driver.find_element_by_name("last_name")
        phone_number = driver.find_element_by_name("phone_number")
        account_number = driver.find_element_by_name("account_number")

        submit_button = driver.find_element_by_name("submit_button")

        first_name.send_keys("Ali")
        last_name.send_keys("Alavi")
        phone_number.clear()
        phone_number.send_keys("54")
        account_number.clear()
        account_number.send_keys("123445666")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        submit_button.click()

        try:
            WebDriverWait(driver, 1) \
                .until(expected_conditions.presence_of_element_located((By.ID, "success")))
            flag = True
        except TimeoutException:
            flag = False

        assert flag

    def test_user_change_profile_data_empty_field(self):
        driver = self.driver

        self.login_as_user()

        driver.get("http://127.0.0.1:8085/edit_profile")
        first_name = driver.find_element_by_name("first_name")
        last_name = driver.find_element_by_name("last_name")
        phone_number = driver.find_element_by_name("phone_number")
        account_number = driver.find_element_by_name("account_number")

        submit_button = driver.find_element_by_name("submit_button")

        first_name.clear()
        first_name.send_keys("")
        last_name.send_keys("Alavi")
        phone_number.send_keys("")
        phone_number.send_keys("54")
        account_number.send_keys("")
        account_number.send_keys("123445666")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        submit_button.click()

        try:
            WebDriverWait(driver, 2) \
                .until(expected_conditions.presence_of_element_located((By.ID, "form_errors")))
            flag = True
        except TimeoutException:
            flag = False

        assert flag

    def test_user_change_password_valid(self):
        driver = self.driver

        self.login_as_user()

        driver.get("http://127.0.0.1:8085/change_password")
        old_password = driver.find_element_by_name("old_password")
        new_password = driver.find_element_by_name("new_password")
        new_password_again = driver.find_element_by_name("new_password_confirmation")

        submit_button = driver.find_element_by_name("submit_button")

        old_password.send_keys("2w2w2w2w")
        new_password.send_keys("1q1q1q1q")
        new_password_again.send_keys("1q1q1q1q")

        submit_button.click()

        try:
            WebDriverWait(driver, 1) \
                .until(expected_conditions.presence_of_element_located((By.ID, "success")))
            flag = True
        except TimeoutException:
            flag = False

        assert flag

    def test_user_change_password_invalid(self):
        driver = self.driver

        self.login_as_user()

        driver.get("http://127.0.0.1:8085/change_password")
        old_password = driver.find_element_by_name("old_password")
        new_password = driver.find_element_by_name("new_password")
        new_password_again = driver.find_element_by_name("new_password_confirmation")

        submit_button = driver.find_element_by_name("submit_button")

        old_password.send_keys("1q1q1q1q")
        new_password.send_keys("1q1q1q1q")
        new_password_again.send_keys("3432asdf")

        submit_button.click()

        try:
            WebDriverWait(driver, 2) \
                .until(expected_conditions.presence_of_element_located((By.NAME, "form_errors")))
            flag = True
        except TimeoutException:
            flag = False

        assert flag


if __name__ == '__main__':
    unittest.main()
