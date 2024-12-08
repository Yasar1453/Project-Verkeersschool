import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def random_delay(min_seconds=3, max_seconds=7):
    time.sleep(random.uniform(min_seconds, max_seconds))

def random_search_delay(min_seconds=10, max_seconds=20):
    time.sleep(random.uniform(min_seconds, max_seconds))

# Set up the Safari driver
driver = webdriver.Safari()

driver.get("https://top.cbr.nl/Top/LogOnView.aspx?ReturnUrl=%2fTop%2fLogOnView.aspx%3fReturnUrl%3d%252ftop")
random_delay()
input_element_name = driver.find_element(By.ID, "ctl00_ctl00_ctl00_DefaultContent_DefaultContent_DefaultContent_LogOnUserName")
input_element_name.send_keys("mustafa")
random_delay()
input_element_ww = driver.find_element(By.ID, "ctl00_ctl00_ctl00_DefaultContent_DefaultContent_DefaultContent_LogOnPassword")
input_element_ww.send_keys("Yasar2002!" + Keys.ENTER)

WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "aanvragen"))
)

random_delay()
link_aanvragen = driver.find_element(By.PARTIAL_LINK_TEXT, "aanvragen")
link_aanvragen.click()

WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.ID, "ctl00_ctl00_DefaultContent_DefaultContent_FindRequests"))
)

random_delay()
link_zoek = driver.find_element(By.ID, "ctl00_ctl00_DefaultContent_DefaultContent_FindRequests")
link_zoek.click()

candidate_number = "4612337549"  # Kandidaatnummer handmatig aanpassen
candidate_xpath = f"//span[text()='{candidate_number}']"

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, candidate_xpath))
)

random_delay()
link_kandidaat = driver.find_element(By.XPATH, candidate_xpath)
link_kandidaat.click()

# Wait for the button to be present and visible
reserve_button_locator = (By.XPATH, "//a[@title='Aanvraag reserveren']")
try:
    element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(reserve_button_locator)
    )
    print("Element found!")
    random_delay()
    # Scroll the element into view and click it
    driver.execute_script("arguments[0].scrollIntoView();", element)
    element.click()
except TimeoutException:
    print("Element not found within the specified timeout")

# Locate the date input field by its ID and send the desired date string
try:
    # Wait for the input field to be present and visible
    date_input_locator = (By.ID, "ctl00_ctl00_DefaultContent_DefaultContent_CapacityDateUpToDatePicker_dateInput")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(date_input_locator)
    )
    random_delay()
    date_input = driver.find_element(*date_input_locator)
except:
    # Alternative method to locate the date input field by its name
    date_input_locator = (By.NAME, "ctl00$ctl00$DefaultContent$DefaultContent$CapacityDateUpToDatePicker$dateInput")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(date_input_locator)
    )
    random_delay()
    date_input = driver.find_element(*date_input_locator)

date_input.send_keys("30-08-2025")

# Implementing the while loop to keep searching until "reserveren" is found
while True:
    random_search_delay()  # Use the longer delay for the while loop
    search_button = driver.find_element(By.ID, "ctl00_ctl00_DefaultContent_DefaultContent_Find")
    search_button.click()
    
    try:
        reserveren_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'CapacityContainer$AvailableCapacityTab$AvailableCapacityGrid') and text()='reserveren']"))
        )
        print("Found 'reserveren' link!")
        break
    except:
        print("Link not found yet, trying again...")
        continue

driver.quit()
