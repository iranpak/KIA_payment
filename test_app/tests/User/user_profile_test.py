from selenium import webdriver
import unittest

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class UserTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.close()

    def test_user_observe_profile_data(self):
        global element_existence, value_existence
        driver = self.driver
        driver.get("http://127.0.0.1:8085/user_profile/")

        elements = [driver.find_element_by_name("first_name"),
                    driver.find_element_by_name("last_name"),
                    driver.find_element_by_name("last_name"),
                    driver.find_element_by_name("email"),
                    driver.find_element_by_name("old_pass"),
                    driver.find_element_by_name("new_pass"),
                    driver.find_element_by_name("new_pass_again")]

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
        driver.get("http://127.0.0.1:8085/user_profile/")

        first_name = driver.find_element_by_name("first_name")
        last_name = driver.find_element_by_name("last_name")
        phone_number = driver.find_element_by_name("phone_number")
        email = driver.find_element_by_name("email")

        submit_button = driver.find_element_by_name("sendButton")

        first_name.send_keys("Ali")
        last_name.send_keys("Alavi")
        phone_number.send_keys("09120123456")
        email.send_keys("alialavi@gmail.com")

        submit_button.click()

        try:
            WebDriverWait(driver, 2) \
                .until(expected_conditions.presence_of_element_located((By.NAME, "successful_change")))
            flag = True
        except TimeoutException:
            flag = False

        assert flag

    # def test_user_change_profile_data_invalid_name(self):
    #     driver = self.driver
    #     driver.get("http://127.0.0.1:8085/user_profile/")
    #
    #     first_name = driver.find_element_by_name("first_name")
    #     last_name = driver.find_element_by_name("last_name")
    #     phone_number = driver.find_element_by_name("phone_number")
    #     email = driver.find_element_by_name("email")
    #
    #     submit_button = driver.find_element_by_name("sendButton")
    #
    #     first_name.send_keys("")
    #     last_name.send_keys("Alavi")
    #     phone_number.send_keys("09120123456")
    #     email.send_keys("alialavi@gmail.com")
    #
    #     submit_button.click()
    #
    #     try:
    #         WebDriverWait(driver, 2) \
    #             .until(expected_conditions.presence_of_element_located((By.NAME, "invalid_name")))
    #         flag = True
    #     except TimeoutException:
    #         flag = False
    #
    #     assert flag

    def test_user_change_profile_data_invalid_number(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8085/user_profile/")

        first_name = driver.find_element_by_name("first_name")
        last_name = driver.find_element_by_name("last_name")
        phone_number = driver.find_element_by_name("phone_number")
        email = driver.find_element_by_name("email")

        submit_button = driver.find_element_by_name("sendButton")

        first_name.send_keys("Ali")
        last_name.send_keys("Alavi")
        phone_number.send_keys("ne12n")
        email.send_keys("alialavi@gmail.com")

        submit_button.click()

        try:
            WebDriverWait(driver, 2) \
                .until(expected_conditions.presence_of_element_located((By.NAME, "invalid_number")))
            flag = True
        except TimeoutException:
            flag = False

        assert flag

    # def test_user_change_profile_data_invalid_mail(self):
    #     driver = self.driver
    #     driver.get("http://127.0.0.1:8085/user_profile/")
    #
    #     first_name = driver.find_element_by_name("first_name")
    #     last_name = driver.find_element_by_name("last_name")
    #     phone_number = driver.find_element_by_name("phone_number")
    #     email = driver.find_element_by_name("email")
    #
    #     submit_button = driver.find_element_by_name("sendButton")
    #
    #     first_name.send_keys("Ali")
    #     last_name.send_keys("Alavi")
    #     phone_number.send_keys("09120123456")
    #     email.send_keys("alialavimail")
    #
    #     submit_button.click()
    #
    #     try:
    #         WebDriverWait(driver, 2) \
    #             .until(expected_conditions.presence_of_element_located((By.NAME, "invalid_number")))
    #         flag = True
    #     except TimeoutException:
    #         flag = False
    #
    #     assert flag

    def test_user_change_password_valid(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8085/user_profile/")

        first_name = driver.find_element_by_name("first_name")
        last_name = driver.find_element_by_name("last_name")
        phone_number = driver.find_element_by_name("phone_number")
        email = driver.find_element_by_name("email")

        new_password = driver.find_element_by_name("new_pass")
        new_password_again = driver.find_element_by_name("new_pass_again")

        submit_button = driver.find_element_by_name("sendButton")

        first_name.send_keys("Ali")
        last_name.send_keys("Alavi")
        phone_number.send_keys("09120123456")
        email.send_keys("alialavi@gmail.com")

        new_password.send_keys("1234")
        new_password_again.send_keys("1234")

        submit_button.click()

        try:
            WebDriverWait(driver, 2) \
                .until(expected_conditions.presence_of_element_located((By.NAME, "successful_pass_change")))
            flag = True
        except TimeoutException:
            flag = False

        assert flag

    def test_user_change_password_invalid(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8085/user_profile/")

        first_name = driver.find_element_by_name("first_name")
        last_name = driver.find_element_by_name("last_name")
        phone_number = driver.find_element_by_name("phone_number")
        email = driver.find_element_by_name("email")

        new_password = driver.find_element_by_name("new_pass")
        new_password_again = driver.find_element_by_name("new_pass_again")

        submit_button = driver.find_element_by_name("sendButton")

        first_name.send_keys("Ali")
        last_name.send_keys("Alavi")
        phone_number.send_keys("09120123456")
        email.send_keys("alialavi@gmail.com")

        new_password.send_keys("1234")
        new_password_again.send_keys("123")

        submit_button.click()

        try:
            WebDriverWait(driver, 2) \
                .until(expected_conditions.presence_of_element_located((By.NAME, "unsuccessful_pass_change")))
            flag = True
        except TimeoutException:
            flag = False

        assert flag


if __name__ == '__main__':
    unittest.main()
