from selenium import webdriver
import unittest
import time

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = '1q1q1q1q'


class CheckActivities(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def login_as_admin(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8085/login")
        username = driver.find_element_by_name('username')
        username.send_keys(ADMIN_USERNAME)
        password = driver.find_element_by_name('password')
        password.send_keys(ADMIN_PASSWORD)
        button = driver.find_element_by_name('submit_button')
        button.click()
        time.sleep(1)

    def test_elements_exist(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8085/homepage")

        assert driver.find_element_by_id("carousel") is not None
        assert driver.find_element_by_id("features") is not None
        assert driver.find_element_by_id("services") is not None
        assert driver.find_element_by_id("properties") is not None

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()