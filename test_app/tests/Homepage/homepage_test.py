from selenium import webdriver
import unittest


class CheckActivities(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_elements_exist(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8085/homepage")

        assert driver.find_element_by_name("profile") is not None
        assert driver.find_element_by_name("services") is not None
        assert driver.find_element_by_name("logout") is not None
        assert driver.find_element_by_name("toefl") is not None
        assert driver.find_element_by_name("ielts") is not None
        assert driver.find_element_by_name("iran_air") is not None

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()