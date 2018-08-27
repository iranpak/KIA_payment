from selenium import webdriver
import unittest

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


### DONE

class ContactUsNotEmptyField(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_contact_us_success_send_message(self):
        driver = self.driver

        driver.get("http://127.0.0.1:8085/contact_us")
        name = driver.find_element_by_name("name")
        phone_number = driver.find_element_by_name("phone")
        email = driver.find_element_by_name("email")
        message = driver.find_element_by_name("message")
        send_button = driver.find_element_by_name("submit_button")

        name.send_keys("ali alavi")
        email.send_keys("ali@gmail.com")
        phone_number.send_keys("12345")
        message.send_keys("very good")

        send_button.click()

        try:
            WebDriverWait(driver, 1) \
                .until(expected_conditions.presence_of_element_located((By.ID, "success")))
            flag = True
        except TimeoutException:
            flag = False

        assert flag

    def test_contact_us_not_empty_field(self):
        driver = self.driver

        driver.get("http://127.0.0.1:8085/contact_us")
        name = driver.find_element_by_name("name")
        phone_number = driver.find_element_by_name("phone")
        email = driver.find_element_by_name("email")
        message = driver.find_element_by_name("message")
        send_button = driver.find_element_by_name("submit_button")

        name.send_keys("ali alavi")
        email.send_keys("ali@gmail.com")
        phone_number.send_keys("")
        message.send_keys("very good")

        send_button.click()

        try:
            WebDriverWait(driver, 1) \
                .until(expected_conditions.presence_of_element_located((By.ID, "form_errors")))
            flag = True
        except TimeoutException:
            flag = False

        assert flag

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()