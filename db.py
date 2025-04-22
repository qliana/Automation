import psycopg2
from selenium import webdriver
from selenium.webdriver.common.by import By

db_host = "localhost"  # Host where your PostgreSQL database is running
db_port="5433"
db_name = "postgres"  # Database name
db_user = "postgres"  # Database user
db_password = "Quiet@2310"  # Database password

# Connect to PostgreSQL
try:
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        dbname=db_name,
        user=db_user,
        password=db_password
    )
    cursor = conn.cursor()
    print("Connected to PostgreSQL")

except Exception as e:
    print("Error connecting to PostgreSQL:", e)
    exit()
