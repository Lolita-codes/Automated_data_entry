import requests
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

# Manually create a form using Google forms with three short-answer questions which are:
# What's the address of the property?
# What's the price per month?
# What's the link to the property?
# Copy the link address of the form

# The zillow web address to be scraped
zillow_link = 'https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.70524062109375%2C%22east%22%3A-122.10373915625%2C%22south%22%3A37.30313318106246%2C%22north%22%3A38.01414292179115%7D%2C%22isMapVisible%22%3Afalse%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D'

header = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    "Accept-Language": 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Device-Type': 'Computer',
    'Browser & Version': 'Chrome 103.0.0'
}

# Using Selenium for scraping the listings from the Zillow web address
CHROME_DRIVER_PATH ='C:\Development\chromedriver.exe'
driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
driver.get(zillow_link)
sleep(5)

# Creates a list of prices for all the scraped listings
prices = driver.find_elements(By.CLASS_NAME, 'list-card-price')
price_list = [item.text.split('+')[0].split('/')[0] for item in prices]
print(price_list)

# Creates a list of links for all the scraped listings
links = driver.find_elements(By.CSS_SELECTOR, 'div.list-card-info a')
link_list = []
for link in links:
    # Some links gotten from Zillow may be incomplete
    full = link.get_attribute('href')
    if 'http' not in full:
        link_list.append(f"https://www.zillow.com{full}")
    else:
        link_list.append(full)
print(link_list)

# Creates a list of addresses for all the scraped listings
addresses = driver.find_elements(By.CLASS_NAME, 'list-card-addr')
address_list = [item.text for item in addresses]
print(address_list)
sleep(5)


# Using Beautiful Soup for scraping the listings from the Zillow web address
# response = requests.get(url=zillow_link)
# page = response.text
# soup = BeautifulSoup(page, "html.parser")
#
# all_link_elements = soup.select(".list-card-top a")
#
# all_links = []
# for link in all_link_elements:
#     href = link["href"]
#     print(href)
#     if "http" not in href:
#         all_links.append(f"https://www.zillow.com{href}")
#     else:
#         all_links.append(href)
# print(all_links)
# all_address_elements = soup.select(".list-card-info address")
# all_addresses = [address.get_text().split(" | ")[-1] for address in all_address_elements]

# all_price_elements = soup.select(".list-card-heading")
# all_prices = []
# for element in all_price_elements:
#     # Gets the prices. Single and multiple listings have different tag & class structures
#     try:
#         # Price with only one listing
#         price = element.select(".list-card-price")[0].contents[0]
#     except IndexError:
#         print('Multiple listings for the card')
#         # Price with multiple listings
#         price = element.select(".list-card-details li")[0].contents[0]
#     finally:
#         all_prices.append(price)
#


# Fills in a new form for each new listing with its price, address and link
for i in range(len(price_list)):
    driver.get('https://docs.google.com/forms/d/e/1FAIpQLSeYBJ4dQCkQfQv64-YqrLSWhwAylI5Iig6iafmYluKnwZywMg/viewform?usp=sf_link')
    sleep(5)
    address = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span')
    address.send_keys(address_list[i])
    price.send_keys(price_list[i])
    link.send_keys(link_list[i])
    submit.click()

# Manually click on the 'Sheet' icon t create a Google Sheet from the responses to the Google form.
   #driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll)
#'https://docs.google.com/forms/d/e/1FAIpQLSeYBJ4dQCkQfQv64-YqrLSWhwAylI5Iig6iafmYluKnwZywMg/viewform?usp=sf_link'