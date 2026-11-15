from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class CustomerPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    SEARCH_FIELD = (AppiumBy.XPATH, "//android.view.View[@content-desc='Search']//android.widget.EditText")

    def search_customer(self, search_term):
        print(f"Searching for customer: {search_term}")
        search_bar = self.wait.until(EC.element_to_be_clickable(self.SEARCH_FIELD))
        
        try:
            search_bar.click()
        except:
            self.driver.execute_script('mobile: clickGesture', {'elementId': search_bar.id})
            
        time.sleep(1)
        search_bar.clear()
        search_bar.send_keys(search_term)
        
        try:
            self.driver.hide_keyboard()
            time.sleep(2) # Wait for list to filter
        except:
            pass

    def select_customer(self, customer_name):
        print(f"Selecting customer containing: {customer_name}")
        
        # Case-insensitive search for the customer
        xpath = f"//*[contains(translate(@content-desc, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{customer_name.lower()}') and @clickable='true']"
        
        try:
            customer = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, xpath)))
            
            # FORCE NATIVE CLICK (Bypasses the React Native silent failure)
            print("Found customer. Forcing native click...")
            self.driver.execute_script('mobile: clickGesture', {'elementId': customer.id})
                
            print(f"✅ Selected customer: {customer_name}")
            time.sleep(3) # Wait for the next screen to load
            
        except Exception as e:
            print(f"❌ Could not find or click customer: {e}")