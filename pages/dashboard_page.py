from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DashboardPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    # The XML shows the content-desc has a newline character (\n) between the two "Customers"
    CUSTOMERS_BTN = (AppiumBy.ACCESSIBILITY_ID, "Customers\nCustomers")
    TRANSACTIONS_BTN = (AppiumBy.ACCESSIBILITY_ID, "Transactions")

    def open_customers(self):
        print("Opening Customers list...")
        btn = self.wait.until(EC.presence_of_element_located(self.CUSTOMERS_BTN))
        try:
            btn.click()
        except:
            self.driver.execute_script('mobile: clickGesture', {'elementId': btn.id})