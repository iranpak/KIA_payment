from selenium import webdriver
import unittest


class ValidEmailContactUs(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_contact_us_valid_email(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8085/contact_us/")
        ticket_box = driver.find_element_by_name("ticketBox")
        first_name = driver.find_element_by_name("firstName")
        last_name = driver.find_element_by_name("lastName")
        email = driver.find_element_by_name("email")
        send_button = driver.find_element_by_name("sendButton")
        ticket_box.send_keys("")
        first_name.send_keys("ali")
        last_name.send_keys("alavi")
        email.send_keys("ali@gmail.com")
        send_button.click()
        assert driver.find_element_by_name("invalidEmail") is not None

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()