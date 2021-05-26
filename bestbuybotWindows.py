from selenium import webdriver
import json
import time
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
from twilio.rest import Client

#setup
myinfo = open("info.json", "r")
urls = myinfo.read()
obj = json.loads(urls)
account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)
options = Options()
#options.add_argument("--headless")
driver = webdriver.Chrome(options=options, executable_path="./chromedriver.exe")


# login
driver.get("https://www.bestbuy.com/signin")
time.sleep(1)
login_email = driver.find_element_by_xpath("/html/body/div[1]/div/section/main/div[2]/div[1]/div/div/div/div/form/div[1]/div/input")
login_email.send_keys(obj["email"])
login_password = driver.find_element_by_xpath("/html/body/div[1]/div/section/main/div[2]/div[1]/div/div/div/div/form/div[2]/div/div/input")
login_password.send_keys(obj["password"])
login = driver.find_element_by_xpath("/html/body/div[1]/div/section/main/div[2]/div[1]/div/div/div/div/form/div[4]/button")
login.click()
print("Logged in")


time.sleep(2)

#starting
driver.get(obj['url1'])
search_count = 0
complete = True
while complete:
    try:
        addtocart = driver.find_element_by_xpath("//*[ text() = 'Add to Cart']")
    except NoSuchElementException:
        driver.refresh()
        search_count += 1
        print("Sold Out or Unavailable. Attempt " + str(search_count))
        continue
    addtocart.click()
    print("Added to cart")
    time.sleep(3)
    try:
        gotocart = driver.find_element_by_xpath("/html/body/div[8]/div/div[1]/div/div/div/div/div[1]/div[3]/a")
        gotocart.click()
        print("Going to cart")
        time.sleep(2)
        checkout = driver.find_element_by_xpath("/html/body/div[1]/main/div/div[2]/div[1]/div/div[1]/div[1]/section[2]/div/div/div[3]/div/div[1]/button")
        checkout.click()
        print("Checking out")
        time.sleep(7)
        try:
            security_code = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[2]/div[1]/div[1]/main/div[2]/div[2]/div/div[2]/div[1]/div[2]/div/div[1]/div/div[1]/div[2]/div/div[2]/div/input").send_keys(obj['cvv'])
        except NoSuchElementException:
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            print("Going to bottom of page to click place Your Order")
            time.sleep(3)
            placeorder = driver.find_element_by_xpath("//*[ text() = 'Place Your Order']")
            placeorder.click()
            time.sleep(2)
            print("Order placed!")
            break
    except:
        print("Retrying")
        driver.get(obj['url1'])
        pass
