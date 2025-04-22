from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time

service = Service(executable_path="chromedriver.exe") 
driver = webdriver.Chrome(service=service)
driver.get("http://books.toscrape.com/")
driver.maximize_window()
WebDriverWait(driver, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")
travel=driver.find_element(By.XPATH,"//*[contains(@href,'catalogue/category/books/travel')]")
travel.click()
books = driver.find_elements(By.XPATH, "//*[@class='product_pod']//following::h3")


conv_text = []
conv_rate = []
for title in books:
    text=title.text
    conv_text.append(text)

rate=driver.find_elements(By.XPATH,"//*[contains(@class,'star-rating')]")
for rates in rate:
    rating = rates.get_attribute("class")
    last_word = rating[rating.rfind(" ") + 1:]
    conv_rate.append(last_word)
    


print(type(conv_text))
print(type(conv_rate))
print(conv_text)
print(conv_rate)

for index, value in enumerate(conv_text):
    print(conv_text[index], conv_rate[index])


number_of_books = len(books)
print(f"Number of books in the Travel category: {number_of_books}")
driver.quit()









