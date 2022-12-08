from selenium import webdriver
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

opts = webdriver.ChromeOptions()
opts.add_argument('''user-agent = Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4)

                                      AppleWebKit/537.36 (KHTML, like Gecko)
                                      Chrome/81.0.4044.92 Safari/537.36''')

driver = webdriver.Chrome(executable_path=r"/Users/Demetrick/Desktop/chromedriver", options=opts)

def get_gas(user_name, password):
    url = "https://myaccount.enbridgegas.com/Sign-In"
    driver.get(url)
    driver.find_element(By.ID,"signin-username").send_keys(os.getenv('58_UTIL_EMAIL')) 
    driver.find_element(By.ID,"signin-password").send_keys(os.getenv('58_UTIL_PASSWORD'))
    driver.find_element(By.ID,"signin-password").send_keys(Keys.RETURN)


    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "cancelNotification"))).click()
   
    path = r'/html/body/div[3]/div/div/div/div/div/div[1]/div/div/div/div/div/div/div/div[2]/section[1]/div/div[2]/div/div/div/div[2]/div/div[1]/div[1]/div/div[2]/div/div/b'
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, path)))

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
    print(get_hydro())
