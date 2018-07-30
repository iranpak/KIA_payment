from selenium import webdriver
import unittest

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class SendEmail(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_successful_send(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8085/send_email/")
        text = driver.find_element_by_name("text")
        subject = driver.find_element_by_name("subject")
        email = driver.find_element_by_name("email")
        send_button = driver.find_element_by_name("sendButton")
        text.send_keys("Hello user")
        subject.send_keys("A message")
        email.send_keys("user@gmail.com")
        send_button.click()

        try:
            WebDriverWait(driver, 2) \
                .until(expected_conditions.presence_of_element_located((By.NAME, "email_sent")))
            flag = True
        except TimeoutException:
            flag = False

        assert flag

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()