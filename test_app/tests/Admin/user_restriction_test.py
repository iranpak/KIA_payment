from selenium import webdriver
import unittest

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import time


#### DONE

class UserRestriction(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_successfully_restrict_users(self):
        driver = self.driver

        driver.get("http://127.0.0.1:8085/login")
        username = driver.find_element_by_name('username')
        username.send_keys('admin')
        password = driver.find_element_by_name('password')
        password.send_keys('1q1q1q1q')
        button = driver.find_element_by_name('submit_button')
        button.click()
        time.sleep(1)

        driver.get("http://127.0.0.1:8085/admin/restrict_user")
        username_field = WebDriverWait(driver, 1).until(
            expected_conditions.presence_of_element_located((By.ID, "res_username"))
        )
        message_field = driver.find_element_by_id("restrict_message")
        submit_button = driver.find_element_by_id("submit_button")
        username_field.send_keys("khafan")
        message_field.send_keys("for your bad actions")
        submit_button.click()

        try:
            WebDriverWait(driver, 1) \
                .until(expected_conditions.presence_of_element_located((By.ID, "success")))
            flag = True
        except TimeoutException:
            flag = False

        assert flag

    def test_successfully_remove_restriction_of_users(self):
        driver = self.driver

        driver.get("http://127.0.0.1:8085/login")
        username = driver.find_element_by_name('username')
        username.send_keys('admin')
        password = driver.find_element_by_name('password')
        password.send_keys('1q1q1q1q')
        button = driver.find_element_by_name('submit_button')
        button.click()
        time.sleep(1)

        driver.get("http://127.0.0.1:8085/admin/restrict_user")
        username_field = WebDriverWait(driver, 1).until(
            expected_conditions.presence_of_element_located((By.ID, "res_username")))
        message_field = driver.find_element_by_name("restrict_message")
        submit_button = driver.find_element_by_name("submit_button")
        username_field.send_keys("khafan")
        message_field.send_keys("your restriction is finished")
        submit_button.click()

        try:
            WebDriverWait(driver, 1) \
                .until(expected_conditions.presence_of_element_located((By.ID, "success")))
            flag = True
        except TimeoutException:
            flag = False

        assert flag

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()