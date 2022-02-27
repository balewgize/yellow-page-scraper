"""
Scrape Business listing information from Yellow pages Australia
"""

import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC


options = Options()
options.add_argument("start-maximized")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), 
    options=options
)


# Search for electricians in each city
with open("keywords.txt") as f:
    keywords = f.readlines()


for keyword in keywords:
    print(f"Searching for {keyword} on yello pages Australia...")
    
    try:
        for i in range(1, 30):
            page_url = f"https://www.yellowpages.com.au/search/listings?clue={keyword}&pageNumber={i}"
            driver.get(page_url)
            print(f"Scraping page {i}...")

            div = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located (
                    (By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div/div[1]')
                )
            )
            WebDriverWait(driver, 30).until(
                    EC.presence_of_all_elements_located(
                        (By.LINK_TEXT, "View Website")
                    )
            )
            # check if we reached the end or search results
            end_text = "Oh no! Sorry, we can't seem to find any exact matches for your search"
            if end_text in driver.page_source:
                # no more result for the current city
                print(f"Finished scraping.")
                break

            websites_links = div.find_elements(By.XPATH, './/a[contains(., "View Website")]')
            print(f"Websites found on page {i}: {len(websites_links)}\n{'-'*30}")

            with open("data.txt", "a") as f:
                for website in websites_links:
                    f.write(f'{website.get_attribute("href")}\n')

            time.sleep(random.randint(10, 15))
    except Exception as e:
        print("ERROR: ", e)
    
    # before moving to the next city
    time.sleep(random.randint(20, 25))

print("Finished scraping for all search keywords.")

driver.quit()