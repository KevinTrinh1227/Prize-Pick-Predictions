from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get("https://app.prizepicks.com/")


driver.find_element(By.CLASS_NAME, "close").click()


time.sleep(2)

driver.find_element(By.XPATH, "//div[@class='name'][normalize-space()='NBA']").click()

time.sleep(2)

# Wait for the stat-container element to be present and visible
stat_container = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "stat-container")))

# Find all stat elements within the stat-container
stat_elements = driver.find_elements(By.CSS_SELECTOR, "div.stat")

# Iterate over each stat element
for stat in stat_elements:

    try:
        # Click the stat element
        stat.click()

        projections = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".projection")))
        print("\n\n=================================================================")
        
        for projection in projections:
            names = projection.find_element(By.XPATH, './/div[@class="name"]').text
            points = projection.find_element(By.XPATH, './/div[@class="presale-score"]').get_attribute('innerHTML')
            print(f"Player: {names:30} Strike Value: {points} pts")
            
    except:
        pass

   
print("===================================================================\n")

driver.quit()