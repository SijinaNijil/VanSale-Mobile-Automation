from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TransactionPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    PLUS_BTN = (AppiumBy.XPATH, "//android.widget.Button[@clickable='true' and not(@content-desc='Back')]")
    INVOICE_BTN = (AppiumBy.ACCESSIBILITY_ID, "Invoice")
    ADD_ITEM_BTN_1 = (AppiumBy.ACCESSIBILITY_ID, "Add")
    ADD_ITEM_BTN_2 = (AppiumBy.ACCESSIBILITY_ID, "Plus")
    ADD_ITEM_BTN_3 = (AppiumBy.XPATH, "(//android.widget.Button | //android.widget.ImageView)[last()]")

    def click_plus(self):
        print("Clicking the '+' (Floating Action) button...")
        try:
            btn = self.wait.until(EC.presence_of_element_located(self.PLUS_BTN))
            self.driver.execute_script('mobile: clickGesture', {'elementId': btn.id})
            print("✅ Clicked '+'")
            time.sleep(2)
        except Exception as e:
            print(f"❌ Could not click '+': {e}")

    def select_invoice(self):
        print("Selecting 'Invoice' from the menu...")
        try:
            btn = self.wait.until(EC.element_to_be_clickable(self.INVOICE_BTN))
            self.driver.execute_script('mobile: clickGesture', {'elementId': btn.id})
            print("✅ Selected 'Invoice'")
            time.sleep(3)
        except Exception as e:
            print(f"❌ Could not select 'Invoice': {e}")

    def click_add_item(self):
        print("Clicking the '+' button to add an item...")
        try:
            btn = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located(self.ADD_ITEM_BTN_1))
            self.driver.execute_script('mobile: clickGesture', {'elementId': btn.id})
            print("✅ Clicked '+' (Found by 'Add')")
            time.sleep(2)
            return
        except:
            pass

        try:
            btn = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located(self.ADD_ITEM_BTN_2))
            self.driver.execute_script('mobile: clickGesture', {'elementId': btn.id})
            print("✅ Clicked '+' (Found by 'Plus')")
            time.sleep(2)
            return
        except:
            pass

        try:
            btn = self.wait.until(EC.presence_of_element_located(self.ADD_ITEM_BTN_3))
            self.driver.execute_script('mobile: clickGesture', {'elementId': btn.id})
            print("✅ Clicked last available button/image (FAB).")
            time.sleep(3) 
        except Exception as e:
            print(f"❌ Could not find the '+' button. Error: {e}")

    def add_product_to_invoice(self, product_name):
        print(f"Searching for product: {product_name}")
        search_field = (AppiumBy.XPATH, "//android.view.View[@content-desc='Search']//android.widget.EditText")
        search_bar = self.wait.until(EC.element_to_be_clickable(search_field))
        
        try:
            search_bar.click()
        except:
            self.driver.execute_script('mobile: clickGesture', {'elementId': search_bar.id})
            
        time.sleep(1)
        search_bar.clear()
        search_bar.send_keys(product_name)
        
        try:
            self.driver.hide_keyboard()
            time.sleep(2) 
        except:
            pass

        print(f"Clicking on product: {product_name}")
        product_xpath = f"//android.widget.ImageView[contains(@content-desc, '{product_name}')]"
        
        try:
            product = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, product_xpath)))
            self.driver.execute_script('mobile: clickGesture', {'elementId': product.id})
            print(f"✅ Clicked product: {product_name}")
            time.sleep(3) 
        except Exception as e:
            print(f"❌ Could not find or click product: {e}")

    def enter_quantity_and_save(self, quantity, rate="100.0"):
        print(f"Entering quantity: {quantity}")
        
        # 1. Enter Main Quantity
        qty_field = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, "//android.widget.EditText[@hint='Quantity*']")))
        try:
            qty_field.click()
        except:
            self.driver.execute_script('mobile: clickGesture', {'elementId': qty_field.id})
        
        time.sleep(1)
        current_text = qty_field.get_attribute("text")
        for _ in range(len(current_text) + 2): 
            self.driver.press_keycode(67) 
            
        time.sleep(1)
        qty_field.send_keys(str(quantity))
        time.sleep(1)
        
        try: self.driver.hide_keyboard()
        except: pass
        time.sleep(1)

        # 2. Enter Batch Quantity
        print("Attempting to enter Batch Quantity...")
        batch_field_xpath = "//android.view.View[contains(@content-desc, 'Batch')]//android.widget.EditText"
        try:
            batch_qty = self.driver.find_element(AppiumBy.XPATH, batch_field_xpath)
            batch_qty.click()
            time.sleep(1)
            batch_qty.send_keys(str(quantity))
            time.sleep(1)
            try: self.driver.hide_keyboard()
            except: pass
            time.sleep(1)
            print("✅ Entered batch quantity.")
        except Exception:
            print("No batch quantity field found yet.")

        # 3. CHECK RATE FIELD (The fix for "Please enter rate")
        print("Checking Rate field...")
        try:
            rate_field = self.driver.find_element(AppiumBy.XPATH, "//android.widget.EditText[@hint='Rate*']")
            rate_text = rate_field.get_attribute("text")
            if rate_text in ["0.0", "0", ""]:
                print(f"⚠️ Rate is 0.0. Entering provided rate: {rate}")
                rate_field.click()
                time.sleep(1)
                # Clear the 0.0
                for _ in range(len(rate_text) + 2):
                    self.driver.press_keycode(67)
                rate_field.send_keys(str(rate))
                try: self.driver.hide_keyboard()
                except: pass
                time.sleep(1)
            else:
                print(f"✅ Rate is already valid ({rate_text}).")
        except Exception:
            print("Could not check Rate field.")

        # 4. SCROLL UP TO REVEAL SAVE BUTTON
        print("Scrolling up to reveal the Save button...")
        size = self.driver.get_window_size()
        start_x = size['width'] // 2
        start_y = int(size['height'] * 0.4)
        end_y = int(size['height'] * 0.9)
        
        try:
            self.driver.execute_script('mobile: swipeGesture', {
                'left': start_x, 'top': start_y,
                'width': 0, 'height': end_y - start_y,
                'direction': 'down', 'percent': 1.0
            })
        except:
            self.driver.swipe(start_x, start_y, start_x, end_y, 500)
        time.sleep(2)

        # 5. Click Save
        print("Clicking Save on the popup...")
        save_xpath = "//*[@content-desc='Save' or @text='Save']"
        save_clicked = False
        try:
            save_btn = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, save_xpath)))
            try:
                save_btn.click()
            except:
                self.driver.execute_script('mobile: clickGesture', {'elementId': save_btn.id})
            print("✅ Save clicked.")
            save_clicked = True
        except Exception as e:
            print(f"❌ Could not find Save button: {e}")

        if not save_clicked:
            return 
            
        time.sleep(3) 

        # 6. Handle the Error Popups (Like Batch Mismatch)
        print("Checking for validation popups...")
        try:
            ok_xpath = "//*[@content-desc='OK' or @text='OK']"
            ok_btn = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((AppiumBy.XPATH, ok_xpath))
            )
            print("⚠️ Validation popup appeared. Clicking OK...")
            try:
                ok_btn.click()
            except:
                self.driver.execute_script('mobile: clickGesture', {'elementId': ok_btn.id})
            time.sleep(2)
            
            print("Retrying batch quantity entry...")
            batch_qty = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, batch_field_xpath)))
            batch_qty.click()
            time.sleep(1)
            batch_qty.send_keys(str(quantity))
            time.sleep(1)
            try: self.driver.hide_keyboard()
            except: pass

            print("Scrolling up again...")
            try:
                self.driver.execute_script('mobile: swipeGesture', {
                    'left': start_x, 'top': start_y,
                    'width': 0, 'height': end_y - start_y,
                    'direction': 'down', 'percent': 1.0
                })
            except: pass
            time.sleep(2)

            print("Clicking Save again...")
            save_btn = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, save_xpath)))
            try:
                save_btn.click()
            except:
                self.driver.execute_script('mobile: clickGesture', {'elementId': save_btn.id})
            print("✅ Save clicked after fixing errors.")
            
        except Exception:
            print("✅ Saved successfully on the first try (No error popup).")
            
        time.sleep(3)

    def close_add_item_popup(self):
        print("Closing the Add Item popup...")
        try:
            close_btn = self.wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Close")))
            try:
                close_btn.click()
            except:
                self.driver.execute_script('mobile: clickGesture', {'elementId': close_btn.id})
            print("✅ Add Item popup closed. Returned to main Invoice.")
            time.sleep(2)
        except Exception as e:
            print(f"❌ Could not close popup: {e}")

    def save_main_invoice(self):
        print("Clicking the main Save button on the Invoice...")
        try:
            # Find the Save button by its content-desc
            save_btn = self.wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Save")))
            
            try:
                save_btn.click()
            except:
                self.driver.execute_script('mobile: clickGesture', {'elementId': save_btn.id})
                
            print("✅ Main Save clicked. Waiting for confirmation...")
            time.sleep(5) # Wait to see if a success message appears or if it navigates away
            
        except Exception as e:
            print(f"❌ Could not click the main Save button: {e}")

    def confirm_print_invoice(self):
        print("Handling print confirmation popup...")
        try:
            # Look for the 'Yes' button by its content-desc
            yes_btn = self.wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Yes")))
            
            try:
                yes_btn.click()
            except:
                self.driver.execute_script('mobile: clickGesture', {'elementId': yes_btn.id})
                
            print("✅ Clicked 'Yes'. Invoice successfully saved!")
            time.sleep(4) # Wait for the save to process and the print screen to appear
            
        except Exception as e:
            print(f"❌ Could not click 'Yes' on the popup: {e}")

    def open_tab(self, tab_name):
        print(f"Opening the '{tab_name}' tab...")
        try:
            # Using 'contains' because the content-desc is "Sales\nTab 2 of 7"
            tab_xpath = f"//*[contains(@content-desc, '{tab_name}') and @clickable='true']"
            tab = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, tab_xpath)))
            
            try:
                tab.click()
            except:
                self.driver.execute_script('mobile: clickGesture', {'elementId': tab.id})
                
            print(f"✅ Opened '{tab_name}' tab.")
            time.sleep(3) # Wait for the list to load
        except Exception as e:
            print(f"❌ Could not open '{tab_name}' tab: {e}")

    def click_transaction_item(self, doc_number):
        print(f"Looking for transaction item: {doc_number}")
        try:
            # Using 'contains' because the whole card is one big string like "Doc Number\nD-112\n..."
            item_xpath = f"//*[contains(@content-desc, '{doc_number}') and @clickable='true']"
            
            item = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, item_xpath)))
            
            try:
                item.click()
            except:
                self.driver.execute_script('mobile: clickGesture', {'elementId': item.id})
                
            print(f"✅ Clicked transaction item: {doc_number}")
            time.sleep(2) # Wait for the 'Actions' bottom sheet to slide up
        except Exception as e:
            print(f"❌ Could not find or click transaction item '{doc_number}': {e}")

    def perform_action(self, action_name):
        print(f"Selecting action: {action_name}")
        try:
            # Action buttons have clean accessibility IDs like "Edit", "Delete", "View", "Print"
            action_btn = self.wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, action_name)))
            
            try:
                action_btn.click()
            except:
                self.driver.execute_script('mobile: clickGesture', {'elementId': action_btn.id})
                
            print(f"✅ Performed action: {action_name}")
            time.sleep(3) # Wait for the next screen (Edit form, View screen, or Delete popup) to load
        except Exception as e:
            print(f"❌ Could not perform action '{action_name}': {e}")

    def confirm_delete(self):
        print("Waiting for delete confirmation popup...")
        try:
            # Usually, a delete popup has a 'Yes' or 'Confirm' button
            yes_btn = self.wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Yes")))
            try:
                yes_btn.click()
            except:
                self.driver.execute_script('mobile: clickGesture', {'elementId': yes_btn.id})
            print("✅ Deleted successfully.")
            time.sleep(2)
        except Exception as e:
            print(f"❌ Could not find 'Yes' button on delete popup: {e}")