from appium import webdriver
from appium.options.android import UiAutomator2Options
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.customer_page import CustomerPage
from pages.transaction_page import TransactionPage
import time

# 1. Setup Capabilities
options = UiAutomator2Options()
options.platform_name = "Android"
options.device_name = "863d00583048303634510cfb40274c"
options.app_package = "com.saang.vansale"
options.app_activity = "com.saang.vansale.MainActivity"
options.automation_name = "UiAutomator2"
options.no_reset = False 
options.ignore_hidden_api_policy_error = True 
print("Starting Appium...")
driver = webdriver.Remote("http://127.0.0.1:4723", options=options)

try:
    # --- 1. LOGIN ---
    login_page = LoginPage(driver)
    print("Logging in...")
    login_page.enter_username("u2")
    login_page.enter_password("Test@123")
    login_page.select_company("Rastilari")
    login_page.click_login()
    time.sleep(5)

    # --- 2. DASHBOARD ---
    print("Navigating to Customers...")
    dashboard_page = DashboardPage(driver)
    dashboard_page.open_customers()
    time.sleep(3) 

    # --- 3. CUSTOMER SEARCH & SELECT ---
    customer_page = CustomerPage(driver)
    customer_page.search_customer("sij")
    customer_page.select_customer("sij")
    time.sleep(3)
    print("✅ Customer Selected!")

    # --- 4. TRANSACTION FLOW ---
    transaction_page = TransactionPage(driver)
    transaction_page.click_plus()
    transaction_page.select_invoice()
    time.sleep(4)
    print("✅ Invoice screen opened!")

    # --- 5. ADD ITEM FLOW ---
    transaction_page.click_add_item()
    time.sleep(4)
    print("✅ Add Item screen opened!")

        # --- 6. FIRST PRODUCT ---
    transaction_page.add_product_to_invoice("LARI SWEET KERNEL")
    transaction_page.enter_quantity_and_save("10")
    time.sleep(3)

    # --- 7. SECOND PRODUCT (Optional) ---
    # Because we are back on the product list, we can just call it again!
    print("Adding a second product...")
    transaction_page.add_product_to_invoice("BOPP TAPE") 
    transaction_page.enter_quantity_and_save("5")
    time.sleep(3)

    # --- 8. FINISH ADDING ITEMS ---
    # Click 'Close' to go back to the main invoice
    transaction_page.close_add_item_popup()
    
    time.sleep(3)
    print("✅ Finished adding items. Ready to save the Invoice!")

    # --- 9. SAVE THE MAIN INVOICE ---
    transaction_page.save_main_invoice()
    
    time.sleep(5)
    print("🎉 INVOICE SAVED SUCCESSFULLY!")

    # --- 10. CONFIRM PRINT / SAVE ---
    transaction_page.confirm_print_invoice()

    time.sleep(5)
    print("🎉 ENTIRE TRANSACTION COMPLETED SUCCESSFULLY!")

    # --- 11. TESTING THE TABS AND ACTIONS ---
    print("Navigating to the Sales tab to view created invoices...")
    transaction_page.open_tab("Sales")
    
    time.sleep(3) # Wait for the list to load
    
    # Click on a specific transaction. 
    # Change "D-112" to the actual doc number of the invoice you just created!
    transaction_page.click_transaction_item("1511")
    
    time.sleep(2) # Wait for the 'Actions' bottom sheet to slide up
    
    # Click 'Edit' (or 'View' or 'Delete')
    print("Clicking Edit...")
    transaction_page.perform_action("Edit")
    
    time.sleep(5)
    print("🎉 Successfully navigated to the next screen!")

    # --- 12. EDIT THE INVOICE (REUSING EXISTING FUNCTIONS) ---
    print("Editing the invoice...")
    
    # 1. Let's add another product to the existing invoice!
    transaction_page.click_add_item()
    time.sleep(3)
    transaction_page.add_product_to_invoice("BOPP TAPE")
    transaction_page.enter_quantity_and_save("5", rate="100.0")
    time.sleep(2)
    transaction_page.close_add_item_popup()
    time.sleep(2)

    # 2. Let's save the main invoice again to apply the edit
    print("Saving the edited invoice...")
    transaction_page.save_main_invoice()
    time.sleep(2)
    
    # 3. Handle the "Do you want to print?" popup again
    transaction_page.confirm_print_invoice()
    time.sleep(3)

    print("🎉 Successfully edited and saved the invoice!")
except Exception as e:
    print(f"❌ Error: {e}")

finally:
    print("Closing app...")
    try:
        driver.quit()
    except Exception:
        pass  # Ignore cleanup errors so the test finishes cleanly