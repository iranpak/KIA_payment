from selenium import webdriver
import unittest


class CurrencyToRial(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_successful_login(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8085/user_login/")
        username = driver.find_element_by_name("username")
        password = driver.find_element_by_name("password")
        login_button = driver.find_element_by_name("loginButton")
        username.send_keys("karegar@gmail.com")
        password.send_keys("123456")
        login_button.click()
        assert driver.find_element_by_name("loginSuccessful") is not None

    def test_empty_field_login(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8085/user_login/")
        username = driver.find_element_by_name("username")
        password = driver.find_element_by_name("password")
        login_button = driver.find_element_by_name("loginButton")
        username.send_keys("karegar@gmail.com")
        password.send_keys("")
        login_button.click()
        assert driver.find_element_by_name("emptyField") is not None
    
    def test_wrong_pattern_login(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8085/user_login/")
        username = driver.find_element_by_name("username")
        password = driver.find_element_by_name("password")
        login_button = driver.find_element_by_name("loginButton")
        username.send_keys("wrong.email@pattern")
        password.send_keys("123456")
        login_button.click()
        assert driver.find_element_by_name("wrongEmailPattern") is not None
    
    def test_wrong_username_login(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8085/user_login/")
        username = driver.find_element_by_name("username")
        password = driver.find_element_by_name("password")
        login_button = driver.find_element_by_name("loginButton")
        username.send_keys("unregistered@gmail.com")
        password.send_keys("123456")
        login_button.click()
        assert driver.find_element_by_name("wrongUsernameOrPassword") is not None

    def test_wrong_password_login(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8085/user_login/")
        username = driver.find_element_by_name("username")
        password = driver.find_element_by_name("password")
        login_button = driver.find_element_by_name("loginButton")
        username.send_keys("karegar@gmail.com")
        password.send_keys("wrongPassword")
        login_button.click()
        assert driver.find_element_by_name("wrongUsernameOrPassword") is not None

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()