from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Function to handle login
def login(driver, username, password):
    # Wait for the username input field to be present
    username_xpath = "//form[@id='frmLoginSignup']//input[@type='text' and @name='username']"
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, username_xpath))
    ).send_keys(username)  # Input username

    # Wait for the password input field to be present
    password_xpath = "//form[@id='frmLoginSignup']//input[@type='password' and @name='password']"
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, password_xpath))
    ).send_keys(password)  # Input password

    # Optional: Fetch the value of the hidden input (if needed)
    xs_token_xpath = "//input[@type='hidden' and @name='__xsToken']"
    xs_token = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xs_token_xpath))
    ).get_attribute("value")
    
    print(f"CSRF Token: {xs_token}")  # This can help in debugging

    # Click the login button
    login_button_xpath = "//input[@type='submit' and @value='Login']"  # Adjust as necessary
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, login_button_xpath))
    ).click()  # Click the login button
    print("Logged in successfully.")




# Define the main function for checking and booking a slot
def check_and_book():
    # Initialize the WebDriver for Chrome (make sure ChromeDriver is installed)
    driver = webdriver.Chrome()

    try:
        # Step 1: Open the booking website
        driver.get("https://northwestbadmintonacademy.sites.zenplanner.com/calendar.cfm")

        # Step 2 Navigate to the desired date
        right_arrow = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "icon-chevron-right"))
        )

        while True:
            right_arrow.click()

        # Define the XPath for the Saturday button
            sat_button_xpath = "//a[contains(@class, 'btn btn-mini') and contains(text(), 'Sat')]"

            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, sat_button_xpath))
                )
                print("Saturday button is now visible.")
                break
            except Exception as e:
                print("Saturday button not found yet, clicking again...")
                time.sleep(1)

        # Step 3: Check for Time Slot
        slot_xpath = "//td[contains(@class, 'items') and contains(text(), 'Slot 8:00 PM - 9:00 PM')]"
        while True:
            try:
                # Wait for the slot to be present
                slot_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, slot_xpath))
                    )

                # Check if the slot is available for $0
                if "$0" in slot_element.text:
                    time_slot_xpath = "//div[contains(@class, 'clickable hover-opacity-8 calendar-custom-color-2bff00') and contains(text(), '8:00 PM')]"
                    time_slot_element = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, time_slot_xpath))
                        )
                    time_slot_element.click()  # Click the 8:00 PM slot
                    print("Clicked On Slot 8:00 PM - 9:00 PM is available for $0.")
                    time.sleep(5)

                    try:
                    # Check if we are redirected to a login page
                        WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.ID, "frmLoginSignup"))
                            )
                        print("Redirected to login page. Please enter credentials.")

                        username = "email"
                        password = 'password'
                        login(driver, username, password)
                # Optionally, handle login here
                # (You could add a login function to fill in the username and password)

                    except Exception:
                        # If not redirected, try to click the reserve button directly
                        reserve_button_xpath = "//a[@class='btn btn-primary' and @id='reserve_1']"
                        reserve_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, reserve_button_xpath))
                            )
                        reserve_button.click()  # Click the reserve button
                        print("Reservation button clicked.")

                    break  # Exit the loop after processing the slot

                else:
                    print("Slot found but not available for $0, waiting for a manual release...")
                    time.sleep(5)  # Wait a bit before checking again
            except Exception as e:
                print("Slot not found yet, waiting...")
                time.sleep(10)  # Wait before trying again
        
        # Step 4: Reserve (check if re-direct to loggin)



    except Exception as e:
        print("Error during booking process:", e)
        return False  # Useful if this function is called in a retry loop

    finally:
        # Close the WebDriver instance to free resources
        driver.quit()
