from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

target_url = "https://www.imdb.com/chart/top/"
options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = None

try:
    driver = webdriver.Chrome(options=options)
    print("[+] Chrome Driver Created!")
except Exception as e:
    print(f"Chrome driver failed: {e}")
    exit(1)

if driver:
    print("[+] Driver Created Successfully!")
    
    try:
        driver.get(target_url)
        print("[+] Page loaded successfully!")
        
        time.sleep(5)
        print("[+] Waited 5 seconds after page load")
        
        films = driver.find_elements(By.CSS_SELECTOR,"h3.ipc-title__text")
        if films:
            print(f"[+] Found {len(films)} movies!")
            for title in films[0:250]:
                print(f"{title.text.strip()}")
        else:
            print("[-] No movies found. Page structure might have changed.")
    except Exception as e:
        print(f"Error occurred: {e}")
        
    finally:
        driver.quit()
        print("[+] Driver closed successfully!")
else:
    print("[-] Failed to create driver!")