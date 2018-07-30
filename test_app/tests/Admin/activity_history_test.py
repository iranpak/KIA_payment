from selenium import webdriver
import unittest

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class CheckActivities(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_check_users_activities(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8085/admin/panel")
        user_activities_button = driver.find_element_by_name("users_activities_btn")
        user_activities_button.click()

        try:
            WebDriverWait(driver, 2) \
                .until(expected_conditions.presence_of_element_located((By.NAME, "user_activities_table")))
            flag = True
        except TimeoutException:
            flag = False

        assert flag

    def test_check_employees_activities(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8085/admin/panel")
        employees_activities_button = driver.find_element_by_name("emp_activities_btn")
        employees_activities_button.click()

        try:
            WebDriverWait(driver, 2) \
                .until(expected_conditions.presence_of_element_located((By.NAME, "emp_activities_table")))
            flag = True
        except TimeoutException:
            flag = False

        assert flag

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()
