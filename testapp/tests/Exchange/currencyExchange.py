from selenium import webdriver
import unittest


class CurrencyToRial(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_correct_currency(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8085/currency_to_rial/")
        currency_name = driver.find_element_by_name("currencyName")
        send_button = driver.find_element_by_name("sendButton")
        currency_name.send_keys("Dollar")
        send_button.click()
        assert driver.find_element_by_name("rialPrice") is not None

    def test_incorrect_currency(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8085/currency_to_rial/")
        currency_name = driver.find_element_by_name("currencyName")
        send_button = driver.find_element_by_name("sendButton")
        currency_name.send_keys("FakeCurrency")
        send_button.click()
        assert driver.find_element_by_name("incorrectCurrency") is not None

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()