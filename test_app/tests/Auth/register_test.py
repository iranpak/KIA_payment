from selenium import webdriver
import unittest
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class RegisterTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_successfully_registered(self):
        driver = self.driver

        driver.get("http://127.0.0.1:8085/signup")
        first_name = driver.find_element_by_name("first_name")
        last_name = driver.find_element_by_name("last_name")
        username = driver.find_element_by_name("username")
        password = driver.find_element_by_name("password1")
        repassword = driver.find_element_by_name("password2")
        email = driver.find_element_by_name("email")
        phone_number = driver.find_element_by_name("phone_number")
        account_number = driver.find_element_by_name("account_number")
        register_button = driver.find_element_by_name("account_number")
        first_name.send_keys("ali")
        last_name.send_keys("alavi")
        username.send_keys("new_user")
        password.send_keys("1q1q1q1q")
        repassword.send_keys("1q1q1q1q")
        email.send_keys("new_user@gmail.com")
        phone_number.send_keys("09121234567")
        account_number.send_keys("123456")
        register_button.click()
        time.sleep(3)

        try:
            WebDriverWait(driver, 2) \
                .until(expected_conditions.url_matches("http://127.0.0.1:8085"))
            flag = True
        except TimeoutException:
            flag = False

        assert flag

    def test_passwords_equality(self):
        driver = self.driver

        driver.get("http://127.0.0.1:8085/signup")
        first_name = driver.find_element_by_name("first_name")
        last_name = driver.find_element_by_name("last_name")
        username = driver.find_element_by_name("username")
        password = driver.find_element_by_name("password1")
        repassword = driver.find_element_by_name("password2")
        email = driver.find_element_by_name("email")
        phone_number = driver.find_element_by_name("phone_number")
        account_number = driver.find_element_by_name("account_number")
        register_button = driver.find_element_by_name("account_number")
        first_name.send_keys("ali")
        last_name.send_keys("alavi")
        username.send_keys("new_user")
        password.send_keys("1q1q1q1q")
        repassword.send_keys("sadf;lksf")
        email.send_keys("new_user@gmail.com")
        phone_number.send_keys("09121234567")
        account_number.send_keys("123456")
        register_button.click()
        time.sleep(3)

        try:
            WebDriverWait(driver, 2) \
                .until(expected_conditions.url_matches("http://127.0.0.1:8085/signup"))
            flag = True
        except TimeoutException:
            flag = False

        assert flag

    def test_not_empty_field(self):
        driver = self.driver

        driver.get("http://127.0.0.1:8085/signup")
        first_name = driver.find_element_by_name("first_name")
        last_name = driver.find_element_by_name("last_name")
        username = driver.find_element_by_name("username")
        password = driver.find_element_by_name("password1")
        repassword = driver.find_element_by_name("password2")
        email = driver.find_element_by_name("email")
        phone_number = driver.find_element_by_name("phone_number")
        account_number = driver.find_element_by_name("account_number")
        register_button = driver.find_element_by_name("account_number")
        first_name.send_keys("ali")
        last_name.send_keys("alavi")
        username.send_keys("")
        password.send_keys("1q1q1q1q")
        repassword.send_keys("sadf;lksf")
        email.send_keys("new_user@gmail.com")
        phone_number.send_keys("09121234567")
        account_number.send_keys("123456")
        register_button.click()
        time.sleep(3)

        try:
            WebDriverWait(driver, 2) \
                .until(expected_conditions.url_matches("http://127.0.0.1:8085/signup"))
            flag = True
        except TimeoutException:
            flag = False

        assert flag

    def test_valid_email(self):
        driver = self.driver

        driver.get("http://127.0.0.1:8085/signup")
        first_name = driver.find_element_by_name("first_name")
        last_name = driver.find_element_by_name("last_name")
        username = driver.find_element_by_name("username")
        password = driver.find_element_by_name("password1")
        repassword = driver.find_element_by_name("password2")
        email = driver.find_element_by_name("email")
        phone_number = driver.find_element_by_name("phone_number")
        account_number = driver.find_element_by_name("account_number")
        register_button = driver.find_element_by_name("account_number")
        first_name.send_keys("ali")
        last_name.send_keys("alavi")
        username.send_keys("new_user")
        password.send_keys("1q1q1q1q")
        repassword.send_keys("1q1q1q1q")
        email.send_keys("new_usergmlcom")
        phone_number.send_keys("09121234567")
        account_number.send_keys("123456")
        register_button.click()
        time.sleep(3)

        try:
            WebDriverWait(driver, 2) \
                .until(expected_conditions.url_matches("http://127.0.0.1:8085/signup"))
            flag = True
        except TimeoutException:
            flag = False

        assert flag


if __name__ == '__main__':
    unittest.main()
