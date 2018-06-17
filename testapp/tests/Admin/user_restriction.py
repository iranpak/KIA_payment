from selenium import webdriver
import unittest


class UserRestriction(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_successfully_restrict_users(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8085/admin/restrict_user")
        username_field = driver.find_element_by_name("username")
        message_field = driver.find_element_by_name("message")
        submit_button = driver.find_element_by_name("submit_button")
        username_field.send_keys("ali@gmail.com")
        message_field.send_keys("for your bad actions")
        submit_button.click()
        assert driver.find_element_by_name("successfully_done") is not None

    def test_not_empty_username(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8085/admin/restrict_user")
        username_field = driver.find_element_by_name("username")
        message_field = driver.find_element_by_name("message")
        submit_button = driver.find_element_by_name("submit_button")
        username_field.send_keys("")
        message_field.send_keys("for your bad actions")
        submit_button.click()
        assert driver.find_element_by_name("empty_field") is not None

    def test_successfully_delete_restriction_of_users(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8085/admin/restrict_user")
        username_field = driver.find_element_by_name("username")
        message_field = driver.find_element_by_name("message")
        submit_button = driver.find_element_by_name("submit_button")
        username_field.send_keys("ali@gmail.com")
        message_field.send_keys("your restriction is finished")
        submit_button.click()
        assert driver.find_element_by_name("successfully_done") is not None

    def test_valid_username(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8085/admin/restrict_user")
        username_field = driver.find_element_by_name("username")
        message_field = driver.find_element_by_name("message")
        submit_button = driver.find_element_by_name("submit_button")
        username_field.send_keys("ali@gmadsail.com")
        message_field.send_keys("your restriction is finished")
        submit_button.click()
        assert driver.find_element_by_name("invalid_input") is not None

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()