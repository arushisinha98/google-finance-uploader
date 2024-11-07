from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
import time
import os
import tempfile

class GoogleFinanceAutomator:
    def __init__(self):
        try:
            # Set up Chrome options
            chrome_options = Options()
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            
            # Create a temporary profile directory
            temp_profile_dir = os.path.join(tempfile.mkdtemp(), 'chrome_profile')
            os.makedirs(temp_profile_dir, exist_ok=True)
            chrome_options.add_argument(f"--user-data-dir={temp_profile_dir}")
            
            # Add other necessary options
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Initialize Chrome service
            service = Service()
            
            print("Starting Chrome...")
            self.driver = webdriver.Chrome(
                service=service,
                options=chrome_options
            )
            
            # Set window size explicitly
            self.driver.set_window_size(1920, 1080)
            
            # Initialize wait
            self.wait = WebDriverWait(self.driver, 10)
            print("Chrome initialized successfully")
            
        except Exception as e:
            print(f"Error initializing Chrome: {str(e)}")
            raise
    
    def wait_and_click(self, locator):
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
            time.sleep(1)
        except Exception as e:
                print(e)

    def wait_and_send_keys(self, locator, keys):
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            element.clear()
            element.send_keys(keys)
            time.sleep(1)
        except Exception as e:
                print(e)

    def start_manual_process(self):
        """Start the process with manual login"""
        try:
            print("\nStarting manual login process...")
            
            # Open Google Finance
            print("Opening Google Finance...")
            self.driver.get("https://www.google.com/finance/portfolio")
            
            print("\nPlease follow these steps:")
            print("1. Log in to your Google account")
            print("2. Navigate to your portfolio")
            print("3. Once you're ready, press Enter to continue...")
            
            input("\nPress Enter when you're on the portfolio page...")
            
            # Give extra time for page load
            time.sleep(1)
            
            # Verify we're on the portfolio page
            try:
                self.wait.until(
                    EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Portfolio')]"))
                )
                print("Successfully verified portfolio page")
                return True
            except:
                print("Could not verify portfolio page. Are you on the correct page?")
                retry = input("Would you like to try again? (y/n): ")
                if retry.lower() == 'y':
                    return self.start_manual_process()
                return False
                
        except Exception as e:
            print(f"Error during manual process: {str(e)}")
            return False

    def add_investment(self, symbol, quantity, purchase_date, purchase_price):
        """Add a single investment to the portfolio"""
        if quantity < 0:
            print("This script can only add buys to your Google Finance portfolio")
            return False
        try:
            print(f"\nAttempting to add investment: {symbol}")

            button1='#yDmH0d > c-wiz.zQTmif.SSPGKf.yd8gve > div > c-wiz > div.e1AOyf > div > div:nth-child(2) > div > div > c-wiz > div > div > div.T7rHJe > div > div.VfPpkd-dgl2Hf-ppHlrf-sM5MNb > button'
            button2='#yDmH0d div > c-wiz > div.e1AOyf > div > div:nth-child(2) > div > div > c-wiz > div > div > div > div > div.VfPpkd-dgl2Hf-ppHlrf-sM5MNb > button > span'
            search_stock='#yDmH0d > div.VfPpkd-Sx9Kwc.cC1eCc.UDxLd.PzCPDd.OHihnb.VfPpkd-Sx9Kwc-OWXEXe-FNFY6c > div.VfPpkd-wzTsW > div > div.VfPpkd-cnG4Wd > div > div:nth-child(2) > div > div > div > div.d1dlne > input.Ax4B8.ZAGvjd'
            choice_1 = '#yDmH0d > div.VfPpkd-Sx9Kwc.cC1eCc.UDxLd.PzCPDd.OHihnb.VfPpkd-Sx9Kwc-OWXEXe-FNFY6c > div.VfPpkd-wzTsW > div > div.VfPpkd-cnG4Wd > div > div:nth-child(2) > div > div > div > div:nth-child(2) > div > div > div > div:nth-child(3) > div:nth-child(1)'
            common_selector='#yDmH0d > div.VfPpkd-Sx9Kwc.cC1eCc.UDxLd.PzCPDd.OHihnb.VfPpkd-Sx9Kwc-OWXEXe-FNFY6c > div.VfPpkd-wzTsW > div > div.VfPpkd-cnG4Wd > div > div:nth-child(3) > div:nth-child(1) >'
            quantity_button=f'{common_selector} div > div:nth-child(1) > div > div > div > label > input'
            date_button=f'{common_selector} div > div:nth-child(2) > div > div > div > div.aCsJod.oJeWuf > div > div.Xb9hP > input'
            price_button=f'{common_selector} div > div:nth-child(3) > div > label > input'
            add_more_button=f'#yDmH0d > div.VfPpkd-Sx9Kwc.cC1eCc.UDxLd.PzCPDd.OHihnb.VfPpkd-Sx9Kwc-OWXEXe-FNFY6c > div.VfPpkd-wzTsW > div > div.VfPpkd-T0kwCb > div > div:nth-child(2) > button'
            save_button=f'#yDmH0d > div.VfPpkd-Sx9Kwc.cC1eCc.UDxLd.PzCPDd.OHihnb.VfPpkd-Sx9Kwc-OWXEXe-FNFY6c > div.VfPpkd-wzTsW > div > div.VfPpkd-T0kwCb > div > div:nth-child(3) > button'
            highlight='/html/body/c-wiz[3]/div/c-wiz/div[2]/div/div[1]/div[2]/div[2]/div'

            try:
                self.driver.find_element(By.XPATH, highlight)
                self.wait_and_click((By.CSS_SELECTOR, button1))
            except Exception as e:
                try:
                    self.wait_and_click((By.CSS_SELECTOR, button2))
                except Exception as e:
                    self.wait_and_click((By.CSS_SELECTOR, add_more_button))
            
            self.wait_and_send_keys((By.CSS_SELECTOR, search_stock), symbol)
            self.wait_and_click((By.CSS_SELECTOR, choice_1))
            self.wait_and_send_keys((By.CSS_SELECTOR, quantity_button), quantity)
            self.wait_and_send_keys((By.CSS_SELECTOR, date_button), purchase_date)
            if purchase_price is not None:
                self.wait_and_send_keys((By.CSS_SELECTOR, price_button), purchase_price)
            self.wait_and_click((By.CSS_SELECTOR, save_button))
            return True
                
        except Exception as e:
            print(f"Error adding investment: {str(e)}")
            return False

    def close(self):
        """Close the browser"""
        try:
            self.driver.quit()
            print("Browser closed successfully")
        except Exception as e:
            print(f"Error closing browser: {str(e)}")