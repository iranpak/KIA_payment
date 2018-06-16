from selenium import webdriver
import unittest


class AddFeatureTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_add_feature_notif(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8085/add_feature/")
        feature_name = driver.find_element_by_name("featureName")
        feature_type = driver.find_element_by_name("featureType")
        add_button = driver.find_element_by_name("addButton")
        feature_name.send_keys("New Exam")
        feature_type.send_keys("English")
        add_button.click()
        assert driver.find_element_by_name("notificationSent") is not None

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()