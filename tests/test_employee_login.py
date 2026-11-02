import os
import unittest
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


PORTAL_URL = "http://localhost:5000"
VALID_EMPLOYEE_ID = "EMP001"
VALID_PASSWORD = "password123"
INVALID_PASSWORD = "wrong-password"


class EmployeePortalLoginTests(unittest.TestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        chrome_binary = os.environ.get("CHROME_BINARY")
        if chrome_binary:
            options.binary_location = chrome_binary
        elif Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe").is_file():
            options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def login(self, employee_id, password):
        self.driver.get(PORTAL_URL)
        employee_id_field = self.wait.until(
            EC.visibility_of_element_located((By.ID, "employee_id"))
        )
        password_field = self.wait.until(
            EC.visibility_of_element_located((By.ID, "password"))
        )
        login_button = self.wait.until(
            EC.element_to_be_clickable((By.ID, "login_button"))
        )
        employee_id_field.clear()
        employee_id_field.send_keys(employee_id)
        password_field.clear()
        password_field.send_keys(password)
        login_button.click()

    def test_valid_credentials_show_employee_dashboard(self):
        self.login(VALID_EMPLOYEE_ID, VALID_PASSWORD)

        welcome_message = self.wait.until(
            EC.visibility_of_element_located((By.ID, "welcome_message"))
        )
        self.assertEqual("Welcome, EMP001", welcome_message.text)
        self.assertTrue(self.driver.current_url.endswith("/dashboard"))

    def test_invalid_credentials_show_error_message(self):
        self.login(VALID_EMPLOYEE_ID, INVALID_PASSWORD)

        error_message = self.wait.until(
            EC.visibility_of_element_located((By.ID, "error_message"))
        )
        self.assertEqual("Invalid employee ID or password.", error_message.text)


if __name__ == "__main__":
    unittest.main()
