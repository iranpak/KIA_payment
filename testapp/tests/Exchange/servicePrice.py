from selenium import webdriver
import unittest


class CurrencyToRial(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_correct_service(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8085/get_service_price/")
        service_name = driver.find_element_by_name("serviceName")
        send_button = driver.find_element_by_name("sendButton")
        service_name.send_keys("TOEFL")
        send_button.click()
        assert driver.find_element_by_name("price") is not None
        assert driver.find_element_by_name("currencyName") is not None

    def test_incorrect_service(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8085/get_service_price/")
        service_name = driver.find_element_by_name("serviceName")
        send_button = driver.find_element_by_name("sendButton")
        service_name.send_keys("FakeService")
        send_button.click()
        assert driver.find_element_by_name("incorrectService") is not None


    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()