from selenium import webdriver
import unittest


class CurrencyToRial(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_dollar(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8085/all_transactions")

        currency_list = driver.find_element_by_id("currency_list")
        assert currency_list is not None

        assert currency_list.find_element_by_class_name("dollar_row") is not None

    def test_euro(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8085/all_transactions")

        currency_list = driver.find_element_by_id("currency_list")
        assert currency_list is not None

        assert currency_list.find_element_by_class_name("euro_row") is not None


    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()