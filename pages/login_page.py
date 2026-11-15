from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    # --- LOCATORS ---
    USERNAME_FIELD = (AppiumBy.XPATH, "//android.widget.EditText[@hint='Username*']")
    PASSWORD_FIELD = (AppiumBy.XPATH, "//android.widget.EditText[@hint='Password*']")
    COMPANY_DROPDOWN = (AppiumBy.XPATH, "//*[@hint='Company*']")
    LOGIN_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Login")

    # --- ACTIONS ---
    def enter_username(self, username):
        username_element = self.wait.until(EC.element_to_be_clickable(self.USERNAME_FIELD))
        username_element.click()
        username_element.send_keys(username)

    def enter_password(self, password):
        password_element = self.wait.until(EC.element_to_be_clickable(self.PASSWORD_FIELD))
        password_element.click()
        password_element.send_keys(password)

    def select_company(self, company_name):
        # Hide keyboard so it doesn't block the dropdown
        try:
            self.driver.hide_keyboard()
            time.sleep(1)
        except:
            pass

        dropdown = self.wait.until(EC.presence_of_element_located(self.COMPANY_DROPDOWN))
        try:
            dropdown.click()
        except:
            self.driver.execute_script('mobile: clickGesture', {'elementId': dropdown.id})
        
        # Wait for list to open and select company
        try:
            company_item = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, company_name))
            )
            company_item.click()
        except Exception:
            first_item = self.driver.find_element(AppiumBy.XPATH, "//android.view.View[@content-desc][@clickable='true']")
            first_item.click()
        time.sleep(1)

    def click_login(self):
        try:
            self.driver.hide_keyboard()
        except:
            pass
            
        login_btn = self.wait.until(EC.presence_of_element_located(self.LOGIN_BUTTON))
        try:
            login_btn.click()
        except:
            self.driver.execute_script('mobile: clickGesture', {'elementId': login_btn.id})