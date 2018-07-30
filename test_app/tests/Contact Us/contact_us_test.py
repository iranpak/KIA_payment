from selenium import webdriver
import unittest

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class ContactUsNotEmptyField(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_contact_us_not_empty_field(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8085/contact_us/")

        ticket_box = driver.find_element_by_name("ticketBox")
        first_name = driver.find_element_by_name("firstName")
        last_name = driver.find_element_by_name("lastName")
        email = driver.find_element_by_name("email")
        send_button = driver.find_element_by_name("sendButton")

        ticket_box.send_keys("salam")
        first_name.send_keys("ali")
        last_name.send_keys("alavi")
        email.send_keys("ali@gmail.com")

        send_button.click()

        try:
            WebDriverWait(driver, 2) \
                .until(expected_conditions.presence_of_element_located((By.NAME, "successfully_sent")))
            flag = True
        except TimeoutException:
            flag = False

        assert flag

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()