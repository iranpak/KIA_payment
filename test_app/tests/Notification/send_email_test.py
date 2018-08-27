from selenium import webdriver
import unittest
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

EMP_USERNAME = 'emp'
EMP_PASSWORD = '1q1q1q1q'


class SendEmail(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def login_as_emp(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8085/login")
        username = driver.find_element_by_name('username')
        username.send_keys(EMP_USERNAME)
        password = driver.find_element_by_name('password')
        password.send_keys(EMP_PASSWORD)
        button = driver.find_element_by_name('submit_button')
        button.click()
        time.sleep(1)

    def test_successful_send(self):
        driver = self.driver

        self.login_as_emp()

        driver.get("http://127.0.0.1:8085/send_email")

        username = driver.find_element_by_name("receiver_username")
        text = driver.find_element_by_name("message_body")
        subject = driver.find_element_by_name("subject")
        send_button = driver.find_element_by_name("submit_button")

        text.send_keys("Hello dear user")
        subject.send_keys("A message")
        username.send_keys("user")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        send_button.click()

        try:
            WebDriverWait(driver, 10) \
                .until(expected_conditions.presence_of_element_located((By.ID, "success")))
            flag = True
        except TimeoutException:
            flag = False

        assert flag

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()