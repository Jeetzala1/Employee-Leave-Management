import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class LoginTest(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get("http://localhost:5000")
        self.wait.until(EC.visibility_of_element_located((By.ID, "login_button")))

    def test_valid_login(self):
        self.driver.find_element(By.ID, "employee_id").send_keys("EMP001")
        self.driver.find_element(By.ID, "password").send_keys("password123")
        self.wait.until(EC.element_to_be_clickable((By.ID, "login_button"))).click()

        self.wait.until(EC.url_contains("dashboard"))
        welcome = self.wait.until(EC.visibility_of_element_located((By.ID, "welcome_message")))
        self.assertEqual("Welcome, EMP001", welcome.text)

    def test_invalid_login(self):
        self.driver.find_element(By.ID, "employee_id").send_keys("EMP001")
        self.driver.find_element(By.ID, "password").send_keys("wrong-password")
        self.wait.until(EC.element_to_be_clickable((By.ID, "login_button"))).click()

        error = self.wait.until(
            EC.visibility_of_element_located((By.ID, "error_message"))
        )
        self.assertEqual(error.text, "Invalid employee ID or password.")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()