from selenium import webdriver
import unittest


class AaminCheckTickets(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_admin_check_tickets(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8085/admin/check_tickets/")
        assert driver.find_element_by_name("ticketsList") is not None

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()