from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
from bs4 import BeautifulSoup
import pdb
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os

load_dotenv()

# opts = webdriver.ChromeOptions()

opts = Options()
opts.add_argument('''user-agent = Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4)
                                      AppleWebKit/537.36 (KHTML, like Gecko)
                                      Chrome/81.0.4044.92 Safari/537.36''')
opts.add_argument("start-maximized", )
opts.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

def get_gas(address):
    url = "https://enbridgegas.okta.com/login/login.htm?"
    driver.get(url)
    if address == '58':
        driver.find_element(By.ID,"okta-signin-username").send_keys(os.getenv('58_UTIL_EMAIL')) 
        driver.find_element(By.ID,"okta-signin-password").send_keys(os.getenv('58_UTIL_PASSWORD'))
    else:
        driver.find_element(By.ID,"okta-signin-username").send_keys(os.getenv('23_UTIL_EMAIL')) 
        driver.find_element(By.ID,"okta-signin-password").send_keys(os.getenv('58_UTIL_PASSWORD'))
    driver.find_element(By.ID,"okta-signin-password").send_keys(Keys.RETURN)
    time.sleep(3)
    driver.get('https://myaccount.enbridgegas.com/my-account/my-bill')
    #time.sleep(3)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div/div/div/div/div[3]/div[2]/div[1]/div/div/form/fieldset/button"))).click()

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "btnSkipMFA"))).click()
    
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "cancelNotification"))).click()

    # path = r'/html/body/div[3]/div/div/div/div/div/div[3]/div[2]/div[1]/div/div/form/fieldset/button'
    # WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, path)))
    
    time.sleep(1)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    num = soup.find_all('div', {'class' : r'gas-uasge-details' })[1].find('b').text

    return float(num.replace('$', ''))


def get_hydro():
    url= "https://www.torontohydro.com/log-in"
    driver.get(url)
    driver.find_element(By.ID,"email").send_keys(os.getenv('58_UTIL_EMAIL'))
    driver.find_element(By.ID,"password").send_keys(os.getenv('58_UTIL_PASSWORD'))
    driver.find_element(By.ID,"password").send_keys(Keys.RETURN)
    driver.get('https://www.torontohydro.com/my-account/bills-and-payments')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return float(soup.find('tr', class_='type-bill').find(class_='text-right').text.strip().replace('$', ''))

def get_electricity():
    url = "https://myaccount.alectrautilities.com/app/capricorn?para=index"

    driver.get(url)
    driver.find_element(By.ID,"accessEmail").send_keys(os.getenv('ACCOUNT_NUMBER'))
    driver.find_element(By.ID,"password1").send_keys(os.getenv('58_UTIL_PASSWORD'))
    driver.find_element(By.ID,"password1").send_keys(Keys.RETURN)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    for i in soup.find_all('strong'):
        if '$' in i.text:
            num = i.text
            break
    else:
        print('could not find gas')
    return float(num.replace('$', ''))

if __name__ == "__main__":
    print(get_gas())
