from selenium import webdriver
import unittest


class CheckActivities(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_check_users_activities(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8085/admin/panel")
        user_activities_button = driver.find_element_by_name("users_activities_btn")
        user_activities_button.click()
        assert driver.find_element_by_name("user_activities_table") is not None

    def test_check_employees_activities(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8085/admin/panel")
        employees_activities_button = driver.find_element_by_name("emp_activities_btn")
        employees_activities_button.click()
        assert driver.find_element_by_name("emp_activities_table") is not None



    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()