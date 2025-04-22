from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import psycopg2
import time

db_host = "localhost"
db_port = "5433" 
db_name = "postgres"
db_user = "postgres"
db_password = "Quiet@2310"


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
max_length = 220

# Truncate each string in the list
for i in range(len(conv_text)):
    conv_text[i] = conv_text[i][:max_length] 


print(conv_text)
print(conv_rate)

for index, value in enumerate(conv_text):
    print(conv_text[index], conv_rate[index])


number_of_books = len(books)
print(f"Number of books in the Travel category: {number_of_books}")

driver.quit()

try:
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        database=db_name,
        user=db_user,
        password=db_password
    )
    print("Connected to PostgreSQL")

    # Create a cursor object to execute SQL commands
    cur = conn.cursor()
    


    for item,star in zip(conv_text, conv_rate):
        # Step 2: Check if the combination of title and rating exists in the database
        check_query = """
        SELECT COUNT(*) FROM selenium_data WHERE title = %s AND rating = %s;
        """
        cur.execute(check_query, (item, star))
        result = cur.fetchone()

        # Step 3: If the data does not exist, insert it
        if result[0] == 0:
            insert_query = """
            INSERT INTO selenium_data (title, rating) VALUES (%s, %s);
            """
            cur.execute(insert_query, (item, star))
            conn.commit()
            print(f"Data inserted for {title} with rating {rating}.")
        else:
            print(f"Data for {item} with rating {star} already exists, skipping insertion.")
    

     
    #for item,star in zip(conv_text, conv_rate):
       # cur.execute("INSERT INTO selenium_data (title, rating) VALUES (%s, %s)", (item, star))

     



    conn.commit()

    print("Data inserted successfully")

    # Close the cursor and connection
    cur.close()
    conn.close()

except Exception as e:
    print("Error connecting to PostgreSQL or inserting data:", e)









