from selenium import webdriver
import unittest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class NotEmptyField(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_not_empty_field(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8085/register/")
        first_name = driver.find_element_by_name("firstName")
        last_name = driver.find_element_by_name("lastName")
        password = driver.find_element_by_name("password")
        repassword = driver.find_element_by_name("repassword")
        email = driver.find_element_by_name("email")
        phone_number = driver.find_element_by_name("")
        register_button = driver.find_element_by_name("registerButton")
        first_name.send_keys("ali")
        last_name.send_keys("alavi")
        password.send_keys("1234")
        repassword.send_keys("1234")
        email.send_keys("ali@gmail.com")
        phone_number.send_keys("09121234567")
        register_button.click()
        assert driver.find_element_by_name("emptyField") is not None

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()